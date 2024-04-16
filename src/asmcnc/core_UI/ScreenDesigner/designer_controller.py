import os
import re

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Line
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.core_UI import path_utils as pu
from asmcnc.core_UI.ScreenDesigner.component_selector_widget import ComponentSelectorWidget
from asmcnc.core_UI.components.buttons.button_base import ButtonBase
from asmcnc.core_UI.hoverable import InspectorSingleton


class DesignerController(object):
    """
    This class provides the main functionality for the screen designer:
    - handling widget manipulation
    - creating the main screen
    - handling interaction between widgets
    """
    def __init__(self):
        self.inspector = InspectorSingleton()
        self.inspector.enable()

        # create designer screen
        self.screen_manager = App.get_running_app().sm
        self.component_widget = None
        self.screen_drop_down = None
        self.screen_name_input = None

        self.designer_screen = None

        self.available_screens = {}
        self.modifying_screen = False
        self.current_screen_name = ''
        self.current_screen_layout = None

    def load_generated_screens(self, *args):
        """
        Walks through all files in ScreenDesigner/generated_screens and populates the dropdown with the
        screens names.
        Saves a dict with the screen name and its import path for later use.
        Assumes that screen name == class name. The import path ("asmcnc.core_UI.screen_designer")
        derives from the file path.
        """
        children = [c for c in self.screen_drop_down.children[0].children]
        for c in children:
            self.screen_drop_down.remove_widget(c)
        path = pu.get_path('generated_screens')
        for screen_file in os.listdir(path):
            prepped_filename = screen_file.replace('.py', '')
            class_name = self.screenname_to_filename(prepped_filename, True)
            import_path = path.replace('/', '.').split('src')[1][1:] + '.' + prepped_filename
            if screen_file.startswith('__init__') or screen_file.endswith('.pyc'):
                continue
            # fill dropdown with class names
            btn = ButtonBase(text=class_name, size_hint_y=None, height=40, id='DESIGNER')
            btn.bind(on_release=lambda btn: self.screen_drop_down.select(btn.text))
            self.screen_drop_down.add_widget(btn)
            # saves class names (=screen names) and import path for later
            self.available_screens[class_name] = import_path


    @staticmethod
    def screenname_to_filename(name_to_convert, reverse=False):
        # type: (str, bool) -> str
        """
        reverse = False:
            takes a screen name (e.g. MyFirstScreen) and returns the filename (my_first_screen)

        reverse = True:
            takes a filename (e.g. my_first_screen) and return a screen name (MyFirstScreen)
        """
        if reverse:
            return re.sub(r'_([a-z])', lambda pat: pat.group(1).upper(), '_' + name_to_convert)
        else:
            return re.sub(r'([A-Z])', lambda pat: '_' + pat.group(1).lower(), name_to_convert)[1:]

    def create_screen(self, screen_name):
        """
        Creates a new instance of the selected screen. Imports the corresponding module first.
        """
        try:
            test = __import__(name=self.available_screens[screen_name], fromlist=[screen_name])
            reload(test)
            screen_class = getattr(test, screen_name)
            screen = screen_class()
            return screen
        except ImportError as ex:
            Logger.exception(ex)
            return None

    def new_screen(self, *args):
        """Load a new screen."""
        screen_name = self.screen_name_input.text
        screen_layout = FloatLayout(id='screen_layout', size_hint=[None, None], size=[800, 480])
        self.modifying_screen = False
        self.current_screen_name = screen_name
        self.add_editing_object_to_designer(screen_layout)
        App.get_running_app().title = "Inspector Widget - " + screen_name

    def open_screen(self, instance, screen_name):
        """
        Creates an instance of the given screen_name assuming that screen_name = class_name.
        Shows the selected screen
        """
        screen = self.create_screen(screen_name)
        if screen:
            self.modifying_screen = True
            self.current_screen_name = screen_name
            layout = screen.children[0]
            screen.remove_widget(layout)
            self.add_editing_object_to_designer(layout)


    def add_editing_object_to_designer(self, layout):
        """
        Adds the given layout to the designer screen.

        Layout can be the main layout of a screen or a widget.

        A rectangle line is drawn to mark the outline of the
        """
        if self.current_screen_layout:
            self.designer_screen.children[0].remove_widget(self.current_screen_layout)
        self.designer_screen.children[0].add_widget(layout)
        self.current_screen_layout = layout
        with layout.canvas.before:
            Color(1, 1, 1)
            Line(rectangle=(0, 0, layout.width, layout.height))
        self.component_widget.widget_to_add_to = layout

    def screen_name_input_focus(self, instance, state):
        if state:
            InspectorSingleton().disable_key_input()
        else:
            InspectorSingleton().enable_key_input()

    def build_designer_screen(self):
        """Creates the main designer screen and fills it with widgets."""
        self.designer_screen = Screen(name='DesignerScreen')
        self.component_widget = ComponentSelectorWidget()
        main_layout = FloatLayout(size_hint=[1, 1], id='MainLayout')

        main_layout.add_widget(self.component_widget)
        self.designer_screen.add_widget(main_layout)

        # Add new_screen button:
        btn_new_screen = ButtonBase(size=(100, 50), size_hint=(None, None), pos=(220, 650), text='New screen...', id='DESIGNER')
        btn_new_screen.bind(on_release=self.new_screen)
        main_layout.add_widget(btn_new_screen)
        # text input for screen name:
        self.screen_name_input = TextInput(size=(200, 30), size_hint=(None, None), pos=(10, 650), text='ScreenName1')
        self.screen_name_input.bind(focus=self.screen_name_input_focus)
        main_layout.add_widget(self.screen_name_input)
        # screen dropdown:
        screen_drop_down_btn = ButtonBase(size=(200, 50), size_hint=(None, None), pos=(10, 600), text='Select screen...', id='DESIGNER')
        self.screen_drop_down = DropDown(size=(200, 200), size_hint=(None, None))
        main_layout.add_widget(screen_drop_down_btn)
        screen_drop_down_btn.bind(on_release=self.screen_drop_down.open)
        self.screen_drop_down.bind(on_select=self.open_screen)

        self.screen_manager.add_widget(self.designer_screen)

        self.load_generated_screens()
        self.screen_manager.current = self.designer_screen.name
