from pygame.math import Vector2

from boid import Boid


class SpacialGrid[T]:

    def __init__(self, cell_size: int) -> None:
        self._grid: dict[tuple[int, int], list[T]] = {}
        self._cell_size: int = cell_size

    def clear(self) -> None:
        self._grid = {}

    def add(self, position: Vector2, obj: T) -> None:
        index: Vector2 = position // self._cell_size
        if (index.y, index.x) not in self._grid:
            self._grid[(index.y, index.x)] = [obj]
        else:
            self._grid[(index.y, index.x)].append(obj)

    def get_surrounding(self, position: Vector2) -> list[Boid]:
        index: Vector2 = position // self._cell_size
        return self._grid.get((index.y, index.x), [])
