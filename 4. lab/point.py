class Point:
    def __init__(self, x: float, y: float):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get(self):
        return self.__x, self.__y

    def translate(self, dp: "Point"):
        return self + dp

    def difference(self, p: "Point"):
        return self + ((-1) * p)

    def __add__(self, p: "Point"):
        return Point(self.__x + p.get_x(), self.__y + p.get_y())

    def __mul__(self, scalar: float):
        return Point(self.__x * scalar, self.__y * scalar)

    def __rmul__(self, scalar: float):
        return Point(self.__x * scalar, self.__y * scalar)

    def __repr__(self):
        return f"({self.__x}, {self.__y})"
