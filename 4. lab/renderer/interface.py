from abc import ABC, abstractmethod

from point import Point


class Renderer(ABC):
    @abstractmethod
    def draw_line(self, s: Point, e: Point): ...

    @abstractmethod
    def fill_polygon(self, points: list[Point]): ...
