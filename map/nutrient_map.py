import numpy as np

from map.utils import create_noise

def generate_nutrient_map(
        width: int,
        height: int,
        scale: int,
        octaves: int,
        persistence: float,
        lacunarity: int,
        offset: float = 0
) -> np.ndarray:
    nutrient_map = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            nx = i / scale + offset
            ny = j / scale  + offset
            nutrient_map[i, j] = create_noise(nx=nx, ny=ny, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
    return nutrient_map
