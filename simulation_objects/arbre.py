from typing import Union
import pygame
import numpy as np
import random

class Arbre:
    def __init__(self, x: int, y: int, nutriments: Union[float, np.float64]):
        self.pos = np.array([x, y], dtype=float)
        self.color = (255, 255, 255)
        self.nutriments = (nutriments/255)*100  # Nutriments à la position initiale
        self.state = "seed"# Etats possibles : "seed", "alive", "dead"
        self.rayon_top_max = random.randint(10, 100) # Les rayons max
        self.rayon_top = 0 # Début à 0 quand c'est une graine, ils pousseront quand la plante éclot
        self.max_age = random.randint(1, 40)
        self.age = 0
        self.energie=0
        self.stored_energy=0

    def update(self):
        if self.state == "seed":
            if random.random() < 0.001:
                self.state = "dead"
            elif random.random() < 0.005:
                self.state = "alive"
                self.rayon_top = 1
                self.energie = random.randint(1, 5)
        elif self.state == "alive":
            if self.age >= self.max_age or self.energie<=0:
                self.state = "dead"
                return
            #area_top = np.pi * (self.rayon_top**2)
            #top_factor = 1.0
            self.calcule_energie()
            if 50 < self.energie < 60:
                if random.randint(1, 100) > 20:
                    self.energie -= 20*(self.age/10)
                    self.rayon_top += 0.1
                    #print("prise de risque!!!!!")

            if self.energie >60:
                self.rayon_top += 0.1

            
            
            elif self.energie <10:
                self.state = "dead"
            """# Vérifier si une plante plus grande recouvre celle-ci pour le rayon_top
            for autre in arbres:
                if autre is self or autre.state != "alive":
                    continue
                dist = np.linalg.norm(self.pos - autre.pos)
                # Check overlap top
                if dist < (self.rayon_top + autre.rayon_top):
                    # Il y a chevauchement aérien
                    if autre.rayon_top > self.rayon_top:
                        # Cette plante est plus petite, elle subit un -50% sur la production aérienne
                        top_factor *= 0.5"""

    def calcule_energie(self):
        self.energie = 100-np.log(self.rayon_top)*30*self.nutriments/100
        
    def draw(self, screen, width, height):
        if self.state == "dead":
            return
        if self.state == "seed":
            # Dessiner la graine comme un petit point
            pygame.draw.circle(screen, (255, 0, 0), self.pos.astype(int), 2)
            return
        # state = "alive"
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        alpha = 50  
        color_feuilles = (43, 255, 0, alpha)
        couleur_tronc = (150, 75, 25)
        # Le rayon_top représente la canopée, on la dessine en vert transparent
        pygame.draw.circle(surface, color_feuilles, self.pos.astype(int), int(self.rayon_top))
        screen.blit(surface, (0, 0))
        # Un point blanc au centre
        pygame.draw.circle(screen, self.color, self.pos.astype(int), 3)
    