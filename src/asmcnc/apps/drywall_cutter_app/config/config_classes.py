class Cutter:
    def __init__(self, cutter_description, units, diameter, material, cutting_spindle_speed,
                 cutting_feedrate, plunge_rate, cutting_direction, allowable_toolpath_offsets,
                 max_depth_per_pass, max_depth_total, stepover, yeti_pilot_target_powers):
        self.cutter_description = cutter_description
        self.units = units
        self.diameter = diameter
        self.material = material
        self.cutting_spindle_speed = cutting_spindle_speed
        self.cutting_feedrate = cutting_feedrate
        self.plunge_rate = plunge_rate
        self.cutting_direction = cutting_direction
        self.allowable_toolpath_offsets = AllowableToolpathOffsets(**allowable_toolpath_offsets)
        self.max_depth_per_pass = max_depth_per_pass
        self.max_depth_total = max_depth_total
        self.stepover = stepover
        self.yeti_pilot_target_powers = yeti_pilot_target_powers


class AllowableToolpathOffsets:
    def __init__(self, inside, outside, on):
        self.inside = inside
        self.outside = outside
        self.on = on


class CanvasShapeDims:
    def __init__(self, x, y, r, d, l):
        self.x = x
        self.y = y
        self.r = r
        self.d = d
        self.l = l


class CuttingDepths:
    def __init__(self, material_thickness, bottom_offset, auto_pass, depth_per_pass):
        self.material_thickness = material_thickness
        self.bottom_offset = bottom_offset
        self.auto_pass = auto_pass
        self.depth_per_pass = depth_per_pass


class DatumPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Configuration:
    def __init__(self, shape_type, units, canvas_shape_dims, cutter_type, toolpath_offset, cutting_depths,
                 datum_position):
        self.shape_type = shape_type
        self.units = units
        self.canvas_shape_dims = CanvasShapeDims(**canvas_shape_dims)
        self.cutter_type = cutter_type
        self.toolpath_offset = toolpath_offset
        self.cutting_depths = CuttingDepths(**cutting_depths)
        self.datum_position = DatumPosition(**datum_position)

