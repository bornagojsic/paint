from point import Point


class Rectangle:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_points(self) -> list[Point]:
        return [
            Point(self.__x, self.__y),
            Point(self.__x + self.__width, self.__y),
            Point(self.__x + self.__width, self.__y + self.__height),
            Point(self.__x, self.__y + self.__height),
        ]

    def __repr__(self):
        return f"Rectangle(x={self.__x}, y={self.__y}, width={self.__width}, height={self.__height})"
