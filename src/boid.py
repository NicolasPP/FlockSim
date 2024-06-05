from __future__ import annotations

from random import uniform

from pygame import (
    draw,
    mouse
)
from pygame.math import Vector2
from pygame.surface import Surface

from sim_params import (
    SimulationParameters,
    WallState
)
from utils import (
    scale_to_length,
    clamp_magnitude
)


class Boid:

    @staticmethod
    def random_unit() -> Vector2:
        return Vector2(uniform(-1, 1), uniform(-1, 1)).normalize() * SimulationParameters.get().max_speed

    def __init__(self, pos: Vector2) -> None:
        self._position: Vector2 = pos
        self._velocity: Vector2 = Boid.random_unit()
        self._acceleration: Vector2 = Vector2(0)

        self._surface: Surface = Surface(Vector2(10))
        self._surface.fill("blue")

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
        params: SimulationParameters = SimulationParameters.get()
        draw.line(parent, "blue", self._position, self._position + (self._velocity.normalize() * params.boid_length),
                  params.boid_width)

    def update(self) -> None:
        self._velocity = self._velocity + self._acceleration
        self._position = self._position + self._velocity
        self._acceleration = Vector2(0)

    def seek(self, target: Vector2) -> None:
        params: SimulationParameters = SimulationParameters.get()
        desired_velocity: Vector2 = target - self._position
        scale_to_length(desired_velocity, params.max_speed)
        seek: Vector2 = desired_velocity - self._velocity
        self._apply_force(seek, params.seek_force)

    def avoid(self, target: Vector2) -> None:
        params: SimulationParameters = SimulationParameters.get()
        if self._position.distance_squared_to(target) > params.others_perception * params.others_perception:
            return

        desired_velocity: Vector2 = (target - self._position) * -1
        scale_to_length(desired_velocity, params.max_speed)
        avoid: Vector2 = desired_velocity - self._velocity
        self._apply_force(avoid, params.avoid_force)

    def wrap_wall(self) -> None:
        params: SimulationParameters = SimulationParameters.get()
        if params.wall_state is not WallState.WRAP:
            return

        if self._position.x > params.screen_width:
            self._position.x = 0

        elif self._position.x < 0:
            self._position.x = params.screen_width

        elif self._position.y > params.screen_height:
            self._position.y = 0

        elif self._position.y < 0:
            self._position.y = params.screen_height

    def avoid_wall(self) -> None:
        params: SimulationParameters = SimulationParameters.get()
        if params.wall_state is not WallState.AVOID:
            return

        if any([self._position.x > params.screen_width - params.wall_perception,
                self._position.x < params.wall_perception,
                self._position.y > params.screen_height - params.wall_perception,
                self._position.y < params.wall_perception]):
            self.seek(Vector2(params.screen_width, params.screen_height) // 2)

    def avoid_cursor(self) -> None:
        if not SimulationParameters.get().avoid_cursor:
            return

        self.avoid(Vector2(mouse.get_pos()))

    def flock(self, neighbours: list[Boid]) -> None:
        params: SimulationParameters = SimulationParameters.get()
        neighbours_size: int = len(neighbours)

        if neighbours_size == 0:
            return

        cohesion = separation = alignment = Vector2(0)
        for neighbour in neighbours:
            cohesion = cohesion + neighbour._position
            separation += (self._position - neighbour._position) / neighbour._position.distance_to(self._position)
            alignment = alignment + neighbour._velocity

        # Alignment
        alignment = alignment / neighbours_size
        scale_to_length(alignment, params.max_speed)
        self._apply_force(alignment - self._velocity, params.alignment_force)

        # Cohesion
        cohesion = cohesion / neighbours_size
        self._apply_force(cohesion - self._position, params.cohesion_force)

        # Separation
        separation = separation / neighbours_size
        scale_to_length(separation, params.max_speed)
        self._apply_force(separation, params.separation_force)

    def _apply_force(self, force: Vector2, strength: float) -> None:
        clamp_magnitude(force, strength)
        self._acceleration += force
