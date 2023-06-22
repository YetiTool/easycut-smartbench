 # -*- coding: utf-8 -*-

from kivy.config import Config

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
python -m tests.manual_tests.visual_screen_tests.pro_plus_safety_screen_test

'''
try: from mock import Mock
except: pass

import sys, os
sys.path.append('./src')
os.chdir('./src')

 from kivy.app import App
 from kivy.uix.screenmanager import ScreenManager

 from asmcnc.comms import localization
from asmcnc.comms import router_machine
from settings import settings_manager
from asmcnc.comms import smartbench_flurry_database_connection
from asmcnc.job.yetipilot.yetipilot import YetiPilot

from asmcnc.apps.start_up_sequence.screens.screen_pro_plus_safety import ProPlusSafetyScreen
from asmcnc.apps.start_up_sequence.data_consent_app.screens import wifi_and_data_consent_1


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

        # Initialise YP
        yp = YetiPilot(screen_manager=sm, machine=m, job_data=jd, localization=l)

        # Create database object to talk to
        db = smartbench_flurry_database_connection.DatabaseEventManager(sm, m, sett)

        start_seq = Mock()


        consent_1_screen = wifi_and_data_consent_1.WiFiAndDataConsentScreen1(name='consent_1', start_sequence = start_seq, consent_manager = self, localization = l)
        sm.add_widget(consent_1_screen)

        sm.add_widget(ProPlusSafetyScreen(name='basic', start_sequence = start_seq, screen_manager =sm, localization =l))
        sm.current = 'basic'
        return sm

if __name__ == '__main__':
    TestApp().run()