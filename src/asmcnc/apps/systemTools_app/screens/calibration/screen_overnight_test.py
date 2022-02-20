from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from datetime import datetime
from asmcnc.skavaUI import popup_info
import math

Builder.load_string("""
<OvernightTesting>:
    y_rt_load:y_rt_load
    x_rt_load:x_rt_load
    z_rt_load:z_rt_load
    y1_rt_load:y1_rt_load
    y2_rt_load:y2_rt_load

    y_peak_load:y_peak_load
    x_peak_load:x_peak_load
    z_peak_load:z_peak_load
    y1_peak_load:y1_peak_load
    y2_peak_load:y2_peak_load

    overnight_test_check:overnight_test_check

    BoxLayout:
        orientation: 'vertical'

        GridLayout:
            cols: 2

            Button:
                text: 'Back'
                on_press: root.back_to_fac_settings()

            Button:
                text: 'STOP'
                background_color: [1,0,0,1]
                on_press: root.stop()

            GridLayout:
                cols: 2
                Button:
                    text: 'Run overnight test (6hr)'
                    on_press: root.run_overnight_test()

                Image:
                    id: overnight_test_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

        GridLayout:
            cols: 2

            GridLayout:
                rows: 6

                Label:
                    text: 'Real time load:'

                Label:
                    id: y_rt_load
                    text: 'Y:'

                Label:
                    id: y1_rt_load
                    text: 'Y1:'

                Label:
                    id: y2_rt_load
                    text: 'Y2:'

                Label:
                    id: x_rt_load
                    text: 'X:'

                Label:
                    id: z_rt_load
                    text: 'Z:'

            GridLayout:
                rows: 6

                Label:
                    text: 'Peak load:'

                Label:
                    id: y_peak_load
                    text: 'Y:'

                Label:
                    id: y1_peak_load
                    text: 'Y1:'

                Label:
                    id: y2_peak_load
                    text: 'Y2:'

                Label:
                    id: x_peak_load
                    text: 'X:'

                Label:
                    id: z_peak_load
                    text: 'Z:'

""")

MAX_XY_SPEED = 1186
MAX_Z_SPEED = 75

MAX_Z_DISTANCE = 115
MAX_X_DISTANCE = 1135
MAX_Y_DISTANCE = 2275

