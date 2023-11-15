"""
This module contains the classes used to store the configuration data for the drywall cutter app.

Data types are not confirmed.
"""


class Cutter:
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
        self.allowable_toolpath_offsets = AllowableToolpathOffsets(**allowable_toolpath_offsets)  # type: AllowableToolpathOffsets
        self.max_depth_per_pass = max_depth_per_pass  # type: float
        self.max_depth_total = max_depth_total  # type: float
        self.stepover = stepover  # type: float
        self.yeti_pilot_target_powers = yeti_pilot_target_powers  # type: float
        self.image_path = image_path  # type: str


class AllowableToolpathOffsets:
    def __init__(self, inside, outside, on):
        self.inside = inside  # type: float
        self.outside = outside  # type: float
        self.on = on  # type: float

    @staticmethod
    def default():
        return AllowableToolpathOffsets(inside=0.0, outside=0.0, on=0.0)


class CanvasShapeDims:
    def __init__(self, x, y, r, d, l):
        self.x = x  # type: float
        self.y = y  # type: float
        self.r = r  # type: float
        self.d = d  # type: float
        self.l = l  # type: float

    @staticmethod
    def default():
        return CanvasShapeDims(x=0.0, y=0.0, r=0.0, d=0.0, l=0.0)


class CuttingDepths:
    def __init__(self, material_thickness, bottom_offset, auto_pass, depth_per_pass):
        self.material_thickness = material_thickness  # type: float
        self.bottom_offset = bottom_offset  # type: float
        self.auto_pass = auto_pass  # type: bool
        self.depth_per_pass = depth_per_pass  # type: float

    @staticmethod
    def default():
        return CuttingDepths(material_thickness=0.0, bottom_offset=0.0, auto_pass=False, depth_per_pass=0.0)


class DatumPosition:
    def __init__(self, x, y):
        self.x = x  # type: float
        self.y = y  # type: float

    @staticmethod
    def default():
        return DatumPosition(x=0.0, y=0.0)


class Configuration:
    def __init__(self, shape_type, units, rotation, canvas_shape_dims, cutter_type, toolpath_offset, cutting_depths,
                 datum_position):
        self.shape_type = shape_type  # type: str
        self.units = units  # type: str
        self.rotation = rotation
        self.canvas_shape_dims = CanvasShapeDims(**canvas_shape_dims)  # type: CanvasShapeDims
        self.cutter_type = cutter_type  # type: str
        self.toolpath_offset = toolpath_offset  # type: str
        self.cutting_depths = CuttingDepths(**cutting_depths)  # type: CuttingDepths
        self.datum_position = DatumPosition(**datum_position)  # type: DatumPosition

    @staticmethod
    def default():
        return Configuration(shape_type='Square', units='mm', rotation='horizontal',
                             canvas_shape_dims={'x': 100.0, 'y': 100.0, 'r': 0.0, 'd': 100.0, 'l': 100.0},
                             cutter_type='test_cutter.json',
                             toolpath_offset='inside',
                             cutting_depths={'material_thickness': 12.0, 'bottom_offset': 0.5, 'auto_pass': True,
                                             'depth_per_pass': 6.0},
                             datum_position={'x': 0.0, 'y': 0.0})
