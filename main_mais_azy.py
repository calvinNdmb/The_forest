#🧐
import pygame
import numpy as np
import random
import noise
import math
width, height = 720, 640

def generate_nutrient_map(scale, octaves, persistence, lacunarity):
    nutrient_map = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            nx = i / scale
            ny = j / scale
            val = noise.pnoise2(nx, ny, octaves=octaves, persistence=persistence, 
                                lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=9)
            pixel_val = (val + 1) / 2 * 255
            # Discrétisation
            if pixel_val <= 50:
                pixel_val = 0
            elif pixel_val <= 100 and pixel_val > 50:
                pixel_val = 100
            elif pixel_val <= 150 and pixel_val > 100:
                pixel_val = 150
            elif pixel_val <= 200 and pixel_val > 150:
                pixel_val = 255
            nutrient_map[i, j] = pixel_val
    return nutrient_map

class Arbre:
    def __init__(self, x, y, nutriments):
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

    def update(self, arbres):
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
            if self.energie >50 and self.energie<60:
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
        self.energie=100-np.log(self.rayon_top)*30*self.nutriments/100
        
    def draw(self, screen):
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

def main():
    
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Gravité")

    # Paramètres du bruit
    scale = 50
    octaves = 7
    persistence = 0.5
    lacunarity = 1
    nutrient_map = generate_nutrient_map(scale, octaves, persistence, lacunarity)
    nutrient_map_rgb = np.stack((nutrient_map, nutrient_map, nutrient_map), axis=-1).astype(np.uint8)
    numb_tree = 100
    trees = []
    for i in range(numb_tree):
        x, y = np.random.rand(2) * [width, height]
        nutriments = nutrient_map[int(x) % width, int(y) % height]
        trees.append(Arbre(x, y, nutriments))

    # Boucle principale=======================================
    running = True
    day=0
    while running:
        day+=1
        nutrient_surf = pygame.surfarray.make_surface(nutrient_map_rgb)
        screen.blit(nutrient_surf, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Clic pour afficher les nutriments d'un arbre
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                for arbre in trees:
                    dist = np.sqrt((arbre.pos[0] - mouse_x)**2 + (arbre.pos[1] - mouse_y)**2)
                    # On considère le rayon_top comme la zone cliquable si l'arbre est vivant
                    if arbre.state == "alive" and dist <= arbre.rayon_top:
                        print(f"Nutriments de l'arbre : {arbre.nutriments}, age : {arbre.age} , position : {arbre.pos}, energie : {arbre.energie}, rayon_top : {arbre.rayon_top}")
                        break
                    elif arbre.state == "seed" and dist <= 2:
                        print(f"Graine : nutriments {arbre.nutriments}, position : {arbre.pos}")

        # Update et draw
        for p in trees:
            p.update(trees)
            p.draw(screen)
        if day%100==0:
            print(f"New year!!!!!🎉🎉🎉{day}")
            for p in trees:
                p.age+=1
        pygame.display.flip()
        pygame.time.delay(1)

    pygame.quit()
main()
