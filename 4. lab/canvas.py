import tkinter as tk
from typing import TYPE_CHECKING

from document_model_listener import DocumentModelListener
from g2d_renderer import G2DRenderer
from point import Point
from state.idle import IdleState

if TYPE_CHECKING:
    from document_model import DocumentModel
    from gui import GUI


class Canvas(tk.Frame, DocumentModelListener):
    LINE_WIDTH: float = 1.75

    def __init__(
        self,
        master: tk.Tk,
        gui: GUI,
        document_model: DocumentModel,
        width: int,
        height: int,
    ):
        super().__init__(master)
        self._gui = gui
        self._document_model = document_model
        self._width = width
        self._height = height
        self._canvas = tk.Canvas(master, bg="white", width=width, height=height)
        self._canvas.pack(fill="both", expand=True)

        self._document_model.add_document_model_listener(self)

        self._canvas.focus_set()

        self._canvas.bind("w", lambda e: self._gui.destroy())
        self._canvas.bind(
            "<Button-1>",
            lambda e: self._gui.get_state().mouse_down(
                Point(e.x, e.y),
                shift_down=self._shift_used(e),
                ctrl_down=self._ctrl_used(e),
            ),
        )
        self._canvas.bind("<Escape>", lambda e: self._gui.set_state(IdleState()))

    def _shift_used(self, event: tk.Event) -> bool:
        return (event.state & 0x0001) != 0

    def _ctrl_used(self, event: tk.Event) -> bool:
        return (event.state & 0x0004) != 0

    def _get_renderer(self):
        return G2DRenderer(self)

    def create_line(self, x1: float, y1: float, x2: float, y2: float, fill: str):
        self._canvas.create_line(x1, y1, x2, y2, fill=fill, width=self.LINE_WIDTH)

    def create_polygon(
        self, coords: list[tuple[float, float]], fill: str, outline: str
    ):
        self._canvas.create_polygon(coords, fill=fill, outline=outline)

    def paint_component(self):
        self._canvas.delete("all")
        r = self._get_renderer()
        for o in self._document_model.list():
            o.render(r)

    def document_change(self):
        self.paint_component()
