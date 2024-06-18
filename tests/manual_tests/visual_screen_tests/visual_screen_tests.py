 # -*- coding: utf-8 -*-

import sys, os

from src.asmcnc.comms.logging_system.logging_system import Logger

if len(sys.argv) != 2:
    Logger.info("Correct usage: python -m tests.manual_tests.visual_screen_tests.visual_screen_tests <test_function_name>")
    sys.exit(0)

from kivy.config import Config
from kivy.clock import Clock
Config.set('kivy', 'keyboard_mode', 'systemanddock')

if sys.platform.startswith("linux"):
    # get screen resolution as "1280x800" or "800x480"
    resolution = os.popen(""" fbset | grep -oP 'mode "\K[^"]+' """).read().strip()
    width, height = resolution.split("x")
    Config.set('graphics', 'width', width)
    Config.set('graphics', 'height', height)
else:
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '480')

Config.set('graphics', 'maxfps', '60')
Config.set('kivy', 'KIVY_CLOCK', 'interrupt')

'''
########################################################
IMPORTANT!!
Run from easycut-smartbench folder, with 
python -m tests.manual_tests.visual_screen_tests.visual_screen_tests <test_function_name>
'''

from tests.manual_tests.visual_screen_tests.screen_maker import ScreenMaker

path_to_EC = os.getcwd()
sys.path.append('./src')
os.chdir('./src')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from asmcnc.comms import localization
from asmcnc.keyboard import custom_keyboard
from asmcnc.comms import router_machine
from settings import settings_manager
from asmcnc.comms import smartbench_flurry_database_connection
from asmcnc.apps import app_manager
from asmcnc.job.yetipilot.yetipilot import YetiPilot
from asmcnc.comms.smart_transfer import server_connection
from asmcnc.core_UI.popup_manager import PopupManager
from asmcnc.core_UI import scaling_utils
from asmcnc.comms.user_settings_manager import UserSettingsManager

