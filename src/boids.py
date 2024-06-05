from dataclasses import dataclass
from random import randint

from pygame import mouse
from pygame.math import Vector2
from pygame.surface import Surface

from accumulator import Accumulator
from config import (
    UPDATE_RATE,
    MAX_SPEED,
    PERCEPTION,
    TURN_AROUND_DIST
)
from vehicle import Vehicle


@dataclass(slots=True)
class Neighbour:
    distance: float
    boid: Vehicle


class Flocking:

    def __init__(self, screen_width: int, screen_height: int, boids_count: int = 10) -> None:
        self._screen_height: int = screen_height
        self._screen_width: int = screen_width
        self._boids_count: int = boids_count
        self._update_rate: Accumulator = Accumulator(UPDATE_RATE)

        self._boids: list[Vehicle] = self._create_boids()
        self._awareness: int = 40

    def _create_boids(self) -> list[Vehicle]:
        return [Vehicle(Vector2(randint(0, self._screen_height), randint(0, self._screen_width))) for _ in
                range(self._boids_count)]

    def _get_neighbours(self, other: Vehicle) -> list[Neighbour]:
        neighbours: list[Neighbour] = []
        for boid in self._boids:
            if boid is other:
                continue

            if 0 < boid.position.distance_squared_to(other.position) < PERCEPTION * PERCEPTION:
                neighbours.append(Neighbour(boid.position.distance_to(other.position), boid))

        return neighbours

    def _wrap(self) -> None:
        for boid in self._boids:
            if boid.position.x > self._screen_width:
                boid.position.x = 0

            elif boid.position.x < 0:
                boid.position.x = self._screen_width

            elif boid.position.y > self._screen_height:
                boid.position.y = 0

            elif boid.position.y < 0:
                boid.position.y = self._screen_height

    def _avoid_wall(self) -> None:
        for boid in self._boids:
            if any([boid.position.x > self._screen_width - TURN_AROUND_DIST, boid.position.x < TURN_AROUND_DIST,
                    boid.position.y > self._screen_height - TURN_AROUND_DIST, boid.position.y < TURN_AROUND_DIST]):
                boid.seek(Vector2(self._screen_width, self._screen_height) // 2)

    def update(self, delta_time: float) -> None:
        if not self._update_rate.wait(delta_time):
            return

        # self._wrap()
        self._avoid_wall()

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
            if average_direction.length() > 1e-15:
                average_direction.scale_to_length(MAX_SPEED)
            boid.apply_force(average_direction - boid.velocity)

            # Cohesion
            average_position = average_position / len(neighbours)
            boid.apply_force(average_position - boid.position)

            # Separation
            avoid_force = avoid_force / neighbours_size
            if avoid_force.length() > 1e-15:
                avoid_force.scale_to_length(MAX_SPEED)
            boid.apply_force(avoid_force, 0.15)

            boid.avoid(Vector2(mouse.get_pos()))

        for boid in self._boids:
            boid.update()

    def render(self, parent: Surface) -> None:
        for boid in self._boids:
            boid.render(parent)
