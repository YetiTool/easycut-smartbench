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
python -m tests.manual_tests.visual_screen_tests.z_head_qc_pcb_set_up_screen_test
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


from asmcnc.production.z_head_qc_jig import z_head_qc_pcb_set_up

try: 
    from mock import Mock, MagicMock
    from serial_mock.mock import MockSerial, DummySerial
    from random import randint

except: 
    pass

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

        # CHANGE ME
        test_screen = z_head_qc_pcb_set_up.ZHeadPCBSetUp(name='test', sm = sm, m = m)
        sm.add_widget(test_screen)
        sm.get_screen('test').usb_path = path_to_EC + "/tests/test_resources/media/usb/"
        sm.current = 'test'

        return sm

ScreenTest().run()