"""This module contains the classes used to store the configuration data for the drywall cutter app."""
import enum
import json
import os
from asmcnc.job.database.profile_database import ProfileDatabase

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
SETTINGS_DIR = os.path.join(CURRENT_DIR, "settings")

DEFAULT_CONFIG_PATH = os.path.join(SETTINGS_DIR, "default_config.json")
DEFAULT_CUTTER_UID = "-0001"


class Cutter(object):
    """Class to store the cutter data."""

    def __init__(
        self,
        uid,
        description,
        manufacturer,
        manufacturer_part_number,
        tool_type,
        generic_definition,
        dimensions,
        flutes,
        available_isas
    ):
        self.uid = uid  # type: str
        self.description = description.encode("utf-8")  # type: str
        self.manufacturer = str(manufacturer)  # type: str
        self.manufacturer_part_number = str(manufacturer_part_number)  # type: str
        self.tool_type = str(tool_type)  # type: str
        self.generic_definition = ToolGenericDefinition(**generic_definition)  # type: ToolGenericDefinition
        self.dimensions = Dimensions(**dimensions)  # type: Dimensions
        self.flutes = Flutes(**flutes)  # type: Flutes
        self.available_isas = available_isas  # type: list[str]

    @classmethod
    def from_json(cls, json_data):
        """Create a Cutter object from a JSON object."""
        return Cutter(**json_data)

    @classmethod
    def default(cls):
        """Get the default cutter."""
        profile_db = ProfileDatabase()
        default_cutter = profile_db.get_tool(DEFAULT_CUTTER_UID)
        return Cutter.from_json(default_cutter)


class ToolGenericDefinition(object):
    """Class to store the cutter generic definition."""

    def __init__(self,
                 uid,
                 string,
                 dimension,
                 unit,
                 type,
                 toolpath_offsets,
                 required_operations):
        self.uid = uid  # type: str
        self.string = str(string)  # type: str
        self.dimension = int(dimension)  # type: int
        self.unit = str(unit)  # type: str
        self.type = str(type)  # type: str
        self.toolpath_offsets = AllowableToolpathOffsets(**toolpath_offsets)
        self.required_operations = RequiredOperations(**required_operations)


class RequiredOperations(object):
    """Class to store the required operations."""

    def __init__(self, lead_in):
        self.lead_in = bool(lead_in)  # type: bool


class Dimensions(object):
    """Class to store the cutter dimensions."""

    def __init__(self, shank_diameter, tool_diameter, unit, angle):
        self.shank_diameter = float(shank_diameter)  # type: float
        self.tool_diameter = float(tool_diameter) if tool_diameter else None  # type: float
        self.unit = str(unit)  # type: str
        self.angle = int(angle) if angle else None  # type: int


class AllowableToolpathOffsets(object):
    """Class to store the allowable toolpath offsets."""

    def __init__(self, inside, outside, on, pocket):
        self.inside = inside  # type: bool
        self.outside = outside  # type: bool
        self.on = on  # type: bool
        self.pocket = pocket  # type: bool


class Flutes(object):
    """Class to store the cutter flutes."""

    def __init__(self,
                 type,
                 lengths,
                 quantity,
                 material,
                 coated,
                 coating):
        self.type = str(type)  # type: str
        self.lengths = FluteLengths(**lengths)  # type: FluteLengths
        self.quantity = int(quantity)  # type: int
        self.material = str(material)  # type: str
        self.coated = bool(coated)  # type: bool
        self.coating = str(coating) if coating else None  # type: str


class FluteLengths(object):
    """Class to store the cutter flute lengths."""

    def __init__(self, upcut_straight, downcut, total, unit):
        self.upcut_straight = int(upcut_straight)  # type: int
        self.downcut = int(downcut)  # type: int
        self.total = int(total)  # type: int
        self.unit = str(unit)  # type: str


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

    def __init__(self, material_thickness, bottom_offset, auto_pass, depth_per_pass, tabs=False):
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


class Profile(object):
    """Class to store the profile data"""

    def __init__(
        self,
        uid,
        generic_tool,
        material,
        cutting_parameters,
        applicable_tools
    ):
        self.uid = str(uid)  # type: str
        self.generic_tool = ProfileGenericTool(**generic_tool)  # type: ProfileGenericTool
        self.material = ProfileMaterial(**material)  # type: ProfileMaterial
        self.cutting_parameters = ProfileCuttingParameters(**cutting_parameters)  # type: ProfileCuttingParameters
        self.applicable_tools = applicable_tools  # type: list

    @classmethod
    def from_json(cls, json_data):
        """Create a Configuration object from a JSON object."""
        return Profile(**json_data)

    @classmethod
    def default(cls):
        """Get the default configuration."""
        profile_db = ProfileDatabase()
        default_profile = profile_db.get_profile("-0001")
        return Profile.from_json(default_profile)


class ProfileGenericTool(object):
    """Class to store the profile generic tool data"""

    def __init__(
        self,
        uid,
        description
    ):
        self.uid = str(uid)  # type: str
        self.description = str(description)  # type: str


class ProfileMaterial(object):
    """Class to store the profile material data"""

    def __init__(
        self,
        uid,
        description
    ):
        self.uid = str(uid)  # type: str
        self.description = str(description)  # type: str


class ProfileCuttingParameters(object):
    """Class to store the profile cutting parameters data"""

    def __init__(
        self,
        recommendations,
        spindle_speed,
        max_feedrate,
        plungerate,
        target_tool_load
    ):
        self.recommendations = ProfileRecommendations(**recommendations)  # type: ProfileRecommendations
        self.spindle_speed = int(spindle_speed)  # type: int
        self.max_feedrate = int(max_feedrate)  # type: int
        self.plungerate = int(plungerate)  # type: int
        self.target_tool_load = int(target_tool_load)  # type: int


class ProfileRecommendations(object):
    """Class to store the profile recommendations data"""

    def __init__(
        self,
        stepdown,
        stepover,
        unit,
        cutting_direction
    ):
        self.stepdown = float(stepdown)  # type: float
        self.stepover = float(stepover) if stepover else None  # type: float
        self.unit = str(unit)  # type: str
        self.cutting_direction = str(cutting_direction)  # type: str


class Configuration(object):
    """Class to store the configuration data."""

    def __init__(
        self,
        shape_type,
        units,
        rotation,
        canvas_shape_dims,
        material,
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
        self.material = str(material)  # type: str
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
    print(Cutter.default().description)
