# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys

'''
########################################################
IMPORTANT!!
Run from easycut-smartbench folder, with 
python -m tests.manual_tests.experiments.experiment_fonts

'''

sys.path.append('./src')


Builder.load_string('''
<TestScreen>
    Label:
        font_name: root.font_path
        text: root.test_text
''')

class TestScreen(Screen):

    font_path = "./src/asmcnc/keyboard/fonts/NotoSansJP-Bold.ttf"
    test_text = "速い茶色のキツネは、のろまな古いイヌに飛びかかった。"

class TestApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(TestScreen(name='test', sm=sm))

        sm.current = 'test'

        return sm

if __name__ == '__main__':
    TestApp().run()