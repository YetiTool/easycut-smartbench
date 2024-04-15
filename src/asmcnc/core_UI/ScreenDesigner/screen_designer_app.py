import os
import re

from kivy.app import App
from kivy.config import Config
from kivy.graphics import Color, Line
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

from asmcnc.comms.localization import Localization
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.core_UI.ScreenDesigner.component_selector_widget import ComponentSelectorWidget
from asmcnc.core_UI.components.buttons.button_base import ButtonBase
from asmcnc.core_UI.hoverable import InspectorSingleton
import asmcnc.core_UI.path_utils as pu


class DesignerMainScreen(Screen):
    """
    Start screen of the designer. Offers a dropdown with existing screens.

    Load screen:
    Click the screen name in the dropdown and be patient. Your screen will be ready for you soon!

    Create new screen:
    Enter the desired screen name in the text_input and click "New screen...".
    !!! The screen name has to be CamelCase !!!
    """
    def __init__(self, **kwargs):
        super(DesignerMainScreen, self).__init__(name='ScreenDesigner', **kwargs)

        self.sm = App.get_running_app().sm
        self.available_screens = {}
        self.main_layout = FloatLayout()
        self.add_widget(self.main_layout)
        # background image
        self.test_btn = ButtonBase(size=(5, 5), size_hint=(None, None), pos=(368, 40), id='DESIGNER')
        self.background_image = Image(source=pu.get_path('Inspector_Widget_old.png'), text='.')
        self.test_btn.bind(on_release=lambda i: setattr(self.background_image,"source",self.background_image.source.replace('_old.', '.')))
        self.test_btn.opacity = 0
        self.main_layout.add_widget(self.background_image)
        self.main_layout.add_widget(self.test_btn)
        # Add new_screen button:
        self.btn_new_screen = ButtonBase(size=(100, 50), size_hint=(None, None), pos=(690, 10), text='New screen...', id='DESIGNER')
        self.btn_new_screen.bind(on_release=self.new_screen)
        self.main_layout.add_widget(self.btn_new_screen)
        # text input for screen name:
        self.screen_name_input = TextInput(size=(200, 30), size_hint=(None, None), pos=(480, 15), text='ScreenName1')
        self.main_layout.add_widget(self.screen_name_input)
        # screen dropdown:
        self.screen_drop_down_btn = ButtonBase(size=(200, 50), size_hint=(None, None), pos=(10, 10), text='Select screen...', id='DESIGNER')
        self.screen_drop_down = DropDown(size=(200, 200), size_hint=(None, None))
        self.main_layout.add_widget(self.screen_drop_down_btn)
        self.screen_drop_down_btn.bind(on_release=self.screen_drop_down.open)
        self.screen_drop_down.bind(on_select=self.open_screen)


    def on_enter(self, *args):
        # disable Inspector to not mess with key inputs while entering filename
        InspectorSingleton().disable_key_input()
        # reload generated screens, in case one was just created.
        self.load_generated_screens()
        App.get_running_app().title = "Inspector Widget"

    def on_leave(self, *args):
        InspectorSingleton().enable_key_input()

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
            class_name = ScreenDesignerApp.screenname_to_filename(prepped_filename, True)
            import_path = path.replace('/', '.').split('src')[1][1:] + '.' + prepped_filename
            if screen_file.startswith('__init__') or screen_file.endswith('.pyc'):
                continue
            # fill dropdown with class names
            btn = ButtonBase(text=class_name, size_hint_y=None, height=40, id='DESIGNER')
            btn.bind(on_release=lambda btn: self.screen_drop_down.select(btn.text))
            self.screen_drop_down.add_widget(btn)
            # saves class names (=screen names) and import path for later
            self.available_screens[class_name] = import_path

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

    def open_screen(self, instance, screen_name):
        """
        Creates an instance of the given screen_name assuming that screen_name = class_name.
        Shows the selected screen
        """
        screen = self.create_screen(screen_name)
        if screen:
            App.get_running_app().modifying_screen = True
            App.get_running_app().current_screen_name = screen_name
            layout = screen.children[0]
            screen.remove_widget(layout)
            self.build_designer_screen(layout)

    def new_screen(self, *args):
        screen_layout = FloatLayout(id='screen_layout', size_hint=[None, None], size=[800, 480])
        App.get_running_app().current_screen_name = self.screen_name_input.text
        App.get_running_app().modifying_screen = False
        self.build_designer_screen(screen_layout)

    def build_designer_screen(self, layout, *args):
        """
        Creates a new empty screen from scratch.
        """
        if self.sm.has_screen(App.get_running_app().current_screen_name):
            self.sm.remove_widget(self.sm.get_screen(App.get_running_app().current_screen_name))
        new_screen = Screen(name=App.get_running_app().current_screen_name)
        main_layout = FloatLayout(id='main_layout')
        main_layout.add_widget(layout)
        with layout.canvas.before:
            Color(1, 1, 1)
            Line(rectangle=(0, 0, layout.width, layout.height))
        component_widget = ComponentSelectorWidget()
        component_widget.widget_to_add_to = layout
        main_layout.add_widget(component_widget)
        new_screen.add_widget(main_layout)
        self.sm.add_widget(new_screen)
        App.get_running_app().title = "Inspector Widget - " + App.get_running_app().current_screen_name
        App.get_running_app().update_widget(main_layout)

        self.sm.current = new_screen.name


class ScreenDesignerApp(App):
    """
    This app can be used to develop screens. You can either edit existing screens or create a new screen from scratch.

    To add new widgets to screens, press [w]. press [h] for help.
    """

    width = Window.width
    height = Window.height if Window.height == 480 else Window.height - 32
    current_screen_name = ''

    def __init__(self, **kwargs):
        super(ScreenDesignerApp, self).__init__(**kwargs)

        self.l = Localization()
        self.sm = ScreenManager(transition=NoTransition())
        self.inspector = InspectorSingleton()
        self.inspector.enable()
        self.modifying_screen = False
        self.icon = pu.get_path('inspection.png')

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

    def update_widget(self, widget):
        """
        Updates the widget in the designer popup and in the inspector, so it will be the new
        parent for inserted widgets and the inspector can move it around.
        """
        self.inspector.set_widget(widget)



    def build(self):
        main_screen = DesignerMainScreen()

        self.sm.add_widget(main_screen)
        self.title = "Inspector Widget"
        return self.sm


if __name__ == '__main__':
    try:
        Config.set('graphics', 'width', '1200')
        Config.set('graphics', 'height', '720')
        Config.write()

        ScreenDesignerApp().run()
    except Exception as e:
        Logger.exception(e)
