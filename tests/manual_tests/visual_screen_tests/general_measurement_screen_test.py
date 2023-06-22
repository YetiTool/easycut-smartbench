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
python -m tests.manual_tests.visual_screen_tests.general_measurement_screen_test
'''

import sys, os
sys.path.append('./src')
os.chdir('./src')

 from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
 from asmcnc.comms import localization
from asmcnc.comms import router_machine
from settings import settings_manager


from asmcnc.apps.systemTools_app.screens.calibration import screen_general_measurement

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

        systemtools_sm = Mock()
        systemtools_sm.sm = sm

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

        m.measured_running_data = [
            [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
            [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
            [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
            [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
            ]

        # CHANGE ME
        test_screen = screen_general_measurement.GeneralMeasurementScreen(name='test', systemtools = systemtools_sm, machine = m)
        sm.add_widget(test_screen)
        sm.current = 'test'

        return sm

ScreenTest().run()