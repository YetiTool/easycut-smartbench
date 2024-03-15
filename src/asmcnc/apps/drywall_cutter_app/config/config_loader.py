import json
import os

from asmcnc.comms.logging_system.logging_system import Logger

import config_classes
import inspect

current_dir = os.path.dirname(os.path.realpath(__file__))
configurations_dir = os.path.join(current_dir, 'configurations')
cutters_dir = os.path.join(current_dir, 'cutters')
temp_dir = os.path.join(current_dir, 'temp')

TEMP_CONFIG_PATH = os.path.join(temp_dir, 'temp_config.json')
DEBUG_MODE = False
INDENT_VALUE = "    "


def debug(func):
    def wrapper(*args, **kwargs):
        if DEBUG_MODE:
            Logger.debug('Calling function: ' + func.__name__ + ' with args: ' + str(args) + ' and kwargs: ' + str(
                kwargs))
        return func(*args, **kwargs)

    return wrapper


def get_display_preview(json_obj):
    preview = get_shape_type(json_obj)
    preview += "Units: " + json_obj['units'] + "\n"
    #preview += "Rotation: " + json_obj['rotation'] + "\n"
    preview += "Canvas shape dims: \n"
    preview += get_shape_dimensions(json_obj)
    preview += "Cutter type: " + json_obj['cutter_type'] + "\n"
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
    if json_obj['shape_type'] in ['square', 'rectangle']:
        dims =  INDENT_VALUE + "X: " + str(json_obj['canvas_shape_dims']['x']) + "\n"
        dims += INDENT_VALUE + "Y: " + str(json_obj['canvas_shape_dims']['y']) + "\n"
        dims += INDENT_VALUE + "R: " + str(json_obj['canvas_shape_dims']['r']) + "\n"
    elif json_obj['shape_type'] == 'circle':
        dims = INDENT_VALUE + "D: " + str(json_obj['canvas_shape_dims']['d']) + "\n"
    elif json_obj['shape_type'] == 'line':
        dims = INDENT_VALUE + "L: " + str(json_obj['canvas_shape_dims']['l']) + "\n"
    else:
        dims = ""
    return dims

class DWTConfig(object):
    active_config = None  # type: config_classes.Configuration
    active_cutter = None  # type: config_classes.Cutter

    def __init__(self, screen_drywall_cutter=None):
        self.screen_drywall_cutter = screen_drywall_cutter
        # Load the temp config if it exists, otherwise load the default config.
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        if os.path.exists(TEMP_CONFIG_PATH):
            self.load_temp_config()
        else:
            self.active_config = config_classes.Configuration.default()
            self.load_cutter(self.active_config.cutter_type)

    @staticmethod
    @debug
    def is_valid_configuration(config_name):
        # type (str) -> bool
        """
        Checks if a configuration file is valid/complete.

        :param config_name: The name of the configuration file to check.
        :return: True if the configuration file is valid/complete, otherwise False.
        """

        file_path = os.path.join(configurations_dir, config_name)

        if not os.path.exists(file_path):
            return False

        with open(file_path, 'r') as f:
            cfg = json.load(f)

        field_count = len(cfg)

        valid_field_count = len(inspect.getargspec(config_classes.Configuration.__init__).args) - 1

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

        file_path = os.path.join(configurations_dir, config_name)

        if not os.path.exists(file_path):
            return False

        with open(file_path, 'r') as f:
            cfg = json.load(f)

        valid_field_names = inspect.getargspec(config_classes.Configuration.__init__).args[1:]

        for field_name in valid_field_names:
            if field_name not in cfg:
                cfg[field_name] = getattr(config_classes.Configuration.default(), field_name)

        with open(file_path, 'w') as f:
            json.dump(cfg, f, indent=4, default=lambda o: o.__dict__)

        return True

    @debug
    def load_config(self, config_name):
        # type (str) -> None
        """
        Loads a configuration file from the configuration directory.

        :param config_name: The name of the configuration file to load.
        """
        file_path = os.path.join(configurations_dir, config_name)

        if not os.path.exists(file_path):
            raise Exception('Configuration file does not exist. ' + file_path + ' ' + os.getcwd())

        if not self.is_valid_configuration(config_name):
            if not self.fix_config(config_name):
                self.active_config = config_classes.Configuration.default()
                self.save_temp_config()

        with open(file_path, 'r') as f:
            self.active_config = config_classes.Configuration(**json.load(f))

        self.load_cutter(self.active_config.cutter_type)

    @debug
    def save_config(self, config_name):
        # type (str) -> None
        """
        Saves the active configuration to the configuration directory.

        :param config_name: The name of to save the configuration file as.
        """
        file_path = os.path.join(configurations_dir, config_name)

        with open(file_path, 'w') as f:
            json.dump(self.active_config, f, indent=4, default=lambda o: o.__dict__)

    @debug
    def load_cutter(self, cutter_name):
        # type (str) -> None
        """
        Loads a cutter file from the cutter directory.

        :param cutter_name: The name of the cutter file to load.
        """
        file_path = os.path.join(cutters_dir, cutter_name)

        if not os.path.exists(file_path):
            raise Exception('Cutter file does not exist. ' + file_path + ' ' + os.getcwd())

        with open(file_path, 'r') as f:
            self.active_cutter = config_classes.Cutter(**json.load(f))

    @staticmethod
    @debug
    def get_available_cutter_names():
        # type () -> dict{str: str}
        """
        :return: A list of the available cutter names and their file names.
        """
        cutters = {}
        for f_name in os.listdir(cutters_dir):
            if not f_name.endswith('.json'):
                continue

            file_path = os.path.join(cutters_dir, f_name)

            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    cutter = json.load(f)

                    if 'cutter_description' in cutter:
                        cutters[cutter['cutter_description']] = f_name
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

        if '.' in parameter_name:
            parameter_names = parameter_name.split('.')
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

    def __set_new_configuration_label(self):
        if self.screen_drywall_cutter:
            self.screen_drywall_cutter.drywall_shape_display_widget.config_name_label.text = "New Configuration"
