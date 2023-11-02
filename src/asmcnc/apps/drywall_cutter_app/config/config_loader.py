import json
import os
import config_classes

configurations_dir = 'asmcnc/apps/drywall_cutter_app/config/configurations'
cutters_dir = 'asmcnc/apps/drywall_cutter_app/config/cutters'


class DWTConfig(object):
    active_config = None  # type: config_classes.Configuration
    active_cutter = None  # type: config_classes.Cutter

    def __init__(self):
        # Load the temp config if it exists, otherwise load the default config.
        if os.path.exists(os.path.join(configurations_dir, 'temp_config.json')):
            self.load_config('temp_config.json')
        else:
            self.active_config = config_classes.Configuration.default()
            self.active_cutter = self.load_cutter(self.active_config.cutter_type)

    def load_config(self, config_name):
        # type (str) -> None
        """
        Loads a configuration file from the configurations directory.

        :param config_name: The name of the configuration file to load.
        """
        file_path = os.path.join(configurations_dir, config_name)

        if not os.path.exists(file_path):
            raise Exception('Configuration file does not exist. ' + file_path + ' ' + os.getcwd())

        with open(file_path, 'r') as f:
            self.active_config = config_classes.Configuration(**json.load(f))

        self.load_cutter(self.active_config.cutter_type)

    def save_config(self, config_name):
        # type (str) -> None
        """
        Saves the active configuration to the configurations directory.

        :param config_name: The name of to save the configuration file as.
        """
        file_path = os.path.join(configurations_dir, config_name)

        with open(file_path, 'w') as f:
            json.dump(self.active_config, f, indent=4, default=lambda o: o.__dict__)

    def load_cutter(self, cutter_name):
        # type (str) -> None
        """
        Loads a cutter file from the cutters directory.

        :param cutter_name: The name of the cutter file to load.
        """
        file_path = os.path.join(cutters_dir, cutter_name)

        if not os.path.exists(file_path):
            raise Exception('Cutter file does not exist. ' + file_path + ' ' + os.getcwd())

        with open(file_path, 'r') as f:
            self.active_cutter = config_classes.Cutter(**json.load(f))

    def save_temp_config(self):
        # type () -> None
        """
        Saves the active configuration to a temporary file.

        This is used to save the configuration when the Drywall Cutter screen is left.
        """
        self.save_config('temp_config.json')

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

            setattr(parameter, parameter_names[-1], parameter_value)
        else:
            setattr(self.active_config, parameter_name, parameter_value)

