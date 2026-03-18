from typing import TYPE_CHECKING

from renderer import Renderer

if TYPE_CHECKING:
    from canvas import Canvas
    from point import Point


class G2DRenderer(Renderer):
    HOT_POINT_SIZE = 8

    def __init__(self, g2d: Canvas):
        self.__g2d = g2d

    def draw_line(self, s: Point, e: Point):
        self.__g2d.create_line(*s.get(), *e.get(), fill="blue")

    def fill_polygon(self, points: list[Point]):
        coords = [p.get() for p in points]
        self.__g2d.create_polygon(coords, fill="blue", outline="red")
