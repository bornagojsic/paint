from math import cos, sin
from math import pi as PI
from typing import TYPE_CHECKING

from geometry_util import GeometryUtil
from graphical_objects.abstract_go import AbstractGraphicalObject
from point import Point
from rectangle import Rectangle

if TYPE_CHECKING:
    from graphical_objects.interface import GraphicalObject
    from renderer import Renderer


class Oval(AbstractGraphicalObject):
    NUMBER_OF_POINTS: int = 100

    def __init__(
        self,
        right_hot_point: Point = Point(10, 0),
        down_hot_point: Point = Point(0, 10),
    ):
        self._hot_points = [right_hot_point, down_hot_point]
        super().__init__(self._hot_points)

    def _set_center_a_b(self, right_hot_point: Point, down_hot_point: Point):
        self._right_hot_point = right_hot_point
        self._down_hot_point = down_hot_point
        self._center = Point(down_hot_point.get_x(), right_hot_point.get_y())
        self._a = abs(self._center.get_x() - self._right_hot_point.get_x())
        self._b = abs(self._center.get_y() - self._down_hot_point.get_y())

    def get_shape_name(self):
        return "Oval"

    def get_shape_id(self) -> int: ...

    def duplicate(self):
        right_hot_point, down_hot_point = self._hot_points
        return Oval(right_hot_point, down_hot_point)

    def __get_point_at_t(self, t: float) -> Point:
        x = self._a * cos(t) + self._center.get_x()
        y = self._b * sin(t) + self._center.get_y()
        return Point(x, y)

    def __get_t(self, i: int) -> float:
        return 2 * PI * i / self.NUMBER_OF_POINTS

    def __get_point(self, i: int) -> Point:
        t = self.__get_t(i)
        return self.__get_point_at_t(t)

    def __get_points(self) -> list[Point]:
        right_hot_point, down_hot_point = self._hot_points
        self._set_center_a_b(right_hot_point, down_hot_point)
        return [self.__get_point(i) for i in range(self.NUMBER_OF_POINTS)]

    def render(self, r: Renderer):
        points = self.__get_points()
        r.fill_polygon(points)

    def __is_inside(self, mouse_point: Point) -> bool:
        x = mouse_point.get_x() - self._center.get_x()
        y = mouse_point.get_y() - self._center.get_y()
        return (x**2) / (self._a**2) + (y**2) / (self._b**2) <= 1

    def selection_distance(self, mouse_point: Point) -> float:
        points = self.__get_points()

        if self.__is_inside(mouse_point):
            return 0

        return min(
            GeometryUtil.distance_from_point(points[i], mouse_point)
            for i in range(len(points))
        )

    def get_bounding_box(self) -> Rectangle:
        self._set_center_a_b(*self._hot_points)
        top_left = Point(self._center.get_x() - self._a, self._center.get_y() - self._b)
        x, y = top_left.get()
        width = 2 * self._a
        height = 2 * self._b
        return Rectangle(x, y, width, height)

    def load(self, stack: list[GraphicalObject], data: str): ...

    def save(self, rows: list[str]): ...
