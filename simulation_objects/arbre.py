import pygame
import numpy as np
import random

class Arbre:
    def __init__(self, map_width, map_height, x, y, nutriments):
        self.map_width = map_width
        self.map_height = map_height
        self.pos = np.array([x, y], dtype=float)
        self.color = (255, 255, 255)
        self.nutriments = nutriments  # Nutriments à la position initiale

        # Etats possibles : "seed", "alive", "dead"
        self.state = "seed"
        # Les rayons max
        self.rayon_top_max = random.randint(10, 40)
        self.rayon_bot_max = random.randint(10, 20)
        # Début à 0 quand c'est une graine, ils pousseront quand la plante éclot
        self.rayon_top = 0
        self.rayon_bot = 0
        self.max_age = random.randint(1, 40)
        self.age = 0

    def update(self, arbres):
        if self.state == "seed":
            # La graine a une probabilité de mourir ou d'éclore
            # Disons une probabilité de 0.001 de mourir à chaque update
            # et une probabilité de 0.005 d'éclore
            if random.random() < 0.001:
                self.state = "dead"
            elif random.random() < 0.005:
                self.state = "alive"
                self.rayon_top = 1
                self.rayon_bot = 1
        elif self.state == "alive":
            if self.age >= self.max_age:
                self.state = "dead"
                return
            # Calcul de la production d'énergie (simplifiée)
            # Énergie aérienne (soleil)
            area_top = np.pi * (self.rayon_top**2)
            # Énergie souterraine (racines)
            area_bot = np.pi * (self.rayon_bot**2)

            top_factor = 1.0
            bot_factor = 1.0

            # Vérifier si une plante plus grande recouvre celle-ci pour le rayon_top
            for autre in arbres:
                if autre is self or autre.state != "alive":
                    continue
                dist = np.linalg.norm(self.pos - autre.pos)
                # Check overlap top
                if dist < (self.rayon_top + autre.rayon_top):
                    # Il y a chevauchement aérien
                    if autre.rayon_top > self.rayon_top:
                        # Cette plante est plus petite, elle subit un -50% sur la production aérienne
                        top_factor *= 0.5

                # Check overlap bottom
                if dist < (self.rayon_bot + autre.rayon_bot):
                    # Il y a chevauchement souterrain
                    if autre.rayon_bot > self.rayon_bot:
                        # Cette plante est moins profonde, -50% sur la prod souterraine
                        bot_factor *= 0.5

            # Énergie totale (très simplifiée)
            production_top = area_top * top_factor
            production_bot = area_bot * bot_factor
            production = production_top + production_bot

            # Une partie de l'énergie sert à grandir si pas encore au max
            if self.rayon_top < self.rayon_top_max:
                # Consommer un peu d'énergie pour croître
                growth_cost = 5  # Coût arbitraire pour grandir le top
                if production > growth_cost:
                    self.rayon_top += 0.1
                    production -= growth_cost

            if self.rayon_bot < self.rayon_bot_max:
                # Consommer un peu d'énergie pour croître le bottom
                growth_cost = 5
                if production > growth_cost:
                    self.rayon_bot += 0.1
                    production -= growth_cost

            # S'il n'y a plus d'énergie (production très faible), la plante pourrait régresser, voire mourir
            # Ici on n'implémente pas la mort par manque d'énergie, mais on pourrait.

        # Si dead, ne rien faire

    def draw(self, screen):
        if self.state == "dead":
            return
        if self.state == "seed":
            # Dessiner la graine comme un petit point
            pygame.draw.circle(screen, (255, 0, 0), self.pos.astype(int), 2)
            return
        # state = "alive"
        surface = pygame.Surface((self.map_width, self.map_height), pygame.SRCALPHA)
        alpha = 50
        color_feuilles = (43, 255, 0, alpha)
        couleur_tronc = (150, 75, 25)
        # Le rayon_bot représente la partie souterraine, on la dessine en marron
        """pygame.draw.circle(surface, couleur_tronc, self.pos.astype(int), int(self.rayon_bot))
        screen.blit(surface, (0, 0))"""
        # Le rayon_top représente la canopée, on la dessine en vert transparent
        pygame.draw.circle(surface, color_feuilles, self.pos.astype(int), int(self.rayon_top))
        screen.blit(surface, (0, 0))
        # Un point blanc au centre
        pygame.draw.circle(screen, self.color, self.pos.astype(int), 3)