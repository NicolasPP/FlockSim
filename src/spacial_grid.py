from itertools import product

from pygame import (
    draw,
    mouse
)
from pygame.math import Vector2
from pygame.surface import Surface

from boid import Boid


class SpacialGrid[T]:

    def __init__(self, cell_size: int, space_width: int, space_height: int) -> None:
        self._space_width: int = space_width
        self._space_height: int = space_height
        self._grid: dict[tuple[int, int], list[T]] = {}
        self._surrounding_cells: dict[tuple[int, int], list[tuple[int, int]]] = {}
        self._cell_size: int = cell_size
        self._populate_surrounding_cells()

    def _populate_surrounding_cells(self) -> None:
        for row, col in product(range(self._space_height // self._cell_size),
                                range(self._space_width // self._cell_size)):
            self._surrounding_cells[(row, col)] = [
                (row - 1, col),  # top
                (row + 1, col),  # bottom
                (row, col + 1),  # right
                (row, col - 1),  # left
                (row - 1, col + 1),  # top right
                (row - 1, col - 1),  # top left
                (row + 1, col + 1),  # bottom right
                (row + 1, col - 1)  # bottom left
            ]

    def clear(self) -> None:
        self._grid = {}

    def add(self, position: Vector2, obj: T) -> None:
        index: Vector2 = position // self._cell_size
        if (index.y, index.x) not in self._grid:
            self._grid[(index.y, index.x)] = [obj]
        else:
            self._grid[(index.y, index.x)].append(obj)

    def query(self, position: Vector2, surround_cells: bool = True) -> list[T]:
        index: Vector2 = position // self._cell_size
        result: list[T] = self._grid.get((index.y, index.x), []).copy()

        if not surround_cells:
            return result

        for surrounding_index in self._surrounding_cells.get((index.y, index.x), []):
            result.extend(self._grid.get(surrounding_index, []))

        return result

    def show_hover(self, parent: Surface) -> None:
        pos_index: Vector2 = Vector2(mouse.get_pos()) // self._cell_size
        center: Vector2 = (pos_index * self._cell_size) + Vector2(self._cell_size // 2)
        draw.circle(parent, "white", center, self._cell_size * 2, 4)

    def get_surrounding(self, position: Vector2) -> list[Boid]:
        index: Vector2 = position // self._cell_size
        return self._grid.get((index.y, index.x), [])
