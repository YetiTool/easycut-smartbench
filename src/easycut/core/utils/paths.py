"""
Paths for the easycut-smartbench repository.
This module should sit in the directory below src (currently easycut-smartbench/src/asmcnc/paths.py).

Permanent Paths:
    ROOT_PATH: Source root directory of the repository (easycut-smartbench/src) (working directory)
    EASYCUT_SMARTBENCH_PATH: Root directory of the repository (easycut-smartbench)
    ASMCNC_PATH: Path to the asmcnc directory. (easycut-smartbench/src/asmcnc)
    SKAVA_UI_PATH: Path to the skavaUI directory. (easycut-smartbench/src/asmcnc/skavaUI)
    SKAVA_UI_IMG_PATH: Path to the img directory in skavaUI. (easycut-smartbench/src/asmcnc/skavaUI/img)
    CORE_UI_PATH: Path to the core_UI directory. (easycut-smartbench/src/asmcnc/core_UI)
    APPS_PATH: Path to the apps directory. (easycut-smartbench/src/asmcnc/apps)
    SHAPE_CUTTER_APP_PATH: Path to the shapeCutter_app directory. (easycut-smartbench/src/asmcnc/apps/shapeCutter_app)
    SHAPE_CUTTER_IMG_PATH: Path to the img directory in shapeCutter_app. (easycut-smartbench/src/asmcnc/apps/shapeCutter_app/img)
    SW_UPDATE_APP_PATH: Path to the SWupdater_app directory. (easycut-smartbench/src/asmcnc/apps/SWupdater_app)
    SW_UPDATE_IMG_PATH: Path to the img directory in SWupdater_app. (easycut-smartbench/src/asmcnc/apps/SWupdater_app/img)
    CALIBRATION_APP_PATH: Path to the calibration_app directory. (easycut-smartbench/src/asmcnc/calibration_app)
    CALIBRATION_IMG_PATH: Path to the img directory in calibration_app. (easycut-smartbench/src/asmcnc/calibration_app/img)
    MAINTENANCE_APP_PATH: Path to the maintenance_app directory. (easycut-smartbench/src/asmcnc/apps/maintenance_app)
    MAINTENANCE_IMG_PATH: Path to the img directory in maintenance_app. (easycut-smartbench/src/asmcnc/apps/maintenance_app/img)
    DWT_APP_PATH: Path to the drywall_cutter_app directory. (easycut-smartbench/src/asmcnc/apps/drywall_cutter_app)
    DWT_IMG_PATH: Path to the img directory in drywall_cutter_app. (easycut-smartbench/src/asmcnc/apps/drywall_cutter_app/img)
    SYSTEM_TOOLS_APP_PATH: Path to the systemTools_app directory. (easycut-smartbench/src/asmcnc/apps/systemTools_app)
    SYSTEM_TOOLS_IMG_PATH: Path to the img directory in systemTools_app. (easycut-smartbench/src/asmcnc/apps/systemTools_app/img)
    UPGRADE_APP_PATH: Path to the upgrade_app directory. (easycut-smartbench/src/asmcnc/apps/upgrade_app)
    UPGRADE_IMG_PATH: Path to the img directory in upgrade_app. (easycut-smartbench/src/asmcnc/apps/upgrade_app/img)
    WIFI_APP_PATH: Path to the wifi_app directory. (easycut-smartbench/src/asmcnc/apps/wifi_app)
    WIFI_IMG_PATH: Path to the img directory in wifi_app. (easycut-smartbench/src/asmcnc/apps/wifi_app/img)
    START_UP_SEQUENCE_PATH: Path to the start_up_sequence directory. (easycut-smartbench/src/asmcnc/apps/start_up_sequence)
    START_UP_SEQUENCE_IMG_PATH: Path to the img directory in start_up_sequence. (easycut-smartbench/src/asmcnc/apps/start_up_sequence/img)
    DATA_CONSENT_APP_PATH: Path to the data_consent_app directory. (easycut-smartbench/src/asmcnc/apps/start_up_sequence/data_consent_app)
    DATA_CONSENT_IMG_PATH: Path to the img directory in data_consent_app. (easycut-smartbench/src/asmcnc/apps/start_up_sequence/data_consent_app/img)
    WARRANTY_APP_PATH: Path to the warranty_app directory. (easycut-smartbench/src/asmcnc/apps/start_up_sequence/warranty_app)
    WARRANTY_IMG_PATH: Path to the img directory in warranty_app. (easycut-smartbench/src/asmcnc/apps/start_up_sequence/warranty_app/img)
    WELCOME_TO_SMARTBENCH_APP_PATH: Path to the welcome_to_smartbench_app directory. (easycut-smartbench/src/asmcnc/apps/start_up_sequence/welcome_to_smartbench_app)
    WELCOME_TO_SMARTBENCH_IMG_PATH: Path to the img directory in welcome_to_smartbench_app. (easycut-smartbench/src/asmcnc/apps/start_up_sequence/welcome_to_smartbench_app/img)
    JOB_GO_IMG_PATH: Path to the img directory in job_go. (easycut-smartbench/src/asmcnc/core_UI/job_go/img)
    SEQUENCE_ALARM_IMG_PATH: Path to the img directory in sequence_alarm. (easycut-smartbench/src/asmcnc/core_UI/sequence_alarm/img)

Paths that may need to be created:
    SB_VALUES_PATH: Path to the sb_values directory. (easycut-smartbench/src/sb_values)
    DWT_TEMP_GCODE_PATH: Path to the temp gcode directory in drywall_cutter_app. (easycut-smartbench/src/asmcnc/apps/drywall_cutter_app/gcode/temp)

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

from asmcnc.comms.logging_system.logging_system import Logger

# Root directory of the repository (easycut-smartbench/src) (working directory)
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Permanent paths
EASYCUT_SMARTBENCH_PATH = os.path.dirname(ROOT_PATH)
ASMCNC_PATH = os.path.join(ROOT_PATH, "asmcnc")
COMMS_PATH = os.path.join(ASMCNC_PATH, "comms")

SKAVA_UI_PATH = os.path.join(ASMCNC_PATH, "skavaUI")
SKAVA_UI_IMG_PATH = os.path.join(SKAVA_UI_PATH, "img")

CORE_UI_PATH = os.path.join(ASMCNC_PATH, "core_UI")

APPS_PATH = os.path.join(ASMCNC_PATH, "apps")

SHAPE_CUTTER_APP_PATH = os.path.join(APPS_PATH, "shapeCutter_app")
SHAPE_CUTTER_IMG_PATH = os.path.join(SHAPE_CUTTER_APP_PATH, "img")

SW_UPDATE_APP_PATH = os.path.join(APPS_PATH, "SWupdater_app")
SW_UPDATE_IMG_PATH = os.path.join(SW_UPDATE_APP_PATH, "img")

CALIBRATION_APP_PATH = os.path.join(ASMCNC_PATH, "calibration_app")
CALIBRATION_IMG_PATH = os.path.join(CALIBRATION_APP_PATH, "img")

MAINTENANCE_APP_PATH = os.path.join(APPS_PATH, "maintenance_app")
MAINTENANCE_IMG_PATH = os.path.join(MAINTENANCE_APP_PATH, "img")

DWT_APP_PATH = os.path.join(APPS_PATH, "drywall_cutter_app")
DWT_IMG_PATH = os.path.join(DWT_APP_PATH, "img")

SYSTEM_TOOLS_APP_PATH = os.path.join(APPS_PATH, "systemTools_app")
SYSTEM_TOOLS_IMG_PATH = os.path.join(SYSTEM_TOOLS_APP_PATH, "img")

UPGRADE_APP_PATH = os.path.join(APPS_PATH, "upgrade_app")
UPGRADE_IMG_PATH = os.path.join(UPGRADE_APP_PATH, "img")

WIFI_APP_PATH = os.path.join(APPS_PATH, "wifi_app")
WIFI_IMG_PATH = os.path.join(WIFI_APP_PATH, "img")

START_UP_SEQUENCE_PATH = os.path.join(APPS_PATH, "start_up_sequence")
START_UP_SEQUENCE_IMG_PATH = os.path.join(START_UP_SEQUENCE_PATH, "screens", "img")

DATA_CONSENT_APP_PATH = os.path.join(START_UP_SEQUENCE_PATH, "data_consent_app")
DATA_CONSENT_IMG_PATH = os.path.join(DATA_CONSENT_APP_PATH, "img")

WARRANTY_APP_PATH = os.path.join(START_UP_SEQUENCE_PATH, "warranty_app")
WARRANTY_IMG_PATH = os.path.join(WARRANTY_APP_PATH, "img")

WELCOME_TO_SMARTBENCH_APP_PATH = os.path.join(START_UP_SEQUENCE_PATH, "welcome_to_smartbench_app")
WELCOME_TO_SMARTBENCH_IMG_PATH = os.path.join(WELCOME_TO_SMARTBENCH_APP_PATH, "img")

JOB_GO_IMG_PATH = os.path.join(CORE_UI_PATH, "job_go", "img")

SEQUENCE_ALARM_IMG_PATH = os.path.join(CORE_UI_PATH, "sequence_alarm", "img")

# Paths that may need to be created
SB_VALUES_PATH = os.path.join(ROOT_PATH, "sb_values")
DWT_TEMP_GCODE_PATH = os.path.join(DWT_APP_PATH, "gcode", "temp")


def create_paths():
    if not os.path.exists(SB_VALUES_PATH):
        Logger.warning("SB values directory not found, creating...")
        os.makedirs(SB_VALUES_PATH)
    if not os.path.exists(DWT_TEMP_GCODE_PATH):
        Logger.warning("Drywall cutter temp gcode directory not found, creating...")
        os.makedirs(DWT_TEMP_GCODE_PATH)


# Register any paths that contain resources
resource_add_path(SKAVA_UI_IMG_PATH)
resource_add_path(SHAPE_CUTTER_IMG_PATH)
resource_add_path(CALIBRATION_IMG_PATH)
resource_add_path(MAINTENANCE_IMG_PATH)
resource_add_path(DWT_IMG_PATH)
resource_add_path(SYSTEM_TOOLS_IMG_PATH)
resource_add_path(UPGRADE_IMG_PATH)
resource_add_path(WIFI_IMG_PATH)
resource_add_path(START_UP_SEQUENCE_IMG_PATH)
resource_add_path(DATA_CONSENT_IMG_PATH)
resource_add_path(WARRANTY_IMG_PATH)
resource_add_path(WELCOME_TO_SMARTBENCH_IMG_PATH)
resource_add_path(JOB_GO_IMG_PATH)
resource_add_path(SEQUENCE_ALARM_IMG_PATH)


# Functions for finding resources
def get_resource(file_name):
    return resource_find(file_name)


if __name__ == "__main__":
    print(get_resource("arrow_down.png"))
    print(ROOT_PATH)
    print(ASMCNC_PATH)
    print(SKAVA_UI_PATH)
    print(SKAVA_UI_IMG_PATH)
    print(CORE_UI_PATH)
    print(APPS_PATH)
    print(SHAPE_CUTTER_APP_PATH)
    print(SHAPE_CUTTER_IMG_PATH)
    print(SW_UPDATE_APP_PATH)
    print(SW_UPDATE_IMG_PATH)
    print(CALIBRATION_APP_PATH)
    print(CALIBRATION_IMG_PATH)
    print(MAINTENANCE_APP_PATH)
    print(MAINTENANCE_IMG_PATH)
    print(DWT_APP_PATH)
    print(DWT_IMG_PATH)
    print(SYSTEM_TOOLS_APP_PATH)
    print(SYSTEM_TOOLS_IMG_PATH)
    print(UPGRADE_APP_PATH)
    print(UPGRADE_IMG_PATH)
    print(WIFI_APP_PATH)
    print(WIFI_IMG_PATH)
    print(START_UP_SEQUENCE_PATH)
    print(START_UP_SEQUENCE_IMG_PATH)
    print(DATA_CONSENT_APP_PATH)
    print(DATA_CONSENT_IMG_PATH)
    print(WARRANTY_APP_PATH)
    print(WARRANTY_IMG_PATH)
    print(WELCOME_TO_SMARTBENCH_APP_PATH)
    print(WELCOME_TO_SMARTBENCH_IMG_PATH)
    print(JOB_GO_IMG_PATH)
    print(SEQUENCE_ALARM_IMG_PATH)
    print(SB_VALUES_PATH)
