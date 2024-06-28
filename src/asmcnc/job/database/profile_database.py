import json
import os

from asmcnc import paths


class ProfileDatabase(object):
    """
    This class holds all information about profiles, material and cutters.

    Dont instantiate yourself. Get your instance from App.get_running_app()."""

    MATERIAL_DB = os.path.join(paths.ASMCNC_PATH, 'job/database/material_database.json')
    PROFILE_DB = os.path.join(paths.ASMCNC_PATH, 'job/database/profile_database.json')
    TOOL_DB = os.path.join(paths.ASMCNC_PATH, 'job/database/tool_database.json')

    def __init__(self):
        # Load the material, tool and profile data
        with open(self.MATERIAL_DB) as f:
            self.material_data = json.load(f)

        with open(self.TOOL_DB) as f:
            self.tool_data = json.load(f)

        with open(self.PROFILE_DB) as f:
            self.profile_data = json.load(f)

    def get_material_name(self, uid):
        """Returns the material name for a given uid."""
        for material in self.material_data:
            if material['uid'] == uid:
                return material['description']

    def get_material_names(self, isa=None):
        """Returns a list of strings with the material names."""
        if isa:
            return [material['description'] for material in self.material_data if isa.value in material['available_isas']]
        return [material['description'] for material in self.material_data]

    def get_geberit_tools(self):
        """Returns a list of cutter UIDs  that are appropriate for Geberit."""
        cutters = []
        for profile in self.profile_data:
            if profile["material"]["uid"] == "0010":
                for tool in profile["applicable_tools"]:
                    cutters.append(tool["uid"])
        return cutters

    def get_tool_names(self, chosen_material=None):
        """
        Returns a list a tool_names suitable for the given Material.
        If no material is given, an empty list is returned.
        """
        if not chosen_material:
            return []

        tool_names = []

        for profile in self.profile_data:
            if profile['material']['uid'] == chosen_material:
                for tool in profile['applicable_tools']:
                    tool_names.append(tool['description'])

        return tool_names

    def get_tool_name(self, uid):
        """Returns the tool name for a given uid."""
        for tool in self.tool_data:
            if tool['uid'] == uid:
                return tool['description']

    def get_tool_id(self, description):
        """Returns the uid of a tool for a given description."""
        for tool in self.tool_data:
            if tool['description'] == description:
                return tool['uid']

    def get_tool_generic_id(self, uid):
        for tool in self.tool_data:
            if tool['uid'] == uid:
                return tool['generic_definition']['uid']

    def get_tool(self, uid):
        """Returns the tool for a given uid."""
        for tool in self.tool_data:
            if tool['uid'] == uid:
                return tool

    def get_material_id(self, description):
        """Returns the uid of a tool for a given description."""
        for material in self.material_data:
            if material['description'] == description:
                return material['uid']

    def get_profile_id(self, material_id, tool_generic_id):
        """Returns the profile for a given tool and material."""
        for profile in self.profile_data:
            if profile['generic_tool']['uid'] == tool_generic_id and profile['material']['uid'] == material_id:
                return profile['uid']

    def get_profile(self, profile_id):
        """Returns the profile for a given profile_id."""
        for profile in self.profile_data:
            if profile['uid'] == profile_id:
                return profile



