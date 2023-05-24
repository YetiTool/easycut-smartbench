"""
@author archiejarvis on 24/05/2023
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from asmcnc.tests.screen_tests.random_text_screen import RandomTextScreen


class ScreenTests(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(RandomTextScreen(name='random_text_screen'))

        return sm


if __name__ == '__main__':
    ScreenTests().run()
