import json
import os
import inspect

from kivy.event import EventDispatcher
from kivy.properties import StringProperty, ObjectProperty

import config_classes
from asmcnc.comms.logging_system.logging_system import Logger

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIGURATIONS_DIR = os.path.join(CURRENT_DIR, "configurations")
CUTTERS_DIR = os.path.join(CURRENT_DIR, "cutters")
TEMP_DIR = os.path.join(CURRENT_DIR, "temp")
SETTINGS_DIR = os.path.join(CURRENT_DIR, "settings")

SETTINGS_PATH = os.path.join(SETTINGS_DIR, "settings.json")
TEMP_CONFIG_PATH = os.path.join(TEMP_DIR, "temp_config.json")

DEBUG_MODE = False
INDENT_VALUE = "    "


def debug(func):
    def wrapper(*args, **kwargs):
        if DEBUG_MODE:
            Logger.debug(
                "Calling function: "
                + func.__name__
                + " with args: "
                + str(args)
                + " and kwargs: "
                + str(kwargs)
            )
        return func(*args, **kwargs)

    return wrapper


def get_display_preview(json_obj):
    preview = get_shape_type(json_obj)
    preview += "Units: " + json_obj['units'] + "\n"
    # preview += "Rotation: " + json_obj['rotation'] + "\n"
    preview += "Canvas shape dims: \n"
    preview += get_shape_dimensions(json_obj)
    preview += "Cutter type: " + json_obj['cutter_type'][:-5] + "\n"
    preview += "Toolpath offset: " + json_obj['toolpath_offset'] + "\n"
    preview += "Cutting depths: \n"
    preview += INDENT_VALUE + "Material thickness: " + str(json_obj['cutting_depths']['material_thickness']) + "\n"
    preview += INDENT_VALUE + "Bottom offset: " + str(json_obj['cutting_depths']['bottom_offset']) + "\n"
    preview += INDENT_VALUE + "Auto pass: " + str(json_obj['cutting_depths']['auto_pass']) + "\n"
    preview += INDENT_VALUE + "Depth per pass: " + str(json_obj['cutting_depths']['depth_per_pass']) + "\n"
    preview += "Datum position: \n"
    preview += INDENT_VALUE + "X: " + str(json_obj['datum_position']['x']) + "\n"
    preview += INDENT_VALUE + "Y: " + str(json_obj['datum_position']['y']) + "\n"
    return preview


def get_shape_type(json_obj):
    if json_obj['shape_type'] in ['line', 'rectangle']:
        return "Shape type: " + json_obj['rotation'] + " " + json_obj['shape_type'] + "\n"
    else:
        return "Shape type: " + json_obj['shape_type'] + "\n"


def get_shape_dimensions(json_obj):
    if json_obj['shape_type'] == 'rectangle':
        dims = INDENT_VALUE + "X: " + str(json_obj['canvas_shape_dims']['x']) + "\n"
        dims += INDENT_VALUE + "Y: " + str(json_obj['canvas_shape_dims']['y']) + "\n"
        dims += INDENT_VALUE + "R: " + str(json_obj['canvas_shape_dims']['r']) + "\n"
    elif json_obj['shape_type'] == 'square':
        dims = INDENT_VALUE + "Y: " + str(json_obj['canvas_shape_dims']['y']) + "\n"
        dims += INDENT_VALUE + "R: " + str(json_obj['canvas_shape_dims']['r']) + "\n"
    elif json_obj['shape_type'] == 'circle':
        dims = INDENT_VALUE + "D: " + str(json_obj['canvas_shape_dims']['d']) + "\n"
    elif json_obj['shape_type'] == 'line':
        dims = INDENT_VALUE + "L: " + str(json_obj['canvas_shape_dims']['l']) + "\n"
    else:
        dims = ""
    return dims


