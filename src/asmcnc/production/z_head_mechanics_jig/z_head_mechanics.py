from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from asmcnc.skavaUI import popup_info
from asmcnc.production.z_head_mechanics_jig.popup_z_head_mechanics import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

Builder.load_string("""
<ZHeadMechanics>:

    begin_test_button:begin_test_button
    stop_button:stop_button
    calibrate_button:calibrate_button

    test_progress_label:test_progress_label

    load_up_peak:load_up_peak
    load_down_peak:load_down_peak
    load_up_average:load_up_average
    load_down_average:load_down_average
    load_realtime:load_realtime
    current_realtime:current_realtime

    load_graph:load_graph

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'
            padding: dp(5)
            spacing: dp(5)

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(5)

                Button:
                    id: calibrate_button
                    text: 'Calibrate Motor'
                    bold: True
                    font_size: dp(20)
                    background_color: hex('#FF9900FF')
                    background_normal: ''
                    on_press: root.show_calibration_popup()

                Button:
                    id: begin_test_button
                    text: 'Begin Test'
                    bold: True
                    font_size: dp(20)
                    background_color: hex('#00C300FF')
                    background_normal: ''
                    on_press: root.prepare_for_test()

            BoxLayout:
                size_hint_x: 2.5
                orientation: 'horizontal'

                # Load value table
                GridLayout:
                    size_hint_x: 3
                    rows: 3
                    cols: 3

                    Label

                    Label:
                        text: 'Up'
                        bold: True

                    Label:
                        text: 'Down'
                        bold: True

                    Label:
                        text: 'Peak load'
                        text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        bold: True

                    Label:
                        id: load_up_peak
                        text: '-'

                    Label:
                        id: load_down_peak
                        text: '-'

                    Label:
                        text: 'Average load'
                        text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        bold: True

                    Label:
                        id: load_up_average
                        text: '-'

                    Label:
                        id: load_down_average
                        text: '-'

                BoxLayout:
                    orientation: 'vertical'

                    Label:
                        text: 'Realtime load'
                        bold: True
                        text_size: self.size
                        halign: 'center'
                        valign: 'middle'

                    Label:
                        id: load_realtime
                        size_hint_y: 2
                        text: '-'
                        font_size: dp(25)

                BoxLayout:
                    orientation: 'vertical'

                    Label:
                        text: 'Realtime current'
                        bold: True
                        text_size: self.size
                        halign: 'center'
                        valign: 'middle'

                    Label:
                        id: current_realtime
                        size_hint_y: 2
                        text: '-'
                        font_size: dp(25)

            BoxLayout:
                size_hint_x: 0.7
                orientation: 'vertical'
                spacing: dp(5)

                Button:
                    text: 'Serial Monitor'
                    bold: True
                    font_size: dp(20)
                    text_size: self.size
                    valign: 'middle'
                    halign: 'center'
                    background_color: color_provider.get_rgba("grey")
                    background_normal: ''
                    on_press: root.go_to_monitor()

                Button:
                    text: 'Manual Move'
                    bold: True
                    font_size: dp(20)
                    text_size: self.size
                    valign: 'middle'
                    halign: 'center'
                    background_color: hex('#F1C232FF')
                    background_normal: ''
                    on_press: root.go_to_manual_move()

            Button:
                id: stop_button
                text: 'STOP'
                bold: True
                font_size: dp(20)
                background_color: color_provider.get_rgba("monochrome_red")
                background_normal: ''
                on_press: root.stop()

        Label:
            id: test_progress_label
            size_hint_y: 3
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
            height: dp(355)
            width: dp(790)
            x: dp(5)
            y: dp(5)
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

    phase_one_current = 25
    phase_two_current = 13

    def __init__(self, **kwargs):
        super(ZHeadMechanics, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.l = kwargs['l']

        Clock.schedule_interval(self.update_realtime_load, 0.1)

    def prepare_for_test(self):
        self.test_waiting_to_start = True
        self.m.set_motor_current("Z", self.phase_one_current)
        self.current_realtime.text = str(self.phase_one_current)
        self.m.send_command_to_motor("ENABLE MOTOR DRIVERS", motor=TMC_Z, command=SET_MOTOR_ENERGIZED, value=1)

        self.test_running = True
        self.begin_test_button.disabled = True
        self.calibrate_button.disabled = True
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
            Clock.schedule_once(self.begin_test, 1)

    def begin_test(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.jog_absolute_single_axis('Z', -1, self.z_axis_max_speed)
                Clock.schedule_once(self.start_moving_down, 1)
            else:
                Clock.schedule_once(self.begin_test, 0.1)

    def start_moving_down(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.jog_absolute_single_axis('Z', self.z_axis_max_travel, self.z_axis_max_speed / 5)
                Clock.schedule_once(self.record_down_values, 0.4)
            else:
                Clock.schedule_once(self.start_moving_down, 0.1)

    def record_down_values(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.jog_absolute_single_axis('Z', -1, self.z_axis_max_speed / 5)
                Clock.schedule_once(self.record_up_values, 0.4)
            else:
                if self.m.s.sg_z_motor_axis != -999:
                    self.sg_values_down.append(self.m.s.sg_z_motor_axis)
                    self.z_pos_values_down.append(self.m.mpos_z())
                Clock.schedule_once(self.record_down_values, 0.1)

    def record_up_values(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                PopupPhaseTwo(self.sm, self.l)
            else:
                if self.m.s.sg_z_motor_axis != -999:
                    self.sg_values_up.append(self.m.s.sg_z_motor_axis)
                    self.z_pos_values_up.append(self.m.mpos_z())
                Clock.schedule_once(self.record_up_values, 0.1)


    def phase_two(self):
        if self.test_running:
            self.m.set_motor_current("Z", self.phase_two_current)
            self.current_realtime.text = str(self.phase_two_current)
            self.m.jog_absolute_single_axis('Z', self.z_axis_max_travel, self.z_axis_max_speed)
            Clock.schedule_once(self.continue_phase_two, 0.4)

    def continue_phase_two(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.jog_absolute_single_axis('Z', -1, self.z_axis_max_speed)
                Clock.schedule_once(self.finish_test, 0.4)
            else:
                Clock.schedule_once(self.continue_phase_two, 0.1)

    def finish_test(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.set_motor_current("Z", self.phase_one_current)
                self.current_realtime.text = str(self.phase_one_current)
                self.display_results()
                self.reset_after_stop()
            else:
                Clock.schedule_once(self.finish_test, 0.1)

    def display_results(self):
        self.load_up_peak.text = str(max(self.sg_values_up))
        self.load_down_peak.text = str(max(self.sg_values_down))
        self.load_up_average.text = str(sum(self.sg_values_up) / len(self.sg_values_up))
        self.load_down_average.text = str(sum(self.sg_values_down) / len(self.sg_values_down))

        plt.rcParams["figure.figsize"] = (7.9,3.55)
        plt.plot(self.z_pos_values_down, self.sg_values_down, 'b', label='Z SG Down')
        plt.plot(self.z_pos_values_up, self.sg_values_up, 'r', label='Z SG Up')
        plt.legend()
        plt.title('Z motor load vs Z coordinate')
        plt.xlabel('Z coordinate, mm')
        plt.ylabel('Z load')
        ax = plt.gca()
        ax.set_ylim([0, 100])
        ax.set_xlim([min(self.z_pos_values_down + self.z_pos_values_up), max(self.z_pos_values_down + self.z_pos_values_up)])
        loc = plticker.MultipleLocator(base=10)
        ax.yaxis.set_major_locator(loc)
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
        self.calibrate_button.disabled = False
        self.test_progress_label.text = 'Waiting...'

        self.m.send_command_to_motor("DISABLE MOTOR DRIVERS", motor=TMC_Z, command=SET_MOTOR_ENERGIZED, value=0)

        self.sg_values_down = []
        self.sg_values_up = []
        self.z_pos_values_down = []
        self.z_pos_values_up = []


    def show_calibration_popup(self):
        PopupCalibrate(self.sm, self.l)

    def calibrate_motor(self):
        self.load_graph.opacity = 0
        self.begin_test_button.disabled = True
        self.calibrate_button.disabled = True
        self.stop_button.disabled = True
        self.test_progress_label.text = 'Calibrating...'

        self.m.send_command_to_motor("ENABLE MOTOR DRIVERS", motor=TMC_Z, command=SET_MOTOR_ENERGIZED, value=1)
        self.m.calibrate_Z()

        Clock.schedule_once(self.wait_for_calibration_end, 1)

    def wait_for_calibration_end(self, dt):
        if not self.m.run_calibration:
            self.m.send_command_to_motor("DISABLE MOTOR DRIVERS", motor=TMC_Z, command=SET_MOTOR_ENERGIZED, value=0)

            popup_info.PopupInfo(self.sm, self.l, 500, 'Calibration complete!')

            self.begin_test_button.disabled = False
            self.calibrate_button.disabled = False
            self.stop_button.disabled = False
            self.test_progress_label.text = 'Waiting...'
        else:
            Clock.schedule_once(self.wait_for_calibration_end, 1)

    def update_realtime_load(self, dt):
        if self.m.s.sg_z_motor_axis == -999 or self.m.s.sg_z_motor_axis == None:
            self.load_realtime.text = '-'
        else:
            self.load_realtime.text = str(self.m.s.sg_z_motor_axis)


    def go_to_monitor(self):
        self.sm.get_screen('monitor').parent_screen = 'mechanics'
        self.sm.current = 'monitor'

    def go_to_manual_move(self):
        self.sm.current = 'manual_move'
