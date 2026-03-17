from abc import ABC, abstractmethod

from point import Point


class Renderer(ABC):
    @abstractmethod
    def draw_line(self, s: Point, e: Point): ...

    @abstractmethod
    def fill_polygon(self, points: list[Point]): ...

    @abstractmethod
    def draw_bounding_box(self, points: list[Point]): ...

    @abstractmethod
    def draw_hot_points(self, points: list[Point]): ...
