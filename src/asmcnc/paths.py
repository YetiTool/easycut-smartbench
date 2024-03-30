import os

from kivy.resources import resource_add_path, resource_find

from asmcnc.comms.logging_system.logging_system import Logger

# Project root directory is the parent of the 'paths' module
ENTRY_POINT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Common paths that will always exist
EASYCUT_SMARTBENCH_PATH = os.path.abspath(os.path.join(ENTRY_POINT_PATH, os.pardir))
ASMCNC_PATH = os.path.abspath(os.path.dirname(__file__))
SKAVA_UI_PATH = os.path.abspath(os.path.join(ASMCNC_PATH, "skavaUI"))
SKAVA_UI_IMG_PATH = os.path.abspath(os.path.join(SKAVA_UI_PATH, "img"))

# Create paths that may not exist on first launch
SB_VALUES_PATH = os.path.join(ENTRY_POINT_PATH, "sb_values")
if not os.path.exists(SB_VALUES_PATH):
    os.makedirs(SB_VALUES_PATH)

# Register the resource paths for Kivy
resource_add_path(SKAVA_UI_IMG_PATH)


def get_resource(resource_name):
    """
    Get the path to a resource.

    :param resource_name: The name of the resource.
    :return: The path to the resource.
    """
    resource_path = resource_find(resource_name)
    if not resource_path:
        Logger.warning("Resource '{}' not found.".format(resource_name))
    return resource_path

