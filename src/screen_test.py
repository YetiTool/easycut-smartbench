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

from mock import Mock, MagicMock
from asmcnc.comms import router_machine

from asmcnc.tests.screen_test import TestScreen

from asmcnc.comms.yeti_grbl_protocol.c_defines import *

Cmport = 'COM3'

class ScreenTest(App):

    def build(self):

        # Establish screens
        sm = Mock()

        # Localization/language object
        l = localization.Localization()

        # Initialise settings object
        sett = Mock()
        sett.ip_address = ''

        # Initialise 'j'ob 'd'ata object
        jd = Mock()

        # Initialise 'm'achine object
        m = router_machine.RouterMachine(Cmport, sm, sett, l, jd)

        test_sm = ScreenManager(transition=NoTransition())

        test_screen = TestScreen(name='st', screen_manager = test_sm, machine = m)
        test_sm.add_widget(test_screen)

        test_sm.current = 'st'

        return test_sm

ScreenTest().run()


