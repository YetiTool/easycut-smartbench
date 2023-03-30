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
python -m tests.manual_tests.visual_screen_tests.go_screen_sc2_overload_test.py
'''

import sys, os
sys.path.append('./src')
os.chdir('./src')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from asmcnc.comms import localization
from asmcnc.comms import router_machine
from settings import settings_manager
from asmcnc.skavaUI import screen_go, screen_job_feedback, screen_home
from asmcnc.comms import smartbench_flurry_database_connection
from asmcnc.apps import app_manager
from asmcnc.job.yetipilot.yetipilot import YetiPilot

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

    
    fw_version = "2.4.2"

    alarm_message = "\n"

    killtime = 9
    killtime_status = "<Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:G|Ld:75, 20, " + str(killtime) + ", 240>\n"

    def give_status(self):

        return self.killtime_status

    def give_me_a_PCB(outerSelf):

        class YETIPCB(MockSerial):
            simple_queries = {
                "?": outerSelf.give_status(),
                "\x18": "",
                "*LFFFF00": "ok",
                "$$": outerSelf.alarm_message
            }

        return YETIPCB

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
        

        # Initialise YP
        yp = YetiPilot(screen_manager=sm, machine=m, job_data=jd, localization=l)

        # Create database object to talk to
        db = smartbench_flurry_database_connection.DatabaseEventManager(sm, m, sett)

        # App manager object
        config_flag = False
        initial_version = 'v2.1.0'
        am = app_manager.AppManagerClass(sm, m, sett, l, jd, db, config_flag, initial_version)

        m.s.s = DummySerial(self.give_me_a_PCB())
        m.s.s.fd = 1 # this is needed to force it to run
        m.s.fw_version = self.fw_version
        m.s.setting_50 = 0.03
        m.s.yp = yp

        home_screen = screen_home.HomeScreen(name='home', screen_manager = sm, machine = m, job = jd, settings = sett, localization = l)
        sm.add_widget(home_screen)

        job_feedback_screen = screen_job_feedback.JobFeedbackScreen(name = 'job_feedback', screen_manager = sm, machine =m, database = db, job = jd, localization = l)
        sm.add_widget(job_feedback_screen)

        go_screen = screen_go.GoScreen(name='go', screen_manager = sm, machine = m, job = jd, app_manager = am, database=db, localization = l,  yetipilot=yp)
        sm.add_widget(go_screen)
        
        m.is_using_sc2 = Mock(return_value=True)
        m.is_spindle_health_check_active = Mock(return_value=True)
        m.has_spindle_health_check_failed = Mock(return_value=True)
        sm.get_screen('go').is_job_started_already = True

        sm.current = 'go'
        
        Clock.schedule_once(m.s.start_services, 0.1)

        return sm

ScreenTest().run()