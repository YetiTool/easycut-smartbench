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
python -m tests.manual_tests.visual_screen_tests.maintenance_app_screen_test.py
'''

import sys, os
sys.path.append('./src')
os.chdir('./src')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from asmcnc.comms import localization
from asmcnc.comms import router_machine
from settings import settings_manager
from asmcnc.comms import smartbench_flurry_database_connection
from asmcnc.apps import app_manager
from asmcnc.job.yetipilot.yetipilot import YetiPilot
from asmcnc.skavaUI import screen_go, screen_job_feedback, screen_home, \
screen_spindle_shutdown, screen_stop_or_resume_decision
from asmcnc.apps.maintenance_app import screen_maintenance

try: 
    from mock import Mock
    from serial_mock.mock import MockSerial, DummySerial

except: 
    pass



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
        m.is_using_sc2 = Mock(return_value=True)
        m.theateam = Mock(return_value=True)

        # Initialise YP
        yp = YetiPilot(screen_manager=sm, machine=m, job_data=jd, localization=l)

        # Create database object to talk to
        db = smartbench_flurry_database_connection.DatabaseEventManager(sm, m, sett)

        # App manager object
        config_flag = False
        initial_version = 'v2.1.0'
        am = app_manager.AppManagerClass(sm, m, sett, l, jd, db, config_flag, initial_version)

        home_screen = screen_home.HomeScreen(name='home', screen_manager = sm, machine = m, job = jd, settings = sett, localization = l)
        sm.add_widget(home_screen)

        job_feedback_screen = screen_job_feedback.JobFeedbackScreen(name = 'job_feedback', screen_manager = sm, machine =m, database = db, job = jd, localization = l)
        sm.add_widget(job_feedback_screen)

        spindle_shutdown_screen = screen_spindle_shutdown.SpindleShutdownScreen(name = 'spindle_shutdown', screen_manager = sm, machine =m, job = jd, database = db, localization = l)
        sm.add_widget(spindle_shutdown_screen)

        stop_or_resume_decision_screen = screen_stop_or_resume_decision.StopOrResumeDecisionScreen(name = 'stop_or_resume_job_decision', screen_manager = sm, machine =m, job = jd, database = db, localization = l)
        sm.add_widget(stop_or_resume_decision_screen)

        go_screen = screen_go.GoScreen(name='go', screen_manager = sm, machine = m, job = jd, app_manager = am, database=db, localization = l,  yetipilot=yp)
        sm.add_widget(go_screen)

        maintenance_screen = screen_maintenance.MaintenanceScreenClass(name = 'maintenance', screen_manager = sm, machine = m, localization = l, job = jd)
        sm.add_widget(maintenance_screen)

        landing_tab = 'spindle_health_check_tab'
        sm.get_screen('maintenance').landing_tab = landing_tab
        sm.current = 'maintenance'

        return sm

ScreenTest().run()