class OvernightTesting(Screen):
    def __init__(self, **kwargs):
        super(OvernightTesting, self).__init__(**kwargs)

        self.m = kwargs['m']
        self.systemtools_sm = kwargs['systemtools']

        self.setup_arrays()
        self.overnight_running = False

    def on_enter(self):
        self.m.s.FINAL_TEST = True

    def on_exit(self):
        self.m.s.FINAL_TEST = False

    def stop(self):
        self.overnight_running = False
        popup_info.PopupStop(self.m, self.sm, self.l)

    def setup_arrays(self):
        #x loads with vector & pos
        self.x_vals = []
        #raw x loads
        self.raw_x_vals = []

        #z loads with vector & pos
        self.z_vals = []
        #raw z loads
        self.raw_z_vals = []

        #y_motor loads with vector & pos
        self.y_vals = []
        #raw y_motor loads
        self.raw_y_vals = []

        #y1_motor loads with vector & pos
        self.y1_vals = []
        #raw y1 loads
        self.raw_y1_vals = []

        #y2_motor loads with vector & pos
        self.y2_vals = []
        #raw y2 vals
        self.raw_y2_vals = []

    def back_to_fac_settings(self):
        self.systemtools_sm.open_factory_settings_screen()

    def run_overnight_test(self):
        self.overnight_running = True
        self.OVERNIGHT_TIME_TO_RUN = 21600

        X_TOTAL_TIME = MAX_X_DISTANCE / MAX_XY_SPEED

        Z_TOTAL_TIME = MAX_Z_DISTANCE / MAX_Z_SPEED

        Y_TOTAL_TIME = MAX_Y_DISTANCE / MAX_XY_SPEED

        self.OVERNIGHT_RECTANGLE_TIME = ((X_TOTAL_TIME * 60) + (Z_TOTAL_TIME * 60) + (Y_TOTAL_TIME * 60)) * 2

        self.OVERNIGHT_TOTAL_RUNS = 0

        self.OVERNIGHT_REQUIRED_RUNS = math.ceil(self.OVERNIGHT_TIME_TO_RUN / self.OVERNIGHT_RECTANGLE_TIME)

        def run_rectangle(dt):
            if not self.overnight_running:
                Clock.unschedule(self.OVERNIGHT_CLOCK)
                return

            if self.OVERNIGHT_TOTAL_RUNS == self.OVERNIGHT_REQUIRED_RUNS:
                Clock.unschedule(self.OVERNIGHT_CLOCK)
                self.overnight_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
                self.overnight_running = False

            self.m.jog_relative('Z', -MAX_Z_DISTANCE, MAX_Z_SPEED)
            self.m.jog_relative('X', MAX_X_DISTANCE, MAX_XY_SPEED)
            self.m.jog_relative('Y', MAX_Y_DISTANCE, MAX_XY_SPEED)

            self.m.jog_relative('Z', MAX_Z_DISTANCE, MAX_Z_SPEED)
            self.m.jog_relative('X', -MAX_X_DISTANCE, MAX_XY_SPEED)
            self.m.jog_relative('Y', -MAX_Y_DISTANCE, MAX_XY_SPEED)

            self.OVERNIGHT_TIME_TO_RUN -= self.OVERNIGHT_RECTANGLE_TIME
            self.OVERNIGHT_TOTAL_RUNS += 1

        run_rectangle(None)
        self.OVERNIGHT_CLOCK = Clock.schedule_interval(run_rectangle, self.OVERNIGHT_RECTANGLE_TIME)

    def measure(self):
        if self.overnight_running:
            if not self.m.s.z_motor_axis == "-999":
                if len(self.z_vals) > 0:
                    cur_pos = self.m.mpos_z()
                    if self.z_vals[len(self.z_vals)-1][1] <  cur_pos:
                        self.z_vals.append(['Z+', self.m.s.m_z, self.m.s.z_motor_axis])
                    else:
                        self.z_vals.append(['Z-', self.m.s.m_z, self.m.s.z_motor_axis])
                else:
                    self.z_vals.append(['Z-', self.m.s.m_z, self.m.s.z_motor_axis])

                self.raw_z_vals.append(self.m.s.z_motor_axis)
                self.z_peak_load.text = "Z: " + str(max(self.raw_z_vals))
                self.z_rt_load.text = "Z: " + str(self.m.s.z_motor_axis)

            if not self.m.s.y_axis == "-999":
                if len(self.y_vals) > 0:
                    cur_pos = self.m.mpos_y()
                    if self.y_vals[len(self.y_vals)-1][1] <  cur_pos:
                        self.y_vals.append(['Y+', self.m.mpos_y(), self.m.s.y_axis, self.m.s.y1_motor, self.m.s.y2_motor])
                    else:
                        self.y_vals.append(['Y-', self.m.mpos_y(), self.m.s.y_axis, self.m.s.y1_motor, self.m.s.y2_motor])
                else:
                    self.y_vals.append(['Y-', self.m.mpos_y(), self.m.s.y_axis, self.m.s.y1_motor, self.m.s.y2_motor])

                self.raw_y_vals.append(self.m.s.y_axis)
                self.raw_y1_vals.append(self.m.s.y1_motor)
                self.raw_y2_vals.append(self.m.s.y2_motor)
                self.y_peak_load.text = "Y: " + str(max(self.raw_y_vals))
                self.y_rt_load.text = "Y: " + str(self.m.s.y_axis)
                self.y1_peak_load.text = "Y: " + str(max(self.raw_y1_vals))
                self.y2_peak_load.text = "Y: " + str(max(self.raw_y2_vals))
                self.y1_rt_load.text = "Y: " + str(self.m.s.y1_motor)
                self.y2_rt_load.text = "Y: " + str(self.m.s.y2_motor)

            if not self.m.s.x_motor_axis == "-999":
                if len(self.x_vals) > 0:
                    cur_pos = self.m.mpos_x()
                    if self.x_vals[len(self.x_vals)-1][1] <  cur_pos:
                        self.x_vals.append(['X+', self.m.mpos_x(), self.m.s.x_motor_axis])
                    else:
                        self.x_vals.append(['X-', self.m.mpos_x(), self.m.s.x_motor_axis])
                else:
                    self.x_vals.append(['X-', self.m.mpos_x(), self.m.s.x_motor_axis])

                self.raw_x_vals.append(self.m.s.x_motor_axis)
                self.x_peak_load.text = "X: " + str(max(self.raw_x_vals))
                self.x_rt_load.text = "X: " + str(self.m.s.x_motor_axis)