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

path_to_EC = os.getcwd()
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
from asmcnc.apps import app_manager
from asmcnc.job.yetipilot.yetipilot import YetiPilot

from asmcnc.skavaUI import screen_go, screen_job_feedback, screen_home
from asmcnc.apps.systemTools_app.screens.calibration import screen_general_measurement
from asmcnc.skavaUI import screen_go, screen_job_feedback, screen_home, screen_spindle_shutdown, screen_stop_or_resume_decision
from asmcnc.apps.maintenance_app import screen_maintenance
from asmcnc.apps.start_up_sequence.screens import screen_pro_plus_safety
from asmcnc.apps.start_up_sequence.data_consent_app.screens import wifi_and_data_consent_1
from asmcnc.core_UI.job_go.screens import screen_spindle_health_check
from asmcnc.apps.systemTools_app.screens.calibration import screen_stall_jig
from asmcnc.core_UI.job_go.popups import popup_yetipilot_settings
from asmcnc.production.z_head_qc_jig import z_head_qc_pcb_set_up_outcome, z_head_qc_pcb_set_up

try: 
    from mock import Mock, MagicMock
    from serial_mock.mock import MockSerial, DummySerial
    from random import randint

except: 
    pass


from asmcnc.comms.yeti_grbl_protocol.c_defines import *

Builder.load_string("""
<BasicScreen>:

""")

