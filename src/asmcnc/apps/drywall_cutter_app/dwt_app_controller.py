from kivy.properties import ObjectProperty

from asmcnc.apps.drywall_cutter_app import material_setup_popup, screen_config_filesaver, screen_config_filechooser
from asmcnc.apps.drywall_cutter_app.config.config_loader import DWTConfig
from asmcnc.apps.drywall_cutter_app.dwt_app_view import DrywallCutterView
from asmcnc.apps.drywall_cutter_app.engine import GCodeEngine
from asmcnc.skavaUI import popup_info


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

    def __init__(self, name, machine, screen_manager, keyboard, localization):
        self.name = name
        self.model = DrywallCutterModel()
        self.screen_manager = screen_manager
        self.router_machine = machine
        self.keyboard = keyboard
        self.localization = localization

        # Build the view last
        self.view = DrywallCutterView(name=self.name, controller=self)
        self.material_setup_popup = material_setup_popup.CuttingDepthsPopup(
            self.localization, self.keyboard, self.model.config
        )

        self.__load_default_state()

    def __load_default_state(self):
        # Set the dropdown images to the correct images
        self.view.set_cutter_drop_down_image(
            self.model.config.cutter_options[str(self.model.config.active_config.cutter_type)]["image_path"])
        self.view.set_shape_drop_down_image(
            self.model.config.shape_options[str(self.model.config.active_config.shape_type)]["image_path"])
        self.view.set_toolpath_offset_drop_down_image(
            self.model.config.toolpath_offset_buttons[str(self.model.config.active_config.toolpath_offset)]["image_path"])

        # Handle the integration of the config into the view
        self.handle_cutter_selection_changed(self.model.config.active_config.cutter_type)
        self.handle_shape_selection_changed(self.model.config.active_config.shape_type)
        self.handle_toolpath_offset_selection_changed(self.model.config.active_config.toolpath_offset)

    def handle_cutter_selection_changed(self, cutter):
        """
        Called when a cutter is selected from the dropdown.

        Does all the logic for what happens when the cutter is selected.
        :param cutter: The cutter file name
        :return:
        """
        # Update the config with the new cutter
        self.model.config.set_cutter_type(cutter)

    def handle_shape_selection_changed(self, shape):
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
            not self.model.config.is_shape_rotatable(shape)
        )

        # Update the dropdown with the available toolpath offsets
        self.view.shape_display_widget.select_shape(shape, self.model.config.active_config.rotation)
        self.update_toolpath_offsets_drop_down()

        # Update the toolpath offset image on the shape display widget
        self.handle_toolpath_offset_selection_changed(self.model.config.active_config.toolpath_offset)

        # If the shape requires rotation (from current value), rotate it
        if self.view.shape_display_widget.rotation_required():
            self.view.rotate_shape(
                shape, self.model.config.active_config.rotation, swap_lengths=False
            )

    def update_toolpath_offsets_drop_down(self):
        """
        Updates the available toolpath offsets in the dropdown based on the selected shape.

        :return: None
        """
        self.view.toolpath_offset_drop_down.set_options(self.model.config.get_toolpath_offset_options())
        self.view.set_toolpath_offset_drop_down_image(
            self.model.config.toolpath_offset_buttons[self.model.config.active_config.toolpath_offset]["image_path"])

    def handle_toolpath_offset_selection_changed(self, toolpath_offset):
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
        toolpath_offset = self.model.config.active_config.toolpath_offset

        self.view.shape_display_widget.select_shape(shape, rotation, swap_lengths)
        self.view.shape_display_widget.select_toolpath(shape, toolpath_offset, rotation)

    def handle_stop_button_pressed(self):
        """
        Called when the stop button is pressed.

        Opens the stop popup
        :return: None
        """
        # Need to refactor so that the popup system module is singleton, so I don't have to pass it around
        popup_info.PopupStop(self.router_machine, self.screen_manager, self.localization)

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

    def __handle_filechooser_callback(self, file_path):
        """
        Callback for the filechooser.

        :param file_path: The file path selected
        :return: None
        """
        self.model.config.load_config(file_path)
        self.__load_default_state()

    def handle_load_filechooser_pressed(self):
        """
        Called when the load button is pressed.
        :return: None
        """
        if not self.screen_manager.has_screen('config_filechooser'):
            self.screen_manager.add_widget(
                screen_config_filechooser.ConfigFileChooser(name='config_filechooser',
                                                            screen_manager=self.screen_manager,
                                                            localization=self.localization,
                                                            callback=self.__handle_filechooser_callback))
        self.screen_manager.current = 'config_filechooser'

    def handle_material_setup_pressed(self):
        """
        Called when the material setup button is pressed.
        :return: None
        """
        self.material_setup_popup.open()

    def handle_simulate_pressed(self):
        """
        Called when the simulate button is pressed.
        :return: None
        """
        # self.model.engine.simulate()
        pass

    def __handle_filesaver_callback(self, file_path):
        """
        Callback for the filesaver.

        :param file_path: The file path selected
        :return: None
        """
        self.model.config.save_config(file_path)

    def handle_save_pressed(self):
        """
        Called when the save button is pressed.
        :return: None
        """
        if not self.screen_manager.has_screen('config_filesaver'):
            self.screen_manager.add_widget(
                screen_config_filesaver.ConfigFileSaver(name='config_filesaver',
                                                        screen_manager=self.screen_manager,
                                                        localization=self.localization,
                                                        callback=self.__handle_filesaver_callback,
                                                        keyboard=self.keyboard))
        self.screen_manager.current = 'config_filesaver'

    def handle_run_pressed(self):
        """
        Called when the run button is pressed.
        :return: None
        """
        self.model.engine.engine_run()

    def get_screen(self):
        """
        Returns the view/screen of the controller.
        :return: None
        """
        return self.view
