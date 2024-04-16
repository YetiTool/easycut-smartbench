import os
import re

from kivy.app import App
from kivy.graphics import Color, Line, InstructionGroup
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.core_UI import path_utils as pu
from asmcnc.core_UI.ScreenDesigner.component_selector_widget import ComponentSelectorWidget
from asmcnc.core_UI.components.buttons.button_base import ButtonBase
from asmcnc.core_UI.components.text_inputs.base_text_input import TextInputBase
from asmcnc.core_UI.hoverable import InspectorSingleton
import asmcnc.core_UI.ScreenDesigner.string_builder as sb

GENERATED_SCREENS_FOLDER = pu.get_path('generated_code/screens')
GENERATED_WIDGETS_FOLDER = pu.get_path('generated_code/widgets')


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
        self.inspector.bind(on_new_widget_to_add_to=lambda *args: self.set_widget_to_add_to(args[1]))
        self.widget_to_add_to = None
        self.widget_to_add_to_rectangle = None

        self.screen_manager = App.get_running_app().sm
        # create designer screen
        self.component_widget = None
        self.screen_drop_down = None
        self.screen_name_input = None
        self.text_text_input = None
        self.widget_size_input = None
        self.widgets_drop_down = None
        self.designer_screen = None

        # data needed for code generation:
        self.base_class = 'Screen'
        self.available_screens = {}
        self.available_widgets = {}
        self.modifying_screen = False
        self.current_class_name = ''
        self.current_screen_layout = None

    def load_generated_screens(self, *args):
        """
        Walks through all files in ScreenDesigner/generated_code/screens and populates the dropdown with the
        screens names.
        Saves a dict with the screen name and its import path for later use.
        Assumes that screen name == class name. The import path ("asmcnc.core_UI.screen_designer")
        derives from the file path.
        """
        children = [c for c in self.screen_drop_down.children[0].children]
        for c in children:
            self.screen_drop_down.remove_widget(c)
        path = GENERATED_SCREENS_FOLDER
        for screen_file in os.listdir(path):
            prepped_filename = screen_file.replace('.py', '')
            class_name = self.classname_to_filename(prepped_filename, True)
            import_path = path.replace('/', '.').split('src')[1][1:] + '.' + prepped_filename
            if screen_file.startswith('__init__') or screen_file.endswith('.pyc'):
                continue
            # fill dropdown with class names
            btn = ButtonBase(text=class_name, size_hint_y=None, height=40, id='DESIGNER')
            btn.bind(on_release=lambda btn: self.screen_drop_down.select(btn.text))
            self.screen_drop_down.add_widget(btn)
            # saves class names (=screen names) and import path for later
            self.available_screens[class_name] = import_path

    def load_generated_widgets(self, *args):
        """
        Walks through all files in ScreenDesigner/generated_code/widgets and populates the dropdown with the
        screens names.
        Saves a dict with the screen name and its import path for later use.
        Assumes that screen name == class name. The import path ("asmcnc.core_UI.screen_designer")
        derives from the file path.
        """
        children = [c for c in self.widgets_drop_down.children[0].children]
        for c in children:
            self.widgets_drop_down.remove_widget(c)
        path = GENERATED_WIDGETS_FOLDER
        for widget_file in os.listdir(path):
            if widget_file.startswith('__init__') or widget_file.endswith('.pyc'):
                continue
            prepped_filename = widget_file.replace('.py', '')
            class_name = self.classname_to_filename(prepped_filename, True)
            import_path = path.replace('/', '.').split('src')[1][1:] + '.' + prepped_filename
            # fill dropdown with class names
            btn = ButtonBase(text=class_name, size_hint_y=None, height=40, id='DESIGNER')
            btn.bind(on_release=lambda btn: self.widgets_drop_down.select(btn.text))
            self.widgets_drop_down.add_widget(btn)
            # saves class names (=screen names) and import path for later
            self.available_widgets[class_name] = import_path


    def classname_to_filename(self, name_to_convert, reverse=False):
        # type: (str, bool) -> str
        """
        reverse = False:
            takes a screen name (e.g. MyFirstScreen) and returns the filename (screen_my_first)

        reverse = True:
            takes a filename (e.g. screen_my_first) and return a screen name (MyFirstScreen)
        """
        if reverse:
            # snake_case to CamelCase:
            tmp = re.sub(r'_([a-z0-9])', lambda pat: pat.group(1).upper(), '_' + name_to_convert)
            # move 'Screen' to the back:
            return re.sub(r'({})([A-Za-z0-9]*)'.format(self.base_class), lambda pat: pat.group(2) + pat.group(1) , tmp)
        else:
            # CamelCase to snake_case:
            tmp = re.sub(r'([A-Z0-9])', lambda pat: '_' + pat.group(1).lower(), name_to_convert)[1:]
            # move 'screen' to the front:
            return re.sub(r'([a-z0-9_]*)_({})'.format(self.base_class.lower()), lambda pat: pat.group(2) + '_' + pat.group(1), tmp)

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
            Logger.exception('Could not create class: {}'.format(screen_name))
            return None

    def create_widget(self, widget_name):
        """
        Creates a new instance of the selected widget. Imports the corresponding module first.
        """
        try:
            test = __import__(name=self.available_widgets[widget_name], fromlist=[widget_name])
            reload(test)
            widget_class = getattr(test, widget_name)
            widget = widget_class()
            return widget
        except ImportError as ex:
            Logger.exception('Could not create widget: {}'.format(widget_name))
            return None

    def new_screen(self, *args):
        """Load a new screen."""
        screen_name = self.screen_name_input.text
        screen_layout = FloatLayout(id='screen_layout', size_hint=[None, None], size=[800, 480], pos=[0, 0])
        self.modifying_screen = False
        self.base_class = 'Screen'
        self.current_class_name = screen_name
        self.add_editing_object_to_designer(screen_layout)
        App.get_running_app().title = "Inspector Widget - " + screen_name

    def new_widget(self, *args):
        """Load a new widget."""
        widget_name = self.screen_name_input.text
        widget_layout = FloatLayout(id='widget_layout', size_hint=[None, None], pos=[0, 0])
        try:
            m = re.match(r'([\d.]+),\s*([\d.]+)', self.widget_size_input.text)
            widget_layout.size=[m.group(1), m.group(2)]
        except AttributeError, ValueError:
            Logger.exception('widget_size_input.text could not be converted in size. Expected format: [123, 456]')
            return

        self.modifying_screen = False
        self.base_class = 'Widget'
        self.current_class_name = widget_name
        self.add_editing_object_to_designer(widget_layout)
        App.get_running_app().title = "Inspector Widget - " + widget_name

    def open_screen(self, instance, screen_name):
        """
        Creates an instance of the given screen_name assuming that screen_name = class_name.
        Shows the selected screen
        """
        screen = self.create_screen(screen_name)
        if screen:
            self.modifying_screen = True
            self.base_class = 'Screen'
            self.current_class_name = screen_name
            layout = screen.children[0]
            screen.remove_widget(layout)
            self.add_editing_object_to_designer(layout)

    def open_widget(self, instance, widget_name):
        """
        Creates an instance of the given widget_name assuming that widget_name = class_name.
        Shows the selected widget
        """
        widget = self.create_widget(widget_name)
        if widget:
            self.modifying_screen = True
            self.base_class = 'Widget'
            self.current_class_name = widget_name
            layout = widget.children[0]
            widget.remove_widget(layout)
            self.add_editing_object_to_designer(layout)

    def add_editing_object_to_designer(self, layout):
        """
        Adds the given layout to the designer screen.

        Layout can be the main layout of a screen or a widget.

        A rectangle line is drawn to mark the outline of the
        """
        # remove layout from previous loaded screen or widget
        if self.current_screen_layout:
            self.designer_screen.children[0].remove_widget(self.current_screen_layout)
        self.designer_screen.children[0].add_widget(layout)
        self.current_screen_layout = layout
        with layout.canvas.before:
            Color(0.2, 1, 0.2)
            Line(rectangle=(0, 0, layout.width, layout.height))
        self.set_widget_to_add_to(layout)

    def text_input_focus(self, instance, state):
        """
        Is called when the screen name text_input gains or loses focus, to disable inspector key inputs while typing.
        """
        if state:
            InspectorSingleton().disable_key_input()
        else:
            InspectorSingleton().enable_key_input()

    def build_designer_screen(self):
        """Creates the main designer screen and fills it with widgets."""
        self.designer_screen = Screen(name='DesignerScreen')
        self.component_widget = ComponentSelectorWidget(self)
        main_layout = FloatLayout(size_hint=[1, 1], id='MainLayout')

        main_layout.add_widget(self.component_widget)
        self.designer_screen.add_widget(main_layout)

        # Add new_screen button:
        btn_new_screen = ButtonBase(size=(100, 50), size_hint=(None, None), pos=(420, 650), text='New screen...', id='DESIGNER')
        btn_new_screen.bind(on_release=self.new_screen)
        main_layout.add_widget(btn_new_screen)
        # text input for screen name:
        self.screen_name_input = TextInputBase(size=(200, 30), size_hint=(None, None), pos=(210, 650), text='ScreenName1', id='DESIGNER')
        self.screen_name_input.bind(focus=self.text_input_focus)
        main_layout.add_widget(self.screen_name_input)
        # Add new_widget button:
        btn_new_widget = ButtonBase(size=(100, 50), size_hint=(None, None), pos=(420, 600), text='New widget...', id='DESIGNER')
        btn_new_widget.bind(on_release=self.new_widget)
        main_layout.add_widget(btn_new_widget)
        # text input for widget size:
        self.widget_size_input = TextInputBase(size=(200, 30), size_hint=(None, None), pos=(210, 600), text='[100, 100]', id='DESIGNER')
        self.widget_size_input.bind(focus=self.text_input_focus)
        main_layout.add_widget(self.widget_size_input)
        # screen dropdown:
        screen_drop_down_btn = ButtonBase(size=(200, 50), size_hint=(None, None), pos=(10, 650), text='Load screen...', id='DESIGNER')
        self.screen_drop_down = DropDown(size=(200, 200), size_hint=(None, None))
        main_layout.add_widget(screen_drop_down_btn)
        screen_drop_down_btn.bind(on_release=self.screen_drop_down.open)
        self.screen_drop_down.bind(on_select=self.open_screen)
        # widgets dropdown:
        widgets_drop_down_btn = ButtonBase(size=(200, 50), size_hint=(None, None), pos=(10, 600), text='Load widget...', id='DESIGNER')
        self.widgets_drop_down = DropDown(size=(200, 200), size_hint=(None, None))
        main_layout.add_widget(widgets_drop_down_btn)
        widgets_drop_down_btn.bind(on_release=self.widgets_drop_down.open)
        self.widgets_drop_down.bind(on_select=self.open_widget)
        # text text_input
        self.text_text_input = TextInputBase(size=(200, 30), size_hint=(None, None), pos=(810, 250), text='text to show', id='DESIGNER')
        self.text_text_input.bind(focus=self.text_input_focus)
        main_layout.add_widget(self.text_text_input)

        self.screen_manager.add_widget(self.designer_screen)

        # draw grey boundary box:
        with main_layout.canvas.before:
            Color(1, 1, 1)
            Line(rectangle=(0, 0, 800, 480))

        self.load_generated_screens()
        self.load_generated_widgets()
        self.screen_manager.current = self.designer_screen.name

    def save_to_file(self):
        """
        Takes generated python code from the StringBuilder and saves it to a file.
        The filename is converted from CamelCase to snake_case.
        """
        # e.g. turn "MyFirstScreen" into "my_first_screen":
        filename = self.classname_to_filename(self.current_class_name)
        s = sb.get_python_code_from_screen(self.widget_to_add_to, self.modifying_screen, self.current_class_name, filename, self.base_class)
        if self.base_class == 'Screen':
            path = pu.join(GENERATED_SCREENS_FOLDER, filename + '.py')
        else:
            path = pu.join(GENERATED_WIDGETS_FOLDER, filename + '.py')
        with open(path, 'w') as f:
            f.write(s)

    def get_widget_to_add_to(self):
        """Getter for widget_to_add_to (which is the widget that new elements will be added to.)"""
        return self.widget_to_add_to

    def set_widget_to_add_to(self, widget):
        """
        Getter for widget_to_add_to (which is the widget that new elements will be added to.)

        removes the old green rectangle and paints a new one.
        """
        self.remove_widget_to_add_to_rectangle()
        self.widget_to_add_to = widget
        self.paint_widget_to_add_to_rectangle()

    def paint_widget_to_add_to_rectangle(self):
        """
        Paints the red selection rectangle on the selected widget.

        Removes old one if left over."""
        if self.widget_to_add_to and self.widget_to_add_to_rectangle:
            self.widget_to_add_to.canvas.remove(self.widget_to_add_to_rectangle)
        self.widget_to_add_to_rectangle = InstructionGroup()
        self.widget_to_add_to_rectangle.add(Color(0.2, 1, 0.2))
        self.widget_to_add_to_rectangle.add(Line(rectangle=(self.widget_to_add_to.x,
                                                            self.widget_to_add_to.y,
                                                            self.widget_to_add_to.width,
                                                            self.widget_to_add_to.height)))
        self.widget_to_add_to.canvas.add(self.widget_to_add_to_rectangle)

    def remove_widget_to_add_to_rectangle(self):
        """Removes the last painted red selection rectangle."""
        if self.widget_to_add_to and self.widget_to_add_to_rectangle:
            self.widget_to_add_to.canvas.remove(self.widget_to_add_to_rectangle)
