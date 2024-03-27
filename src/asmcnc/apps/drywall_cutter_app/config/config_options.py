"""Module to define the config options"""

from enum import Enum


class CuttingDirection(Enum):
    """Enum to define the cutting direction options."""
    BOTH = "both"
    CLIMB = "climb"


class ToolpathOffset(Enum):
    """Enum to define the toolpath offset options."""
    INSIDE = "inside"
    OUTSIDE = "outside"
    ON = "on"


class ShapeType(Enum):
    """Enum to define the shape type options."""
    CIRCLE = "circle"
    RECTANGLE = "rectangle"
    SQUARE = "square"
    LINE = "line"
    GEBERIT = "geberit"
