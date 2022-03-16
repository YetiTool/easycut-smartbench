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

# from asmcnc.production.lowerbeam_calibration_jig.lowerbeam_calibration_2 import LBCalibration2
from asmcnc.production.z_head_qc_jig.z_head_qc_4 import ZHeadQC4

from asmcnc.comms.yeti_grbl_protocol.c_defines import *

Cmport = 'COM3'

class ScreenTest(App):

    def build(self):

        # Establish screens
        sm = ScreenManager(transition=NoTransition())

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
        m.run_calibration = False
        m.tuning_in_progress = False


        # lb_calibration_2 = LBCalibration2(name = 'lbc2', sm = sm, m = m)
        # sm.add_widget(lb_calibration_2)

        lb_calibration_2 = ZHeadQC4(name = 'lbc2', sm = sm, m = m)
        sm.add_widget(lb_calibration_2)

        sm.current = 'lbc2'

        m.calibration_tuning_fail_info = "I am really really long. If your temps are bad, try again later on but it might be a problem with the PCB. And I am even longer!!"


        def update_label(dt):
            very_long = "I am really really long. If your temps are bad, try again later on but it might be a problem with the PCB"
            sm.get_screen('lbc2').calibration_label.text = very_long

        Clock.schedule_once(update_label, 4)
        # Clock.schedule_once(m.s.start_services, 4)

        return sm

ScreenTest().run()


