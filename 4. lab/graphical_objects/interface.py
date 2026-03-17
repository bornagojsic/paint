from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from point import Point
from rectangle import Rectangle

if TYPE_CHECKING:
    from graphical_objects.listener import GraphicalObjectListener
    from renderer import Renderer


class GraphicalObject(ABC):
    # Podrška za uređivanje objekta

    @abstractmethod
    def is_selected(self) -> bool: ...

    @abstractmethod
    def set_selected(self, selected: bool): ...

    @abstractmethod
    def get_number_of_hot_points(self) -> int: ...

    @abstractmethod
    def get_hot_point(self, index: int) -> Point: ...

    @abstractmethod
    def set_hot_point(self, index: int, point: Point): ...

    @abstractmethod
    def is_hot_point_selected(self, index: int) -> bool: ...

    @abstractmethod
    def set_hot_point_selected(self, index: int, selected: bool): ...

    @abstractmethod
    def get_hot_point_distance(self, index: int, mouse_point: Point) -> float: ...

    # Geometrijska operacija nad oblikom

    @abstractmethod
    def translate(self, delta: Point): ...

    @abstractmethod
    def get_bounding_box(self) -> Rectangle: ...

    @abstractmethod
    def selection_distance(self, mouse_point: Point) -> float: ...

    # Podrška za crtanje (dio mosta)

    @abstractmethod
    def render(self, r: Renderer): ...

    # Observer za dojavu promjena modelu

    @abstractmethod
    def add_graphical_object_listener(self, listener: "GraphicalObjectListener"): ...

    @abstractmethod
    def remove_graphical_object_listener(self, listener: "GraphicalObjectListener"): ...

    # Podrška za prototip (alatna traka, stvaranje objekata u crtežu, ...)

    @abstractmethod
    def get_shape_name(self) -> str: ...

    @abstractmethod
    def duplicate(self) -> "GraphicalObject": ...

    # Podrška za snimanje i učitavanje

    @abstractmethod
    def get_shape_id(self) -> str: ...

    @abstractmethod
    def load(self, stack: list["GraphicalObject"], data: str): ...

    @abstractmethod
    def save(self, rows: list[str]): ...