from asmcnc.skavaUI import screen_error, screen_rebooting, screen_file_loading, screen_lobby
from asmcnc.skavaUI import screen_job_recovery, screen_nudge, screen_recovery_decision, screen_homing_decision, popup_nudge
from asmcnc.skavaUI import screen_go, screen_job_feedback, screen_home, screen_spindle_shutdown, screen_stop_or_resume_decision
from asmcnc.skavaUI import screen_door, screen_mstate_warning, screen_serial_failure, screen_squaring_active, screen_jobstart_warning
from asmcnc.skavaUI import screen_check_job, popup_info, screen_dust_shoe_alarm
from asmcnc.apps.systemTools_app.screens.calibration import screen_general_measurement
from asmcnc.apps.start_up_sequence.screens import screen_pro_plus_safety
from asmcnc.apps.start_up_sequence.data_consent_app.screens import wifi_and_data_consent_1
from asmcnc.apps.systemTools_app.screens.calibration import screen_stall_jig
from asmcnc.apps.upgrade_app import screen_upgrade, screen_upgrade_successful, screen_already_upgraded
from asmcnc.core_UI.job_go.screens import screen_spindle_health_check
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
    width = Window.width
    height = Window.height if Window.height == 480 else Window.height - 32

    user_settings_manager = UserSettingsManager()

    def get_scaled_width(self, val):
        return scaling_utils.get_scaled_width(val)

    def get_scaled_height(self, val):
        return scaling_utils.get_scaled_height(val)

    def get_scaled_sp(self, val):
        return scaling_utils.get_scaled_sp(val)

    lang_idx = 0
    cycle_languages = True
    cycle_time = 10

    gb = "English (GB)"
    de = "Deutsch (DE)"
    fr = "Français (FR)"
    it = "Italiano (IT)"
    fi = "Suomalainen (FI)"
    pl = "Polski (PL)"
    dk = "Dansk (DK)"
    ko = "한국어 (KO)"
    nl = "Nederlands (NL)"

    test_languages = [
                        gb,
                        de,
                        fr,
                        it, 
                        fi, 
                        pl,
                        dk,
                        ko
                    ]

    # 0 - English (y)
    # 1 - German (y)
    # 2 - French (y)
    # 3 - Italian (y)
    # 4 - Finnish (y)
    # 5 - Polish (y)
    # 6 - Danish (y)
    # 7 - Korean (y)

    fw_version = "2.4.2"

    def give_me_a_PCB(outerSelf, status, alarm_message):

        class YETIPCB(MockSerial):
            simple_queries = {
                "?": status,
                "\x18": "",
                "*LFFFF00": "ok",
                "*LFF0000": "ok",
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

        # Arg-less version if you don't care about statuses
        def set_up_dummy_serial_stateless():
            set_up_dummy_serial("", "")

        # Call with list of screen names to run through multiple screens automatically
        def cycle_through_screens(screen_list):
            def show_next_screen(screen_list, index):
                sm.current = screen_list[index]

                index += 1
                if index >= len(screen_list):
                    Clock.schedule_once(lambda dt: show_next_screen(screen_list, 0), 5)
                else:
                    Clock.schedule_once(lambda dt: show_next_screen(screen_list, index), 5)

            show_next_screen(screen_list, 0)

        # To use this, set the cycle_languages variable to True
        def cycle_through_languages(test_languages):

            def show_next_language(test_languages, index):
                lang = test_languages[index]
                l.load_in_new_language(lang)
                Logger.info("New lang: " + str(lang))
                try:
                    current_screen = sm.get_screen(str(sm.current))
                    current_screen.update_strings()
                    for widget in current_screen.walk():
                        if isinstance(widget, Label):
                            widget.font_name = l.font_regular
                except: 
                    Logger.info(str(sm.current) + " has no update strings function")

                index += 1
                if index >= len(test_languages):
                    Clock.schedule_once(lambda dt: show_next_language(test_languages, 0), self.cycle_time)
                else:
                    Clock.schedule_once(lambda dt: show_next_language(test_languages, index), self.cycle_time)

            show_next_language(test_languages, 0)

        # Call with list of pairs of screen constructors and their names
        def set_up_screens(screen_list):
            for screen, name in screen_list:
                sm.add_widget(screen_maker.create_screen(screen, name))


        # Add tests as functions below

        # REGULAR SCREENS

        def maintenance_app_screen_test():
            # Switch this between Idle and Alarm to test get data error message
            m.state = Mock(return_value='Idle')

            set_up_dummy_serial_stateless()

            m.is_using_sc2 = Mock(return_value=True)
            m.theateam = Mock(return_value=True)
            m.smartbench_is_busy = Mock(return_value=False)

            m.s.digital_spindle_ld_qdA = 0
            m.s.spindle_serial_number = 0
            m.s.spindle_serial_number = 0
            m.s.spindle_production_year = 0
            m.s.spindle_production_week = 0
            m.s.spindle_firmware_version = 0
            m.s.spindle_total_run_time_seconds = 0
            m.s.spindle_brush_run_time_seconds = 0
            m.s.spindle_mains_frequency_hertz = 0

            set_up_screens([[screen_home.HomeScreen, 'home'],
                            [screen_job_feedback.JobFeedbackScreen, 'job_feedback'],
                            [screen_spindle_shutdown.SpindleShutdownScreen, 'spindle_shutdown'],
                            [screen_stop_or_resume_decision.StopOrResumeDecisionScreen, 'stop_or_resume_job_decision'],
                            [screen_go.GoScreen, 'go']])

            landing_tab = 'spindle_health_check_tab'
            sm.get_screen('maintenance').landing_tab = landing_tab
            sm.current = 'maintenance'

        def screen_stop_or_resume_decision_test():

            '''
            This test can be used to check the various cases of the stop/resume decision screen
            '''

            m.is_using_sc2 = Mock(return_value=True)

            set_up_screens([[screen_home.HomeScreen, 'home'],
                            [screen_job_feedback.JobFeedbackScreen, 'job_feedback'],
                            [screen_go.GoScreen, 'go'],
                            [screen_stop_or_resume_decision.StopOrResumeDecisionScreen, 'stop_or_resume_job_decision']])

            sm.get_screen('stop_or_resume_job_decision').return_screen = 'go'

            # sm.get_screen('stop_or_resume_job_decision').reason_for_pause = 'spindle_overload'
            sm.get_screen('stop_or_resume_job_decision').reason_for_pause = 'job_pause'
            # sm.get_screen('stop_or_resume_job_decision').reason_for_pause = 'yetipilot_low_feed'
            # sm.get_screen('stop_or_resume_job_decision').reason_for_pause = 'yetipilot_spindle_data_loss'
            # sm.get_screen('stop_or_resume_job_decision').reason_for_pause = 'spindle_health_check_failed'

            # Set yetipilot initially enabled, to test disable on unpause
            sm.get_screen('go').is_job_started_already = True
            sm.get_screen('go').yp_widget.switch.active = True
            sm.get_screen('go').yp_widget.toggle_yeti_pilot(sm.get_screen('go').yp_widget.switch)

            sm.current = 'stop_or_resume_job_decision'

        def start_up_sequence_test():
            am.start_up.cc = True

            am.start_up.welcome_user = Mock(return_value=True)
            am.start_up.show_user_data_consent = Mock(return_value=True)
            am.start_up.show_warranty_app = Mock(return_value=True)
            am.start_up.show_user_pro_plus_safety = Mock(return_value=True)
            am.start_up.reboot_in_sequence = True

            am.start_up.set_up_sequence()
            # Delete first two unwanted screens from sequence, which the am init set up
            del am.start_up.screen_sequence[:2]
            am.start_up.start_sequence()

            # Automatically place activation code in text input
            serial_number = sm.get_screen('warranty_2').serial_number_label.text
            activation_code = sm.get_screen('warranty_3').generate_activation_code(serial_number)
            sm.get_screen('warranty_3').activation_code.text = str(activation_code)

            set_up_screens([[screen_rebooting.RebootingScreen, 'rebooting']])

        def starting_smartbench_test():
            set_up_screens([[screen_home.HomeScreen, 'home'],
                            [screen_lobby.LobbyScreen, 'lobby']])
            sm.get_screen('starting_smartbench').next_screen = Mock()
            sm.current = 'starting_smartbench'

        def release_notes_test():

            '''
            This test displays the release notes screen with the file stored in easycut-smartbench/src

            If this test does not run properly, try updating the initial_version variable in the main set up code
            '''

            am.start_up.cc = True

            am.start_up.show_release_notes = Mock(return_value=True)

            am.start_up.set_up_sequence()
            # Delete first two unwanted screens from sequence, which the am init set up
            del am.start_up.screen_sequence[:2]
            am.start_up.start_sequence()

        def job_recovery_tests():
            # Set this to None, -1, or 6 for the three cases on the decision screen
            # Set this to 1 to show arc movement message on line selection screen
            # jd.job_recovery_cancel_line = 1
            # jd.job_recovery_cancel_line = None
            jd.job_recovery_cancel_line = -1

            # Choose between following cases to show different error messages on completion
            success, message = True, ''
            # success, message = False, l.get_str('The last positioning declaration was incremental (G91), and therefore this job cannot be recovered.')
            # success, message = False, l.get_str('Job recovery does not currently support arc distance modes. This job contains N, and therefore cannot be recovered.').replace('N', 'G90.1')
            # success, message = False, l.get_str('Job recovery only supports feed rate mode G94. This job contains N, and therefore cannot be recovered.').replace('N', 'G93')
            # success, message = False, l.get_str('This job cannot be recovered! Please check your job for errors.')

            jd.generate_recovery_gcode = Mock(return_value=(success, message))

            # Long filename to check if it fits on screen
            jd.job_recovery_filepath = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHH.gcode'

            os.path.isfile = Mock(return_value=True)

            jd.job_gcode = [
                'G90',
                'G91',
                'G90.1',
                'G93',
                'G1 X1000 Y1000 Z100 F1000',
                'M5'
            ]

            jd.job_recovery_selected_line = -1
            jd.filename = jd.job_recovery_filepath

            m.state = Mock(return_value='Idle')
            m.s.g54_x = 0
            m.s.g54_y = 0

            set_up_screens([[screen_home.HomeScreen, 'home'],
                            [screen_job_recovery.JobRecoveryScreen, 'job_recovery'],
                            [screen_nudge.NudgeScreen, 'nudge'],
                            [screen_recovery_decision.RecoveryDecisionScreen, 'recovery_decision'],
                            [screen_homing_decision.HomingDecisionScreen, 'homing_decision'],
                            [screen_file_loading.LoadingScreen, 'loading']])

            sm.current = 'recovery_decision'

        def homing_decision_test():
            set_up_screens([
                            # [screen_home.HomeScreen, 'home'],
                            # [screen_job_recovery.JobRecoveryScreen, 'job_recovery'],
                            # [screen_nudge.NudgeScreen, 'nudge'],
                            # [screen_recovery_decision.RecoveryDecisionScreen, 'recovery_decision'],
                            [screen_homing_decision.HomingDecisionScreen, 'homing_decision'],
                            # [screen_file_loading.LoadingScreen, 'loading']
                            ])

            sm.current = 'homing_decision'


        def job_recovery_nudge_warning_popup_test():
            set_up_screens([[BasicScreen, 'basic']])
            popup_nudge.PopupNudgeWarning(sm, m, l, '5.05')
            sm.current = 'basic'

        def lobby_update_popup_test():
            set_up_screens([[screen_lobby.LobbyScreen, 'lobby']])
            sm.get_screen('lobby').trigger_update_popup = True
            m.trigger_setup = False
            sm.current = 'lobby'

        def upgrade_screen_test():
            # This number needs to be entered for successful upgrade
            unlock_code = 0

            # Set this to -999 to get "no spindle detected"
            m.s.digital_spindle_ld_qdA = 0
            m.s.spindle_serial_number = 0

            # Change this to decide whether to show "already upgraded" screen
            m.theateam = Mock(return_value=False)
            m.smartbench_model = Mock(return_value='V1.3')
            m.state = Mock(return_value='Idle')

            set_up_screens([[screen_upgrade.UpgradeScreen, 'upgrade'],
                            [screen_upgrade_successful.UpgradeSuccessfulScreen, 'upgrade_successful'],
                            [screen_already_upgraded.AlreadyUpgradedScreen, 'already_upgraded'],
                            [screen_lobby.LobbyScreen, 'lobby'],
                            [screen_pro_plus_safety.ProPlusSafetyScreen, 'pro_plus_safety']])

            sm.get_screen('upgrade').get_correct_unlock_code = Mock(return_value=str(unlock_code))
            sm.get_screen('lobby').carousel.index = 3

            Logger.info(sm.get_screen('upgrade').get_correct_unlock_code())

            sm.current = 'lobby'

        def squaring_active_screen_test():
            set_up_screens([[screen_squaring_active.SquaringScreenActive, 'squaring_active']])
            m.homing_interrupted = False
            m.homing_in_progress = True
            sm.current = 'squaring_active'

        def spindle_shutdown_screen_test():

            # m.stylus_router_choice = "router"
            m.stylus_router_choice = "stylus"

            set_up_screens([[screen_spindle_shutdown.SpindleShutdownScreen, 'spindle_shutdown'],
                            [screen_stop_or_resume_decision.StopOrResumeDecisionScreen, 'stop_or_resume_job_decision']],
                )
            sm.get_screen('spindle_shutdown').time_to_allow_spindle_to_rest = 1000
            sm.current = 'spindle_shutdown'

        def go_screen_reminder_popup_test():
            set_up_dummy_serial_stateless()

            set_up_screens([[screen_go.GoScreen, 'go'],
                            [screen_job_feedback.JobFeedbackScreen, 'job_feedback'],
                            [screen_home.HomeScreen, 'home'],
                            [screen_jobstart_warning.JobstartWarningScreen, 'jobstart_warning']])

            m.reminders_enabled = True

            m.spindle_brush_use_seconds = m.spindle_brush_lifetime_seconds + 1
            m.time_since_z_head_lubricated_seconds = m.time_to_remind_user_to_lube_z_seconds + 1
            m.time_since_calibration_seconds = m.time_to_remind_user_to_calibrate_seconds + 1

            sm.current = 'jobstart_warning'

        def check_job_screen_test():
            set_up_screens([[screen_check_job.CheckingScreen, 'check_job'],
                            [screen_home.HomeScreen, 'home']])

            check_job_screen = sm.get_screen('check_job')

            # Vary these lines to achieve different errors/states
            check_job_screen.entry_screen = 'file_loading'
            # check_job_screen.boundary_check = Mock(side_effect=Exception)
            m.state = Mock(return_value='Idle')
            # check_job_screen.check_gcode = Mock(side_effect=Exception)
            # m.is_connected = Mock(return_value=False)
            # check_job_screen.is_job_within_bounds = Mock(return_value='job is within bounds')
            check_job_screen.error_log = ['error:34']
            jd.job_gcode = ['test']
            # check_job_screen.flag_spindle_off = False
            # check_job_screen.flag_max_feed_rate = True
            # check_job_screen.flag_min_feed_rate = True

            sm.current = 'check_job'

        def usb_error_popup_test():
            set_up_screens([[BasicScreen, 'basic']])

            popup_info.PopupUSBError(sm, l, None)

            sm.current = 'basic'

        def usb_info_popup_tests():
            set_up_screens([[BasicScreen, 'basic']])

            mode = "ejecting"

            if mode == "connected": popup_mode = 'mounted'
            elif mode == "ejected": popup_mode = True
            elif mode == "ejecting": popup_mode = False

            popup_info.PopupUSBInfo(sm, l, popup_mode)

            sm.current = 'basic'

        def job_feedback_screen_test():
            jd.metadata_dict = {}
            jd.pause_duration = "0"
            jd.actual_runtime = "0"
            jd.post_production_notes  = ""
            jd.metadata_dict["Internal Order Code"] = "Project_name"
            jd.metadata_dict["Process Step"] = "Step 1 of 3"
            jd.job_name = "Job name :).gcode"
            set_up_screens([
                            [screen_job_feedback.JobFeedbackScreen, 'job_feedback'],
                            [screen_go.GoScreen, 'go']
                            ])
            sm.current = 'job_feedback'

        # ALARM/ERROR/DOOR

        def alarm_screen_tests():

            '''
            This test is set up to check that alarms trigger (and that the codes and details are presented correctly) as expected,
            when an alarm status is parsed by the serial module (the dummy serial object creates passes this). 

            Stall/alarm pins and alarm parameters can be modified to conduct tests as needed. 

            At some point it might be worth setting up all possible cases/setting up some kind of automated run through of cases. 
            '''

            # For download popup
            m.s.alarm.usb_stick.is_usb_mounted_flag = True

            # STALL ALARMS
            stall_pin = "z"

            # LIMIT ALARMS
            alarm_pin = "y"

            alarm_number = 1

            stall_alarm_test = False

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

            set_up_screens([[screen_home.HomeScreen, 'home']])

            sm.current = 'home'
        
            Clock.schedule_once(m.s.start_services, 0.1)

        def error_screen_tests():

            error_number = 1

            error_message = "error:" + str(error_number) + "\n"

            status = "<Alarm|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:G>\n"

            set_up_dummy_serial(status, error_message)

            set_up_screens([[screen_home.HomeScreen, 'home'],
                            [screen_error.ErrorScreenClass, 'errorScreen']])

            sm.current = 'home'

            m.s.suppress_error_screens = False

            Clock.schedule_once(m.s.start_services, 0.1)

        def door_screen_test():

            door_message = "Door:0\n"

            door_status = "<Door:0|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:G>\n"

            set_up_dummy_serial(door_status, door_message)

            set_up_screens([[screen_home.HomeScreen, 'home'],
                            [screen_door.DoorScreen, 'door']])

            sm.current = 'home'
        
            Clock.schedule_once(m.s.start_services, 0.1)

        def mstate_warning_screen_test():
            # The options are: Alarm, Check, Door, and one for anything else
            m.state = Mock(return_value="Alarm")

            set_up_screens([[screen_mstate_warning.WarningMState, 'mstate']])

            sm.current = 'mstate'
        
            Clock.schedule_once(m.s.start_services, 0.1)

        def serial_failure_screen_test():
            set_up_screens([[screen_home.HomeScreen, 'home'],
                            [screen_serial_failure.SerialFailureClass, 'serialScreen']])

            sm.current = 'home'

            # Choose between these error messages
            m.s.get_serial_screen('Could not establish a connection on startup.')
            # m.s.get_serial_screen('Could not read line from serial buffer.')
            # m.s.get_serial_screen('Could not process grbl response. Grbl scanner has been stopped.')
            # m.s.get_serial_screen('Could not write last command to serial buffer.')

        def dust_shoe_alarm_screen_test():
            m.s.spindle_on = True
            self.user_settings_manager.set_value('dust_shoe_detection', True)

            set_up_screens([[screen_home.HomeScreen, 'home'],
                            [screen_dust_shoe_alarm.DustShoeAlarmScreen, 'dust_shoe_alarm']])

            sm.current = 'home'

            def dust_shoe_unplugged(dt):
                m.s.dustshoe_is_closed = not m.s.dustshoe_is_closed

            Clock.schedule_interval(dust_shoe_unplugged, 5)


        # FACTORY/PRODUCTION SCREENS

        def general_measurement_screen_test():

            ''' 
            This tests the general measrement dev screen available in the factory settings app. Running data is just to pass
            a test dataset for plotting. 
            '''

            m.measured_running_data = [
                [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
                ]

            set_up_screens([[screen_general_measurement.GeneralMeasurementScreen, 'general_measurement']])

            sm.current = 'general_measurement'

        def stall_jig_screen_tests():

            '''
            This tests that an alarm appears and is registered correctly by stall jig, at the same time as suppressing normal alarm screens
            '''

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

            stall_jig_screen = screen_stall_jig.StallJigScreen(name='stall_jig', systemtools = systemtools_sm, machine = m, job = jd, settings = sett, localization = l, calibration_db = db)
            sm.add_widget(stall_jig_screen)

            sm.current = 'stall_jig'
            
            Clock.schedule_once(m.s.start_services, 0.1)

        def z_head_qc_pcb_outcome_screen_test():

            '''
            These parameters can be modified to check that the outcome screen shows passes/fails correctly, and correctly shows values
            '''

            m.s.fw_version = "2.5.5; HW: 35"

            set_up_screens([[z_head_qc_pcb_set_up.ZHeadPCBSetUp, 'qcpcbsetup'],
                            [z_head_qc_pcb_set_up_outcome.ZHeadPCBSetUpOutcome, 'qcpcbsetupoutcome']])

            sm.get_screen('qcpcbsetup').usb_path = path_to_EC + "/tests/test_resources/media/usb/"
            sm.get_screen('qcpcbsetupoutcome').usb_path = path_to_EC + "/tests/test_resources/media/usb/"

            sm.current = 'qcpcbsetupoutcome'

            zhqc_pcb_set_up = sm.get_screen("qcpcbsetup")
            zhqc_pcb_set_up_outcome = sm.get_screen("qcpcbsetupoutcome")

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

            set_up_screens([[z_head_qc_pcb_set_up.ZHeadPCBSetUp, 'qcpcbsetup']])

            sm.current = 'qcpcbsetup'


        # YETIPILOT/PRO+ SCREENS

        def go_screen_sc2_overload_test():

            '''
            Check that overload message triggers correctly
            '''

            alarm_message = "\n"

            killtime = 9
            killtime_status = "<Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:G|Ld:75, 20, " + str(killtime) + ", 240>\n"

            set_up_dummy_serial(killtime_status, alarm_message)

            set_up_screens([[screen_home.HomeScreen, 'home'],
                            [screen_job_feedback.JobFeedbackScreen, 'job_feedback'],
                            [screen_go.GoScreen, 'go']])

            m.is_using_sc2 = Mock(return_value=True)
            m.is_spindle_health_check_active = Mock(return_value=False)
            # m.has_spindle_health_check_failed = Mock(return_value=True)
            sm.get_screen('go').is_job_started_already = False

            sm.current = 'go'
            
            Clock.schedule_once(m.s.start_services, 0.1)

        def job_pause_tests():

            '''
            Check that job pausing happens correctly from go screen, and that correct pause screen gets called
            (Case can be set by the string put into the pause functions)
            '''

            alarm_message = "\n"

            status = "<Run|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:G>\n"

            set_up_dummy_serial(status, alarm_message)

            set_up_screens([[screen_home.HomeScreen, 'home'],
                            [screen_job_feedback.JobFeedbackScreen, 'job_feedback'],
                            [screen_spindle_shutdown.SpindleShutdownScreen, 'spindle_shutdown'],
                            [screen_stop_or_resume_decision.StopOrResumeDecisionScreen, 'stop_or_resume_job_decision'],
                            [screen_go.GoScreen, 'go']])

            sm.current = 'go'

            sm.get_screen('go').start_or_pause_button_image.source = "./asmcnc/skavaUI/img/pause.png"

            Clock.schedule_once(m.s.start_services, 0.1)

            def stream_and_pause(dt=0):
                m.s.is_job_streaming = True
                m.set_pause(True, 'yetipilot_low_feed')
                Logger.info("STOP FOR STREAM PAUSE")
                # m.stop_for_a_stream_pause('yetipilot_spindle_data_loss')

            Clock.schedule_once(stream_and_pause, 5)

        def pro_plus_safety_screen_test():
            set_up_screens([[wifi_and_data_consent_1.WiFiAndDataConsentScreen1, 'consent_1'],
                            [screen_pro_plus_safety.ProPlusSafetyScreen, 'pro_plus_safety']])

            sm.current = 'pro_plus_safety'

        def screen_spindle_health_check_test():
            alarm_message = "\n"
            status = "<Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:G>\n"
            set_up_dummy_serial(status, alarm_message)

            set_up_screens([[screen_spindle_health_check.SpindleHealthCheckActiveScreen, 'spindle_health_check_active']])

            sm.current = 'spindle_health_check_active'

        def yetipilot_settings_popup_test():
            m.has_spindle_health_check_passed = Mock(return_value=False)

            set_up_screens([[BasicScreen, 'basic'],
                            [screen_go.GoScreen, 'go']])

            popup_yetipilot_settings.PopupYetiPilotSettings(sm, l, m, db, yp, version=not yp.using_advanced_profile)
            sm.current = 'basic'


        # Establish screens
        sm = ScreenManager(transition=NoTransition())

        systemtools_sm = Mock()
        systemtools_sm.sm = sm

        # Localization/language object
        l = localization.Localization()
        l.load_in_new_language(l.approved_languages[self.lang_idx])

        kb = custom_keyboard.Keyboard(localization=l)

        # Initialise settings object
        sett = settings_manager.Settings(sm)
        # sett.ip_address = ''

        # Initialise 'j'ob 'd'ata object
        jd = Mock()
        jd.job_name = ""
        jd.gcode_summary_string = ""
        jd.screen_to_return_to_after_job = ""
        jd.job_gcode_running = []
        jd.job_gcode = []

        # Initialise 'm'achine object
        m = router_machine.RouterMachine(Cmport, sm, sett, l, jd)

        # Initialise YP
        yp = YetiPilot(screen_manager=sm, machine=m, job_data=jd, localization=l)

        # Create database object to talk to
        db = smartbench_flurry_database_connection.DatabaseEventManager(sm, m, sett)

        # Popup manager
        pm = PopupManager(sm, m, l)
        sm.pm = pm  # store in screen manager for access by screens

        # App manager object
        config_flag = False
        initial_version = 'v2.7.0'
        am = app_manager.AppManagerClass(sm, m, sett, l, kb, jd, db, config_flag, initial_version, pm)

        # Server connection object
        sc = server_connection.ServerConnection(sett)

        # Popup manager
        pm = PopupManager(sm, m, l)
        sm.pm = pm  # store in screen manager for access by screens

        start_seq = Mock()

        screen_maker = ScreenMaker(sm, l, kb, sett, jd, m, yp, db, am, sc, systemtools_sm, start_seq)

        # Function for test to run is passed as argument
        eval(sys.argv[1] + "()")

        if self.cycle_languages:
            cycle_through_languages(self.test_languages)

        if self.height == 768:
            root = BoxLayout(orientation='vertical', size_hint=(None, None), size=(self.width, self.height + 32))
            sm.size_hint = (None, None)
            sm.size = (self.width, self.height)
            root.add_widget(sm)
            return root

        return sm

ScreenTest().run()