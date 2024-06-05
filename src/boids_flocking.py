from dataclasses import dataclass
from random import randint

from pygame import mouse
from pygame.math import Vector2
from pygame.surface import Surface

from accumulator import Accumulator
from sim_params import (
    SimulationParameters,
    WallState
)
from vehicle import Vehicle


@dataclass(slots=True)
class Neighbour:
    distance: float
    boid: Vehicle


class BoidsFlock:

    def __init__(self) -> None:
        params: SimulationParameters = SimulationParameters.get()
        self._update_rate: Accumulator = Accumulator(SimulationParameters.get().update_rate)
        self._boids: list[Vehicle] = [
            Vehicle(Vector2(randint(0, params.screen_height), randint(0, params.screen_width)))
            for _ in range(params.boid_count)
        ]

    def _get_neighbours(self, other: Vehicle) -> list[Neighbour]:
        params: SimulationParameters = SimulationParameters.get()
        neighbours: list[Neighbour] = []
        for boid in self._boids:
            if boid is other:
                continue

            if (0 < boid.position.distance_squared_to(other.position) <
                    params.others_perception * params.others_perception):
                neighbours.append(Neighbour(boid.position.distance_to(other.position), boid))

        return neighbours

    def _avoid_cursor(self) -> None:
        for boid in self._boids:
            boid.avoid(Vector2(mouse.get_pos()))

    def _wrap_wall(self) -> None:
        params: SimulationParameters = SimulationParameters.get()
        for boid in self._boids:
            if boid.position.x > params.screen_width:
                boid.position.x = 0

            elif boid.position.x < 0:
                boid.position.x = params.screen_width

            elif boid.position.y > params.screen_height:
                boid.position.y = 0

            elif boid.position.y < 0:
                boid.position.y = params.screen_height

    def _avoid_wall(self) -> None:
        params: SimulationParameters = SimulationParameters.get()
        for boid in self._boids:
            if any([boid.position.x > params.screen_width - params.wall_perception,
                    boid.position.x < params.wall_perception,
                    boid.position.y > params.screen_height - params.wall_perception,
                    boid.position.y < params.wall_perception]):
                boid.seek(Vector2(params.screen_width, params.screen_height) // 2)

    def _flock(self) -> None:
        params: SimulationParameters = SimulationParameters.get()
        for boid in self._boids:

            neighbours: list[Neighbour] = self._get_neighbours(boid)
            neighbours_size: int = len(neighbours)

            if neighbours_size == 0:
                continue

            average_position: Vector2 = Vector2(0)
            avoid_force: Vector2 = Vector2(0)
            average_direction: Vector2 = Vector2(0)

            for neighbour in neighbours:
                average_position = average_position + neighbour.boid.position
                avoid_force = avoid_force + (boid.position - neighbour.boid.position) / neighbour.distance
                average_direction = average_direction + neighbour.boid.velocity

            # Alignment
            average_direction = average_direction / neighbours_size
            if average_direction.length() > 1e-10:
                average_direction.scale_to_length(params.max_speed)
            boid.apply_force(average_direction - boid.velocity)

            # Cohesion
            average_position = average_position / len(neighbours)
            boid.apply_force(average_position - boid.position)

            # Separation
            avoid_force = avoid_force / neighbours_size
            if avoid_force.length() > 1e-10:
                avoid_force.scale_to_length(params.max_speed)
            boid.apply_force(avoid_force, 0.15)

    def update(self, delta_time: float) -> None:
        if not self._update_rate.wait(delta_time):
            return

        params: SimulationParameters = SimulationParameters.get()
        if params.wall_state is WallState.WRAP:
            self._wrap_wall()

        elif params.wall_state is WallState.AVOID:
            self._avoid_wall()

        if params.avoid_cursor:
            self._avoid_cursor()

        self._flock()

        for boid in self._boids:
            boid.update()

    def render(self, parent: Surface) -> None:
        for boid in self._boids:
            boid.render(parent)
