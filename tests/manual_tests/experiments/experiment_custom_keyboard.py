 # -*- coding: utf-8 -*-

'''
########################################################
IMPORTANT!!
Run from easycut-smartbench folder, with 
python -m tests.manual_tests.experiments.experiment_custom_keyboard
'''

import sys, os, subprocess
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
<BasicScreen>:

    t1:t1
    t2:t2
    t3:t3

    on_touch_down: root.on_touch()

    BoxLayout:
        orientation: 'horizontal'
        Button: 
            text: "Test generic for loop alternative"
            on_press: root.test_generic_for_loop_alternative()
            text_size: self.size
            valign: "top"
            halign: "center"
            padding: [0,20]

        Button: 
            text: 'Add keyboard'
            on_press: root.add_keyboard_instance()
            text_size: self.size
            valign: "top"
            halign: "center"
            padding: [0,20]

        Button:
            text: "Does keyboard exist?"
            on_press: root.does_keyboard_exist()
            text_size: self.size
            valign: "top"
            halign: "center"
            padding: [0,20]

        Button: 
            text: "Remove children"
            on_press: root.remove_keyboard()
            text_size: self.size
            valign: "top"
            halign: "center"
            padding: [0,20]

        Button: 
            text: "Raise keyboard with mocks (this will break stuff)"
            on_press: root.raise_keyboard_if_none_exists_with_mocks()
            text_size: self.size
            valign: "top"
            halign: "center"
            padding: [0,20]

        BoxLayout: 
            orientation: "vertical"

            Label:
                text: ""

            TextInput:
                id: t1
                text: ""

            TextInput:
                id: t2
                text: ""

            TextInput:
                id: t3
                text: ""
""")

class BasicScreen(Screen):
    def __init__(self, **kwargs):
        super(BasicScreen, self).__init__(**kwargs)
        self.l = localization.Localization()
        self.text_inputs = [self.t1, self.t2, self.t3]
        self.kb = custom_keyboard.Keyboard(self.text_inputs, localization=self.l)

    def on_touch(self):
        self.kb.defocus_all_text_inputs(self.text_inputs)

    def test_generic_for_loop_alternative(self):

        def func(x):
            print(x)

        list_of_items = list(range(0, 101))
        self.kb.generic_for_loop_alternative(func, list_of_items)

    def add_keyboard_instance(self):
        self.kb.add_keyboard_instance()

    def does_keyboard_exist(self):
        print(self.kb.return_if_keyboard_exists(Window.children[0]))

    def remove_keyboard(self):
        self.kb.remove_children(Window.children[0])

    def raise_keyboard_if_none_exists_with_mocks(self):

        def add_keyboard(*args): print("raise keyboard")
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


