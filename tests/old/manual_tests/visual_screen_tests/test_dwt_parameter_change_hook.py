import sys

from core.logging.logging_system import Logger

sys.path.append('./src')

from apps.drywall_cutter_app.config.config_loader import DWTConfig
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

try:
    import unittest
    import pytest
    from mock import Mock, MagicMock
except:
    Logger.info("Can't import mocking packages, are you on a dev machine?")

"""
RUN WITH python tests/manual_tests/visual_screen_tests/test_dwt_parameter_change_hook.py FROM EASYCUT-SMARTBENCH DIR
"""

class TestApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())

        sm.add_widget(TestScreen(name='test_screen'))

        sm.current = 'test_screen'

        return sm


Builder.load_string("""
<TestScreen>:
    GridLayout:
        rows: 3
        TextInput:
            id: num_input
            text: '0'
            filter: 'int'
            multiline: False
            # This will cause an error if the value is not an int - will be fixed in the future
            on_text: root.dwt_config.on_parameter_change('cutting_depths.material_thickness', int(self.text))
            
        Spinner:
            id: shape_input
            values: root.shape_options
            on_text: root.dwt_config.on_parameter_change('shape_type', self.text)
            
        Button:
            text: 'Change'
            on_press: root.dwt_config.save_temp_config()
""")


class TestScreen(Screen):
    dwt_config = DWTConfig()
    shape_options = ['Circle', 'Square', 'Line', 'Geberit']


if __name__ == '__main__':
    TestApp().run()

