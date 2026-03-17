# public class G2DRendererImpl implements Renderer {

#   private Graphics2D g2d;

#   public G2DRendererImpl(Graphics2D g2d) {
#     // ...
#   }

#   @Override
#   public void drawLine(Point s, Point e) {
#     // Postavi boju na plavu
#     // Nacrtaj linijski segment od S do E
#     // (sve to uporabom g2d dobivenog u konstruktoru)
#   }

#   @Override
#   public void fillPolygon(Point[] points) {
#     // Postavi boju na plavu
#     // Popuni poligon definiran danim točkama
#     // Postavi boju na crvenu
#     // Nacrtaj rub poligona definiranog danim točkama
#     // (sve to uporabom g2d dobivenog u konstruktoru)
#   }

# }

from typing import TYPE_CHECKING

from renderer import Renderer

if TYPE_CHECKING:
    from canvas import Canvas
    from point import Point


class G2DRenderer(Renderer):
    def __init__(self, g2d: Canvas):
        self.__g2d = g2d

    def draw_line(self, s: Point, e: Point):
        self.__g2d.create_line(*s.get(), *e.get(), fill="blue")

    def fill_polygon(self, points: list[Point]):
        coords = [p.get() for p in points]
        self.__g2d.create_polygon(coords, fill="blue", outline="red")
