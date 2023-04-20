from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from asmcnc.skavaUI import popup_info
from asmcnc.apps.systemTools_app.screens.xy_jig.popup_xy_jig import *

from datetime import datetime

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker as plticker
except Exception as e:
    print(str(e))

Builder.load_string("""
<XYJig>:

    begin_test_button:begin_test_button
    stop_button:stop_button
    calibrate_button:calibrate_button
    exit_button:exit_button

    test_progress_label:test_progress_label

    load_home_peak:load_home_peak
    load_away_peak:load_away_peak
    load_home_average:load_home_average
    load_away_average:load_away_average
    load_realtime:load_realtime
    current_realtime:current_realtime

    load_graph_away:load_graph_away
    load_graph_home:load_graph_home

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
                        text: 'Home'
                        bold: True

                    Label:
                        text: 'Away'
                        bold: True

                    Label:
                        text: 'Peak load'
                        text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        bold: True

                    Label:
                        id: load_home_peak
                        text: '-'

                    Label:
                        id: load_away_peak
                        text: '-'

                    Label:
                        text: 'Average load'
                        text_size: self.size
                        halign: 'center'
                        valign: 'middle'
                        bold: True

                    Label:
                        id: load_home_average
                        text: '-'

                    Label:
                        id: load_away_average
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
                orientation: 'vertical'
                spacing: dp(5)

                Button:
                    text: 'Serial Monitor'
                    bold: True
                    font_size: dp(20)
                    text_size: self.size
                    valign: 'middle'
                    halign: 'center'
                    background_color: hex('#0000FFFF')
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

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(5)

                Button:
                    id: exit_button
                    text: 'Exit'
                    bold: True
                    font_size: dp(20)
                    background_color: hex('#888888FF')
                    background_normal: ''
                    on_press: root.exit()

                Button:
                    id: stop_button
                    text: 'STOP'
                    bold: True
                    font_size: dp(20)
                    background_color: [1,0,0,1]
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
            id: load_graph_away
            size_hint: None, None
            height: dp(175)
            width: dp(790)
            x: dp(5)
            y: dp(185)
            allow_stretch: True
            opacity: 0

        Image:
            id: load_graph_home
            size_hint: None, None
            height: dp(180)
            width: dp(790)
            x: dp(5)
            y: dp(5)
            allow_stretch: True
            opacity: 0

""")


