from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from asmcnc.production.z_head_mechanics_jig import widget_z_move_mechanics
Builder.load_string(
    """
<ZHeadMechanicsManualMove>:

    load_label:load_label
    pos_label:pos_label

    z_move_container:z_move_container

    phase_one_input:phase_one_input
    phase_two_input:phase_two_input

    BoxLayout:
        orientation: 'vertical'
        padding: dp([0.0125*app.width, 0.0208333333333*app.height])
        spacing: dp(0.0208333333333*app.height)

        Button:
            text: 'Back'
            bold: True
            font_size: dp(0.03125*app.width)
            on_press: root.back()

        BoxLayout:
            size_hint_y: 8
            orientation: 'horizontal'
            spacing: dp(0.0625*app.height)

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(0.0208333333333*app.height)

                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(0.0125*app.width)

                    TextInput:
                        id: phase_one_input
                        font_size: dp(0.03125*app.width)
                        input_filter: 'int'
                        multiline: False

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint_x: 2
                        text: 'Set phase 1 current (Default 25)'
                        text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        bold: True
                        on_press: root.set_phase_one_current()

                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(0.0125*app.width)

                    TextInput:
                        id: phase_two_input
                        font_size: dp(0.03125*app.width)
                        input_filter: 'int'
                        multiline: False

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint_x: 2
                        text: 'Set phase 2 current (Default 13)'
                        text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        bold: True
                        on_press: root.set_phase_two_current()

                Button:
                    text: 'Set power high'
                    font_size: dp(0.03125*app.width)
                    bold: True
                    background_color: [0,0,1,1]
                    background_normal: ''
                    on_press: root.set_power_high()

                Button:
                    text: 'Set power low'
                    font_size: dp(0.03125*app.width)
                    bold: True
                    background_color: hex('#EAEA00FF')
                    background_normal: ''
                    on_press: root.set_power_low()

                Button:
                    text: 'Energise motor'
                    font_size: dp(0.03125*app.width)
                    bold: True
                    background_color: [0,1,0,1]
                    background_normal: ''
                    on_press: root.energise_motor()

                Button:
                    text: 'De-energise motor'
                    font_size: dp(0.03125*app.width)
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
                        font_size: dp(0.03125*app.width)

                    Label:
                        id: load_label
                        size_hint_y: 2
                        text: '-'
                        font_size: dp(0.0625*app.width)
                        bold: True

                    Label:
                        text: 'Z axis position:'
                        font_size: dp(0.03125*app.width)

                    Label:
                        id: pos_label
                        size_hint_y: 2
                        text: '-'
                        font_size: dp(0.0625*app.width)
                        bold: True

                Button:
                    text: 'Home'
                    font_size: dp(0.03125*app.width)
                    bold: True
                    background_color: hex('#9900FFFF')
                    background_normal: ''
                    on_press: root.home()

            BoxLayout:
                padding:[dp(0), dp(0.104166666667*app.height)]

                BoxLayout:
                    id: z_move_container

                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos

"""
    )


class ZHeadMechanicsManualMove(Screen):

    def __init__(self, **kwargs):
        super(ZHeadMechanicsManualMove, self).__init__(**kwargs)
        self.sm = kwargs['sm']
        self.m = kwargs['m']
        z_move_widget = widget_z_move_mechanics.ZMoveMechanics(machine=self
            .m, screen_manager=self.sm)
        self.z_move_container.add_widget(z_move_widget)
        Clock.schedule_interval(self.update_realtime_labels, 0.1)

    def set_phase_one_current(self):
        if self.phase_one_input.text:
            self.sm.get_screen('mechanics').phase_one_current = int(self.
                phase_one_input.text)

    def set_phase_two_current(self):
        if self.phase_two_input.text:
            self.sm.get_screen('mechanics').phase_two_current = int(self.
                phase_two_input.text)

    def set_power_high(self):
        self.m.set_motor_current('Z', 25)

    def set_power_low(self):
        self.m.set_motor_current('Z', 13)

    def energise_motor(self):
        self.m.send_command_to_motor('ENABLE MOTOR DRIVERS', motor=TMC_Z,
            command=SET_MOTOR_ENERGIZED, value=1)

    def de_energise_motor(self):
        self.m.send_command_to_motor('DISABLE MOTOR DRIVERS', motor=TMC_Z,
            command=SET_MOTOR_ENERGIZED, value=0)

    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('manual_move', 'manual_move')

    def update_realtime_labels(self, dt):
        if (self.m.s.sg_z_motor_axis == -999 or self.m.s.sg_z_motor_axis ==
            None):
            self.load_label.text = '-'
        else:
            self.load_label.text = str(self.m.s.sg_z_motor_axis)
        self.pos_label.text = str(self.m.mpos_z())

    def back(self):
        self.sm.current = 'mechanics'
