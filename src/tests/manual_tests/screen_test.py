 # -*- coding: utf-8 -*-

from kivy.config import Config
from kivy.clock import Clock
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'maxfps', '60')
Config.set('kivy', 'KIVY_CLOCK', 'interrupt')
Config.write()

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from asmcnc.comms import localization

try: 
    from mock import Mock, MagicMock

except: 
    pass

from asmcnc.comms import router_machine

from asmcnc.apps.systemTools_app.screens.calibration.screen_overnight_test import OvernightTesting

from asmcnc.comms.yeti_grbl_protocol.c_defines import *

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
        sett = Mock()
        sett.ip_address = ''

        # Initialise 'j'ob 'd'ata object
        jd = Mock()

        calibration_db = Mock()

        # Initialise 'm'achine object
        # m = router_machine.RouterMachine(Cmport, sm, sett, l, jd)
        m = Mock()

        test_screen = OvernightTesting(name='overnight_testing', m = m, systemtools = systemtools_sm, calibration_db = calibration_db, sm = systemtools_sm.sm, l = l)
        sm.add_widget(test_screen)

        sm.current = 'overnight_testing'
        
        # Clock.schedule_once(m.s.start_services, 4)

        return sm

ScreenTest().run()


