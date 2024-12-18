import pygame
import numpy as np
import noise

# Dimensions de la fenêtre
width, height = 720, 640

def generate_nutrient_map(scale, octaves, persistence, lacunarity, offset):
    nutrient_map = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            nx = (i / scale) + offset
            ny = (j / scale) + offset
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

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Bruit fluide en déplacement")

    # Paramètres du bruit
    scale = 80
    octaves = 8
    persistence = 0.5
    lacunarity = 1

    # Initialisation de la variable de décalage
    offset = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Génération d'une nouvelle carte de nutriments avec un décalage temporel
        nutrient_map = generate_nutrient_map(scale, octaves, persistence, lacunarity, offset)
        nutrient_map_rgb = np.stack((nutrient_map, nutrient_map, nutrient_map), axis=-1).astype(np.uint8)
        nutrient_surf = pygame.surfarray.make_surface(nutrient_map_rgb)
        screen.blit(nutrient_surf, (0, 0))

        # Mise à jour de l'affichage
        pygame.display.flip()

        # Augmentation de l'offset pour déplacer le bruit
        offset += 0.1  # Changez cette valeur pour ajuster la vitesse du déplacement

        pygame.time.delay(10)

    pygame.quit()

main()
