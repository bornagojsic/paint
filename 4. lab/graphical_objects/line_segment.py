from typing import TYPE_CHECKING

from geometry_util import GeometryUtil
from graphical_objects.abstract_go import AbstractGraphicalObject
from point import Point
from rectangle import Rectangle

if TYPE_CHECKING:
    from graphical_objects.interface import GraphicalObject
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

    def selection_distance(self, mouse_point: Point) -> float:
        return GeometryUtil.distance_from_line_segment(*self._hot_points, mouse_point)

    def get_bounding_box(self) -> Rectangle:
        right_hot_point, down_hot_point = self._hot_points
        center = (down_hot_point + right_hot_point) * 0.5
        a = abs(center.get_x() - right_hot_point.get_x())
        b = abs(center.get_y() - down_hot_point.get_y())
        top_left = Point(center.get_x() - a, center.get_y() - b)
        return Rectangle(*top_left.get(), 2 * a, 2 * b)

    ## TODO: Implementirati ...
    def load(self, stack: list[GraphicalObject], data: str): ...

    def save(self, rows: list[str]): ...

    def __str__(self):
        return f"LineSegment from {self._hot_points[0]} to {self._hot_points[1]}"
