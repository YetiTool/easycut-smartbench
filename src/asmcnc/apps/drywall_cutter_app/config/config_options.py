from enum import Enum

"""This module contains the enums for the config options."""


class Rotation(Enum):
    """Rotation enum."""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class Shape(Enum):
    """Shape enum."""
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    LINE = "line"
    SQUARE = "square"
    GEBERIT = "geberit"


class ToolpathOffset(Enum):
    """Toolpath offset enum."""
    INSIDE = "inside"
    OUTSIDE = "outside"
    ON = "on"


class Unit(Enum):
    """Unit enum."""
    INCH = "inch"
    MM = "mm"
