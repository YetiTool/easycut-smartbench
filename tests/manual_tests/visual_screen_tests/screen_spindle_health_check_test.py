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
python -m tests.manual_tests.visual_screen_tests.screen_spindle_health_check_test
'''
try: from mock import Mock
except: pass

import sys, os
sys.path.append('./src')
os.chdir('./src')

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window

from asmcnc.comms import localization
from asmcnc.comms import router_machine
from settings import settings_manager
from asmcnc.comms import smartbench_flurry_database_connection
from asmcnc.job.yetipilot.yetipilot import YetiPilot

from asmcnc.core_UI.job_go.screens.screen_spindle_health_check import SpindleHealthCheckActiveScreen


Cmport = "COM3"

class TestApp(App):

    lang_idx = 0

    # 0 - English (y)
    # 1 - Italian (y)
    # 2 - Finnish (y)
    # 3 - German (y)
    # 4 - French (y)
    # 5 - Polish (y)
    # 6 - Danish (y)

    def build(self):
        # Create the screen manager
        sm = ScreenManager()

        l = localization.Localization()
        l.load_in_new_language(l.approved_languages[self.lang_idx])

        # Initialise 'j'ob 'd'ata object
        jd = Mock()
        jd.job_name = ""
        jd.gcode_summary_string = ""
        jd.screen_to_return_to_after_job = ""
        jd.job_gcode_running = []

        # Initialise settings object
        sett = settings_manager.Settings(sm)

        # Initialise 'm'achine object
        m = router_machine.RouterMachine(Cmport, sm, sett, l, jd)

        sm.add_widget(SpindleHealthCheckActiveScreen(name='test', screen_manager =sm, localization =l, machine=m))
        sm.current = 'test'
        return sm

if __name__ == '__main__':
    TestApp().run()