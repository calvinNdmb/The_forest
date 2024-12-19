import numpy as np

from map.utils import create_noise

def generate_nutrient_map(
        width: int,
        height: int,
        scale: int,
        octaves: int,
        persistence: float,
        lacunarity: int
) -> np.ndarray:
    nutrient_map = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            nx = i / scale
            ny = j / scale
            nutrient_map[i, j] = create_noise(nx=nx, ny=ny, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
    return nutrient_map
