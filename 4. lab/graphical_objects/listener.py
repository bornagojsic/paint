from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from graphical_objects.interface import GraphicalObject


class GraphicalObjectListener(ABC):
    @abstractmethod
    def graphical_object_changed(self, go: GraphicalObject): ...

    @abstractmethod
    def graphical_object_selection_changed(self, go: GraphicalObject): ...
