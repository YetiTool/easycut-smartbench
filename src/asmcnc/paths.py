"""
Paths for the easycut-smartbench repository.
This module should sit in the directory below src (currently easycut-smartbench/src/asmcnc/paths.py).

Paths:
    ROOT_DIR (easycut-smartbench/src)
    ASMCNC_DIR (easycut-smartbench/src/asmcnc)
    SKAVA_UI_PATH (easycut-smartbench/src/asmcnc/skavaUI)
    SKAVA_UI_IMG_PATH (easycut-smartbench/src/asmcnc/skavaUI/img)
    SB_VALUES_PATH (easycut-smartbench/src/sb_values)

Functions:
    get_resource(file_name) -> str: Returns the path of a resource file.

Notes:
    - Any resource paths should be registered using resource_add_path.
    - If there are multiple resources with the same name, the first one found will be returned. (Use unique names)
    - This module should be imported first thing in main.py and call create_paths() to create any necessary directories.
"""

import os

from kivy.resources import resource_add_path, resource_find

from asmcnc.comms.logging_system.logging_system import Logger

# Root directory of the repository (easycut-smartbench/src) (working directory)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Permanent paths
ASMCNC_DIR = os.path.join(ROOT_DIR, "asmcnc")
SKAVA_UI_PATH = os.path.join(ASMCNC_DIR, "skavaUI")
SKAVA_UI_IMG_PATH = os.path.join(SKAVA_UI_PATH, "img")
SHAPE_CUTTER_IMG_PATH = os.path.join(ASMCNC_DIR, "apps", "shapeCutter_app", "img")

# Paths that may need to be created
SB_VALUES_PATH = os.path.join(ROOT_DIR, "sb_values")


def create_paths():
    if not os.path.exists(SB_VALUES_PATH):
        Logger.info("SB values directory not found, creating...")
        os.makedirs(SB_VALUES_PATH)


# Register any paths that contain resources
resource_add_path(SKAVA_UI_IMG_PATH)
resource_add_path(SHAPE_CUTTER_IMG_PATH)


# Functions for finding resources
def get_resource(file_name):
    return resource_find(file_name)


if __name__ == "__main__":
    print(get_resource("arrow_down.png"))
    print(ROOT_DIR)
    print(ASMCNC_DIR)
    print(SKAVA_UI_PATH)
    print(SKAVA_UI_IMG_PATH)
    print(SB_VALUES_PATH)
    print(SHAPE_CUTTER_IMG_PATH)
