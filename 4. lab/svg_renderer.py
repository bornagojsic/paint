from typing import TYPE_CHECKING

from renderer import Renderer

if TYPE_CHECKING:
    from point import Point


class SVGRenderer(Renderer):
    def __init__(self, file_name: str):
        self._file_name = file_name
        self._lines = ['<svg xmlns="http://www.w3.org/2000/svg" version="1.1">']

    def close(self):
        self._lines.append("</svg>")
        with open(self._file_name, "w") as f:
            f.write("\n".join(self._lines))

    def draw_line(self, s: Point, e: Point):
        line = f'<line x1="{s.get_x()}" y1="{s.get_y()}" x2="{e.get_x()}" y2="{e.get_y()}" style="stroke:blue;"/>'
        self._lines.append(line)

    def fill_polygon(self, points: list[Point]):
        points_str = " ".join(f"{p.get_x()},{p.get_y()}" for p in points)
        polygon = f'<polygon points="{points_str}" style="stroke:red; fill:blue;"/>'
        self._lines.append(polygon)
