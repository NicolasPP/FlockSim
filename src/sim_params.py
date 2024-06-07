from __future__ import annotations

from dataclasses import dataclass
from enum import (
    Enum,
    auto
)
from typing import (
    Optional,
    ClassVar
)


class WallState(Enum):
    WRAP = auto()
    AVOID = auto()


@dataclass(slots=True)
class SimulationParameters:
    params: ClassVar[Optional[SimulationParameters]] = None

    @staticmethod
    def get() -> SimulationParameters:
        if SimulationParameters.params is None:
            SimulationParameters.params = SimulationParameters()

        return SimulationParameters.params

    screen_width: int = 1200
    screen_height: int = 800
    update_rate: float = 0.02
    max_speed: float = 7.0
    others_perception: int = 55
    wall_perception: int = 60
    boid_count: int = 1000
    wall_state: WallState = WallState.AVOID
    avoid_cursor: bool = True
    boid_length: int = 15
    boid_width: int = 4
    avoid_wall_force: float = 0.5
    avoid_cursor_force: float = 1
    alignment_force: float = 0.1
    cohesion_force: float = 0.1
    separation_force: float = 0.2
    grid_cell_size: int = 15
    max_boid_neighbours: int = 100
