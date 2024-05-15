 # -*- coding: utf-8 -*-

'''
########################################################
IMPORTANT!!
Run from easycut-smartbench folder, with 
python -m tests.manual_tests.experiments.experiment_custom_keyboard
'''

import sys, os, subprocess

 from asmcnc.comms.logging_system.logging_system import Logger

 sys.path.append('./src')
os.chdir('./src')

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from asmcnc.comms import localization
from asmcnc.keyboard import custom_keyboard

try: 
    from mock import Mock

except:
    pass


Builder.load_string("""

<FormattedButton@Button>:

    text_size: self.size
    valign: "top"
    halign: "center"
    padding: app.get_scaled_tuple([0, 20])


<BasicScreen>:

    t1:t1
    t2:t2
    t3:t3

    on_touch_down: root.on_touch()

    BoxLayout:
        orientation: 'horizontal'
        FormattedButton: 
            text: "Test generic for loop alternative"
            on_press: root.test_generic_for_loop_alternative()

        FormattedButton: 
            text: "Test generic for loop alternative with end func"
            on_press: root.test_generic_for_loop_alternative_with_end_func()

        FormattedButton: 
            text: 'Add keyboard'
            on_press: root.add_keyboard_instance()

        FormattedButton:
            text: "Does keyboard exist?"
            on_press: root.does_keyboard_exist()

        FormattedButton: 
            text: "Remove children"
            on_press: root.remove_keyboard()

        FormattedButton: 
            text: "Raise keyboard with mocks (this will break stuff)"
            on_press: root.raise_keyboard_if_none_exists_with_mocks()

        BoxLayout: 
            orientation: "vertical"

            Label:
                text: ""

            TextInput:
                id: t1
                text: ""
                multiline: False

            TextInput:
                id: t2
                text: ""

            TextInput:
                id: t3
                text: ""
""")

class BasicScreen(Screen):

    list_of_items = list(range(0, 101))

    def __init__(self, **kwargs):
        super(BasicScreen, self).__init__(**kwargs)
        self.l = localization.Localization()
        self.text_inputs = [self.t1, self.t2, self.t3]
        self.kb = custom_keyboard.Keyboard(localization=self.l)
        self.kb.setup_text_inputs(self.text_inputs)

    def on_touch(self):
        self.kb.defocus_all_text_inputs(self.text_inputs)

    def func(self, x):
        Logger.info(x)

    def end_func(self):
        Logger.info("YAY")

    def test_generic_for_loop_alternative(self):
        self.kb.generic_for_loop_alternative(self.func, self.list_of_items)

    def test_generic_for_loop_alternative_with_end_func(self):
        self.kb.generic_for_loop_alternative(self.func, self.list_of_items, end_func=self.end_func)

    def add_keyboard_instance(self):
        self.kb.add_keyboard_instance()

    def does_keyboard_exist(self):
        Logger.info(self.kb.return_if_keyboard_exists(Window.children[0]))

    def remove_keyboard(self):
        self.kb.remove_children(Window.children[0])

    def raise_keyboard_if_none_exists_with_mocks(self):

        def add_keyboard(*args): Logger.info("raise keyboard")
        self.kb.add_keyboard_instance = Mock(side_effect=add_keyboard)

        self.kb.raise_keyboard_if_none_exists()

        

class TestApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(BasicScreen(name='basic'))
        sm.current = 'basic'
        return sm

if __name__ == '__main__':
    TestApp().run()


