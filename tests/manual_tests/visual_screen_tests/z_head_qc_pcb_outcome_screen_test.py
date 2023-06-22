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
python -m tests.manual_tests.visual_screen_tests.z_head_qc_pcb_outcome_screen_test

'''

import sys, os
path_to_EC = os.getcwd()
sys.path.append('./src')
os.chdir('./src')

 from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
 from asmcnc.comms import localization
from asmcnc.comms import router_machine
from settings import settings_manager


from asmcnc.production.z_head_qc_jig import z_head_qc_pcb_set_up_outcome, z_head_qc_pcb_set_up

try: 
    from mock import Mock, MagicMock
    from serial_mock.mock import MockSerial, DummySerial
    from random import randint

except: 
    pass


from asmcnc.comms.yeti_grbl_protocol.c_defines import *

Cmport = 'COM3'

class ScreenTest(App):

    def build(self):

        # Establish screens
        sm = ScreenManager(transition=NoTransition())

        # Localization/language object
        l = localization.Localization()

        # Initialise settings object
        sett = settings_manager.Settings(sm)
        # sett.ip_address = ''

        # Initialise 'j'ob 'd'ata object
        jd = Mock()
        jd.job_name = ""
        jd.gcode_summary_string = ""

        db = Mock()

        # Initialise 'm'achine object
        m = router_machine.RouterMachine(Cmport, sm, sett, l, jd)

        m.s.fw_version = "2.5.5; HW: 35"

        prep_screen = z_head_qc_pcb_set_up.ZHeadPCBSetUp(name='prep', sm = sm, m = m)
        sm.add_widget(prep_screen)
        sm.get_screen('prep').usb_path = path_to_EC + "/tests/test_resources/media/usb/"

        test_screen = z_head_qc_pcb_set_up_outcome.ZHeadPCBSetUpOutcome(name='test', sm = sm, m = m)
        sm.add_widget(test_screen)
        sm.get_screen('test').usb_path = path_to_EC + "/tests/test_resources/media/usb/"
        sm.current = 'test'

        prep = sm.get_screen('prep')
        outcome_screen = sm.get_screen("test")

        outcome_screen.x_current_correct*=prep.check_current(TMC_X1, 0)
        outcome_screen.x_current_correct*=prep.check_current(TMC_X2, 10)
        outcome_screen.y_current_correct*=prep.check_current(TMC_Y1, 12)
        outcome_screen.y_current_correct*=prep.check_current(TMC_Y2, 11)
        outcome_screen.z_current_correct*=prep.check_current(TMC_Z, 2)

        outcome_screen.thermal_coefficients_correct*=prep.check_temp_coeff(TMC_X1, 0)
        outcome_screen.thermal_coefficients_correct*=prep.check_temp_coeff(TMC_X2, 11)
        outcome_screen.thermal_coefficients_correct*=prep.check_temp_coeff(TMC_Y1, 0)
        outcome_screen.thermal_coefficients_correct*=prep.check_temp_coeff(TMC_Y2, 0)
        outcome_screen.thermal_coefficients_correct*=prep.check_temp_coeff(TMC_Z, 0)

        return sm

ScreenTest().run()