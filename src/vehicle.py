from random import uniform

from pygame.math import Vector2
from pygame.surface import Surface

from config import MAX_SPEED, MAX_FORCE, PERCEPTION


class Vehicle:

    @staticmethod
    def random_unit() -> Vector2:
        return Vector2(uniform(-1, 1), uniform(-1, 1)).normalize() * MAX_SPEED

    def __init__(self, pos: Vector2) -> None:
        self._position: Vector2 = pos
        self._velocity: Vector2 = Vehicle.random_unit()
        self._acceleration: Vector2 = Vector2(0)

        self._surface: Surface = Surface(Vector2(10))
        self._surface.fill("blue")

    @property
    def velocity(self) -> Vector2:
        return self._velocity

    @velocity.setter
    def velocity(self, velocity: Vector2) -> None:
        self._velocity = velocity

    @velocity.deleter
    def velocity(self) -> None:
        del self._velocity

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, position: Vector2) -> None:
        self._position = position

    @position.deleter
    def position(self) -> None:
        del self._position

    def render(self, parent: Surface) -> None:
        parent.blit(self._surface, self._surface.get_rect(center=self._position))

    def update(self) -> None:
        self._velocity = self._velocity + self._acceleration
        if self.velocity.length() > 1e-15:
            self._velocity.clamp_magnitude_ip(MAX_SPEED)

        self._position = self._position + self._velocity
        self._acceleration = Vector2(0)

    def seek(self, target: Vector2, seek_force: float = 0.5) -> None:
        desired_velocity: Vector2 = target - self._position
        desired_velocity.scale_to_length(MAX_SPEED)
        self.apply_force(desired_velocity - self._velocity, seek_force)

    def avoid(self, target: Vector2) -> None:
        if self._position.distance_squared_to(target) > PERCEPTION * PERCEPTION:
            return

        desired_velocity: Vector2 = (target - self._position) * -1
        if desired_velocity.length() > 1e-15:
            desired_velocity.scale_to_length(MAX_SPEED)
        self.apply_force(desired_velocity - self._velocity, 0.5)

    def apply_force(self, force: Vector2, max_force: float = MAX_FORCE) -> None:
        if force.magnitude_squared() > 1e-15:
            force.clamp_magnitude_ip(max_force)

        self._acceleration += force
