"""
Paths for the easycut-smartbench repository.

Functions:
    get_resource(file_name) -> str: Returns the path of a resource file.
    create_paths() -> None: Creates any necessary directories that may not exist.

Notes:
    - Any resource paths should be registered using resource_add_path.
    - If there are multiple resources with the same name, the first one found will be returned. (Use unique names)
    - This module should be imported first thing in main.py and call create_paths() to create any necessary directories.
    - Update the create_paths() function if any new paths are added.
    - Update this docstring if any new paths are added.
"""

import os

from kivy.resources import resource_add_path, resource_find

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

SRC_PATH = os.path.join(ROOT_PATH, "src")

RESOURCES_PATH = os.path.join(ROOT_PATH, "resources")
FONTS_PATH = os.path.join(RESOURCES_PATH, "fonts")
IMAGES_PATH = os.path.join(RESOURCES_PATH, "images")
KEYBOARD_LAYOUTS_PATH = os.path.join(RESOURCES_PATH, "keyboard_layouts")
KV_PATH = os.path.join(RESOURCES_PATH, "kv")
LOCALISATION_PATH = os.path.join(RESOURCES_PATH, "localisation")
PROFILES_PATH = os.path.join(RESOURCES_PATH, "profiles")

MISC_PATH = os.path.join(RESOURCES_PATH, "misc")
PRIVACY_NOTICES_PATH = os.path.join(MISC_PATH, "privacy_notice")
PRODUCT_CODE_MIGRATION_PATH = os.path.join(MISC_PATH, "product_code_migration")
SB_VALUES_PATH = os.path.join(MISC_PATH, "sb_values")
WIFI_DOCUMENTATION_PATH = os.path.join(MISC_PATH, "wifi_documentation")
JOB_RECOVERY_PATH = os.path.join(MISC_PATH, "job_recovery")
YETIPILOT_PATH = os.path.join(MISC_PATH, "yetipilot")
DWT_PATH = os.path.join(MISC_PATH, "dwt")

GCODE_PATH = os.path.join(RESOURCES_PATH, "gcode")
FINAL_TEST_FILES_PATH = os.path.join(GCODE_PATH, "final_test_files")
JOB_CACHE_PATH = os.path.join(GCODE_PATH, "job_cache")
MOTOR_BASELINING_FILES_PATH = os.path.join(GCODE_PATH, "motor_baselining_files")

TRANSFER_TMP_PATH = os.path.join(ROOT_PATH, "transfer_tmp")

resource_add_path(RESOURCES_PATH)
resource_add_path(FONTS_PATH)
resource_add_path(IMAGES_PATH)
resource_add_path(KEYBOARD_LAYOUTS_PATH)
resource_add_path(KV_PATH)
resource_add_path(LOCALISATION_PATH)
resource_add_path(PROFILES_PATH)
resource_add_path(PRIVACY_NOTICES_PATH)
resource_add_path(PRODUCT_CODE_MIGRATION_PATH)
resource_add_path(SB_VALUES_PATH)
resource_add_path(WIFI_DOCUMENTATION_PATH)
resource_add_path(GCODE_PATH)
resource_add_path(FINAL_TEST_FILES_PATH)
resource_add_path(JOB_CACHE_PATH)
resource_add_path(MOTOR_BASELINING_FILES_PATH)
resource_add_path(JOB_RECOVERY_PATH)
resource_add_path(YETIPILOT_PATH)
resource_add_path(DWT_PATH)


# Functions for finding resources
def get_resource(file_name):
    return resource_find(file_name)


if __name__ == "__main__":
    print(SRC_PATH)
    print(GCODE_PATH)

    assert os.path.exists(SRC_PATH)
