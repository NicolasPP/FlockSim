import pygame
from pygame import QUIT
from pygame import display
from pygame import event

from boids import Flocking
from config import WIDTH, HEIGHT
from delta_time import DeltaTime
from fps_display import FrameRateDisplay

pygame.init()
display.set_mode((WIDTH, HEIGHT))
display.get_surface().fill("white")

done: bool = False
delta_time: DeltaTime = DeltaTime()
flocking: Flocking = Flocking(WIDTH, HEIGHT, 200)
fps: FrameRateDisplay = FrameRateDisplay()

while not done:

    display.get_surface().fill("white")
    delta_time.set()

    for pygame_event in event.get():
        if pygame_event.type == QUIT:
            done = True

    flocking.update(delta_time.get())
    flocking.render(display.get_surface())
    fps.render(display.get_surface(), delta_time.get_fps())

    display.flip()