class DWTConfig(EventDispatcher):
    active_config_name = StringProperty("")
    active_config = ObjectProperty(config_classes.Configuration.default())
    active_cutter = ObjectProperty(config_classes.Cutter.default())

    def __init__(self, screen_drywall_cutter=None, *args, **kwargs):
        super(DWTConfig, self).__init__(*args, **kwargs)
        self.screen_drywall_cutter = screen_drywall_cutter

        most_recent_config_path = self.get_most_recent_config()
        if most_recent_config_path:
            self.load_config(most_recent_config_path)
        else:
            self.load_temp_config()

    @staticmethod
    def get_most_recent_config():
        """
        Get most recent config from settings.json

        :return: the most recently used config path
        """
        if not os.path.exists(SETTINGS_PATH):
            return None  # No settings file, so no most recent config

        with open(SETTINGS_PATH, "r") as settings_f:
            j_obj = json.load(settings_f)
            return j_obj["most_recent_config"]

    @staticmethod
    def set_most_recent_config(config_path):
        """
        Set the most recent config in settings.json

        :param config_path: the name of the most recently used config
        :return:
        """
        with open(SETTINGS_PATH, "w+") as settings_f:
            j_obj = {"most_recent_config": config_path}
            json.dump(j_obj, settings_f)

    @staticmethod
    @debug
    def is_valid_configuration(config_name):
        # type (str) -> bool
        """
        Checks if a configuration file is valid/complete.

        :param config_name: The name of the configuration file to check.
        :return: True if the configuration file is valid/complete, otherwise False.
        """

        file_path = os.path.join(CONFIGURATIONS_DIR, config_name)

        if not os.path.exists(file_path):
            return False

        with open(file_path, "r") as f:
            cfg = json.load(f)

        field_count = len(cfg)

        valid_field_count = (
                len(inspect.getargspec(config_classes.Configuration.__init__).args) - 1
        )

        if field_count != valid_field_count:
            return False

        return True

    @staticmethod
    @debug
    def fix_config(config_name):
        # type (str) -> bool
        """
        Fixes a configuration file by adding any missing fields.

        :param config_name: The name of the configuration file to fix.
        :return: True if the configuration file was fixed, otherwise False.
        """

        file_path = os.path.join(CONFIGURATIONS_DIR, config_name)

        if not os.path.exists(file_path):
            return False

        with open(file_path, "r") as f:
            cfg = json.load(f)

        valid_field_names = inspect.getargspec(
            config_classes.Configuration.__init__
        ).args[1:]

        for field_name in valid_field_names:
            if field_name not in cfg:
                cfg[field_name] = getattr(
                    config_classes.Configuration.default(), field_name
                )

        with open(file_path, "w") as f:
            json.dump(cfg, f, indent=4, default=lambda o: o.__dict__)

        return True

    @debug
    def load_config(self, config_path):
        # type (str) -> None
        """
        Loads a configuration file from the configuration directory.

        :param config_path: The path of the configuration file to load.
        """
        if not os.path.exists(config_path):
            raise Exception(
                "Configuration file does not exist. " + config_path + " " + os.getcwd()
            )

        if not self.is_valid_configuration(config_path):
            if not self.fix_config(config_path):
                self.active_config = config_classes.Configuration.default()
                self.save_temp_config()

        with open(config_path, "r") as f:
            self.active_config = config_classes.Configuration(**json.load(f))

        if config_path != TEMP_CONFIG_PATH:
            self.set_most_recent_config(config_path)

        self.load_cutter(self.active_config.cutter_type)
        self.active_config_name = config_path.split(os.sep)[
            -1
        ]  # Get the name of the configuration file from the path

    @debug
    def save_config(self, config_path):
        # type (str) -> None
        """
        Saves the active configuration to the configuration directory.

        :param config_path: The path to save the config to
        """
        self.cleanup_active_config()

        with open(config_path, "w") as f:
            json.dump(self.active_config, f, indent=4, default=lambda o: o.__dict__)

    def cleanup_active_config(self):
        if self.active_config.shape_type == 'rectangle':
            self.active_config.canvas_shape_dims.d = 0
            self.active_config.canvas_shape_dims.l = 0
        elif self.active_config.shape_type == 'square':
            self.active_config.canvas_shape_dims.x = 0
            self.active_config.canvas_shape_dims.d = 0
            self.active_config.canvas_shape_dims.l = 0
        elif self.active_config.shape_type == 'circle':
            self.active_config.canvas_shape_dims.x = 0
            self.active_config.canvas_shape_dims.y = 0
            self.active_config.canvas_shape_dims.r = 0
            self.active_config.canvas_shape_dims.l = 0
        elif self.active_config.shape_type == 'line':
            self.active_config.canvas_shape_dims.x = 0
            self.active_config.canvas_shape_dims.y = 0
            self.active_config.canvas_shape_dims.r = 0
            self.active_config.canvas_shape_dims.d = 0

    @debug
    def load_cutter(self, cutter_name):
        # type (str) -> None
        """
        Loads a cutter file from the cutter directory.

        :param cutter_name: The name of the cutter file to load.
        """
        file_path = os.path.join(CUTTERS_DIR, cutter_name)

        if not os.path.exists(file_path):
            Logger.error("Cutter file doesn't exist: " + cutter_name)
            return

        with open(file_path, "r") as f:
            self.active_cutter = config_classes.Cutter.from_json(json.load(f))

    @staticmethod
    @debug
    def get_available_cutter_names():
        # type () -> dict{str: dict{str: str}}
        """
        :return: A list of the available cutter names and their file names.
        """
        cutters = {}
        for cutter_file in sorted(os.listdir(cutters_dir)):
            file_path = os.path.join(CUTTERS_DIR, cutter_file)

            if os.path.isfile(file_path):
                with open(file_path, "r") as f:
                    cutter = json.load(f)

                    if 'cutter_description' in cutter and 'image_path' in cutter:
                        cutters[cutter['cutter_description']] = {
                            'cutter_path': cutter_file,
                            'image_path': cutter['image_path']
                        }
        return cutters

    @debug
    def save_temp_config(self):
        # type () -> None
        """
        Saves the active configuration to a temporary file.

        This is used to save the configuration when the Drywall Cutter screen is left.
        """
        self.save_config(TEMP_CONFIG_PATH)

    @debug
    def load_temp_config(self):
        # type () -> None
        """
        Loads the temporary configuration file.

        This is used to load the configuration when the Drywall Cutter screen is loaded.
        """
        if not os.path.exists(TEMP_CONFIG_PATH):
            Logger.warning(
                "Temporary configuration file doesn't exist! Creating a new one."
            )
            self.active_config = config_classes.Configuration.default()
            self.save_temp_config()
            return

        self.load_config(TEMP_CONFIG_PATH)

    @debug
    def on_parameter_change(self, parameter_name, parameter_value):
        # type: (str, object) -> None
        """
        Should be called when a parameter is changed in the UI.
        Bind this to the widget, e.g.: on_value: root.on_parameter_change('parameter_name', self.value)
        If the parameter is nested, use a dot to separate the names, e.g.: 'nested_parameter_name.parameter_name'

        :param parameter_name: The name of the parameter that was changed.
        :param parameter_value: The new value of the parameter.
        """

        if "." in parameter_name:
            parameter_names = parameter_name.split(".")
            parameter = self.active_config

            for parameter_name in parameter_names[:-1]:
                parameter = getattr(parameter, parameter_name)

            if getattr(parameter, parameter_names[-1]) != parameter_value:
                self.__set_new_configuration_label()

            setattr(parameter, parameter_names[-1], parameter_value)
        else:
            if getattr(self.active_config, parameter_name) != parameter_value:
                self.__set_new_configuration_label()

            setattr(self.active_config, parameter_name, parameter_value)

        # update screen, check bumpers and so on:
        self.screen_drywall_cutter.drywall_shape_display_widget.check_datum_and_extents()

    def __set_new_configuration_label(self):
        if self.screen_drywall_cutter:
            self.active_config_name = "New Configuration"
