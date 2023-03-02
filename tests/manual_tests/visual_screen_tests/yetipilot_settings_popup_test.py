 # -*- coding: utf-8 -*-

from kivy.config import Config
from kivy.clock import Clock
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'maxfps', '60')
Config.set('kivy', 'KIVY_CLOCK', 'interrupt')
Config.write()

'''
########################################################
IMPORTANT!!
Run from easycut-smartbench folder, with 
python -m tests.manual_tests.visual_screen_tests.yetipilot_settings_popup_test

'''

import sys, os
sys.path.append('./src')
os.chdir('./src')

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window

from asmcnc.comms import localization
from asmcnc.core_UI.job_go.popups import popup_yetipilot_settings



Builder.load_string("""
<BasicScreen>:

""")

class BasicScreen(Screen):

    def __init__(self, **kwargs):
        super(BasicScreen, self).__init__(**kwargs)
        self.sm = kwargs['sm']
        self.l = kwargs['l']

    def on_enter(self):
        popup_yetipilot_settings.PopupYetiPilotSettings(self.sm, self.l)


class TestApp(App):

    lang_idx = 0

    def build(self):
        # Create the screen manager
        sm = ScreenManager()

        l = localization.Localization()
        l.load_in_new_language(l.approved_languages[self.lang_idx])

        sm.add_widget(BasicScreen(name='basic', sm=sm, l=l))

        sm.current = 'basic'

        return sm

if __name__ == '__main__':
    TestApp().run()