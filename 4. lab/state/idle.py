from typing import TYPE_CHECKING, Optional

from state.interface import State

if TYPE_CHECKING:
    from graphical_objects import GraphicalObject
    from point import Point
    from renderer import Renderer


class IdleState(State):
    def mouse_down(self, mouse_point: Point, shift_down: bool, ctrl_down: bool): ...

    def mouse_up(self, mouse_point: Point, shift_down: bool, ctrl_down: bool): ...

    def mouse_dragged(self, mouse_point: Point): ...

    def key_pressed(self, key_code: int): ...

    def after_draw(self, r: Renderer, go: Optional[GraphicalObject] = None): ...

    def on_leaving(self): ...
