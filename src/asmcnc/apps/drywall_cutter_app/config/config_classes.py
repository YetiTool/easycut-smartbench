"""
This module contains the classes used to store the configuration data for the drywall cutter app.

Data types are not confirmed.
"""
import json
import os

from kivy.event import EventDispatcher

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
SETTINGS_DIR = os.path.join(CURRENT_DIR, 'settings')
CUTTERS_DIR = os.path.join(CURRENT_DIR, 'cutters')

DEFAULT_CONFIG_PATH = os.path.join(SETTINGS_DIR, "default_config.json")
DEFAULT_CUTTER_NAME = "tool_6mm.json"
DEFAULT_CUTTER_PATH = os.path.join(CUTTERS_DIR, DEFAULT_CUTTER_NAME)


class Cutter(object):
    def __init__(self, cutter_description, units, diameter, material, cutting_spindle_speed,
                 cutting_feedrate, plunge_rate, cutting_direction, allowable_toolpath_offsets,
                 max_depth_per_pass, max_depth_total, stepover, yeti_pilot_target_powers, image_path):
        self.cutter_description = cutter_description  # type: str
        self.units = units  # type: str
        self.diameter = diameter  # type: float
        self.material = material  # type: str
        self.cutting_spindle_speed = cutting_spindle_speed  # type: float
        self.cutting_feedrate = cutting_feedrate  # type: float
        self.plunge_rate = plunge_rate  # type: float
        self.cutting_direction = cutting_direction  # type: str
        self.allowable_toolpath_offsets = AllowableToolpathOffsets(
            **allowable_toolpath_offsets)  # type: AllowableToolpathOffsets
        self.max_depth_per_pass = max_depth_per_pass  # type: float
        self.max_depth_total = max_depth_total  # type: float
        self.stepover = stepover  # type: float
        self.yeti_pilot_target_powers = yeti_pilot_target_powers  # type: float
        self.image_path = image_path  # type: str

    @classmethod
    def from_json(cls, json_data):
        return Cutter(**json_data)

    @classmethod
    def default(cls):
        with open(DEFAULT_CUTTER_PATH, 'r') as f:
            return Cutter.from_json(json.load(f))


class AllowableToolpathOffsets(object):
    def __init__(self, inside, outside, on):
        self.inside = inside  # type: float
        self.outside = outside  # type: float
        self.on = on  # type: float


class CanvasShapeDims(object):
    def __init__(self, x, y, r, d, l):
        self.x = x  # type: float
        self.y = y  # type: float
        self.r = r  # type: float
        self.d = d  # type: float
        self.l = l  # type: float


class CuttingDepths(object):
    def __init__(self, material_thickness, bottom_offset, auto_pass, depth_per_pass):
        self.material_thickness = material_thickness  # type: float
        self.bottom_offset = bottom_offset  # type: float
        self.auto_pass = auto_pass  # type: bool
        self.depth_per_pass = depth_per_pass  # type: float


class DatumPosition(object):
    def __init__(self, x, y):
        self.x = x  # type: float
        self.y = y  # type: float


class Configuration(object):
    def __init__(self, name, shape_type, units, rotation, canvas_shape_dims, cutter_type, toolpath_offset,
                 cutting_depths,
                 datum_position, **kwargs):
        super(Configuration, self).__init__(**kwargs)
        self.name = name  # type: str
        self.shape_type = shape_type  # type: str
        self.units = units  # type: str
        self.rotation = rotation
        self.canvas_shape_dims = CanvasShapeDims(**canvas_shape_dims)  # type: CanvasShapeDims
        self.cutter_type = cutter_type  # type: str
        self.toolpath_offset = toolpath_offset  # type: str
        self.cutting_depths = CuttingDepths(**cutting_depths)  # type: CuttingDepths
        self.datum_position = DatumPosition(**datum_position)  # type: DatumPosition

    @classmethod
    def from_json(cls, name, json_data):
        return Configuration(name=name, **json_data)

    @classmethod
    def default(cls):
        with open(DEFAULT_CONFIG_PATH, 'r') as f:
            return Configuration.from_json("default", json.load(f))


if __name__ == '__main__':
    print(Cutter.default().__dict__)
    print(Configuration.default().__dict__)
