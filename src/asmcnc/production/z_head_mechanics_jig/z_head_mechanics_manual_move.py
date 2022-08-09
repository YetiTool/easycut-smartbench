from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

from asmcnc.comms.yeti_grbl_protocol.c_defines import *

Builder.load_string("""
<ZHeadMechanicsManualMove>:

    load_label:load_label
    pos_label:pos_label

    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)

        Button:
            text: 'Back'
            bold: True
            font_size: dp(25)
            on_press: root.back()

        BoxLayout:
            size_hint_y: 8
            orientation: 'horizontal'
            spacing: dp(30)

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(10)

                Button:
                    text: 'Set power high'
                    font_size: dp(25)
                    bold: True
                    background_color: [0,0,1,1]
                    background_normal: ''
                    on_press: root.set_power_high()

                Button:
                    text: 'Set power low'
                    font_size: dp(25)
                    bold: True
                    background_color: hex('#EAEA00FF')
                    background_normal: ''
                    on_press: root.set_power_low()

                Button:
                    text: 'Energise motor'
                    font_size: dp(25)
                    bold: True
                    background_color: [0,1,0,1]
                    background_normal: ''
                    on_press: root.energise_motor()

                Button:
                    text: 'De-energise motor'
                    font_size: dp(25)
                    bold: True
                    background_color: [1,0,0,1]
                    background_normal: ''
                    on_press: root.de_energise_motor()

            BoxLayout:
                orientation: 'vertical'

                BoxLayout:
                    size_hint_y: 3.3
                    orientation: 'vertical'

                    Label:
                        text: 'Real time load:'
                        font_size: dp(25)

                    Label:
                        id: load_label
                        size_hint_y: 2
                        text: '-'
                        font_size: dp(50)
                        bold: True

                    Label:
                        text: 'Z axis position:'
                        font_size: dp(25)

                    Label:
                        id: pos_label
                        size_hint_y: 2
                        text: '-'
                        font_size: dp(50)
                        bold: True

                Button:
                    text: 'Home'
                    font_size: dp(25)
                    bold: True
                    background_color: hex('#9900FFFF')
                    background_normal: ''
                    on_press: root.home()

            BoxLayout

""")


class ZHeadMechanicsManualMove(Screen):

    def __init__(self, **kwargs):
        super(ZHeadMechanicsManualMove, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

        Clock.schedule_interval(self.update_realtime_labels, 0.1)


    def set_power_high(self):
        self.m.set_motor_current("Z", 25)

    def set_power_low(self):
        self.m.set_motor_current("Z", 13)

    def energise_motor(self):
        self.m.send_command_to_motor("ENABLE MOTOR DRIVERS", motor=TMC_Z, command=SET_MOTOR_ENERGIZED, value=1)

    def de_energise_motor(self):
        self.m.send_command_to_motor("DISABLE MOTOR DRIVERS", motor=TMC_Z, command=SET_MOTOR_ENERGIZED, value=0)


    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('manual_move','manual_move')

    def update_realtime_labels(self, dt):
        if self.m.s.sg_z_motor_axis == -999 or self.m.s.sg_z_motor_axis == None:
            self.load_label.text = '-'
        else:
            self.load_label.text = str(self.m.s.sg_z_motor_axis)

        self.pos_label.text = str(self.m.mpos_z())


    def back(self):
        self.sm.current = 'mechanics'
