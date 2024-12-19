import noise
import numpy as np


def create_noise(nx: float, ny: float, octaves: int, persistence: float, lacunarity: int) -> np.ndarray:
    val = noise.pnoise2(
        nx,
        ny,
        octaves=octaves,
        persistence=persistence,
        lacunarity=lacunarity,
        repeatx=1024,
        repeaty=1024,
        base=9
    )
    pixel_val = (val + 1) / 2 * 255
    # Discrétisation
    if pixel_val <= 25:
        pixel_val = 0
    elif pixel_val <= 50 and pixel_val > 25:
        pixel_val = 50
    elif pixel_val <= 75 and pixel_val > 50:
        pixel_val = 75
    elif pixel_val <= 100 and pixel_val > 75:
        pixel_val = 100
    elif pixel_val <= 125 and pixel_val > 100:
        pixel_val = 125
    elif pixel_val <= 150 and pixel_val > 125:
        pixel_val = 150
    elif pixel_val <= 175 and pixel_val > 150:
        pixel_val = 175
    elif pixel_val <= 200 and pixel_val > 175:
        pixel_val = 200
    elif pixel_val <= 225 and pixel_val > 200:
        pixel_val = 225
    elif pixel_val <= 250 and pixel_val > 225:
        pixel_val = 250
            
    return pixel_val