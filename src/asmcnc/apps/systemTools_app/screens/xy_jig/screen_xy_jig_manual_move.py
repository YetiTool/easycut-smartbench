from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from asmcnc.apps.maintenance_app.widget_maintenance_xy_move import MaintenanceXYMove

Builder.load_string("""
<XYJigManualMove>:

    load_label:load_label
    pos_label:pos_label
    pos_label_header:pos_label_header
    phase_one_current_label:phase_one_current_label
    phase_two_current_label:phase_two_current_label

    xy_move_container:xy_move_container

    phase_one_input:phase_one_input
    phase_two_input:phase_two_input

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

                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(10)

                    TextInput:
                        id: phase_one_input
                        font_size: dp(25)
                        input_filter: 'int'
                        multiline: False

                    Button:
                        id: phase_one_current_label
                        size_hint_x: 2
                        text: 'Set phase 1 current (Default 25)'
                        text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        bold: True
                        on_press: root.set_phase_one_current()

                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(10)

                    TextInput:
                        id: phase_two_input
                        font_size: dp(25)
                        input_filter: 'int'
                        multiline: False

                    Button:
                        id: phase_two_current_label
                        size_hint_x: 2
                        text: 'Set phase 2 current (Default 13)'
                        text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        bold: True
                        on_press: root.set_phase_two_current()

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
                    on_press: root.energise_motors()

                Button:
                    text: 'De-energise motor'
                    font_size: dp(25)
                    bold: True
                    background_color: [1,0,0,1]
                    background_normal: ''
                    on_press: root.de_energise_motors()

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
                        id: pos_label_header
                        text: 'Axis position:'
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

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(10)

                BoxLayout:
                    id: xy_move_container
                    size_hint_y: 4

                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos

                Button:
                    text: 'GRBL Reset'
                    font_size: dp(25)
                    bold: True
                    on_press: root.grbl_reset()

""")


class XYJigManualMove(Screen):

    update_realtime_load_event = None

    phase_one_current = 0
    phase_two_current = 0

    de_energise_on_entry = False

    def __init__(self, **kwargs):
        super(XYJigManualMove, self).__init__(**kwargs)

        self.systemtools_sm = kwargs['systemtools']
        self.m = kwargs['m']

        axis = kwargs['axis']
        self.axis = axis[0] # axis is passed as 'Y', 'X_single', or 'X_double'

        if axis == 'Y':
            self.phase_one_current = 23
            self.phase_two_current = 14
        else:
            if 'single' in axis:
                self.phase_one_current = 13
            elif 'double' in axis:
                self.phase_one_current = 20

            self.phase_two_current = 6

        self.pos_label_header.text = self.axis + ' axis position:'

        self.phase_one_current_label.text = 'Set phase 1 current (Default %s)' % self.phase_one_current
        self.phase_two_current_label.text = 'Set phase 2 current (Default %s)' % self.phase_two_current

        xy_move_widget = MaintenanceXYMove(machine=self.m, screen_manager=self.systemtools_sm.sm)
        self.xy_move_container.add_widget(xy_move_widget)

        self.update_realtime_load_event = Clock.schedule_interval(self.update_realtime_labels, 0.1)


    def on_enter(self):
        if self.de_energise_on_entry:
            self.de_energise_on_entry = False
            self.de_energise_motors()


    def set_phase_one_current(self):
        if self.phase_one_input.text:
            self.systemtools_sm.sm.get_screen('xy_jig').phase_one_current = int(self.phase_one_input.text)

    def set_phase_two_current(self):
        if self.phase_two_input.text:
            self.systemtools_sm.sm.get_screen('xy_jig').phase_two_current = int(self.phase_two_input.text)

    def set_power_high(self):
        self.m.set_motor_current(self.axis, self.phase_one_current)

    def set_power_low(self):
        self.m.set_motor_current(self.axis, self.phase_two_current)

    def energise_motors(self):
        self.m.enable_y_motors()
        self.m.enable_x_motors()

    def de_energise_motors(self):
        self.m.disable_y_motors()
        self.m.disable_x_motors()


    def home(self):
        self.energise_motors()
        self.de_energise_on_entry = True
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('xy_jig_manual_move','xy_jig_manual_move')

    def update_realtime_labels(self, dt):
        if self.axis == 'Y':
            sg_value = self.m.s.sg_y_axis
            self.pos_label.text = self.m.y_pos_str()
        else:
            sg_value = self.m.s.sg_x_motor_axis
            self.pos_label.text = self.m.x_pos_str()

        if sg_value == -999 or sg_value == None:
            self.load_label.text = '-'
        else:
            self.load_label.text = str(sg_value)


    def grbl_reset(self):
        self.m.resume_from_alarm()


    def back(self):
        self.systemtools_sm.sm.current = 'xy_jig'
