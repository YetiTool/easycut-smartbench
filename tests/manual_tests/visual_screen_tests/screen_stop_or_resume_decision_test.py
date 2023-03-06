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
from asmcnc.skavaUI import screen_stop_or_resume_decision, screen_go, screen_home, screen_job_feedback
from asmcnc.job.yetipilot.yetipilot import YetiPilot
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
        m.is_using_sc2 = Mock()
        m.is_using_sc2.return_value = True

        # Create database object to talk to
        db = smartbench_flurry_database_connection.DatabaseEventManager(sm, m, sett)

        # App manager object
        config_flag = False
        initial_version = 'v2.1.0'
        am = app_manager.AppManagerClass(sm, m, sett, l, jd, db, config_flag, initial_version)

        # Initialise yetipilot
        yp = YetiPilot(screen_manager=sm, machine=m, job_data=jd)

        home_screen = screen_home.HomeScreen(name='home', screen_manager = sm, machine = m, job = jd, settings = sett, localization = l)
        sm.add_widget(home_screen)

        job_feedback_screen = screen_job_feedback.JobFeedbackScreen(name = 'job_feedback', screen_manager = sm, machine =m, database = db, job = jd, localization = l)
        sm.add_widget(job_feedback_screen)

        go_screen = screen_go.GoScreen(name='go', screen_manager = sm, machine = m, job = jd, app_manager = am, database=db, localization = l, yetipilot=yp)
        sm.add_widget(go_screen)

        stop_or_resume_decision_screen = screen_stop_or_resume_decision.StopOrResumeDecisionScreen(name='stop_or_resume_job_decision', screen_manager = sm, machine = m, job = jd, database=db, localization = l)
        sm.add_widget(stop_or_resume_decision_screen)

        stop_or_resume_decision_screen.return_screen = 'go'

        # stop_or_resume_decision_screen.reason_for_pause = 'spindle_overload'
        # stop_or_resume_decision_screen.reason_for_pause = 'job_pause'
        stop_or_resume_decision_screen.reason_for_pause = 'yetipilot_low_feed'
        # stop_or_resume_decision_screen.reason_for_pause = 'yetipilot_spindle_data_loss'

        # Set yetipilot initially enabled, to test disable on unpause
        go_screen.is_job_started_already = True
        go_screen.yp_widget.switch.active = True
        go_screen.yp_widget.toggle_yeti_pilot(go_screen.yp_widget.switch)

        sm.current = 'stop_or_resume_job_decision'
        
        Clock.schedule_once(m.s.start_services, 0.1)

        return sm

ScreenTest().run()