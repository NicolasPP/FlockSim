from __future__ import annotations

from enum import (
    Enum,
    auto
)
from typing import Optional


class WallState(Enum):
    WRAP = auto()
    AVOID = auto()


class SimulationParameters:

    params: Optional[SimulationParameters] = None

    @staticmethod
    def get() -> SimulationParameters:
        if SimulationParameters.params is None:
            SimulationParameters.params = SimulationParameters()

        return SimulationParameters.params

    def __init__(self, screen_width: int = 1200, screen_height: int = 800, update_rate: float = 0.02,
                 max_speed: float = 4.0, max_force: float = 0.09, others_perception: int = 50,
                 wall_perception: int = 60, boid_count: int = 300, wall_state: WallState = WallState.AVOID,
                 avoid_cursor: bool = True) -> None:
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.update_rate: float = update_rate
        self.max_speed: float = max_speed
        self.max_force: float = max_force
        self.others_perception: int = others_perception
        self.wall_perception: int = wall_perception
        self.boid_count: int = boid_count
        self.wall_state: WallState = wall_state
        self.avoid_cursor: bool = avoid_cursor
