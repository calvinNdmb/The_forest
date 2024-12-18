import numpy as np
import noise


def generate_nutrient_map(width, height,scale, octaves, persistence, lacunarity):
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
