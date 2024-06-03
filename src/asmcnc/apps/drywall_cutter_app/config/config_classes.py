"""This module contains the classes used to store the configuration data for the drywall cutter app."""
import json
import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
SETTINGS_DIR = os.path.join(CURRENT_DIR, "settings")
CUTTERS_DIR = os.path.join(CURRENT_DIR, "cutters")

DEFAULT_CONFIG_PATH = os.path.join(SETTINGS_DIR, "default_config.json")
DEFAULT_CUTTER_NAME = "tool_6mm.json"
DEFAULT_CUTTER_PATH = os.path.join(CUTTERS_DIR, DEFAULT_CUTTER_NAME)


class Cutter(object):
    """Class to store the cutter data."""

    def __init__(
        self,
        tool_id,
        manufacturer,
        type,
        dimensions,
        flutes,
        material,
        parameters,
        toolpath_offsets,
        image,
    ):
        self.tool_id = tool_id.encode("utf-8")  # type: str
        self.manufacturer = str(manufacturer)  # type: str
        self.type = str(type)  # type: str
        self.dimensions = Dimensions(**dimensions)  # type: Dimensions
        self.flutes = Flutes(**flutes)  # type: Flutes
        self.material = str(material)  # type: str
        self.parameters = Parameters(**parameters)  # type: Parameters
        self.toolpath_offsets = AllowableToolpathOffsets(
            **toolpath_offsets
        )  # type: AllowableToolpathOffsets
        self.image = str(image)  # type: str

    @classmethod
    def from_json(cls, json_data):
        """Create a Cutter object from a JSON object."""
        return Cutter(**json_data)

    @classmethod
    def default(cls):
        """Get the default cutter."""
        with open(DEFAULT_CUTTER_PATH, "r") as f:
            return Cutter.from_json(json.load(f))


class Dimensions(object):
    """Class to store the cutter dimensions."""

    def __init__(self, diameter, angle, units):
        self.diameter = diameter  # type: float
        self.angle = angle  # type: int
        self.units = str(units)  # type: str


class AllowableToolpathOffsets(object):
    """Class to store the allowable toolpath offsets."""

    def __init__(self, inside, outside, on):
        self.inside = inside  # type: bool
        self.outside = outside  # type: bool
        self.on = on  # type: bool


class Flutes(object):
    """Class to store the cutter flutes."""

    def __init__(self, count, length):
        self.count = count  # type: int
        self.length = length  # type: float


class Parameters(object):
    """Class to store the cutter parameters."""

    def __init__(
        self,
        cutting_spindle_speed,
        cutting_feed_rate,
        plunge_feed_rate,
        cutting_direction,
        recommended_depth_per_pass,
        max_depth_total,
        step_over,
        yetipilot_target_power,
    ):
        self.cutting_spindle_speed = cutting_spindle_speed  # type: int
        self.cutting_feed_rate = cutting_feed_rate  # type: float
        self.plunge_feed_rate = plunge_feed_rate  # type: float
        self.cutting_direction = str(cutting_direction)  # type: str
        self.recommended_depth_per_pass = recommended_depth_per_pass  # type: float
        self.max_depth_total = max_depth_total  # type: float
        self.step_over = step_over  # type: float
        self.yetipilot_target_power = yetipilot_target_power  # type: int


class CanvasShapeDims(object):
    """Class to store the canvas shape dimensions."""

    def __init__(self, x, y, r, d, l):
        self.x = x  # type: float
        self.y = y  # type: float
        self.r = r  # type: float
        self.d = d  # type: float
        self.l = l  # type: float


class CuttingDepths(object):
    """Class to store the cutting depths."""

    def __init__(self, material_thickness, bottom_offset, auto_pass, depth_per_pass, tabs):
        self.material_thickness = material_thickness  # type: float
        self.bottom_offset = bottom_offset  # type: float
        self.auto_pass = auto_pass  # type: bool
        self.depth_per_pass = depth_per_pass  # type: float
        self.tabs = tabs  # type: bool


class DatumPosition(object):
    """Class to store the datum position."""

    def __init__(self, x, y):
        self.x = x  # type: float
        self.y = y  # type: float


class Configuration(object):
    """Class to store the configuration data."""

    def __init__(
        self,
        shape_type,
        units,
        rotation,
        canvas_shape_dims,
        cutter_type,
        toolpath_offset,
        cutting_depths,
        datum_position
    ):
        self.shape_type = str(shape_type)  # type: str
        self.units = str(units)  # type: str
        self.rotation = str(rotation)
        self.canvas_shape_dims = CanvasShapeDims(
            **canvas_shape_dims
        )  # type: CanvasShapeDims
        self.cutter_type = str(cutter_type)  # type: str
        self.toolpath_offset = str(toolpath_offset)  # type: str
        self.cutting_depths = CuttingDepths(**cutting_depths)  # type: CuttingDepths
        self.datum_position = DatumPosition(**datum_position)  # type: DatumPosition

    @classmethod
    def from_json(cls, json_data):
        """Create a Configuration object from a JSON object."""
        return Configuration(**json_data)

    @classmethod
    def default(cls):
        """Get the default configuration."""
        with open(DEFAULT_CONFIG_PATH, "r") as f:
            return Configuration.from_json(json.load(f))


if __name__ == "__main__":
    print(Cutter.default().tool_id)
