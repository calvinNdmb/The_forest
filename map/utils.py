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
    if pixel_val <= 50:
        pixel_val = 0
    elif 100 >= pixel_val > 50:
        pixel_val = 100
    elif 150 >= pixel_val > 100:
        pixel_val = 150
    elif 200 >= pixel_val > 150:
        pixel_val = 255
    return pixel_val