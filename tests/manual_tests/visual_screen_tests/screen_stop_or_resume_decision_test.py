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
python -m tests.manual_tests.visual_screen_tests.screen_stop_or_resume_decision_test.py.py
'''

import sys, os
sys.path.append('./src')
os.chdir('./src')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from asmcnc.comms import localization
from asmcnc.comms import router_machine
from settings import settings_manager
from asmcnc.skavaUI import screen_stop_or_resume_decision
from asmcnc.comms import smartbench_flurry_database_connection
from asmcnc.apps import app_manager

try: 
    from mock import Mock
    from serial_mock.mock import MockSerial, DummySerial

except: 
    pass


from asmcnc.comms.yeti_grbl_protocol.c_defines import *

Cmport = 'COM3'

class ScreenTest(App):

    lang_idx = 0

    # 0 - English (y)
    # 1 - Italian (y)
    # 2 - Finnish (y)
    # 3 - German (y)
    # 4 - French (y)
    # 5 - Polish (y)
    # 6 - Danish (y)

    


    def build(self):

        # Establish screens
        sm = ScreenManager(transition=NoTransition())

        systemtools_sm = Mock()
        systemtools_sm.sm = sm

        # Localization/language object
        l = localization.Localization()
        l.load_in_new_language(l.approved_languages[self.lang_idx])

        # Initialise settings object
        sett = settings_manager.Settings(sm)
        # sett.ip_address = ''

        # Initialise 'j'ob 'd'ata object
        jd = Mock()
        jd.job_name = ""
        jd.gcode_summary_string = ""
        jd.screen_to_return_to_after_job = ""
        jd.job_gcode_running = []

        # Initialise 'm'achine object
        m = router_machine.RouterMachine(Cmport, sm, sett, l, jd)

        # Create database object to talk to
        db = smartbench_flurry_database_connection.DatabaseEventManager(sm, m, sett)

        stop_or_resume_decision_screen = screen_stop_or_resume_decision.StopOrResumeDecisionScreen(name='stop_or_resume_job_decision', screen_manager = sm, machine = m, job = jd, database=db, localization = l)
        sm.add_widget(stop_or_resume_decision_screen)

        stop_or_resume_decision_screen.reason_for_pause = 'yetipilot'

        sm.current = 'stop_or_resume_job_decision'
        
        Clock.schedule_once(m.s.start_services, 0.1)

        return sm

ScreenTest().run()