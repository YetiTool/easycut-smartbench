# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import os

'''
########################################################
IMPORTANT!!
Run from easycut-smartbench folder, with 
python -m tests.manual_tests.experiments.experiment_japanese

'''

font_path = "./tests/manual_tests/experiments/NotoSansJP-Regular.ttf"


Builder.load_string('''
<TestScreen>
    Label:
        font_name: "./tests/manual_tests/experiments/NotoSansJP-Regular.ttf"
        text: "速い茶色のキツネは、のろまな古いイヌに飛びかかった。"
''')

class TestScreen(Screen):
    pass

class TestApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(TestScreen(name='test', sm=sm))

        sm.current = 'test'

        return sm

if __name__ == '__main__':
    TestApp().run()