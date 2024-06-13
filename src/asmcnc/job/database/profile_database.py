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

    def get_material_names(self):
        """Returns a list of strings with the material names."""
        return [material['description'] for material in self.material_data]

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

    def get_tool_id(self, description):
        """Returns the uid of a tool for a given description."""
        for tool in self.tool_data:
            if tool['description'] == description:
                return tool['uid']

    def get_material_id(self, description):
        """Returns the uid of a tool for a given description."""
        for material in self.material_data:
            if material['description'] == description:
                return material['uid']



