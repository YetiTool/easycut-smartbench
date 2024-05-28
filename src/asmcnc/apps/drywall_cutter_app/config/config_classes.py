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
        self.tool_id = tool_id.encode("utf-8")
        self.manufacturer = str(manufacturer)
        self.type = str(type)
        self.dimensions = Dimensions(**dimensions)
        self.flutes = Flutes(**flutes)
        self.material = str(material)
        self.parameters = Parameters(**parameters)
        self.toolpath_offsets = AllowableToolpathOffsets(**toolpath_offsets)
        self.image = str(image)

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
        self.diameter = diameter
        self.angle = angle
        self.units = str(units)


class AllowableToolpathOffsets(object):
    """Class to store the allowable toolpath offsets."""

    def __init__(self, inside, outside, on):
        self.inside = inside
        self.outside = outside
        self.on = on


class Flutes(object):
    """Class to store the cutter flutes."""

    def __init__(self, count, length):
        self.count = count
        self.length = length


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
        self.cutting_spindle_speed = cutting_spindle_speed
        self.cutting_feed_rate = cutting_feed_rate
        self.plunge_feed_rate = plunge_feed_rate
        self.cutting_direction = str(cutting_direction)
        self.recommended_depth_per_pass = recommended_depth_per_pass
        self.max_depth_total = max_depth_total
        self.step_over = step_over
        self.yetipilot_target_power = yetipilot_target_power


class CanvasShapeDims(object):
    """Class to store the canvas shape dimensions."""

    def __init__(self, x, y, r, d, l):
        self.x = x
        self.y = y
        self.r = r
        self.d = d
        self.l = l


class CuttingDepths(object):
    """Class to store the cutting depths."""

    def __init__(self, material_thickness, bottom_offset, auto_pass, depth_per_pass):
        self.material_thickness = material_thickness
        self.bottom_offset = bottom_offset
        self.auto_pass = auto_pass
        self.depth_per_pass = depth_per_pass


class DatumPosition(object):
    """Class to store the datum position."""

    def __init__(self, x, y):
        self.x = x
        self.y = y


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
        datum_position,
    ):
        self.shape_type = str(shape_type)
        self.units = str(units)
        self.rotation = str(rotation)
        self.canvas_shape_dims = CanvasShapeDims(**canvas_shape_dims)
        self.cutter_type = str(cutter_type)
        self.toolpath_offset = str(toolpath_offset)
        self.cutting_depths = CuttingDepths(**cutting_depths)
        self.datum_position = DatumPosition(**datum_position)

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
