import pygame
import numpy as np
import matplotlib.pyplot as plt
from map.nutrient_map import generate_nutrient_map
from simulation_objects.arbre import Arbre
from map.utils import graphiques

width, height = 720, 640
number_of_tree_vivants = []
number_of_seeds = []
mean_age = []
mean_rayons_tops = []
mean_energies = []
mean_energies_solaires = []
mean_hauteurs = []
def main(numb_tree = 50):

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
    trees = []
    for i in range(numb_tree):
        x, y = np.random.rand(2) * [width, height]
        nutriments = nutrient_map[int(x) % width, int(y) % height]
        trees.append(Arbre(x, y, nutriments))

    # Boucle principale=======================================
    running = True
    day=0
    nutrient_surf = pygame.surfarray.make_surface(nutrient_map_rgb)
    updated_trees = []
    while running:
        ages = 0
        rayons_tops=0
        energies=0
        energies_solaires=0
        hauteurs=0
        day += 1
        updated_trees = []
        alive_count = 0
        seed_count = 0
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
            # Inclure uniquement les arbres vivants ou les graines
            if p.state == "alive":
                updated_trees.append(p)
                #pour les statistiques
                alive_count += 1
                ages += p.age
                rayons_tops += p.rayon_top
                energies += p.energie
                energies_solaires += p.energie_solaire
                hauteurs += p.hauteur
            elif p.state == "seed":
                seed_count += 1
                updated_trees.append(p)
        trees = updated_trees 
        if day % 5 == 0:   
            if alive_count != 0 :
                mean_age.append(ages/alive_count)
                mean_rayons_tops.append(rayons_tops/alive_count)
                mean_energies.append(energies/alive_count)
                mean_energies_solaires.append(energies_solaires/alive_count)
                mean_hauteurs.append(hauteurs/alive_count) 
            number_of_tree_vivants.append(alive_count)
            number_of_seeds.append(seed_count)

        if day % 100 == 0:
            print(f"New year!!!!!🎉🎉🎉{day/100}, Nombre d'arbre {number_of_tree_vivants[-1]},Nombre de seeds {number_of_seeds[-1]}")

        pygame.display.flip()
        pygame.time.delay(1)
        if alive_count == 0 and seed_count == 0:
            running = False
    pygame.quit()
    return number_of_tree_vivants, number_of_seeds,mean_age, mean_rayons_tops,mean_energies, mean_energies_solaires, mean_hauteurs

if __name__ == '__main__':
    number_of_tree_vivants, number_of_seeds, mean_age, mean_rayons_tops,mean_energies, mean_energies_solaires, mean_hauteurs = main(300)
    graphiques(number_of_tree_vivants, number_of_seeds, mean_age, mean_rayons_tops, 
               mean_energies, mean_energies_solaires, mean_hauteurs)
