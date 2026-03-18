from abc import ABC
from typing import TYPE_CHECKING

from geometry_util import GeometryUtil
from graphical_object.interface import GraphicalObject
from point import Point

if TYPE_CHECKING:
    from graphical_object.listener import GraphicalObjectListener


class AbstractGraphicalObject(GraphicalObject, ABC):
    def __init__(self, hot_points: list[Point] = []):
        self._hot_points: list[Point] = hot_points
        self._hot_points_selected: list[bool] = [False] * len(hot_points)
        self._selected: bool = False
        self.listeners: list = []

    def get_hot_point(self, index: int) -> Point:
        if index < -len(self._hot_points) or index >= len(self._hot_points):
            raise IndexError("Hot point index out of range")
        return self._hot_points[index]

    def set_hot_point(self, index: int, point: Point):
        if index < -len(self._hot_points) or index >= len(self._hot_points):
            raise IndexError("Hot point index out of range")
        self._hot_points[index] = point
        self._notify_listeners()

    def get_number_of_hot_points(self) -> int:
        return len(self._hot_points)

    def get_hot_point_distance(self, index: int, mouse_point: Point) -> float:
        if index < -len(self._hot_points) or index >= len(self._hot_points):
            raise IndexError("Hot point index out of range")
        return GeometryUtil.distance_from_point(self._hot_points[index], mouse_point)

    def is_hot_point_selected(self, index: int) -> bool:
        if index < -len(self._hot_points) or index >= len(self._hot_points):
            raise IndexError("Hot point index out of range")
        return self._hot_points_selected[index]

    def set_hot_point_selected(self, index: int, selected: bool):
        if index < -len(self._hot_points) or index >= len(self._hot_points):
            raise IndexError("Hot point index out of range")
        self._hot_points_selected[index] = selected
        self._notify_listeners()

    def is_selected(self) -> bool:
        return self._selected

    def set_selected(self, selected: bool):
        if self._selected != selected:
            self._selected = selected
            self._notify_selection_listeners()

    def translate(self, delta: Point):
        self._hot_points = [hp.translate(delta) for hp in self._hot_points]
        self._notify_listeners()

    def add_graphical_object_listener(self, listener: GraphicalObjectListener):
        self.listeners.append(listener)

    def remove_graphical_object_listener(self, listener: GraphicalObjectListener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def _notify_listeners(self):
        for listener in self.listeners:
            listener.graphical_object_changed(self)

    def _notify_selection_listeners(self):
        for listener in self.listeners:
            listener.graphical_object_selection_changed(self)
