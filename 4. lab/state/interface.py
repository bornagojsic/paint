# public interface State {
#   // poziva se kad progam registrira da je pritisnuta lijeva tipka miša
#   void mouseDown(Point mousePoint, boolean shiftDown, boolean ctrlDown);
#   // poziva se kad progam registrira da je otpuštena lijeva tipka miša
#   void mouseUp(Point mousePoint, boolean shiftDown, boolean ctrlDown);
#   // poziva se kad progam registrira da korisnik pomiče miš dok je tipka pritisnuta
#   void mouseDragged(Point mousePoint);
#   // poziva se kad progam registrira da je korisnik pritisnuo tipku na tipkovnici
#   void keyPressed(int keyCode);

#   // Poziva se nakon što je platno nacrtalo grafički objekt predan kao argument
#   void afterDraw(Renderer r, GraphicalObject go);
#   // Poziva se nakon što je platno nacrtalo čitav crtež
#   void afterDraw(Renderer r);

#   // Poziva se kada program napušta ovo stanje kako bi prešlo u neko drugo
#   void onLeaving();
# }

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from graphical_objects.interface import GraphicalObject
    from point import Point
    from renderer import Renderer


class State(ABC):
    @abstractmethod
    def mouse_down(self, mouse_point: Point, shift_down: bool, ctrl_down: bool): ...

    @abstractmethod
    def mouse_up(self, mouse_point: Point, shift_down: bool, ctrl_down: bool): ...

    @abstractmethod
    def mouse_dragged(self, mouse_point: Point): ...

    @abstractmethod
    def key_pressed(self, key_code: int): ...

    @abstractmethod
    def after_draw(self, r: Renderer, go: Optional[GraphicalObject] = None): ...

    @abstractmethod
    def on_leaving(self): ...
