from pygame.math import Vector2

from config import VECTOR_EPSILON


def scale_to_length(vector: Vector2, length: float) -> None:
    if vector.length_squared() > VECTOR_EPSILON * VECTOR_EPSILON:
        vector.scale_to_length(length)


def clamp_magnitude(vector: Vector2, magnitude: float):
    if vector.length_squared() > VECTOR_EPSILON * VECTOR_EPSILON:
        vector.clamp_magnitude_ip(magnitude)
