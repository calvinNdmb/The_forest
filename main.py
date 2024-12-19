import pygame
import numpy as np

from map.nutrient_map import generate_nutrient_map
from simulation_objects.arbre import Arbre

width, height = 720, 640

def main():

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("The Forest")

    # Paramètres du bruit
    scale = 50
    octaves = 7
    persistence = 0.5
    lacunarity = 1
    nutrient_map = generate_nutrient_map(width, height,scale, octaves, persistence, lacunarity)
    nutrient_map_rgb = np.stack(
            (np.zeros_like(nutrient_map),  # canal rouge à 0
            nutrient_map,                 # canal vert avec les nutriments
            np.zeros_like(nutrient_map)), # canal bleu à 0
            axis=-1
        ).astype(np.uint8)
    numb_tree = 100
    trees = []
    for i in range(numb_tree):
        x, y = np.random.rand(2) * [width, height]
        nutriments = nutrient_map[int(x) % width, int(y) % height]
        trees.append(Arbre(x, y, nutriments))

    # Boucle principale=======================================
    running = True
    day=0
    nutrient_surf = pygame.surfarray.make_surface(nutrient_map_rgb)
    while running:
        day += 1

        screen.blit(nutrient_surf, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Clic pour afficher les nutriments d'un arbre
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                for arbre in trees:
                    dist = np.sqrt((arbre.pos[0] - mouse_x) ** 2 + (arbre.pos[1] - mouse_y) ** 2)
                    # On considère le rayon_top comme la zone cliquable si l'arbre est vivant
                    if arbre.state == "alive" and dist <= arbre.rayon_top:
                        print(f"Nutriments de l'arbre : {arbre.nutriments}, age : {arbre.age}, energie : {arbre.energie},hauteur : {arbre.hauteur}")
                        break
                    elif arbre.state == "seed" and dist <= 2:
                        print(f"Graine : nutriments {arbre.nutriments}, position : {arbre.pos}")

        # Update et draw
        for p in trees:
            p.update(arbres=trees, day=day, width=width, height=height, nutrient_map=nutrient_map)
            p.draw(screen=screen, width=width, height=height)
        if day % 100 == 0:
            print(f"New year!!!!!🎉🎉🎉{day / 100}")

        pygame.display.flip()
        pygame.time.delay(1)

    pygame.quit()

if __name__ == '__main__':
    main()
