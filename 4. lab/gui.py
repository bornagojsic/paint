import tkinter as tk
from tkinter import filedialog
from typing import TYPE_CHECKING, Optional

from canvas import Canvas
from document_model import DocumentModel
from state import AddShapeState, EraserState, IdleState, SelectShapeState
from svg_renderer import SVGRenderer

if TYPE_CHECKING:
    from graphical_objects import GraphicalObject
    from state import State


## decorator
def activate_button(self: "GUI", func, key: str | None = None):
    def wrapper(*args, **kwargs):
        if key and key in self._toolbar_buttons:
            self._set_active_button(self._toolbar_buttons[key])
        func(*args, **kwargs)

    return wrapper


class GUI:
    def __init__(self, graphical_objects: list[GraphicalObject]):
        self.__canvas_width = 800
        self.__canvas_height = 600

        self._graphical_objects = graphical_objects

        self._document_model = DocumentModel()

        self._root = tk.Tk()

        self._toolbar: tk.Frame = tk.Frame(self._root)
        self._toolbar.bind("<Button-1>", self._set_state_idle)
        self._toolbar.pack(side="top", fill="x")
        self.__generate_toolbar_buttons()

        self._canvas = Canvas(
            self._root,
            self,
            self._document_model,
            self.__canvas_width,
            self.__canvas_height,
        )

        self.__current_state: State = IdleState()

    def __get_shape_button_name(self, shape: GraphicalObject) -> str:
        return shape.get_shape_name().lower().replace(" ", "_")

    def __generate_toolbar_buttons(self):
        toolbar_buttons = {
            "load": {"name": "Učitaj", "command": lambda: ...},
            "save": {"name": "Pohrani", "command": lambda: ...},
            "svg_export": {"name": "SVG export", "command": self.__on_svg_export_click},
            **{
                self.__get_shape_button_name(o): {
                    "name": o.get_shape_name(),
                    "command": lambda o=o: self.__on_shape_click(o),
                }
                for o in self._graphical_objects
            },
            "select": {
                "name": "Selektiraj",
                "command": self.__on_select_click,
            },
            "eraser": {"name": "Brisalo", "command": self.__on_eraser_click},
        }

        self._toolbar_buttons: dict[str, tk.Button] = {}

        for key, button_def in toolbar_buttons.items():
            button = tk.Button(
                self._toolbar,
                text=button_def["name"],
                command=activate_button(self, button_def["command"], key),
            )
            button.pack(side=tk.LEFT, padx=2, pady=2)
            self._toolbar_buttons[key] = button

        self._active_button: Optional[tk.Button] = None

    def get_state(self) -> State:
        return self.__current_state

    def set_state(self, state: State):
        self.__current_state.on_leaving()

        if isinstance(state, IdleState):
            self._set_active_button(None)

        self.__current_state = state

    def _set_active_button(self, button: Optional[tk.Button]):
        print(f"Setting active button: {button}")
        if button == self._active_button:
            return
        self._active_button = button
        for btn in self._toolbar_buttons.values():
            btn.config(relief=tk.RAISED)

        if button is not None:
            button.config(relief=tk.SUNKEN)

    def _set_state_idle(self, *_):
        self.set_state(IdleState())

    def __on_shape_click(self, prototype: GraphicalObject):
        self.set_state(AddShapeState(self._document_model, prototype))

    def __on_select_click(self):
        self.set_state(SelectShapeState(self._document_model))

    def __on_eraser_click(self):
        self.set_state(EraserState(self._document_model))

    # TODO: check for how to set dimensions
    def __on_svg_export_click(self):
        file_name = filedialog.asksaveasfilename(
            defaultextension=".svg",
            filetypes=[("SVG files", "*.svg"), ("All files", "*.*")],
        )
        if not file_name:
            self._set_state_idle()
            return

        r = SVGRenderer(file_name)
        for o in self._document_model.list():
            o.render(r)
        r.close()

        self._set_active_button(None)

    def destroy(self):
        self._root.destroy()

    def set_visible(self, visible: bool):
        if visible:
            self._root.mainloop()
        else:
            self._root.destroy()
