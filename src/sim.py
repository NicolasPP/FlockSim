import pygame
from pygame import (
    QUIT,
    display,
    event
)

from boids_flocking import BoidsFlock
from delta_time import DeltaTime
from fps_display import FrameRateDisplay
from sim_params import SimulationParameters


class Simulation:

    def __init__(self) -> None:
        pygame.init()

        self._flock: BoidsFlock = BoidsFlock()
        self._delta_time: DeltaTime = DeltaTime()
        self._fps: FrameRateDisplay = FrameRateDisplay()
        self._done: bool = False

    def run(self) -> None:
        params: SimulationParameters = SimulationParameters.get()
        display.set_mode((params.screen_width, params.screen_height))

        while not self._done:

            display.get_surface().fill("white")
            self._delta_time.set()

            for pygame_event in event.get():
                if pygame_event.type == QUIT:
                    self._done = True

            self._flock.update(self._delta_time.get())
            self._flock.render(display.get_surface())
            self._fps.render(display.get_surface(), self._delta_time.get_fps())

            display.flip()
