from typing import TYPE_CHECKING, Optional

from document_model import DocumentModel
from point import Point
from rectangle import Rectangle
from state.interface import State

if TYPE_CHECKING:
    from graphical_object import GraphicalObject
    from renderer import Renderer


class SelectShapeState(State):
    def __init__(self, document_model: DocumentModel):
        self._model = document_model
        self._mouse_drag_start: Optional[Point] = None

    def __unselect_all(self):
        for obj in self._model.get_selected_objects():
            obj.set_selected(False)
            for i in range(obj.get_number_of_hot_points()):
                obj.set_hot_point_selected(i, False)

    def mouse_down(self, mouse_point: Point, shift_down: bool, ctrl_down: bool):
        self._mouse_drag_start = mouse_point
        selected_object = self._model.find_selected_graphical_object(mouse_point)
        if not ctrl_down:
            self.__unselect_all()
        if selected_object:
            selected_object.set_selected(True)
            selected_hp = self._model.find_selected_hot_point(
                selected_object, mouse_point
            )
            if selected_hp != -1:
                selected_object.set_hot_point_selected(selected_hp, True)

    def mouse_up(self, mouse_point: Point, shift_down: bool, ctrl_down: bool): ...

    def mouse_dragged(self, mouse_point: Point):
        selected_objects = self._model.get_selected_objects()
        if selected_objects:
            hp_selected = False
            if len(selected_objects) == 1:
                obj = selected_objects[0]
                hp_count = obj.get_number_of_hot_points()
                for i in range(hp_count):
                    if obj.is_hot_point_selected(i):
                        hp_selected = True
                        obj.set_hot_point(i, mouse_point)
                        break
            if self._mouse_drag_start and not hp_selected:
                delta = mouse_point.difference(self._mouse_drag_start)
                [obj.translate(delta) for obj in selected_objects]
            self._mouse_drag_start = mouse_point

    def key_pressed(self, key_code: int):
        selected_objects = self._model.get_selected_objects()

        if key_code == 42:  # G key
            self._model.group_selected_objects()
        elif key_code == 30:  # U key
            self._model.ungroup_selected_objects()
        elif key_code == 113:  # left arrow key
            for obj in selected_objects:
                obj.translate(Point(-1, 0))
        elif key_code == 114:  # right arrow key
            for obj in selected_objects:
                obj.translate(Point(1, 0))
        elif key_code == 111:  # up arrow key
            for obj in selected_objects:
                obj.translate(Point(0, -1))
        elif key_code == 116:  # down arrow key
            for obj in selected_objects:
                obj.translate(Point(0, 1))
        elif key_code == 21 or key_code == 86:  # plus key
            for obj in selected_objects:
                self._model.increase_z(obj)
        elif key_code == 61 or key_code == 82:  # minus key
            for obj in selected_objects:
                self._model.decrease_z(obj)

    def after_draw(self, r: Renderer, go: Optional[GraphicalObject] = None):
        if go and go.is_selected():
            bb_points = go.get_bounding_box().get_points()
            no_of_points = len(bb_points)
            for i in range(no_of_points):
                r.draw_line(bb_points[i], bb_points[(i + 1) % no_of_points])
        elif go is None:
            # TODO: refactor this all
            selected_objects = self._model.get_selected_objects()
            if len(selected_objects) == 1:
                selected_object = selected_objects[0]
                hot_points = [
                    selected_object.get_hot_point(i)
                    for i in range(selected_object.get_number_of_hot_points())
                ]
                for hp in hot_points:
                    x, y = hp.get()
                    top_left = (
                        x - r.HOT_POINT_SIZE // 2,
                        y - r.HOT_POINT_SIZE // 2,
                    )
                    hp_rectangle = Rectangle(
                        *top_left, r.HOT_POINT_SIZE, r.HOT_POINT_SIZE
                    )
                    hp_rectangle_points = hp_rectangle.get_points()
                    for i in range(len(hp_rectangle_points)):
                        r.draw_line(
                            hp_rectangle_points[i],
                            hp_rectangle_points[(i + 1) % len(hp_rectangle_points)],
                        )

    def on_leaving(self):
        self.__unselect_all()
