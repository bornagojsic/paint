from typing import TYPE_CHECKING, Optional

from state.interface import State

if TYPE_CHECKING:
    from document_model import DocumentModel
    from graphical_object import GraphicalObject
    from point import Point
    from renderer import Renderer


class AddShapeState(State):
    def __init__(self, model: DocumentModel, prototype: GraphicalObject):
        self._model = model
        self._prototype = prototype

    def mouse_down(self, mouse_point: Point, shift_down: bool, ctrl_down: bool):
        new_object = self._prototype.duplicate()
        new_object.translate(mouse_point)
        self._model.add_graphical_object(new_object)

    def mouse_up(self, mouse_point: Point, shift_down: bool, ctrl_down: bool): ...

    def mouse_dragged(self, mouse_point: Point): ...

    def key_pressed(self, key_code: int): ...

    def after_draw(self, r: Renderer, go: Optional[GraphicalObject] = None): ...

    def on_leaving(self): ...
