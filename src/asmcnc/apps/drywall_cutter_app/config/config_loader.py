import json
import os
import inspect

from kivy.event import EventDispatcher
from kivy.properties import StringProperty

import config_classes
from asmcnc.comms.logging_system.logging_system import Logger


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIGURATIONS_DIR = os.path.join(CURRENT_DIR, 'configurations')
CUTTERS_DIR = os.path.join(CURRENT_DIR, 'cutters')
TEMP_DIR = os.path.join(CURRENT_DIR, 'temp')
SETTINGS_DIR = os.path.join(CURRENT_DIR, 'settings')

SETTINGS_PATH = os.path.join(SETTINGS_DIR, 'settings.json')
TEMP_CONFIG_PATH = os.path.join(TEMP_DIR, 'temp_config.json')

DEBUG_MODE = False


def debug(func):
    def wrapper(*args, **kwargs):
        if DEBUG_MODE:
            Logger.debug('Calling function: ' + func.__name__ + ' with args: ' + str(args) + ' and kwargs: ' + str(
                kwargs))
        return func(*args, **kwargs)

    return wrapper


class DWTConfig(EventDispatcher):
    active_config_name = StringProperty("")
    active_config = config_classes.Configuration.default()
    active_cutter = config_classes.Cutter.default()

    def __init__(self, screen_drywall_cutter=None, *args, **kwargs):
        super(DWTConfig, self).__init__(*args, **kwargs)
        self.screen_drywall_cutter = screen_drywall_cutter
        self.start_up()

    def start_up(self):
        # Load most recent config
        most_recent_config = self.get_most_recent_config()
        if most_recent_config:
            self.load_config(most_recent_config)
        else:
            # If no configs, try to load temp config
            if os.path.exists(TEMP_CONFIG_PATH):
                self.load_temp_config()
            else:
                # Otherwise, create new config based on the default configuration
                self.active_config = config_classes.Configuration.default()
                self.load_cutter(self.active_config.cutter_type)

    @staticmethod
    def get_most_recent_config():
        """
        Get most recent config from settings.json
        :return: the most recently used config path
        """
        if not os.path.exists(SETTINGS_PATH):
            return None
        else:
            with open(SETTINGS_PATH, 'r') as settings_f:
                j_obj = json.load(settings_f)
                return j_obj["most_recent_config"]

    @staticmethod
    def set_most_recent_config(config_path):
        """
        Set the most recent config in settings.json
        :param config_path: the path to the most recently used config
        :return:
        """
        with open(SETTINGS_PATH, 'w+') as settings_f:
            j_obj = {
                "most_recent_config": config_path
            }
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

        file_path = os.path.join(CONFIGURATIONS_DIR, config_name)

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
        file_path = os.path.join(CONFIGURATIONS_DIR, config_name)

        if not os.path.exists(file_path):
            raise Exception('Configuration file does not exist. ' + file_path + ' ' + os.getcwd())

        if not self.is_valid_configuration(config_name):
            if not self.fix_config(config_name):
                self.active_config = config_classes.Configuration.default()
                self.save_temp_config()

        with open(file_path, 'r') as f:
            self.active_config = config_classes.Configuration(**json.load(f))

        if file_path != TEMP_CONFIG_PATH:
            self.set_most_recent_config(file_path)

        self.load_cutter(self.active_config.cutter_type)
        self.active_config_name = "New Configuration" if file_path == TEMP_CONFIG_PATH else config_name

    @debug
    def save_config(self, config_name):
        # type (str) -> None
        """
        Saves the active configuration to the configuration directory.

        :param config_name: The name of to save the configuration file as.
        """
        file_path = os.path.join(CONFIGURATIONS_DIR, config_name)

        with open(file_path, 'w') as f:
            json.dump(self.active_config, f, indent=4, default=lambda o: o.__dict__)

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

        with open(file_path, 'r') as f:
            self.active_cutter = config_classes.Cutter.from_json(json.load(f))

    @staticmethod
    @debug
    def get_available_cutter_names():
        # type () -> dict{str: str}
        """
        :return: A list of the available cutter names and their file names.
        """
        cutters = {}
        for f_name in os.listdir(CUTTERS_DIR):
            if not f_name.endswith('.json'):
                continue

            file_path = os.path.join(CUTTERS_DIR, f_name)

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
            self.active_config_name = "New Configuration"
