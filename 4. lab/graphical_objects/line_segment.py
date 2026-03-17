from typing import TYPE_CHECKING

from graphical_objects.abstract_go import AbstractGraphicalObject
from point import Point

if TYPE_CHECKING:
    from graphical_objects.interface import GraphicalObject
    from rectangle import Rectangle
    from renderer import Renderer


class LineSegment(AbstractGraphicalObject):
    def __init__(
        self, start_point: Point = Point(0, 0), end_point: Point = Point(10, 0)
    ):
        self._hot_points = [start_point, end_point]
        super().__init__(self._hot_points)

    def get_shape_name(self):
        return "Linija"

    ## TODO: Implementirati
    def get_shape_id(self) -> int: ...

    def duplicate(self):
        start_point, end_point = self._hot_points
        return LineSegment(start_point, end_point)

    def render(self, r: Renderer):
        start_point, end_point = self._hot_points
        r.draw_line(start_point, end_point)

    ## TODO: Implementirati ...
    def selection_distance(self, mouse_point: Point) -> float: ...

    def get_bounding_box(self) -> Rectangle: ...

    def load(self, stack: list[GraphicalObject], data: str): ...

    def save(self, rows: list[str]): ...

    def __str__(self):
        return f"LineSegment from {self._hot_points[0]} to {self._hot_points[1]}"
