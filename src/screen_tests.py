"""
@author archiejarvis on 24/05/2023
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from asmcnc.tests.screen_tests.random_text_screen import RandomTextScreen

import cProfile


class ScreenTests(App):
    profile = None

    def build(self):
        sm = ScreenManager()

        sm.add_widget(RandomTextScreen(name='random_text_screen'))

        return sm

    def on_start(self):
        self.profile = cProfile.Profile()
        self.profile.enable()
        print("Starting profile")


app = None

if __name__ == '__main__':
    app = ScreenTests()
    app.run()
