from graphical_object import LineSegment, Oval
from gui import GUI
from point import Point


def main():
    objects = []

    objects.append(LineSegment(Point(-50, -50), Point(50, 50)))
    objects.append(Oval(Point(50, 0), Point(0, 25)))

    gui = GUI(objects)
    gui.set_visible(True)


if __name__ == "__main__":
    main()
