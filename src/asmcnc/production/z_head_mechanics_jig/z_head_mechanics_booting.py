from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
Builder.load_string(
    """
<ZHeadMechanicsBooting>:

    Label:
        text: 'Booting...'
        font_size: dp(40)

"""
    )


def log(message):
    timestamp = datetime.now()
    print(timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message))


class ZHeadMechanicsBooting(Screen):

    def __init__(self, **kwargs):
        self.sm = kwargs.pop('sm')
        self.m = kwargs.pop('m')
        super(ZHeadMechanicsBooting, self).__init__(**kwargs)

    def on_enter(self):
        Clock.schedule_once(self.next_screen, 5)

    def next_screen(self, dt):
        try:
            self.sm.get_screen('mechanics'
                ).z_axis_max_travel = -self.m.s.setting_132
            self.sm.get_screen('mechanics'
                ).z_axis_max_speed = self.m.s.setting_112
            self.m.send_command_to_motor('DISABLE MOTOR DRIVERS', motor=
                TMC_Z, command=SET_MOTOR_ENERGIZED, value=0)
            self.sm.current = 'mechanics'
        except:
            Clock.schedule_once(self.next_screen, 1)
            log('Failed to read grbl settings, retrying')
