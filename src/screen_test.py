from kivy.config import Config
from kivy.clock import Clock

Config.set("kivy", "keyboard_mode", "systemanddock")
Config.set("graphics", "width", "800")
Config.set("graphics", "height", "480")
Config.set("graphics", "maxfps", "60")
Config.set("kivy", "KIVY_CLOCK", "interrupt")
Config.write()
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from .asmcnc.comms import localization

try:
    from mock import Mock, MagicMock
except:
    pass
from .asmcnc.comms import router_machine
from .asmcnc.apps.systemTools_app.screens.calibration.screen_overnight_test import (
    OvernightTesting,
)
from .asmcnc.comms.yeti_grbl_protocol.c_defines import *

Cmport = "COM3"


class ScreenTest(App):

    def build(self):
        sm = ScreenManager(transition=NoTransition())
        systemtools_sm = Mock()
        systemtools_sm.sm = sm
        l = localization.Localization()
        sett = Mock()
        sett.ip_address = ""
        jd = Mock()
        calibration_db = Mock()
        m = Mock()
        test_screen = OvernightTesting(
            name="overnight_testing",
            m=m,
            systemtools=systemtools_sm,
            calibration_db=calibration_db,
            sm=systemtools_sm.sm,
            l=l,
        )
        sm.add_widget(test_screen)
        sm.current = "overnight_testing"
        return sm


ScreenTest().run()
