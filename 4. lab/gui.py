import tkinter as tk
from typing import TYPE_CHECKING, Optional

from canvas import Canvas
from document_model import DocumentModel
from state.add_shape import AddShapeState
from state.idle import IdleState

if TYPE_CHECKING:
    from graphical_objects.interface import GraphicalObject
    from state.interface import State


class GUI:
    def __init__(self, graphical_objects: list[GraphicalObject]):
        self.__canvas_width = 800
        self.__canvas_height = 600

        self._graphical_objects = graphical_objects

        self._document_model = DocumentModel()

        self._root = tk.Tk()

        self._toolbar: tk.Frame = tk.Frame(self._root)
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
            "svg_export": {"name": "SVG export", "command": lambda: ...},
            **{
                self.__get_shape_button_name(o): {
                    "name": o.get_shape_name(),
                    "command": lambda o=o: self.set_state_add_shape(o),
                }
                for o in self._graphical_objects
            },
            "select": {"name": "Selektiraj", "command": lambda: ...},
            "eraser": {"name": "Brisalo", "command": lambda: ...},
        }

        self._toolbar_buttons: dict[str, tk.Button] = {}

        for key, button_def in toolbar_buttons.items():
            button = tk.Button(
                self._toolbar, text=button_def["name"], command=button_def["command"]
            )
            button.pack(side=tk.LEFT, padx=2, pady=2)
            self._toolbar_buttons[key] = button

        self._active_button: Optional[tk.Button] = None

    def get_state(self) -> State:
        return self.__current_state

    def set_state(self, state: State, new_active_button: Optional[tk.Button] = None):
        if new_active_button is not None:
            if new_active_button == self._active_button:
                return
            self._active_button = new_active_button
            for button in self._toolbar_buttons.values():
                button.config(relief=tk.RAISED)
            new_active_button.config(relief=tk.SUNKEN)

        self.__current_state = state

    def set_state_add_shape(self, prototype: GraphicalObject):
        new_active_button = self._toolbar_buttons[
            self.__get_shape_button_name(prototype)
        ]
        self.set_state(
            AddShapeState(self._document_model, prototype), new_active_button
        )

    def destroy(self):
        self._root.destroy()

    def set_visible(self, visible: bool):
        if visible:
            self._root.mainloop()
        else:
            self._root.destroy()
