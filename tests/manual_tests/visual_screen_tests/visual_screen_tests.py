 # -*- coding: utf-8 -*-

import sys, os

if len(sys.argv) != 2:
    print("Correct usage: python -m tests.manual_tests.visual_screen_tests.visual_screen_tests <test_function_name>")
    sys.exit(0)

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
python -m tests.manual_tests.visual_screen_tests.visual_screen_tests <test_function_name>
'''

sys.path.append('./src')
os.chdir('./src')

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from asmcnc.comms import localization
from asmcnc.comms import router_machine
from settings import settings_manager
from asmcnc.comms import smartbench_flurry_database_connection
from asmcnc.apps import app_manager
from asmcnc.job.yetipilot.yetipilot import YetiPilot

from asmcnc.skavaUI import screen_go, screen_job_feedback, screen_home
from asmcnc.apps.systemTools_app.screens.calibration import screen_general_measurement
from asmcnc.skavaUI import screen_go, screen_job_feedback, screen_home, screen_spindle_shutdown, screen_stop_or_resume_decision
from asmcnc.apps.maintenance_app import screen_maintenance


try: 
    from mock import Mock, MagicMock
    from serial_mock.mock import MockSerial, DummySerial
    from random import randint

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

    def give_me_a_PCB(outerSelf, status, alarm_message):

        class YETIPCB(MockSerial):
            simple_queries = {
                "?": status,
                "\x18": "",
                "*LFFFF00": "ok",
                "$$": alarm_message
            }

        return YETIPCB

    def build(self):

        # Add tests as functions below

        def alarm_screen_tests():
            # STALL ALARMS
            stall_pin = "z"

            # LIMIT ALARMS
            alarm_pin = "y"

            alarm_number = 1

            stall_alarm_test = True

            motor_id = 0
            step_size = 75
            sg_val = 151
            thresh = 150
            distance = 42103020
            temperature = 50
            x_coord = -1084.997
            y_coord = -2487.003
            z_coord = -99.954


            alarm_message = "ALARM:" + str(alarm_number) + "\n"

            limit_status = "<Alarm|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:" + alarm_pin + "|WCO:-166.126,-213.609,-21.822|SG:-999,-20,15,-20,-2>\n"
            sg_alarm_status = "<Alarm|MPos:-685.008,-2487.003,-100.752|Bf:34,255|FS:0,0|Pn:G" + \
                stall_pin + \
                "|SGALARM:" + \
                str(motor_id) + "," + \
                str(step_size) + "," + \
                str(sg_val) + "," + \
                str(thresh) + "," + \
                str(distance) + "," + \
                str(temperature) + "," + \
                str(x_coord) + "," + \
                str(y_coord) + "," + \
                str(z_coord) + ">\n"

            if stall_alarm_test: status = sg_alarm_status
            else: status = limit_status

            m.s.s = DummySerial(self.give_me_a_PCB(status, alarm_message))
            m.s.s.fd = 1 # this is needed to force it to run
            m.s.fw_version = self.fw_version

            sm.current = 'home'
        
            Clock.schedule_once(m.s.start_services, 0.1)

        def general_measurement_screen_test():
            m.measured_running_data = [
                [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
                ]

            sm.current = 'test'

        def go_screen_sc2_overload_test():
            alarm_message = "\n"

            killtime = 9
            killtime_status = "<Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:G|Ld:75, 20, " + str(killtime) + ", 240>\n"

            m.s.s = DummySerial(self.give_me_a_PCB(killtime_status, alarm_message))
            m.s.s.fd = 1 # this is needed to force it to run
            m.s.fw_version = self.fw_version
            m.s.setting_50 = 0.03
            m.s.yp = yp
            
            m.is_using_sc2 = Mock(return_value=True)
            m.is_spindle_health_check_active = Mock(return_value=False)
            # m.has_spindle_health_check_failed = Mock(return_value=True)
            sm.get_screen('go').is_job_started_already = False

            sm.current = 'go'
            
            Clock.schedule_once(m.s.start_services, 0.1)

        def job_pause_tests():
            alarm_message = "\n"

            status = "<Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:G>\n"

            m.s.s = DummySerial(self.give_me_a_PCB(status, alarm_message))
            m.s.s.fd = 1 # this is needed to force it to run
            m.s.fw_version = self.fw_version
            m.s.setting_50 = 0.03
            m.s.yp = yp
            m.s.setting_27 = 1

            sm.current = 'go'

            sm.get_screen('go').start_or_pause_button_image.source = "./asmcnc/skavaUI/img/pause.png"

            Clock.schedule_once(m.s.start_services, 0.1)

            def stream_and_pause(dt=0):
                m.s.is_job_streaming = True
                m.set_pause(True, 'yetipilot_low_feed')
                print("STOP FOR STREAM PAUSE")
                # m.stop_for_a_stream_pause('yetipilot_spindle_data_loss')

            Clock.schedule_once(stream_and_pause, 5)

        def maintenance_app_screen_test():
            m.is_using_sc2 = Mock(return_value=True)
            m.theateam = Mock(return_value=True)

            landing_tab = 'spindle_health_check_tab'
            sm.get_screen('maintenance').landing_tab = landing_tab
            sm.current = 'maintenance'

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

        test_screen = screen_general_measurement.GeneralMeasurementScreen(name='test', systemtools = systemtools_sm, machine = m)
        sm.add_widget(test_screen)

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

        # Function for test to run is passed as argument
        eval(sys.argv[1] + "()")

        return sm

ScreenTest().run()