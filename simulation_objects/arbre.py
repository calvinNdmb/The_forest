from typing import Union, List
import pygame
import numpy as np
import random

from pygame import Surface

#>:/
class Arbre:
    def __init__(self, x: int, y: int,nutriments: Union[float, np.float64]):
        self.pos = np.array([x, y], dtype=float)
        self.color = (255, 255, 255)
        self.nutriments = (nutriments / 255) * 100  # Nutriments à la position initiale
        self.state = "seed" # Etats possibles : "seed", "alive", "dead"
        #self.rayon_top_max = random.randint(10, 100) # Les rayons max
        self.rayon_top = 0 # Début à 0 quand c'est une graine, ils pousseront quand la plante éclot
        self.max_age = random.randint(1, 40)
        self.age = 0
        self.energie = 0
        self.stored_energy = 0
        self.zone_action = 0
        self.graines_produites = 0
        self.dernier_reproduction = 0  # Années depuis la dernière reproduction
        self.energie_solaire = 0
        self.hauteur = 1  # Hauteur initiale (en unités arbitraires)
        #self.max_hauteur = random.randint(35, 50)  # Hauteur max possible
        self.favorite_groth = 50/100  # Facteur de croissance favori

    def update(
            self,
            arbres: List['Arbre'],
            width: int,
            height: int,
            nutrient_map: np.ndarray,
            day: int,
            max_graines_zone: int = 10,
            max_graines_total: int = 20,
            attente_reproduction: int = 2
    ):
        if self.state == "seed":
            if random.random() < 0.001:
                self.state = "dead"
            elif random.random() < 0.005:
                self.state = "alive"
                self.rayon_top = 1
                self.energie = random.randint(1, 5)
        elif self.state == "alive":
            if self.age >= self.max_age or self.energie <= 0:
                self.state = "dead"
                return

            self.calcule_energie(arbres=arbres)
            self.energie -= self.calcule_cout_maintient()

            self.zone_action = self.rayon_top * 2  # Mettre à jour la zone d'action

            cout_croissance_largeur = 0.001 * (np.pi * self.rayon_top ** 2)  # Coût basé sur l'aire de la canopée
            cout_croissance_hauteur = 0.07 * self.hauteur  # Coût basé sur la hauteur actuelle
            # Croissance en largeur
            if self.energie > (40 + cout_croissance_largeur): #and self.rayon_top < self.rayon_top_max:
                self.energie -= cout_croissance_largeur
                self.rayon_top += 0.1
            # Croissance en hauteur
            if self.energie > (40 + cout_croissance_hauteur): #and self.hauteur < self.max_hauteur:
                self.energie -= cout_croissance_hauteur
                self.hauteur += 0.1
            if self.energie < 10:
                self.state = "dead"

            if (self.age >= 1 and random.random() < 0.1 and #t'as modif ça petit con
                self.dernier_reproduction >= attente_reproduction):  # Probabilité de 2% et attente après reproduction
                self.produire_graine(arbres=arbres, nutrient_map=nutrient_map, width=width, height=height,
                                     max_graines_zone=max_graines_zone, max_graines_total=max_graines_total)
                self.dernier_reproduction = 0

                

        if day % 100 == 0:
            self.age += 1
            self.dernier_reproduction += 1

    def produire_graine(
            self,
            arbres: List['Arbre'],
            width:int,
            height: int,
            nutrient_map: np.ndarray,
            max_graines_zone: int,
            max_graines_total: int
    ):
        # Limite de graines par zone
        graines_dans_zone = 0
        for autre_arbre in arbres:
            dist = np.linalg.norm(self.pos - autre_arbre.pos)
            if dist <= self.zone_action and autre_arbre.state == "seed":
                graines_dans_zone += 1

        if graines_dans_zone >= max_graines_zone or self.graines_produites >= max_graines_total:
            return

        # Générer une position aléatoire dans la zone d'action
        x_min = int (max(0, self.pos[0] - max_graines_zone))
        x_max = int (min(width - 1, self.pos[0] + max_graines_zone))
        y_min = int (max(0, self.pos[1] - max_graines_zone))
        y_max = int (min(height - 1, self.pos[1] + max_graines_zone))

        new_x = random.randint(x_min, x_max)
        new_y = random.randint(y_min, y_max)

        # Vérifier que la position est valide (pas de conflit avec d'autres arbres)
        position_valide = True
        for autre_arbre in arbres:
            dist = np.linalg.norm([new_x - autre_arbre.pos[0], new_y - autre_arbre.pos[1]])
            if dist < autre_arbre.rayon_top:
                position_valide = False
                break

        if position_valide:
            nutriments = nutrient_map[int(new_x) % width, int(new_y) % height]
            nouveaux_arbre = Arbre(new_x, new_y, nutriments)
            nouveaux_arbre.color = (255, 255, 0)
            arbres.append(self.mutation(nouveaux_arbre))
            self.graines_produites += 1

    def mutation(self,new_arbre: 'Arbre'):   # Mutations
        # Mutation de la couleur
        if random.random() < 0.1:
            new_arbre.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            new_arbre.max_age = min (max([self.max_age + (random.randint(-30, 30) / 100),1]),100)
            new_arbre.favorite_groth = min (max([self.favorite_groth + (random.randint(-3, 3)/100),1]),100)
            print(f"Mutation!!!! ==> {new_arbre.color} , {new_arbre.max_age} , {new_arbre.favorite_groth}")
            return new_arbre
        else :
            return new_arbre

    def calcule_energie(self, arbres):
        # Base d'énergie solaire proportionnelle à la taille de la canopée
        self.energie_solaire = (np.pi * (self.rayon_top**2))/100
        # Calcul de la réduction due à l'ombre des autres arbres
        for autre in arbres:
            if autre is self or autre.state != "alive":
                continue
            dist = np.linalg.norm(self.pos - autre.pos)
            if dist < autre.rayon_top:  # Si cet arbre est sous la canopée de l'autre
                if autre.hauteur > self.hauteur:
                    # Calcul de l'effet de l'ombre et de la proximité (plus proche, plus d'ombre)
                    ombre_factor = (autre.hauteur - self.hauteur) / autre.hauteur
                    proximity_factor = max(0, 1 - dist / autre.rayon_top)
                    self.energie_solaire *= (1 - ombre_factor * proximity_factor)
        # Calcul de l'énergie totale
        self.energie = self.energie_solaire + (100 - np.log(self.rayon_top + 1) * 30 * self.nutriments / 100)

    def calcule_cout_maintient(self):
        cout_hauteur = self.hauteur * 0.03
        cout_surface = np.pi * (self.rayon_top ** 2) * 0.0001
        # Coût total passif
        return cout_hauteur + cout_surface

    def draw(self, screen: Surface, width: int, height: int):
        if self.state == "dead":
            return
        if self.state == "seed":
            # Dessiner la graine comme un petit point
            pygame.draw.circle(screen, (255, 0, 0), self.pos.astype(int), 2)
            return
        # state = "alive"
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        alpha = 130  # Transparence
        color_feuilles = (0, 255, 0, alpha)
        # Le rayon_top représente la canopée, on la dessine en vert transparent
        pygame.draw.circle(surface, color_feuilles, self.pos.astype(int), int(self.rayon_top))
        screen.blit(surface, (0, 0))
        # Un point blanc au centre
        pygame.draw.circle(screen, self.color, self.pos.astype(int), 3)
