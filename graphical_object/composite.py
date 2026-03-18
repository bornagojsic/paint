from typing import TYPE_CHECKING

from graphical_object.abstract_go import AbstractGraphicalObject
from point import Point
from rectangle import Rectangle

if TYPE_CHECKING:
    from graphical_object.interface import GraphicalObject
    from renderer import Renderer


class CompositeShape(AbstractGraphicalObject):
    def __init__(self, shapes: list[GraphicalObject] = []):
        super().__init__(hot_points=[])
        self._shapes = [shape.duplicate() for shape in shapes]

    def get_shapes(self) -> list[GraphicalObject]:
        return tuple(self._shapes)

    def get_shape_name(self):
        return "Kompozitni oblik"

    def get_shape_id(self) -> str:
        return "@COMP"

    def duplicate(self):
        duplicated_shapes = [shape.duplicate() for shape in self._shapes]
        return CompositeShape(duplicated_shapes)

    def render(self, r: Renderer):
        for shape in self._shapes:
            shape.render(r)

    def selection_distance(self, mouse_point):
        d = min(shape.selection_distance(mouse_point) for shape in self._shapes)
        return d

    def translate(self, delta: Point):
        for shape in self._shapes:
            shape.translate(delta)
        self._notify_listeners()

    def get_bounding_box(self):
        if not self._shapes:
            return Rectangle(Point(0, 0), 0, 0)
        bounding_boxes = [shape.get_bounding_box() for shape in self._shapes]
        min_x = min(bb.get_x() for bb in bounding_boxes)
        min_y = min(bb.get_y() for bb in bounding_boxes)
        max_x = max(bb.get_x() + bb.get_width() for bb in bounding_boxes)
        max_y = max(bb.get_y() + bb.get_height() for bb in bounding_boxes)
        width = max_x - min_x
        height = max_y - min_y
        return Rectangle(min_x, min_y, width, height)

    def load(self, stack: list[GraphicalObject], data: str):
        id, n = data.split()
        if id != self.get_shape_id():
            raise ValueError(f"Invalid shape id: {id}")
        self._shapes = [stack.pop() for _ in range(int(n))]
        new_composite = self.duplicate()
        stack.append(new_composite)

    def save(self, rows: list[str]):
        for shape in self._shapes:
            shape.save(rows)
        row = f"{self.get_shape_id()} {len(self._shapes)}"
        rows.append(row)
