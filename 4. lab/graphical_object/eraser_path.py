from typing import TYPE_CHECKING

from graphical_object.abstract_go import AbstractGraphicalObject
from point import Point
from rectangle import Rectangle

if TYPE_CHECKING:
    from graphical_object.interface import GraphicalObject
    from renderer import Renderer


class EraserPath(AbstractGraphicalObject):
    def __init__(self):
        super().__init__([])
        self._path: list[Point] = []

    def add_point(self, point: Point):
        self._path.append(point)
        self._notify_listeners()

    def get_points(self) -> list[Point]:
        return self._path

    def clear(self):
        self._path.clear()
        self._notify_listeners()

    def render(self, r: Renderer):
        for i in range(len(self._path) - 1):
            r.draw_line(self._path[i], self._path[i + 1])

    def selection_distance(self, mouse_point: Point) -> float:
        return float("inf")

    def get_bounding_box(self) -> Rectangle:
        return Rectangle(0, 0, 0, 0)

    def get_shape_name(self): ...

    def get_shape_id(self) -> str: ...

    def duplicate(self): ...

    def is_intersecting_line(self, line_start: Point, line_end: Point) -> bool: ...

    def load(self, stack: list[GraphicalObject], data: str): ...

    def save(self, rows: list[str]): ...
