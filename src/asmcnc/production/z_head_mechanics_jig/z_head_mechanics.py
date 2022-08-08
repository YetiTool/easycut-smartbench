from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

from asmcnc.comms.yeti_grbl_protocol.c_defines import *

import matplotlib.pyplot as plt

Builder.load_string("""
<ZHeadMechanics>:

    begin_test_button:begin_test_button

    test_progress_label:test_progress_label

    load_up_peak:load_up_peak
    load_down_peak:load_down_peak
    load_up_average:load_up_average
    load_down_average:load_down_average

    load_graph:load_graph

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'
            padding: dp(5)
            spacing: dp(5)

            Button:
                id: begin_test_button
                text: 'Begin Test'
                bold: True
                font_size: dp(25)
                background_color: hex('#00C300FF')
                background_normal: ''
                on_press: root.prepare_for_test()

            # Load value table
            GridLayout:
                size_hint_x: 2
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
                size_hint_x: 0.7
                text: 'Serial Monitor'
                bold: True
                font_size: dp(25)
                text_size: self.size
                valign: 'middle'
                halign: 'center'
                on_press: root.go_to_monitor()

            Button:
                text: 'STOP'
                bold: True
                font_size: dp(25)
                background_color: [1,0,0,1]
                background_normal: ''
                on_press: root.stop()

        Label:
            size_hint_y: 3
            id: test_progress_label
            text: 'Waiting...'
            font_size: dp(30)
            markup: True
            bold: True
            text_size: self.size
            valign: 'middle'
            halign: 'center'

    FloatLayout:
        Image:
            id: load_graph
            size_hint: None, None
            height: dp(360)
            width: dp(800)
            allow_stretch: True
            opacity: 0

""")


class ZHeadMechanics(Screen):

    sg_values_down = []
    sg_values_up = []
    z_pos_values_down = []
    z_pos_values_up = []

    test_running = False
    test_waiting_to_start = False

    def __init__(self, **kwargs):
        super(ZHeadMechanics, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.l = kwargs['l']


    def prepare_for_test(self):
        self.test_waiting_to_start = True
        self.m.set_motor_current("Z", 25)
        self.m.send_command_to_motor("ENABLE MOTOR DRIVERS", motor=TMC_Z, command=SET_MOTOR_ENERGIZED, value=1)

        self.test_running = True
        self.begin_test_button.disabled = True
        self.test_progress_label.text = 'Test running...\n[color=ff0000]WATCH FOR STALL THROUGHOUT ENTIRE TEST[/color]'

        self.load_up_peak.text = '-'
        self.load_down_peak.text = '-'
        self.load_up_average.text = '-'
        self.load_down_average.text = '-'
        self.load_graph.opacity = 0

        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('mechanics','mechanics')

    def on_enter(self):
        if self.test_waiting_to_start:
            self.test_waiting_to_start = False
            self.begin_test()

    def begin_test(self):
        self.m.jog_absolute_single_axis('Z', -1, self.z_axis_max_speed)
        Clock.schedule_once(self.start_moving_down, 0.1)

    def start_moving_down(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.jog_absolute_single_axis('Z', self.z_axis_max_travel, self.z_axis_max_speed / 5)
                Clock.schedule_once(self.record_down_values, 0.1)
            else:
                Clock.schedule_once(self.start_moving_down, 0.1)

    def record_down_values(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.jog_absolute_single_axis('Z', -1, self.z_axis_max_speed / 5)
                Clock.schedule_once(self.record_up_values, 0.1)
            else:
                if self.m.s.sg_z_motor_axis != -999:
                    self.sg_values_down.append(self.m.s.sg_z_motor_axis)
                    self.z_pos_values_down.append(self.m.mpos_z())
                Clock.schedule_once(self.record_down_values, 0.1)

    def record_up_values(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.phase_two()
            else:
                if self.m.s.sg_z_motor_axis != -999:
                    self.sg_values_up.append(self.m.s.sg_z_motor_axis)
                    self.z_pos_values_up.append(self.m.mpos_z())
                Clock.schedule_once(self.record_up_values, 0.1)


    def phase_two(self):
        if self.test_running:
            self.m.set_motor_current("Z", 13)
            self.m.jog_absolute_single_axis('Z', self.z_axis_max_travel, self.z_axis_max_speed)
            Clock.schedule_once(self.continue_phase_two, 0.1)

    def continue_phase_two(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.jog_absolute_single_axis('Z', -1, self.z_axis_max_speed)
                Clock.schedule_once(self.finish_test, 0.1)
            else:
                Clock.schedule_once(self.continue_phase_two, 0.1)

    def finish_test(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.set_motor_current("Z", 25)
                self.display_results()
                self.reset_after_stop()
            else:
                Clock.schedule_once(self.finish_test, 0.1)

    def display_results(self):
        self.load_up_peak.text = str(max(self.sg_values_up))
        self.load_down_peak.text = str(max(self.sg_values_down))
        self.load_up_average.text = str(sum(self.sg_values_up) / len(self.sg_values_up))
        self.load_down_average.text = str(sum(self.sg_values_down) / len(self.sg_values_down))

        plt.rcParams["figure.figsize"] = (8,3.6)
        plt.plot(self.z_pos_values_down, self.sg_values_down, 'b', label='Z SG Down')
        plt.plot(self.z_pos_values_up, self.sg_values_up, 'r', label='Z SG Up')
        plt.legend()
        plt.title('Z motor load vs Z coordinate')
        plt.xlabel('Z coordinate, mm')
        plt.ylabel('Z load')
        ax = plt.gca()
        ax.set_ylim([0, 200])
        ax.set_xlim([min(self.z_pos_values_down + self.z_pos_values_up), max(self.z_pos_values_down + self.z_pos_values_up)])
        plt.tight_layout()
        plt.grid()
        plt.savefig('./asmcnc/production/z_head_mechanics_jig/z_head_mechanics_jig_graph.png')
        plt.close()
        self.load_graph.source = './asmcnc/production/z_head_mechanics_jig/z_head_mechanics_jig_graph.png'
        self.load_graph.reload()
        self.load_graph.opacity = 1


    def stop(self):
        self.m.soft_stop()
        self.reset_after_stop()
        self.m.stop_from_soft_stop_cancel()

    def reset_after_stop(self):
        self.test_running = False
        self.begin_test_button.disabled = False
        self.test_progress_label.text = 'Waiting...'

        self.m.send_command_to_motor("DISABLE MOTOR DRIVERS", motor=TMC_Z, command=SET_MOTOR_ENERGIZED, value=0)

        self.sg_values_down = []
        self.sg_values_up = []
        self.z_pos_values_down = []
        self.z_pos_values_up = []


    def go_to_monitor(self):
        self.sm.current = 'monitor'
