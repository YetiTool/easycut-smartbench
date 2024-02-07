import os

from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from asmcnc.apps.drywall_cutter_app.dwt_app_widgets import ImageButton, DryWallImageDropDownButton
from asmcnc.apps.drywall_cutter_app.widget_drywall_shape_display import (
    DrywallShapeDisplay,
)
from asmcnc.apps.drywall_cutter_app.widget_xy_move_drywall import XYMoveDrywall

IMG_DIR = os.path.join(os.path.dirname(__file__), "img")


class DrywallCutterView(Screen):
    """
    The view for the Drywall Cutter screen.
    """

    def __init__(self, controller, **kwargs):
        super(DrywallCutterView, self).__init__(**kwargs)

        self.controller = controller

        self.build_ui()

    """
    Screen Widgets
    
    Organised by type of widget. Added # parent: <parent> to show the parent widget.
    """
    root = ObjectProperty()  # type: BoxLayout  # parent: self
    header = ObjectProperty()  # type: BoxLayout  # parent: root
    body = ObjectProperty()  # type: BoxLayout  # parent: root
    shape_display_container = ObjectProperty()  # type: BoxLayout  # parent: body
    action_pane_container = ObjectProperty()  # type: BoxLayout  # parent: body
    xy_move_container = ObjectProperty()  # type: BoxLayout  # parent: action_pane_container
    button_container = ObjectProperty()  # type: BoxLayout  # parent: action_pane_container

    home_button = ObjectProperty()  # type: ImageButton  # parent: header
    load_filechooser_button = ObjectProperty()  # type: ImageButton  # parent: header
    rotate_button = ObjectProperty()  # type: ImageButton  # parent: header
    material_setup_button = ObjectProperty()  # type: ImageButton  # parent: header
    stop_button = ObjectProperty()  # type: ImageButton  # parent: header
    exit_button = ObjectProperty()  # type: ImageButton  # parent: header
    simulate_button = ObjectProperty()  # type: ImageButton  # parent: header
    save_button = ObjectProperty()  # type: ImageButton  # parent: header
    run_button = ObjectProperty()  # type: ImageButton  # parent: header

    cutter_drop_down = ObjectProperty()  # type: DryWallImageDropDownButton  # parent: header
    shape_drop_down = ObjectProperty()  # type: DryWallImageDropDownButton  # parent: header
    toolpath_offset_drop_down = ObjectProperty()  # type: DryWallImageDropDownButton  # parent: header

    shape_display_widget = ObjectProperty()  # type: DrywallShapeDisplay  # parent: shape_display_container
    xy_move_widget = ObjectProperty()  # type: XYMoveDrywall  # parent: xy_move_container

    """
    Screen Building Properties
    """
    BUTTON_SIZE_HINT_X = 7

    """
    Screen Building Methods
    """

    def build_ui(self):
        """
        Builds the UI for the screen.
        :return: None
        """
        self.build_root()
        self.build_header()
        self.build_body()
        self.build_shape_display()
        self.build_action_pane()

    def build_root(self):
        """
        Builds the root layout of the screen.
        :return: None
        """
        self.root = BoxLayout(orientation="vertical")
        self.add_widget(self.root)

    def build_header(self):
        """
        Builds the header of the screen.
        :return: None
        """
        self.header = BoxLayout(orientation="horizontal", padding=dp(5), spacing=dp(10))

        self.home_button = ImageButton(
            source=os.path.join(IMG_DIR, "home_button.png"),
            size_hint_x=self.BUTTON_SIZE_HINT_X,
            allow_stretch=True,
            on_press=self.on_home_button_pressed,
        )
        self.header.add_widget(self.home_button)

        self.load_filechooser_button = ImageButton(
            source=os.path.join(IMG_DIR, "open_button.png"),
            size_hint_x=self.BUTTON_SIZE_HINT_X,
            allow_stretch=True,
            on_press=self.on_load_filechooser_button_pressed,
        )
        self.header.add_widget(self.load_filechooser_button)

        self.cutter_drop_down = DryWallImageDropDownButton(
            name_and_image_dict=self.controller.model.config.cutter_options,
            callback=self.on_cutter_selected,
            size_hint_x=self.BUTTON_SIZE_HINT_X,
            allow_stretch=True,
        )
        self.header.add_widget(self.cutter_drop_down)

        self.shape_drop_down = DryWallImageDropDownButton(
            name_and_image_dict=self.controller.model.config.shape_options,
            callback=self.on_shape_selected,
            size_hint_x=self.BUTTON_SIZE_HINT_X,
            allow_stretch=True,
        )
        self.header.add_widget(self.shape_drop_down)

        self.rotate_button = ImageButton(
            source=os.path.join(IMG_DIR, "rotate_button.png"),
            size_hint_x=self.BUTTON_SIZE_HINT_X,
            allow_stretch=True,
            on_press=self.on_rotate_button_pressed,
        )
        self.header.add_widget(self.rotate_button)

        self.toolpath_offset_drop_down = DryWallImageDropDownButton(
            name_and_image_dict=self.controller.model.config.get_toolpath_offset_options(),
            callback=self.on_toolpath_selected,
            size_hint_x=self.BUTTON_SIZE_HINT_X,
            allow_stretch=True,
        )
        self.header.add_widget(self.toolpath_offset_drop_down)

        material_setup_button = ImageButton(
            source=os.path.join(IMG_DIR, "cutting_depths_button.png"),
            size_hint_x=self.BUTTON_SIZE_HINT_X,
            allow_stretch=True,
            on_press=self.on_material_setup_button_pressed,
        )
        self.header.add_widget(material_setup_button)

        self.stop_button = ImageButton(
            source=os.path.join(IMG_DIR, "stop_button.png"),
            size_hint_x=15,
            allow_stretch=True,
            on_press=self.on_stop_button_pressed,
        )
        self.header.add_widget(self.stop_button)

        self.exit_button = ImageButton(
            source=os.path.join(IMG_DIR, "exit_button.png"),
            size_hint_x=self.BUTTON_SIZE_HINT_X,
            allow_stretch=True,
            on_press=self.on_exit_button_pressed,
        )
        self.header.add_widget(self.exit_button)

        self.root.add_widget(self.header)

    def build_body(self):
        """
        Builds the body of the screen.
        :return: None
        """
        self.body = BoxLayout(
            orientation="horizontal", padding=dp(5), spacing=dp(10), size_hint_y=5
        )
        self.root.add_widget(self.body)

    def build_shape_display(self):
        """
        Builds the shape display widget.
        :return: None
        """
        self.shape_display_container = BoxLayout(orientation="vertical", size_hint_x=55)

        self.shape_display_widget = DrywallShapeDisplay(
            machine=self.controller.router_machine, screen_manager=self.controller.screen_manager,
            dwt_config=self.controller.model.config, engine=self.controller.model.engine
        )
        self.shape_display_container.add_widget(self.shape_display_widget)

        self.body.add_widget(self.shape_display_container)

    def build_action_pane(self):
        """
        Builds the action widget.
        :return: None
        """
        self.action_pane_container = BoxLayout(
            orientation="vertical", size_hint_x=23, spacing=dp(10)
        )

        self.xy_move_container = BoxLayout(
            orientation="horizontal", size_hint_y=31, padding=(dp(0), dp(30))
        )

        with self.xy_move_container.canvas.before:
            Color(229.0 / 255, 229.0 / 255, 1, 1)
            Rectangle(pos=self.xy_move_container.pos, size=self.xy_move_container.size)

        self.xy_move_widget = XYMoveDrywall(machine=self.controller.router_machine,
                                            screen_manager=self.controller.screen_manager)

        self.xy_move_container.add_widget(self.xy_move_widget)

        self.action_pane_container.add_widget(self.xy_move_container)

        self.button_container = BoxLayout(
            orientation="horizontal", size_hint_y=7, spacing=dp(10)
        )

        self.simulate_button = ImageButton(
            source=os.path.join(IMG_DIR, "simulate_button.png"),
            allow_stretch=True,
            on_press=self.on_simulate_button_pressed,
        )
        self.button_container.add_widget(self.simulate_button)

        self.save_button = ImageButton(
            source=os.path.join(IMG_DIR, "save_button.png"),
            allow_stretch=True,
            on_press=self.on_save_button_pressed,
        )
        self.button_container.add_widget(self.save_button)

        self.run_button = ImageButton(
            source=os.path.join(IMG_DIR, "start_job_button.png"),
            allow_stretch=True,
            on_press=self.on_run_button_pressed,
        )

        self.body.add_widget(self.action_pane_container)

    """
    Event Handlers
    
    These methods are called when the user interacts with the screen.
    """

    def on_leave(self, *args):
        """
        Called when the screen is left.
        :return: None
        """
        self.controller.handle_on_leave()

    def on_home_button_pressed(self, *args):
        """
        Called when the home button is pressed.
        :return: None
        """
        self.controller.handle_home_button_pressed()

    def on_cutter_selected(self, cutter, *args):
        """
        Called when a cutter is selected from the dropdown.
        :param cutter: The select cutter file name
        :return: None
        """
        self.controller.set_cutter(cutter)

    def on_shape_selected(self, shape, *args):
        """
        Called when a shape is selected from the dropdown.
        :param shape: The selected shape
        :return: None
        """
        self.controller.set_shape(shape)

    def on_toolpath_selected(self, toolpath_offset, *args):
        """
        Called when a toolpath offset is selected from the dropdown.
        :param toolpath_offset: The selected toolpath offset
        :return: None
        """
        self.controller.set_toolpath_offset(toolpath_offset)

    def on_rotate_button_pressed(self, *args):
        """
        Called when the rotate button is pressed.
        :return: None
        """
        self.controller.handle_rotate_button_pressed()

    def on_exit_button_pressed(self, *args):
        """
        Called when the exit button is pressed.
        :return: None
        """
        self.controller.handle_exit_button_pressed()

    def on_stop_button_pressed(self, *args):
        """
        Called when the stop button is pressed.
        :return: None
        """
        self.controller.handle_stop_button_pressed()

    def on_load_filechooser_button_pressed(self, *args):
        """
        Called when the load filechooser button is pressed.
        :return: None
        """
        self.controller.handle_load_filechooser_pressed()

    def on_material_setup_button_pressed(self, *args):
        """
        Called when the material setup button is pressed.
        :return: None
        """
        self.controller.handle_material_setup_pressed()

    def on_simulate_button_pressed(self, *args):
        """
        Called when the simulate button is pressed.
        :return: None
        """
        self.controller.handle_simulate_pressed()

    def on_save_button_pressed(self, *args):
        """
        Called when the save button is pressed.
        :return: None
        """
        self.controller.handle_save_pressed()

    def on_run_button_pressed(self, *args):
        """
        Called when the run button is pressed.
        :return: None
        """
        self.controller.handle_run_pressed()

    """
    UI Methods
    
    These methods are called to update the UI.
    """

    def set_cutter_image(self, image_path):
        """
        Sets the cutter image to the given image path.
        :param image_path: The image path
        :return: None
        """
        self.cutter_drop_down.source = image_path

    def set_toolpath_offset_image(self, image_path):
        """
        Sets the toolpath offset image to the given image path.
        :param image_path: The image path
        :return: None
        """
        self.toolpath_offset_drop_down.source = image_path

    def set_rotate_button_disabled(self, disabled):
        """
        Sets the rotation button to disabled or not.
        :param disabled: True if the button should be disabled, False otherwise
        :return: None
        """
        self.rotate_button.disabled = disabled