class XYJig(Screen):

    sg_values_away = []
    sg_values_away_motor_1 = []
    sg_values_away_motor_2 = []
    sg_values_home = []
    sg_values_home_motor_1 = []
    sg_values_home_motor_2 = []
    pos_values_away = []
    pos_values_away_motor_1 = []
    pos_values_away_motor_2 = []
    pos_values_home = []
    pos_values_home_motor_1 = []
    pos_values_home_motor_2 = []

    test_running = False
    test_waiting_to_start = False
    calibration_waiting_to_start = False

    phase_one_current = 0
    phase_two_current = 0

    update_realtime_load_event = None

    def __init__(self, **kwargs):
        super(XYJig, self).__init__(**kwargs)

        self.systemtools_sm = kwargs['systemtools']
        self.m = kwargs['m']
        self.l = kwargs['l']

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

        self.update_realtime_load_event = Clock.schedule_interval(self.update_realtime_load, 0.1)

    def enable_motor_drivers(self):
        if self.axis == 'Y':
            self.m.enable_y_motors()
        else:
            self.m.enable_x_motors()

    def disable_motor_drivers(self):
        if self.axis == 'Y':
            self.m.disable_y_motors()
        else:
            self.m.disable_x_motors()

    def prepare_for_test(self):
        self.test_waiting_to_start = True
        self.m.set_motor_current(self.axis, self.phase_one_current)
        self.current_realtime.text = str(self.phase_one_current)
        self.enable_motor_drivers()

        self.test_running = True
        self.begin_test_button.disabled = True
        self.calibrate_button.disabled = True
        self.exit_button.disabled = True
        self.test_progress_label.text = 'Test running...\n[color=ff0000]WATCH FOR STALL THROUGHOUT ENTIRE TEST[/color]'

        self.load_home_peak.text = '-'
        self.load_away_peak.text = '-'
        self.load_home_average.text = '-'
        self.load_away_average.text = '-'
        self.load_graph_away.opacity = 0
        self.load_graph_home.opacity = 0

        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('xy_jig','xy_jig')

    def on_enter(self):
        if self.test_waiting_to_start:
            self.test_waiting_to_start = False

            if self.m.state().startswith("Idle"):
                Clock.schedule_once(self.begin_test, 1)
            else:
                popup_info.PopupError(self.systemtools_sm.sm, self.l, "Machine is not idle! Cannot start test")
                self.reset_after_stop()

        if self.calibration_waiting_to_start:
            self.calibration_waiting_to_start = False
            self.calibrate_motor()

    def begin_test(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.jog_absolute_single_axis(self.axis, -1, self.max_speed)
                Clock.schedule_once(self.start_moving_away, 1)
            else:
                Clock.schedule_once(self.begin_test, 0.1)

    def start_moving_away(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.jog_absolute_single_axis(self.axis, self.max_travel, self.max_speed / 5)
                Clock.schedule_once(self.record_away_values, 0.4)
            else:
                Clock.schedule_once(self.start_moving_away, 0.1)

    def record_away_values(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.jog_absolute_single_axis(self.axis, -1, self.max_speed / 5)
                Clock.schedule_once(self.record_home_values, 0.4)
            else:
                if self.axis == 'Y':
                    sg_value = self.m.s.sg_y_axis
                    sg_value_motor_1 = self.m.s.sg_y1_motor
                    sg_value_motor_2 = self.m.s.sg_y2_motor
                    pos = self.m.mpos_y()
                else:
                    sg_value = self.m.s.sg_x_motor_axis
                    sg_value_motor_1 = self.m.s.sg_x1_motor
                    sg_value_motor_2 = self.m.s.sg_x2_motor
                    pos = self.m.mpos_x()

                if sg_value not in [-999, None]:
                    self.sg_values_away.append(sg_value)
                    self.pos_values_away.append(pos)

                if sg_value_motor_1 not in [-999, None]:
                    self.sg_values_away_motor_1.append(sg_value_motor_1)
                    self.pos_values_away_motor_1.append(pos)

                if sg_value_motor_2 not in [-999, None]:
                    self.sg_values_away_motor_2.append(sg_value_motor_2)
                    self.pos_values_away_motor_2.append(pos)

                Clock.schedule_once(self.record_away_values, 0.1)

    def record_home_values(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                PopupPhaseTwo(self.systemtools_sm.sm, self.l)
            else:
                if self.axis == 'Y':
                    sg_value = self.m.s.sg_y_axis
                    sg_value_motor_1 = self.m.s.sg_y1_motor
                    sg_value_motor_2 = self.m.s.sg_y2_motor
                    pos = self.m.mpos_y()
                else:
                    sg_value = self.m.s.sg_x_motor_axis
                    sg_value_motor_1 = self.m.s.sg_x1_motor
                    sg_value_motor_2 = self.m.s.sg_x2_motor
                    pos = self.m.mpos_x()

                if sg_value not in [-999, None]:
                    self.sg_values_home.append(sg_value)
                    self.pos_values_home.append(pos)

                if sg_value_motor_1 not in [-999, None]:
                    self.sg_values_home_motor_1.append(sg_value_motor_1)
                    self.pos_values_home_motor_1.append(pos)

                if sg_value_motor_2 not in [-999, None]:
                    self.sg_values_home_motor_2.append(sg_value_motor_2)
                    self.pos_values_home_motor_2.append(pos)

                Clock.schedule_once(self.record_home_values, 0.1)


    def phase_two(self):
        if self.test_running:
            self.m.set_motor_current(self.axis, self.phase_two_current)
            self.current_realtime.text = str(self.phase_two_current)
            self.m.jog_absolute_single_axis(self.axis, self.max_travel, self.max_speed)
            Clock.schedule_once(self.continue_phase_two, 0.4)

    def continue_phase_two(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.jog_absolute_single_axis(self.axis, -1, self.max_speed)
                Clock.schedule_once(self.finish_test, 1)
            else:
                Clock.schedule_once(self.continue_phase_two, 0.1)

    def finish_test(self, dt):
        if self.test_running:
            if self.m.state().startswith('Idle'):
                self.m.set_motor_current(self.axis, self.phase_one_current)
                self.current_realtime.text = str(self.phase_one_current)
                self.display_results()
                self.reset_after_stop()
            else:
                Clock.schedule_once(self.finish_test, 0.1)

    def display_results(self):
        self.load_home_peak.text = str(max(self.sg_values_home))
        self.load_away_peak.text = str(max(self.sg_values_away))
        self.load_home_average.text = str(sum(self.sg_values_home) / len(self.sg_values_home))
        self.load_away_average.text = str(sum(self.sg_values_away) / len(self.sg_values_away))

        self.create_graph("Away")
        self.load_graph_away.source = './asmcnc/apps/systemTools_app/screens/xy_jig/xy_jig_graph.png'
        self.load_graph_away.reload()
        self.load_graph_away.opacity = 1

        self.create_graph("Home")
        self.load_graph_home.source = './asmcnc/apps/systemTools_app/screens/xy_jig/xy_jig_graph.png'
        self.load_graph_home.reload()
        self.load_graph_home.opacity = 1

    def create_graph(self, direction):
        if direction == "Away":
            plt.rcParams["figure.figsize"] = (7.9,1.75)
            plt.plot(self.pos_values_away, self.sg_values_away, '--', color='cyan', label='Avg')
            plt.plot(self.pos_values_away_motor_1, self.sg_values_away_motor_1, 'green', label='Motor 1')
            plt.plot(self.pos_values_away_motor_2, self.sg_values_away_motor_2, 'orange', label='Motor 2')
            combined_list = self.pos_values_away + self.pos_values_away_motor_1 + self.pos_values_away_motor_2
        else:
            plt.rcParams["figure.figsize"] = (7.9,1.8)
            plt.plot(self.pos_values_home, self.sg_values_home, '--', color='cyan', label='Avg')
            plt.plot(self.pos_values_home_motor_1, self.sg_values_home_motor_1, 'green', label='Motor 1')
            plt.plot(self.pos_values_home_motor_2, self.sg_values_home_motor_2, 'orange', label='Motor 2')
            plt.legend(bbox_to_anchor=(1, -0.25), loc='lower right')
            combined_list = self.pos_values_home + self.pos_values_home_motor_1 + self.pos_values_home_motor_2

        plt.ylabel(self.axis + ' Load (%s)' % direction)
        ax = plt.gca()
        ax.set_ylim([-20, 20])
        ax.set_xlim([min(combined_list), max(combined_list)])
        loc = plticker.MultipleLocator(base=10)
        ax.yaxis.set_major_locator(loc)
        plt.tight_layout(pad=0.3)
        plt.grid()
        plt.savefig('./asmcnc/apps/systemTools_app/screens/xy_jig/xy_jig_graph.png')
        plt.close()


    def stop(self):
        self.m.soft_stop()
        self.reset_after_stop()
        self.m.stop_from_soft_stop_cancel()

    def reset_after_stop(self):
        self.test_running = False
        self.begin_test_button.disabled = False
        self.calibrate_button.disabled = False
        self.exit_button.disabled = False
        self.test_progress_label.text = 'Waiting...'

        self.disable_motor_drivers()

        self.sg_values_away = []
        self.sg_values_away_motor_1 = []
        self.sg_values_away_motor_2 = []
        self.sg_values_home = []
        self.sg_values_home_motor_1 = []
        self.sg_values_home_motor_2 = []
        self.pos_values_away = []
        self.pos_values_away_motor_1 = []
        self.pos_values_away_motor_2 = []
        self.pos_values_home = []
        self.pos_values_home_motor_1 = []
        self.pos_values_home_motor_2 = []


    def show_calibration_popup(self):
        PopupCalibrate(self.systemtools_sm.sm, self.l)

    def home_then_calibrate_motor(self):
        self.enable_motor_drivers()
        self.calibration_waiting_to_start = True
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('xy_jig','xy_jig')

    def calibrate_motor(self):
        self.load_graph_away.opacity = 0
        self.load_graph_home.opacity = 0
        self.begin_test_button.disabled = True
        self.calibrate_button.disabled = True
        self.exit_button.disabled = True
        self.stop_button.disabled = True
        self.test_progress_label.text = 'Calibrating...'

        if self.axis == 'Y':
            self.m.calibrate_Y(zero_position=False, mod_soft_limits=False, fast=True)
        else:
            self.m.calibrate_X(zero_position=False, mod_soft_limits=False, fast=True)

        Clock.schedule_once(self.wait_for_calibration_end, 1)

    def wait_for_calibration_end(self, dt):
        if not self.m.run_calibration:
            self.disable_motor_drivers()

            popup_info.PopupInfo(self.systemtools_sm.sm, self.l, 500, 'Calibration complete!')

            self.begin_test_button.disabled = False
            self.calibrate_button.disabled = False
            self.exit_button.disabled = False
            self.stop_button.disabled = False
            self.test_progress_label.text = 'Waiting...'
        else:
            Clock.schedule_once(self.wait_for_calibration_end, 1)

    def update_realtime_load(self, dt):
        if self.axis == 'Y':
            sg_value = self.m.s.sg_y_axis
        else:
            sg_value = self.m.s.sg_x_motor_axis

        if sg_value == -999 or sg_value == None:
            self.load_realtime.text = '-'
        else:
            self.load_realtime.text = str(sg_value)


    def go_to_monitor(self):
        self.systemtools_sm.sm.current = 'xy_jig_monitor'

    def go_to_manual_move(self):
        self.systemtools_sm.sm.current = 'xy_jig_manual_move'

    def exit(self):
        if not self.m.state().startswith("Idle"):
            popup_info.PopupWarning(self.systemtools_sm.sm,  self.l, "Please ensure SB is idle")
            return

        # Reset currents
        if self.axis == 'Y':
            current = self.m.TMC_motor[TMC_Y1].ActiveCurrentScale
        else:
            current = self.m.TMC_motor[TMC_X1].ActiveCurrentScale

        self.m.set_motor_current(self.axis, current)

        self.enable_motor_drivers()

        # Unschedule all active events
        if self.update_realtime_load_event:
            Clock.unschedule(self.update_realtime_load_event)
        if self.systemtools_sm.sm.get_screen('xy_jig_manual_move').update_realtime_load_event:
            Clock.unschedule(self.systemtools_sm.sm.get_screen('xy_jig_manual_move').update_realtime_load_event)

        self.systemtools_sm.open_factory_settings_screen()
