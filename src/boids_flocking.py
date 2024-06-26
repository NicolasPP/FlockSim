from random import randint

from pygame.math import Vector2
from pygame.surface import Surface

from accumulator import Accumulator
from boid import Boid
from sim_params import (
    SimulationParameters
)
from spacial_grid import SpacialGrid


class BoidsFlock:

    def __init__(self) -> None:
        params: SimulationParameters = SimulationParameters.get()
        self._grid: SpacialGrid[Boid] = SpacialGrid(params.grid_cell_size, params.screen_width, params.screen_height)
        self._update_rate: Accumulator = Accumulator(SimulationParameters.get().update_rate)
        self._boids: list[Boid] = self._create_boids()

    def _create_boids(self) -> list[Boid]:
        boids: list[Boid] = []
        params: SimulationParameters = SimulationParameters.get()
        for _ in range(params.boid_count):
            position: Vector2 = Vector2(randint(0, params.screen_width), randint(0, params.screen_height))
            boid: Boid = Boid(position)
            self._grid.add(position, boid)
            boids.append(boid)

        return boids

    def _get_neighbours(self, boid: Boid) -> list[tuple[Boid, float]]:
        params: SimulationParameters = SimulationParameters.get()
        neighbours: list[tuple[Boid, float]] = []
        for other in self._grid.query(boid.position):
            if other is boid:
                continue

            if len(neighbours) >= params.max_boid_neighbours:
                return neighbours

            distance: float = other.position.distance_to(boid.position)
            if 0 < distance < params.others_perception:
                neighbours.append((other, distance))

        return neighbours

    def update(self, delta_time: float) -> None:
        if not self._update_rate.wait(delta_time):
            return

        for boid in self._boids:

            boid.flock(self._get_neighbours(boid))
            boid.wrap_wall()
            boid.avoid_wall()
            boid.avoid_cursor()
            boid.update()

        self._grid.clear()
        for boid in self._boids:
            self._grid.add(boid.position, boid)

    def render(self, parent: Surface) -> None:
        for boid in self._boids:
            boid.render(parent)
