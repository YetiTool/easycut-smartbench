from kivy.properties import ObjectProperty

from asmcnc.apps.drywall_cutter_app.config.config_loader import DWTConfig
from asmcnc.apps.drywall_cutter_app.dwt_app_view import DrywallCutterView
from asmcnc.apps.drywall_cutter_app.engine import GCodeEngine


class DrywallCutterModel:
    """
    The model for the Drywall Cutter screen.
    """

    config = ObjectProperty()  # type: DWTConfig
    engine = ObjectProperty()  # type: GCodeEngine

    def __init__(self):
        self.config = DWTConfig()
        self.engine = GCodeEngine(self.config)


class DrywallCutterController(object):
    """
    The controller for the Drywall Cutter screen.
    """

    def __init__(self, name, machine, screen_manager):
        self.name = name
        self.model = DrywallCutterModel()
        self.screen_manager = screen_manager
        self.router_machine = machine

        # Build the view last
        self.view = DrywallCutterView(name=self.name, controller=self)

        self.set_shape(self.model.config.active_config.shape_type)

    def set_cutter(self, cutter):
        """
        Called when a cutter is selected from the dropdown.

        Does all the logic for what happens when the cutter is selected.
        :param cutter: The cutter file name
        :return:
        """
        # Update the config with the new cutter
        self.model.config.set_cutter_type(cutter)

        # Update the dropdown with the new cutter image
        self.view.set_cutter_image(self.model.config.active_cutter.image_path)

    def set_shape(self, shape):
        """
        Called when a shape is selected from the dropdown.

        Does all the logic for what happens when the shape is selected.
        :param shape:
        :return:
        """
        # Update the config with the new shape
        self.model.config.set_shape(shape)

        # Set the rotate button to disabled if the shape cannot be rotated
        self.view.set_rotate_button_disabled(
            self.model.config.is_shape_rotatable(shape)
        )

        # Update the dropdown with the available toolpath offsets
        self.update_available_toolpath_offsets()

        # If the shape requires rotation (from current value), rotate it
        if self.view.shape_display_widget.rotation_required():
            self.view.rotate_shape(
                shape, self.model.config.active_config.rotation, swap_lengths=False
            )

    def update_available_toolpath_offsets(self):
        """
        Updates the available toolpath offsets in the dropdown based on the selected shape.

        :return: None
        """
        toolpath_offset_options = self.model.config.get_toolpath_offset_options()
        self.view.toolpath_offset_drop_down.set_options(toolpath_offset_options)

    def set_toolpath_offset(self, toolpath_offset):
        """
        Called when a toolpath offset is selected from the dropdown.

        Does all the logic for what happens when the toolpath offset is selected.
        :param toolpath_offset: The selected toolpath offset
        :return: None
        """
        # Update the config with the new toolpath offset
        self.model.config.set_toolpath_offset(toolpath_offset)

        # Get the shape & rotation from config
        shape = self.model.config.active_config.shape_type

        self.model.config.toggle_rotation()
        rotation = self.model.config.active_config.rotation

        # Set the shape display widget to the new shape & rotation
        self.view.shape_display_widget.select_toolpath(shape, toolpath_offset, rotation)

    def handle_home_button_pressed(self):
        """
        Called when the home button is pressed.
        :return: None
        """
        self.router_machine.request_homing_procedure(self.view.name, self.view.name)

    def handle_rotate_button_pressed(self):
        """
        Called when the rotate button is pressed.

        Toggles the rotation of the shape.
        :return: None
        """
        # if self.model.config.is_current_shape_rotatable():
        # in theory should always be rotatable, as the button should be disabled if not
        self.model.config.toggle_rotation()

        shape = self.model.config.active_config.shape_type
        rotation = self.model.config.active_config.rotation
        swap_lengths = True

        self.view.shape_display_widget.select_shape(shape, rotation, swap_lengths)

    def handle_stop_button_pressed(self):
        """
        Called when the stop button is pressed.

        Opens the stop popup
        :return: None
        """
        # Need to refactor so that the popup system module is singleton, so I don't have to pass it around

    def handle_exit_button_pressed(self):
        """
        Called when the exit button is pressed.

        Exits the Drywall Cutter screen and returns to the lobby.
        :return:
        """
        self.screen_manager.current = "lobby"

    def handle_on_enter(self):
        """
        Called when the screen is entered.
        :return: None
        """

    def handle_on_leave(self):
        """
        Called when the screen is left.
        :return: None
        """
        self.model.config.save_temp_config()

    def handle_load_filechooser_pressed(self):
        pass

    def handle_material_setup_pressed(self):
        pass

    def handle_simulate_pressed(self):
        pass

    def handle_save_pressed(self):
        pass

    def handle_run_pressed(self):
        pass

    def get_screen(self):
        return self.view
