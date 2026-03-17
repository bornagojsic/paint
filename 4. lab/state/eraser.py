from typing import TYPE_CHECKING, Optional

from graphical_objects import EraserPath
from state.interface import State

if TYPE_CHECKING:
    from document_model import DocumentModel
    from graphical_objects import GraphicalObject
    from point import Point
    from renderer import Renderer


class EraserState(State):
    def __init__(self, document_model: DocumentModel):
        self._model = document_model
        self._path: EraserPath = EraserPath()

    def mouse_down(self, mouse_point: Point, shift_down: bool, ctrl_down: bool):
        self._path.add_point(mouse_point)
        self._model.add_graphical_object(self._path)

    def mouse_up(self, mouse_point: Point, shift_down: bool, ctrl_down: bool):
        self._path.add_point(mouse_point)
        self._model.erase(self._path)
        self._model.remove_graphical_object(self._path)
        self._path.clear()

    def mouse_dragged(self, mouse_point: Point):
        self._path.add_point(mouse_point)

    def key_pressed(self, key_code: int): ...

    def after_draw(self, r: Renderer, go: Optional[GraphicalObject] = None): ...

    def on_leaving(self): ...
