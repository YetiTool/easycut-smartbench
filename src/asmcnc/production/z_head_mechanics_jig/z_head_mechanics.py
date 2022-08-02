from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

from asmcnc.skavaUI import widget_status_bar
from asmcnc.comms.yeti_grbl_protocol.c_defines import *

Builder.load_string("""
<ZHeadMechanics>:

    status_container:status_container

    begin_test_button:begin_test_button

    test_progress_label:test_progress_label

    load_up_peak:load_up_peak
    load_down_peak:load_down_peak
    load_up_average:load_up_average
    load_down_average:load_down_average

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.92
            BoxLayout:
                orientation: 'vertical'
                padding: dp(5)
                spacing: dp(5)

                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(5)

                    Button:
                        id: begin_test_button
                        size_hint_x: 2
                        text: 'Begin Test'
                        bold: True
                        font_size: dp(25)
                        background_color: hex('#00C300FF')
                        background_normal: ''
                        on_press: root.begin_test()

                    Button:
                        text: 'STOP'
                        bold: True
                        font_size: dp(25)
                        background_color: [1,0,0,1]
                        background_normal: ''
                        on_press: root.stop()

                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(5)

                    # Load value table
                    GridLayout:
                        size_hint_x: 4
                        rows: 3
                        cols: 3

                        Label

                        Label:
                            text: 'Up'

                        Label:
                            text: 'Down'

                        Label:
                            text: 'Peak load'

                        Label:
                            id: load_up_peak
                            text: '-'

                        Label:
                            id: load_down_peak
                            text: '-'

                        Label:
                            text: 'Average load'

                        Label:
                            id: load_up_average
                            text: '-'

                        Label:
                            id: load_down_average
                            text: '-'

                    Button:
                        text: 'GCODE Monitor'
                        bold: True
                        font_size: dp(25)
                        text_size: self.size
                        valign: 'middle'
                        halign: 'center'
                        on_press: root.go_to_monitor()

                Label:
                    size_hint_y: 2
                    id: test_progress_label
                    text: 'Waiting...'
                    font_size: dp(30)
                    markup: True
                    bold: True
                    text_size: self.size
                    valign: 'middle'
                    halign: 'center'

        # GREEN STATUS BAR

        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos

""")


class ZHeadMechanics(Screen):

    sg_values_down = []
    sg_values_up = []

    test_running = False

    def __init__(self, **kwargs):
        super(ZHeadMechanics, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.l = kwargs['l']

        # Green status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)


    def begin_test(self):
        self.test_running = True
        self.begin_test_button.disabled = True
        self.test_progress_label.text = 'Test running...\n[color=ff0000]WATCH FOR STALL THROUGHOUT ENTIRE TEST[/color]'

        self.load_up_peak.text = '-'
        self.load_down_peak.text = '-'
        self.load_up_average.text = '-'
        self.load_down_average.text = '-'

        self.m.set_motor_current("Z", 25)
        self.m.send_command_to_motor("ENABLE MOTOR DRIVERS", command=SET_MOTOR_ENERGIZED, value=1)

        self.m.jog_absolute_single_axis('Z', -1, self.z_axis_max_speed)
        Clock.schedule_once(self.start_moving_down, 0.4)

    def start_moving_down(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.jog_absolute_single_axis('Z', self.z_axis_max_travel, self.z_axis_max_speed / 5)
                Clock.schedule_once(self.record_down_values, 0.4)
            else:
                Clock.schedule_once(self.start_moving_down, 0.4)

    def record_down_values(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.jog_absolute_single_axis('Z', -1, self.z_axis_max_speed / 5)
                Clock.schedule_once(self.record_up_values, 0.4)
            else:
                if self.m.s.sg_z_motor_axis != -999:
                    self.sg_values_down.append([self.m.s.sg_z_motor_axis, self.m.mpos_z()])
                Clock.schedule_once(self.record_down_values, 0.4)

    def record_up_values(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.phase_two()
            else:
                if self.m.s.sg_z_motor_axis != -999:
                    self.sg_values_up.append([self.m.s.sg_z_motor_axis, self.m.mpos_z()])
                Clock.schedule_once(self.record_up_values, 0.4)


    def phase_two(self):
        if self.test_running:
            self.m.set_motor_current("Z", 13)
            self.m.jog_absolute_single_axis('Z', self.z_axis_max_travel, self.z_axis_max_speed)
            Clock.schedule_once(self.continue_phase_two, 0.4)

    def continue_phase_two(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.jog_absolute_single_axis('Z', -1, self.z_axis_max_speed)
                Clock.schedule_once(self.finish_test, 0.4)
            else:
                Clock.schedule_once(self.continue_phase_two, 0.4)

    def finish_test(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.set_motor_current("Z", 25)
                self.reset_after_stop()
            else:
                Clock.schedule_once(self.finish_test, 0.4)


    def stop(self):
        self.m.soft_stop()
        self.reset_after_stop()
        self.m.stop_from_soft_stop_cancel()

    def reset_after_stop(self):
        self.test_running = False
        self.begin_test_button.disabled = False
        self.test_progress_label.text = 'Waiting...'

        self.m.send_command_to_motor("DISABLE MOTOR DRIVERS", command=SET_MOTOR_ENERGIZED, value=0)

        self.sg_values_down = []
        self.sg_values_up = []


    def go_to_monitor(self):
        self.sm.current = 'monitor'