class BasicScreen(Screen):

    def __init__(self, **kwargs):
        super(BasicScreen, self).__init__(**kwargs)


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

        # Default values for dummy serial, which can be reassigned or added to if needed
        def set_up_dummy_serial(status, alarm_message):
            m.s.s = DummySerial(self.give_me_a_PCB(status, alarm_message))
            m.s.s.fd = 1 # this is needed to force it to run
            m.s.fw_version = self.fw_version
            m.s.setting_50 = 0.03
            m.s.yp = yp
            m.s.setting_27 = 1

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

            set_up_dummy_serial(status, alarm_message)

            sm.current = 'home'
        
            Clock.schedule_once(m.s.start_services, 0.1)

        def general_measurement_screen_test():
            m.measured_running_data = [
                [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
                ]

            sm.current = 'general_measurement'

        def go_screen_sc2_overload_test():
            alarm_message = "\n"

            killtime = 9
            killtime_status = "<Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:G|Ld:75, 20, " + str(killtime) + ", 240>\n"

            set_up_dummy_serial(killtime_status, alarm_message)
            
            m.is_using_sc2 = Mock(return_value=True)
            m.is_spindle_health_check_active = Mock(return_value=False)
            # m.has_spindle_health_check_failed = Mock(return_value=True)
            sm.get_screen('go').is_job_started_already = False

            sm.current = 'go'
            
            Clock.schedule_once(m.s.start_services, 0.1)

        def job_pause_tests():
            alarm_message = "\n"

            status = "<Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:G>\n"

            set_up_dummy_serial(status, alarm_message)

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

        def pro_plus_safety_screen_test():
            sm.current = 'pro_plus_safety'

        def screen_spindle_health_check_test():
            alarm_message = "\n"
            status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:G>\n"
            set_up_dummy_serial(status, alarm_message)

            sm.current = 'spindle_health_check_active'

        def screen_stop_or_resume_decision_test():
            m.is_using_sc2 = Mock(return_value=True)

            stop_or_resume_decision_screen.return_screen = 'go'

            stop_or_resume_decision_screen.reason_for_pause = 'spindle_overload'
            # stop_or_resume_decision_screen.reason_for_pause = 'job_pause'
            # stop_or_resume_decision_screen.reason_for_pause = 'yetipilot_low_feed'
            # stop_or_resume_decision_screen.reason_for_pause = 'yetipilot_spindle_data_loss'
            # stop_or_resume_decision_screen.reason_for_pause = 'spindle_health_check_failed'

            # Set yetipilot initially enabled, to test disable on unpause
            go_screen.is_job_started_already = True
            go_screen.yp_widget.switch.active = True
            go_screen.yp_widget.toggle_yeti_pilot(go_screen.yp_widget.switch)

            sm.current = 'stop_or_resume_job_decision'

        def stall_jig_screen_tests():
            alarm_pin = "Y"

            stall_pin = "S"
            motor_id = 0
            step_size = 75
            sg_val = 151
            thresh = 150
            distance = 42103020
            x_coord = -1084.997
            y_coord = -2487.003
            z_coord = -99.954


            alarm_message = "ALARM:1\n"

            status = "<Alarm|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:" + alarm_pin + "|WCO:-166.126,-213.609,-21.822|SG:-999,-20,15,-20,-2>"
            sg_alarm_status = "<Alarm|MPos:-685.008,-2487.003,-100.752|Bf:34,255|FS:0,0|Pn:G" + \
                stall_pin + \
                "|SGALARM:" + \
                str(motor_id) + "," + \
                str(step_size) + "," + \
                str(sg_val) + "," + \
                str(thresh) + "," + \
                str(distance) + "," + \
                str(x_coord) + "," + \
                str(y_coord) + "," + \
                str(z_coord) + ">\n"
            
            status = sg_alarm_status
            # status = status

            set_up_dummy_serial(status, alarm_message)

            # CHANGE ME
            sm.current = 'stall_jig'
            
            Clock.schedule_once(m.s.start_services, 0.1)

        def yetipilot_settings_popup_test():
            m.has_spindle_health_check_run = Mock(return_value=False)

            popup_yetipilot_settings.PopupYetiPilotSettings(sm, l, m, db, yp, version=not yp.using_advanced_profile)
            sm.current = 'basic'

        def z_head_qc_pcb_outcome_screen_test():
            m.s.fw_version = "2.5.5; HW: 35"

            sm.current = 'qcpcbsetupoutcome'

            zhqc_pcb_set_up_outcome.x_current_correct*=zhqc_pcb_set_up.check_current(TMC_X1, 0)
            zhqc_pcb_set_up_outcome.x_current_correct*=zhqc_pcb_set_up.check_current(TMC_X2, 10)
            zhqc_pcb_set_up_outcome.y_current_correct*=zhqc_pcb_set_up.check_current(TMC_Y1, 12)
            zhqc_pcb_set_up_outcome.y_current_correct*=zhqc_pcb_set_up.check_current(TMC_Y2, 11)
            zhqc_pcb_set_up_outcome.z_current_correct*=zhqc_pcb_set_up.check_current(TMC_Z, 2)

            zhqc_pcb_set_up_outcome.thermal_coefficients_correct*=zhqc_pcb_set_up.check_temp_coeff(TMC_X1, 0)
            zhqc_pcb_set_up_outcome.thermal_coefficients_correct*=zhqc_pcb_set_up.check_temp_coeff(TMC_X2, 11)
            zhqc_pcb_set_up_outcome.thermal_coefficients_correct*=zhqc_pcb_set_up.check_temp_coeff(TMC_Y1, 0)
            zhqc_pcb_set_up_outcome.thermal_coefficients_correct*=zhqc_pcb_set_up.check_temp_coeff(TMC_Y2, 0)
            zhqc_pcb_set_up_outcome.thermal_coefficients_correct*=zhqc_pcb_set_up.check_temp_coeff(TMC_Z, 0)

        def z_head_qc_pcb_set_up_screen_test():
            m.s.fw_version = "2.5.5; HW: 35"

            sm.current = 'qcpcbsetup'

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

        start_seq = Mock()

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

        general_measurement_screen = screen_general_measurement.GeneralMeasurementScreen(name='general_measurement', systemtools = systemtools_sm, machine = m)
        sm.add_widget(general_measurement_screen)

        consent_1_screen = wifi_and_data_consent_1.WiFiAndDataConsentScreen1(name='consent_1', start_sequence = start_seq, consent_manager = self, localization = l)
        sm.add_widget(consent_1_screen)

        pro_plus_safety_screen = screen_pro_plus_safety.ProPlusSafetyScreen(name='pro_plus_safety', start_sequence = start_seq, screen_manager =sm, localization =l)
        sm.add_widget(pro_plus_safety_screen)

        shc_screen = screen_spindle_health_check.SpindleHealthCheckActiveScreen(name='spindle_health_check_active', screen_manager =sm, localization =l, machine=m)
        sm.add_widget(shc_screen)

        stall_jig_screen = screen_stall_jig.StallJigScreen(name='stall_jig', systemtools = systemtools_sm, machine = m, job = jd, settings = sett, localization = l, calibration_db = db)
        sm.add_widget(stall_jig_screen)

        basic_screen = BasicScreen(name='basic')
        sm.add_widget(basic_screen)

        zhqc_pcb_set_up = z_head_qc_pcb_set_up.ZHeadPCBSetUp(name='qcpcbsetup', sm = sm, m = m)
        sm.add_widget(zhqc_pcb_set_up)
        sm.get_screen('qcpcbsetup').usb_path = path_to_EC + "/tests/test_resources/media/usb/"

        zhqc_pcb_set_up_outcome = z_head_qc_pcb_set_up_outcome.ZHeadPCBSetUpOutcome(name='qcpcbsetupoutcome', sm = sm, m = m)
        sm.add_widget(zhqc_pcb_set_up_outcome)
        sm.get_screen('qcpcbsetupoutcome').usb_path = path_to_EC + "/tests/test_resources/media/usb/"

        # Function for test to run is passed as argument
        eval(sys.argv[1] + "()")

        return sm

ScreenTest().run()