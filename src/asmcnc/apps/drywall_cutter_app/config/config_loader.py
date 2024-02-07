import json
import os
import config_classes
import inspect

current_dir = os.path.dirname(__file__)
configurations_dir = os.path.join(current_dir, 'configurations')
cutters_dir = os.path.join(current_dir, 'cutters')
cutters_image_dir = os.path.join(cutters_dir, 'images')
IMG_DIR = os.path.join(current_dir, '..', 'img')

temp_dir = os.path.join(current_dir, 'temp')

TEMP_CONFIG_PATH = os.path.join(temp_dir, 'temp_config')
DEBUG_MODE = True


def debug(func):
    def wrapper(*args, **kwargs):
        if DEBUG_MODE:
            print('Calling function: ' + func.__name__ + ' with args: ' + str(args) + ' and kwargs: ' + str(
                kwargs))
        return func(*args, **kwargs)

    return wrapper


class DWTConfig(object):
    active_config = None  # type: config_classes.Configuration
    active_cutter = None  # type: config_classes.Cutter

    cutter_options = {
        "tool_6mm.json": {
            "image_path": os.path.join(cutters_image_dir, "tool_6mm.png"),
        }
    }

    shape_options = {
        "circle": {
            "image_path": os.path.join(IMG_DIR, "circle_shape_button.png"),
            "toolpath_offset_options": {
                "inside": {
                    "image_path": os.path.join(IMG_DIR, "circle_inside_toolpath.png"),
                },
                "on": {
                    "image_path": os.path.join(IMG_DIR, "circle_on_toolpath.png"),
                },
                "outside": {
                    "image_path": os.path.join(IMG_DIR, "circle_outside_toolpath.png"),
                }
            },
            "rotatable": False
        },
        "square": {
            "image_path": os.path.join(IMG_DIR, "square_shape_button.png"),
            "toolpath_offset_options": {
                "inside": {
                    "image_path": os.path.join(IMG_DIR, "square_inside_toolpath.png"),
                },
                "on": {
                    "image_path": os.path.join(IMG_DIR, "square_on_toolpath.png"),
                },
                "outside": {
                    "image_path": os.path.join(IMG_DIR, "square_outside_toolpath.png"),
                }
            },
            "rotatable": False
        },
        "line": {
            "image_path": os.path.join(IMG_DIR, "line_shape_button.png"),
            "toolpath_offset_options": {
                "on": {
                    "image_path": os.path.join(IMG_DIR, "line_on_toolpath.png"),
                }
            },
            "rotatable": True
        },
        "geberit": {
            "image_path": os.path.join(IMG_DIR, "geberit_shape_button.png"),
            "toolpath_offset_options": {
                "on": {
                    "image_path": os.path.join(IMG_DIR, "geberit_on_toolpath.png"),
                }
            },
            "rotatable": False
        },
        "rectangle": {
            "image_path": os.path.join(IMG_DIR, "rectangle_shape_button.png"),
            "toolpath_offset_options": {
                "inside": {
                    "image_path": os.path.join(IMG_DIR, "rectangle_inside_toolpath.png"),
                },
                "on": {
                    "image_path": os.path.join(IMG_DIR, "rectangle_on_toolpath.png"),
                },
                "outside": {
                    "image_path": os.path.join(IMG_DIR, "rectangle_outside_toolpath.png"),
                }
            },
            "rotatable": True
        }
    }  # type: dict

    toolpath_offset_buttons = {
        'inside': {
            'image_path': os.path.join(IMG_DIR, 'toolpath_offset_inside_button.png')
        },
        'on': {
            'image_path': os.path.join(IMG_DIR, 'toolpath_offset_on_button.png')
        },
        'outside': {
            'image_path': os.path.join(IMG_DIR, 'toolpath_offset_outside_button.png')
        }
    }

    def __init__(self):
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        # Load the temp config if it exists, otherwise load the default config.
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

            setattr(parameter, parameter_names[-1], parameter_value)
        else:
            setattr(self.active_config, parameter_name, parameter_value)

    def set_cutter_type(self, cutter_type):
        """
        Sets the cutter type for the active configuration.

        This sets the active configuration's cutter type and loads the cutter file.

        :param cutter_type: The name of the cutter file to load.
        :return: None
        """
        self.active_config.cutter_type = cutter_type
        self.load_cutter(cutter_type)

    def set_shape(self, shape):
        """
        Sets the shape type for the active configuration.

        This sets the active configuration's shape type and sets the active toolpath offset to the first option for the new shape.

        :param shape: The name of the shape to set (from shape_options)
        :return: None
        """
        # Set shape type
        self.active_config.shape_type = shape

        # If the active toolpath offset is not an option for the new shape,
        # set the active toolpath offset to the first option
        if self.active_config.toolpath_offset not in self.shape_options[shape]['toolpath_offset_options']:
            self.active_config.toolpath_offset = list(self.get_current_shape_toolpath_offsets().keys())[0]
        else:
            self.active_config.toolpath_offset = list(self.get_current_shape_toolpath_offsets())[0]

        # Set the rotation to horizontal by default
        self.active_config.rotation = 'horizontal'

    def set_toolpath_offset(self, toolpath_offset):
        """
        Sets the toolpath offset for the active configuration.

        :param toolpath_offset: The name of the toolpath offset to set (from shape_options)
        :return: None
        """
        self.active_config.toolpath_offset = toolpath_offset

    def toggle_rotation(self):
        """
        Toggles the rotation for the active configuration.

        :return: None
        """
        if self.active_config.rotation == 'horizontal':
            self.active_config.rotation = 'vertical'
        else:
            self.active_config.rotation = 'horizontal'

    def is_current_shape_rotatable(self):
        """
        :return: True if the active configuration's shape is rotatable, otherwise False.
        """
        return self.is_shape_rotatable(self.active_config.shape_type)

    def is_shape_rotatable(self, shape):
        """
        :return: True if the shape is rotatable, otherwise False.
        """
        return self.shape_options[shape]['rotatable']

    def get_current_shape_toolpath_offsets(self):
        """
        :return: The available toolpath offsets for the active configuration's shape.
        """
        return self.shape_options[self.active_config.shape_type]['toolpath_offset_options']

    def get_toolpath_offset_options(self):
        """
        :return: The shape's available toolpath offsets as a dictionary of {toolpath_offset_name: button_image_path}

        """
        current_shape_toolpath_offsets = self.get_current_shape_toolpath_offsets()

        return {key: self.toolpath_offset_buttons[key] for key in current_shape_toolpath_offsets}