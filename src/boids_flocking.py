from random import randint

from pygame.math import Vector2
from pygame.surface import Surface

from accumulator import Accumulator
from boid import Boid
from sim_params import (
    SimulationParameters
)


class BoidsFlock:

    def __init__(self) -> None:
        params: SimulationParameters = SimulationParameters.get()
        self._update_rate: Accumulator = Accumulator(SimulationParameters.get().update_rate)
        self._boids: list[Boid] = [
            Boid(Vector2(randint(0, params.screen_width), randint(0, params.screen_height)))
            for _ in range(params.boid_count)
        ]

    def _get_neighbours(self, other: Boid) -> list[Boid]:
        params: SimulationParameters = SimulationParameters.get()
        neighbours: list[Boid] = []
        for boid in self._boids:
            if boid is other:
                continue

            if (0 < boid.position.distance_squared_to(other.position) <
                    params.others_perception * params.others_perception):
                neighbours.append(boid)

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

    def render(self, parent: Surface) -> None:
        for boid in self._boids:
            boid.render(parent)
