import inspect
import os
import re

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

from asmcnc.comms.localization import Localization
from asmcnc.core_UI.ScreenDesigner.add_widget_popup import AddWidgetPopup
from asmcnc.core_UI.components.base_label import LabelBase
from asmcnc.core_UI.components.buttons.button_base import ButtonBase
from asmcnc.core_UI.hoverable import InspectorSingleton
import asmcnc.core_UI.path_utils as pu


class DesignerMainScreen(Screen):
    def __init__(self, **kwargs):
        super(DesignerMainScreen, self).__init__(name='ScreenDesigner', **kwargs)

        self.sm = App.get_running_app().sm
        self.last_screen_name = 'MyScreen'
        self.main_layout = FloatLayout()
        self.add_widget(self.main_layout)
        # Add new_screen button:
        self.btn_new_screen = ButtonBase(size=(100, 50), size_hint=(None, None), pos=(self.x + 210, App.get_running_app().height - self.height - 5), text='New screen...')
        self.btn_new_screen.bind(on_press=self.create_new_screen)
        self.main_layout.add_widget(self.btn_new_screen)
        # text input for screen name:
        self.screen_name_input = TextInput(size=(200, 30), size_hint=(None, None), pos=(self.x + 5, App.get_running_app().height - self.height + 5), text='ScreenName1')
        self.main_layout.add_widget(self.screen_name_input)
        # screen dropdown:
        self.screen_drop_down_btn = ButtonBase(size=(200, 50), size_hint=(None, None), pos=(self.x + 5, App.get_running_app().height - self.height - 100), text='Select screen...')
        self.screen_drop_down = DropDown(size=(200, 200), size_hint=(None, None))
        self.main_layout.add_widget(self.screen_drop_down_btn)
        self.screen_drop_down_btn.bind(on_release=self.screen_drop_down.open)
        self.screen_drop_down_btn.bind(on_text=lambda instance, text: setattr(self, 'last_screen_name', text))
        self.screen_drop_down.bind(on_select=self.open_screen)
        # Add load_screen button:
        # self.btn_load_screen = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 600, App.get_running_app().height - self.height - 5), text='Load...')
        # self.btn_load_screen.bind(on_press=self.load_screen)
        # self.main_layout.add_widget(self.btn_load_screen)

    def on_enter(self, *args):
        InspectorSingleton().disable()
        self.load_screens()

    def on_leave(self, *args):
        InspectorSingleton().enable()

    def load_screens(self, *args):
        children = [c for c in self.screen_drop_down.children[0].children]
        for c in children:
            self.screen_drop_down.remove_widget(c)
        path = pu.get_path('generated_screens')
        for screen_file in os.listdir(path):
            if screen_file.startswith('__init__') or screen_file.endswith('.pyc'):
                continue
            prepped_filename = screen_file[:-3] # remove ".py"
            class_name = re.sub(r'_([a-z])', lambda pat: pat.group(1).upper(), '_' + prepped_filename)
            btn = ButtonBase(text=class_name, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.screen_drop_down.select(btn.text))
            self.screen_drop_down.add_widget(btn)

    def import_screen(self, screen_name):
        path = pu.get_path('generated_screens')
        for screen_file in os.listdir(path):
            prepped_filename = screen_file[:-3] # remove ".py"
            class_name = re.sub(r'_([a-z])', lambda pat: pat.group(1).upper(), '_' + prepped_filename)
            if screen_file.startswith('__init__') or screen_name != class_name:
                continue
            #juggle with path to get module and class name
            module = path.replace('/', '.').split('src')[1][1:] + '.' + prepped_filename
            try:
                test = __import__(name=module, fromlist=[class_name])
                screen_class = getattr(test, class_name)
                screen = screen_class()
                return screen
            except ImportError as ex:
                pass

    def open_screen(self, instance, screen_name):
        screen = self.import_screen(screen_name)
        if screen:
            if self.sm.has_screen(screen.name):
                self.sm.remove_widget(self.sm.get_screen(screen.name))
            self.sm.add_widget(screen)
            self.sm.current = screen.name

            App.get_running_app().update_widget(screen.children[0])

    def create_new_screen(self, *args):

        if self.sm.has_screen(self.last_screen_name):
            self.sm.remove_widget(self.sm.get_screen(self.last_screen_name))
        self.last_screen_name = self.screen_name_input.text
        new_screen = Screen(name=self.screen_name_input.text)
        base_layout = FloatLayout()
        new_screen.add_widget(base_layout)
        self.sm.add_widget(new_screen)
        App.get_running_app().update_widget(base_layout)

        self.sm.current = new_screen.name


class ScreenDesignerApp(App):

    width = Window.width
    height = Window.height if Window.height == 480 else Window.height - 32

    def __init__(self, **kwargs):
        super(ScreenDesignerApp, self).__init__(**kwargs)
        self.l = Localization()
        self.sm = ScreenManager(transition=NoTransition())
        self.designer_popup = AddWidgetPopup()
        self.inspector = InspectorSingleton()

    def update_widget(self, widget):
        self.designer_popup.widget_to_add_to = widget
        self.inspector.widget = widget



    def build(self):
        main_screen = DesignerMainScreen()

        self.sm.add_widget(main_screen)
        return self.sm


if __name__ == '__main__':
    ScreenDesignerApp().run()
