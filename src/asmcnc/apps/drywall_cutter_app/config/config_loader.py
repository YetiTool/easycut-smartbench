import json
import os
import config_classes

CONFIGURATIONS_DIR = 'asmcnc/apps/drywall_cutter_app/config/configurations'
CUTTERS_DIR = 'asmcnc/apps/drywall_cutter_app/config/configurations'


class DWTConfig(object):
    active_config = None  # type: config_classes.Configuration
    active_cutter = None  # type: config_classes.Cutter

    def load_config(self, config_name):
        # type (str) -> None
        """
        Loads a configuration file from the configurations directory.

        :param config_name: The name of the configuration file to load.
        """
        file_path = os.path.join(CONFIGURATIONS_DIR, config_name)

        if not os.path.exists(file_path):
            raise Exception('Configuration file does not exist. ' + file_path + ' ' + os.getcwd())

        with open(file_path, 'r') as f:
            self.active_config = config_classes.Configuration(**json.load(f))

    def save_config(self, config_name):
        # type (str) -> None
        """
        Saves the active configuration to the configurations directory.

        :param config_name: The name of to save the configuration file as.
        """
        file_path = os.path.join(CONFIGURATIONS_DIR, config_name)

        with open(file_path, 'w') as f:
            json.dump(self.active_config, f, indent=4, default=lambda o: o.__dict__)

    def load_cutter(self, cutter_name):
        # type (str) -> None
        """
        Loads a cutter file from the cutters directory.

        :param cutter_name: The name of the cutter file to load.
        """
        file_path = os.path.join(CONFIGURATIONS_DIR, cutter_name)

        if not os.path.exists(file_path):
            raise Exception('Configuration file does not exist. ' + file_path)

        with open(file_path, 'r') as f:
            self.active_cutter = config_classes.Cutter(**json.load(f))
