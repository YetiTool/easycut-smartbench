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

from asmcnc.production.z_head_qc_jig.z_head_qc_7 import ZHeadQC7

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
        # m = router_machine.RouterMachine(Cmport, sm, sett, l, jd)
        m = Mock()

        sm = ScreenManager(transition=NoTransition())

        z_head_qc_7 = ZHeadQC7(name='qc7', sm = sm, m = m, l = l)
        sm.add_widget(z_head_qc_7)

        sm.current = 'qc7'

        
        Clock.schedule_once(m.s.start_services, 4)

        return sm

ScreenTest().run()


