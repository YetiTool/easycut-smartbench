"""Module to define the shapes and their properties."""
import json

from enum import Enum


class ToolpathOffset(Enum):
    """Enum to define the toolpath offset options."""
    INSIDE = "inside"
    OUTSIDE = "outside"
    ON = "on"


class Shape(object):
    """Class to define the shapes and their properties."""

    name = ""

    x = 0.0
    y = 0.0
    r = 0.0

    rotatable = False

    allowable_toolpath_offsets = []

    def __init__(self, x, y, r, *args, **kwargs):
        super(Shape, self).__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.r = r

    def to_dict(self):
        return {
            "name": self.name,
            "dimensions": {
                "x": self.x,
                "y": self.y,
                "r": self.r
            }
        }


class Rectangle(Shape):
    """Class to define the rectangle shape and its properties."""
    name = "rectangle"

    rotatable = True

    allowable_toolpath_offsets = [ToolpathOffset.INSIDE, ToolpathOffset.OUTSIDE, ToolpathOffset.ON]


class Circle(Shape):
    """Class to define the circle shape and its properties."""
    name = "circle"

    allowable_toolpath_offsets = [ToolpathOffset.INSIDE, ToolpathOffset.OUTSIDE, ToolpathOffset.ON]


class ConfigTest(object):
    def __init__(self, shape, units):
        self.shape = shape
        self.units = units

    def to_dict(self):
        return {
            "shape": self.shape.to_dict(),
            "units": self.units
        }


if __name__ == "__main__":
    rectangle = Rectangle(10, 20, 30)
    circle = Circle(5, 10, 15)
    config = ConfigTest(rectangle, "mm")

    print(rectangle.to_dict())
    print(circle.to_dict())
    print(config.to_dict())

    print(json.dumps(config.to_dict(), indent=4))
