from pygame.font import Font
from pygame.font import SysFont
from pygame.font import get_fonts
from pygame.surface import Surface

from config import FPS_FONT_SIZE


class FrameRateDisplay:

    def __init__(self) -> None:
        self._font: Font = SysFont(get_fonts()[0], FPS_FONT_SIZE)
        self._surface: Surface = self._create_surface()

    def _create_surface(self) -> Surface:
        return Surface(self._font.size("144"))

    def render(self, parent: Surface, fps: float) -> None:
        self._surface.fill("black")
        fps_surface: Surface = self._font.render(str(fps), True, "white", "black")
        self._surface.blit(fps_surface, fps_surface.get_rect(center=self._surface.get_rect().center))
        parent.blit(self._surface, (0, 0))
