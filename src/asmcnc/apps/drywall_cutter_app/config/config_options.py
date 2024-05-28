"""Module to define the config options"""

from enum import Enum


class CuttingDirectionOptions(Enum):
    """Enum to define the cutting direction options."""

    BOTH = "both"
    CLIMB = "climb"


class ToolpathOffsetOptions(Enum):
    """Enum to define the toolpath offset options."""

    INSIDE = "inside"
    OUTSIDE = "outside"
    ON = "on"


class ShapeOptions(Enum):
    """Enum to define the shape type options."""

    CIRCLE = "circle"
    RECTANGLE = "rectangle"
    SQUARE = "square"
    LINE = "line"
    GEBERIT = "geberit"


class RotationOptions(Enum):
    """Enum to define the rotation options."""

    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
