import sys
from datetime import datetime

from asmcnc.comms.logging_system.logging_system import Logger
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

from asmcnc.comms.yeti_grbl_protocol.c_defines import *

Builder.load_string("""
<ZHeadMechanicsBooting>:

    Label:
        text: 'Booting...'
        font_size: dp(40)

""")


class ZHeadMechanicsBooting(Screen):

    def __init__(self, **kwargs):
        super(ZHeadMechanicsBooting, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    def on_enter(self):
        Clock.schedule_once(self.next_screen, 5)

    def next_screen(self, dt):
        try:
            if sys.platform != 'darwin' and sys.platform != 'win32':
                self.sm.get_screen('mechanics').z_axis_max_travel = -self.m.s.setting_132
                self.sm.get_screen('mechanics').z_axis_max_speed = self.m.s.setting_112
                self.m.send_command_to_motor("DISABLE MOTOR DRIVERS", motor=TMC_Z, command=SET_MOTOR_ENERGIZED, value=0)
            self.sm.current = 'mechanics'
        except:
            Clock.schedule_once(self.next_screen, 1)
            Logger.exception('Failed to read grbl settings, retrying')
