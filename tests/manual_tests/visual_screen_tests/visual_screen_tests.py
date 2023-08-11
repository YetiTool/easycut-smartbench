import logging
import sys, os
if len(sys.argv) != 2:
    print(
        'Correct usage: python -m tests.manual_tests.visual_screen_tests.visual_screen_tests <test_function_name>'
        )
    sys.exit(0)
from kivy.config import Config
from kivy.clock import Clock
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'maxfps', '60')
Config.set('kivy', 'KIVY_CLOCK', 'interrupt')
Config.write()
"""
########################################################
IMPORTANT!!
Run from easycut-smartbench folder, with 
python -m tests.manual_tests.visual_screen_tests.visual_screen_tests <test_function_name>
"""
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
    fw_version = '2.4.2'

    def give_me_a_PCB(outerSelf, status, alarm_message):


        class YETIPCB(MockSerial):
            simple_queries = {'?': status, '\x18': '', '*LFFFF00': 'ok',
                '$$': alarm_message}
        return YETIPCB

    def build(self):

        def set_up_dummy_serial(status, alarm_message):
            m.s.s = DummySerial(self.give_me_a_PCB(status, alarm_message))
            m.s.s.fd = 1
            m.s.versions.firmware = self.fw_version
            m.s.settings.s50 = 0.03
            m.s.yp = yp
            m.s.settings.s27 = 1

        def cycle_through_screens(screen_list):

            def show_next_screen(screen_list, index):
                sm.current = screen_list[index]
                index += 1
                if index >= len(screen_list):
                    Clock.schedule_once(lambda dt: show_next_screen(
                        screen_list, 0), 5)
                else:
                    Clock.schedule_once(lambda dt: show_next_screen(
                        screen_list, index), 5)
            show_next_screen(screen_list, 0)

        def alarm_screen_tests():
            """
            This test is set up to check that alarms trigger (and that the codes and details are presented correctly) as expected,
            when an alarm status is parsed by the serial module (the dummy serial object creates passes this).

            Stall/alarm pins and alarm parameters can be modified to conduct tests as needed.

            At some point it might be worth setting up all possible cases/setting up some kind of automated run through of cases.
            """
            stall_pin = 'z'
            alarm_pin = 'y'
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
            alarm_message = 'ALARM:' + str(alarm_number) + '\n'
            limit_status = '<Alarm|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:' + alarm_pin + """|WCO:-166.126,-213.609,-21.822|SG:-999,-20,15,-20,-2>
"""
            sg_alarm_status = (
                '<Alarm|MPos:-685.008,-2487.003,-100.752|Bf:34,255|FS:0,0|Pn:G'
                 + stall_pin + '|SGALARM:' + str(motor_id) + ',' + str(
                step_size) + ',' + str(sg_val) + ',' + str(thresh) + ',' +
                str(distance) + ',' + str(temperature) + ',' + str(x_coord) +
                ',' + str(y_coord) + ',' + str(z_coord) + '>\n')
            if stall_alarm_test:
                status = sg_alarm_status
            else:
                status = limit_status
            set_up_dummy_serial(status, alarm_message)
            sm.current = 'home'
            Clock.schedule_once(m.s.start_services, 0.1)

        def maintenance_app_screen_test():
            m.is_using_sc2 = Mock(return_value=True)
            m.theateam = Mock(return_value=True)
            landing_tab = 'spindle_health_check_tab'
            sm.get_screen('maintenance').landing_tab = landing_tab
            sm.current = 'maintenance'

        def screen_stop_or_resume_decision_test():
            """
            This test can be used to check the various cases of the stop/resume decision screen
            """
            m.is_using_sc2 = Mock(return_value=True)
            stop_or_resume_decision_screen.return_screen = 'go'
            stop_or_resume_decision_screen.reason_for_pause = (
                'spindle_overload')
            go_screen.is_job_started_already = True
            go_screen.yp_widget.switch.active = True
            go_screen.yp_widget.toggle_yeti_pilot(go_screen.yp_widget.switch)
            sm.current = 'stop_or_resume_job_decision'

        def general_measurement_screen_test():
            """
            This tests the general measrement dev screen available in the factory settings app. Running data is just to pass
            a test dataset for plotting.
            """
            m.measured_running_data = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
                11, 12, 13, 14], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                13, 14], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]]
            sm.current = 'general_measurement'

        def stall_jig_screen_tests():
            """
            This tests that an alarm appears and is registered correctly by stall jig, at the same time as suppressing normal alarm screens
            """
            alarm_pin = 'Y'
            stall_pin = 'S'
            motor_id = 0
            step_size = 75
            sg_val = 151
            thresh = 150
            distance = 42103020
            x_coord = -1084.997
            y_coord = -2487.003
            z_coord = -99.954
            alarm_message = 'ALARM:1\n'
            status = ('<Alarm|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:' +
                alarm_pin +
                '|WCO:-166.126,-213.609,-21.822|SG:-999,-20,15,-20,-2>')
            sg_alarm_status = (
                '<Alarm|MPos:-685.008,-2487.003,-100.752|Bf:34,255|FS:0,0|Pn:G'
                 + stall_pin + '|SGALARM:' + str(motor_id) + ',' + str(
                step_size) + ',' + str(sg_val) + ',' + str(thresh) + ',' +
                str(distance) + ',' + str(x_coord) + ',' + str(y_coord) +
                ',' + str(z_coord) + '>\n')
            status = sg_alarm_status
            set_up_dummy_serial(status, alarm_message)
            sm.current = 'stall_jig'
            Clock.schedule_once(m.s.start_services, 0.1)

        def z_head_qc_pcb_outcome_screen_test():
            """
            These parameters can be modified to check that the outcome screen shows passes/fails correctly, and correctly shows values
            """
            m.s.versions.firmware = '2.5.5; HW: 35'
            sm.current = 'qcpcbsetupoutcome'
            zhqc_pcb_set_up_outcome.x_current_correct *= (zhqc_pcb_set_up.
                check_current(TMC_X1, 0))
            zhqc_pcb_set_up_outcome.x_current_correct *= (zhqc_pcb_set_up.
                check_current(TMC_X2, 10))
            zhqc_pcb_set_up_outcome.y_current_correct *= (zhqc_pcb_set_up.
                check_current(TMC_Y1, 12))
            zhqc_pcb_set_up_outcome.y_current_correct *= (zhqc_pcb_set_up.
                check_current(TMC_Y2, 11))
            zhqc_pcb_set_up_outcome.z_current_correct *= (zhqc_pcb_set_up.
                check_current(TMC_Z, 2))
            zhqc_pcb_set_up_outcome.thermal_coefficients_correct *= (
                zhqc_pcb_set_up.check_temp_coeff(TMC_X1, 0))
            zhqc_pcb_set_up_outcome.thermal_coefficients_correct *= (
                zhqc_pcb_set_up.check_temp_coeff(TMC_X2, 11))
            zhqc_pcb_set_up_outcome.thermal_coefficients_correct *= (
                zhqc_pcb_set_up.check_temp_coeff(TMC_Y1, 0))
            zhqc_pcb_set_up_outcome.thermal_coefficients_correct *= (
                zhqc_pcb_set_up.check_temp_coeff(TMC_Y2, 0))
            zhqc_pcb_set_up_outcome.thermal_coefficients_correct *= (
                zhqc_pcb_set_up.check_temp_coeff(TMC_Z, 0))

        def z_head_qc_pcb_set_up_screen_test():
            m.s.versions.firmware = '2.5.5; HW: 35'
            sm.current = 'qcpcbsetup'

        def go_screen_sc2_overload_test():
            """
            Check that overload message triggers correctly
            """
            alarm_message = '\n'
            killtime = 9
            killtime_status = (
                '<Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:G|Ld:75, 20, '
                 + str(killtime) + ', 240>\n')
            set_up_dummy_serial(killtime_status, alarm_message)
            m.is_using_sc2 = Mock(return_value=True)
            m.is_spindle_health_check_active = Mock(return_value=False)
            sm.get_screen('go').is_job_started_already = False
            sm.current = 'go'
            Clock.schedule_once(m.s.start_services, 0.1)

        def job_pause_tests():
            """
            Check that job pausing happens correctly from go screen, and that correct pause screen gets called
            (Case can be set by the string put into the pause functions)
            """
            alarm_message = '\n'
            status = '<Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:G>\n'
            set_up_dummy_serial(status, alarm_message)
            sm.current = 'go'
            sm.get_screen('go').start_or_pause_button_image.source = (
                './asmcnc/skavaUI/img/pause.png')
            Clock.schedule_once(m.s.start_services, 0.1)

            def stream_and_pause(dt=0):
                m.s.is_job_streaming = True
                m.set_pause(True, 'yetipilot_low_feed')
                print('STOP FOR STREAM PAUSE')
            Clock.schedule_once(stream_and_pause, 5)

        def pro_plus_safety_screen_test():
            sm.current = 'pro_plus_safety'

        def screen_spindle_health_check_test():
            alarm_message = '\n'
            status = '<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:G>\n'
            set_up_dummy_serial(status, alarm_message)
            sm.current = 'spindle_health_check_active'

        def yetipilot_settings_popup_test():
            m.has_spindle_health_check_run = Mock(return_value=False)
            popup_yetipilot_settings.PopupYetiPilotSettings(sm, l, m, db,
                yp, version=not yp.using_advanced_profile)
            sm.current = 'basic'
        sm = ScreenManager(transition=NoTransition())
        systemtools_sm = Mock()
        systemtools_sm.sm = sm
        l = localization.Localization()
        l.load_in_new_language(l.approved_languages[self.lang_idx])
        sett = settings_manager.Settings(sm)
        jd = Mock()
        jd.job_name = ''
        jd.gcode_summary_string = ''
        jd.screen_to_return_to_after_job = ''
        jd.job_gcode_running = []
        m = router_machine.RouterMachine(Cmport, sm, sett, l, jd)
        yp = YetiPilot(screen_manager=sm, machine=m, job_data=jd,
            localization=l)
        db = smartbench_flurry_database_connection.DatabaseEventManager(sm,
            m, sett)
        config_flag = False
        initial_version = 'v2.1.0'
        am = app_manager.AppManagerClass(sm, m, sett, l, jd, db,
            config_flag, initial_version)
        start_seq = Mock()
        home_screen = screen_home.HomeScreen(name='home', screen_manager=sm,
            machine=m, job=jd, settings=sett, localization=l)
        sm.add_widget(home_screen)
        job_feedback_screen = screen_job_feedback.JobFeedbackScreen(name=
            'job_feedback', screen_manager=sm, machine=m, database=db, job=
            jd, localization=l)
        sm.add_widget(job_feedback_screen)
        spindle_shutdown_screen = (screen_spindle_shutdown.
            SpindleShutdownScreen(name='spindle_shutdown', screen_manager=
            sm, machine=m, job=jd, database=db, localization=l))
        sm.add_widget(spindle_shutdown_screen)
        stop_or_resume_decision_screen = (screen_stop_or_resume_decision.
            StopOrResumeDecisionScreen(name='stop_or_resume_job_decision',
            screen_manager=sm, machine=m, job=jd, database=db, localization=l))
        sm.add_widget(stop_or_resume_decision_screen)
        go_screen = screen_go.GoScreen(name='go', screen_manager=sm,
            machine=m, job=jd, app_manager=am, database=db, localization=l,
            yetipilot=yp)
        sm.add_widget(go_screen)
        maintenance_screen = screen_maintenance.MaintenanceScreenClass(name
            ='maintenance', screen_manager=sm, machine=m, localization=l,
            job=jd)
        sm.add_widget(maintenance_screen)
        general_measurement_screen = (screen_general_measurement.
            GeneralMeasurementScreen(name='general_measurement',
            systemtools=systemtools_sm, machine=m))
        sm.add_widget(general_measurement_screen)
        consent_1_screen = wifi_and_data_consent_1.WiFiAndDataConsentScreen1(
            name='consent_1', start_sequence=start_seq, consent_manager=
            self, localization=l)
        sm.add_widget(consent_1_screen)
        pro_plus_safety_screen = screen_pro_plus_safety.ProPlusSafetyScreen(
            name='pro_plus_safety', start_sequence=start_seq,
            screen_manager=sm, localization=l)
        sm.add_widget(pro_plus_safety_screen)
        shc_screen = (screen_spindle_health_check.
            SpindleHealthCheckActiveScreen(name=
            'spindle_health_check_active', screen_manager=sm, localization=
            l, machine=m))
        sm.add_widget(shc_screen)
        stall_jig_screen = screen_stall_jig.StallJigScreen(name='stall_jig',
            systemtools=systemtools_sm, machine=m, job=jd, settings=sett,
            localization=l, calibration_db=db)
        sm.add_widget(stall_jig_screen)
        basic_screen = BasicScreen(name='basic')
        sm.add_widget(basic_screen)
        zhqc_pcb_set_up = z_head_qc_pcb_set_up.ZHeadPCBSetUp(name=
            'qcpcbsetup', sm=sm, m=m)
        sm.add_widget(zhqc_pcb_set_up)
        sm.get_screen('qcpcbsetup'
            ).usb_path = path_to_EC + '/tests/test_resources/media/usb/'
        zhqc_pcb_set_up_outcome = (z_head_qc_pcb_set_up_outcome.
            ZHeadPCBSetUpOutcome(name='qcpcbsetupoutcome', sm=sm, m=m))
        sm.add_widget(zhqc_pcb_set_up_outcome)
        sm.get_screen('qcpcbsetupoutcome'
            ).usb_path = path_to_EC + '/tests/test_resources/media/usb/'
        eval(sys.argv[1] + '()')
        return sm


ScreenTest().run()
