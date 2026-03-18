import tkinter as tk
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING, Optional

from canvas import Canvas
from document_model import DocumentModel
from graphical_object.composite import CompositeShape
from renderer import SVGRenderer
from state import AddShapeState, EraserState, IdleState, SelectShapeState

if TYPE_CHECKING:
    from graphical_object import GraphicalObject
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
            "load": {"name": "Load", "command": self.__on_load_click},
            "save": {"name": "Save", "command": self.__on_save_click},
            "svg_export": {"name": "SVG export", "command": self.__on_svg_export_click},
            **{
                self.__get_shape_button_name(o): {
                    "name": o.get_shape_name(),
                    "command": lambda o=o: self.__on_shape_click(o),
                }
                for o in self._graphical_objects
            },
            "select": {
                "name": "Select",
                "command": self.__on_select_click,
            },
            "eraser": {"name": "Eraser", "command": self.__on_eraser_click},
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
        if button == self._active_button:
            return
        self._active_button = button
        for btn in self._toolbar_buttons.values():
            btn.config(relief=tk.RAISED)

        if button is not None:
            button.config(relief=tk.SUNKEN)

    def _set_state_idle(self, *_):
        self.set_state(IdleState())

    def __on_load_click(self):
        self._set_state_idle()
        file_name = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not file_name:
            self._set_active_button(None)
            return

        prototypes: dict[str, GraphicalObject] = {
            **{o.get_shape_id(): o for o in self._graphical_objects},
            "@COMP": CompositeShape(),
        }

        try:
            with open(file_name, "r") as f:
                rows = f.read().splitlines()

            stack = []

            while (data := rows.pop(0)) if rows else None:
                shape_id = data.split()[0]
                if shape_id not in prototypes:
                    raise ValueError(f"Unknown shape id: {shape_id}")
                prototypes[shape_id].load(stack, data)

            self._document_model.clear()
            for o in stack:
                self._document_model.add_graphical_object(o)

            self._set_active_button(None)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
            self._set_active_button(None)

    def __on_save_click(self):
        self._set_state_idle()
        file_name = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not file_name:
            self._set_active_button(None)
            return

        rows: list[str] = []
        for o in self._document_model.list():
            o.save(rows)

        with open(file_name, "w") as f:
            f.write("\n".join(rows))

        self._set_active_button(None)

    # TODO: check for how to set dimensions
    def __on_svg_export_click(self):
        self._set_state_idle()
        file_name = filedialog.asksaveasfilename(
            defaultextension=".svg",
            filetypes=[("SVG files", "*.svg"), ("All files", "*.*")],
        )
        if not file_name:
            self._set_active_button(None)
            return

        r = SVGRenderer(file_name)
        for o in self._document_model.list():
            o.render(r)
        r.close()

        self._set_active_button(None)

    def __on_shape_click(self, prototype: GraphicalObject):
        self.set_state(AddShapeState(self._document_model, prototype))

    def __on_select_click(self):
        self.set_state(SelectShapeState(self._document_model))

    def __on_eraser_click(self):
        self.set_state(EraserState(self._document_model))

    def destroy(self):
        self._root.destroy()

    def set_visible(self, visible: bool):
        if visible:
            self._root.mainloop()
        else:
            self._root.destroy()
