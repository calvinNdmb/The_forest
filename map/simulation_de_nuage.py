import pygame
import numpy as np

from map.nutrient_map import generate_nutrient_map
from map.utils import create_noise

# Dimensions de la fenêtre
width, height = 720, 640
# Fonction de génération des clouds
def generate_clouds_surface(scale, octaves, persistence, lacunarity, offset):
    nutrient_map = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            nx = (i / scale) + offset
            ny = (j / scale) + offset
            nutrient_map[i, j] = create_noise(nx=nx, ny=ny, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
    return nutrient_map


# Fonction principale
def main():
    # Initialisation de Pygame
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Bruit fluide en déplacement avec transparence")

    # Paramètres du bruit =======================================
    scale = 80
    octaves = 8
    persistence = 0.5
    lacunarity = 1
    offset = 1

    # Génération de la carte de nutriments ======================
    nutrient_map = generate_nutrient_map(width, height,scale, octaves, persistence, lacunarity)
    nutrient_map_rgb = np.stack(
            (np.zeros_like(nutrient_map),  # canal rouge à 0
            nutrient_map,                 # canal vert avec les nutriments
            np.zeros_like(nutrient_map)), # canal bleu à 0
            axis=-1
        ).astype(np.uint8) # On convertit en entiers non-signés pour Pygame
    nutrient_surf = pygame.surfarray.make_surface(nutrient_map_rgb)

    # Boucle principale ========================================
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Génération d'une nouvelle carte de clouds à chaque frame pour simuler le mouvement=======================================
        offset += 0.1  # Changez cette valeur pour ajuster la vitesse du déplacement
        nutrient_surface = generate_clouds_surface(scale, octaves, persistence, lacunarity, offset)
        nutrient_surface.set_alpha(100)  # Réglage de la transparence

        # Dessiner la surface à l'écran
        screen.blit(nutrient_surf, (0, 0))
        screen.blit(nutrient_surface, (0, 0))




        pygame.display.flip()
        pygame.time.delay(1)

    pygame.quit()

main()
