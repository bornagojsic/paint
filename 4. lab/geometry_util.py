from math import sqrt

from point import Point


class GeometryUtil:
    @staticmethod
    def distance_from_point(point1: Point, point2: Point) -> float:
        diff_vector = point1.difference(point2)
        return sqrt(diff_vector.get_x() ** 2 + diff_vector.get_y() ** 2)

    @staticmethod
    def distance_from_line_segment(s: Point, e: Point, p: Point) -> float:
        line = e.difference(s)
        line_length = GeometryUtil.distance_from_point(s, e)
        p_s = p.difference(s)

        alpha = (
            p_s.get_x() * line.get_x() + p_s.get_y() * line.get_y()
        ) / line_length**2

        t = s + alpha * line

        pt = GeometryUtil.distance_from_point(p, t)
        ps = GeometryUtil.distance_from_point(p, s)
        pe = GeometryUtil.distance_from_point(p, e)

        return min(pt, ps, pe)
