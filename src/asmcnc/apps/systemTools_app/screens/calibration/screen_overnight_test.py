from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from datetime import datetime
from asmcnc.skavaUI import popup_info
import math
import traceback
from time import sleep
import threading

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
    sent_data_check:sent_data_check
    retry_data_send:retry_data_send

    overnight_test_button:overnight_test_button

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

            Button:
                text: 'Home'
                on_press: root.home()

            GridLayout:
                cols: 2
                Button:
                    text: 'Run overnight test (6hr)'
                    on_press: root.start_overnight_test()
                    id: overnight_test_button

                Image:
                    id: overnight_test_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            GridLayout:
                cols: 2

                Label:
                    text: 'Successfully sent data: '
                
                Image:
                    id: sent_data_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            Button:
                text: 'Retry data send'
                on_press: root.send_overnight_payload()
                id: retry_data_send

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

MAX_XY_SPEED = 6000
MAX_Z_SPEED = 750

MAX_Z_DISTANCE = 149
MAX_X_DISTANCE = 1299
MAX_Y_DISTANCE = 2501

class OvernightTesting(Screen):

    poll_end_of_overnight_file_stream = None

    def __init__(self, **kwargs):
        super(OvernightTesting, self).__init__(**kwargs)

        self.m = kwargs['m']
        self.systemtools_sm = kwargs['systemtools']
        self.calibration_db = kwargs['calibration_db']
        self.sm = kwargs['sm']
        self.l = kwargs['l']

        self.setup_arrays()
        self.overnight_running = False

    def on_enter(self):
        self.m.s.FINAL_TEST = True

    def on_leave(self):
        self.m.s.FINAL_TEST = False

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)
        self.overnight_running = False
        if self.poll_end_of_overnight_file_stream != None: Clock.unschedule(self.poll_end_of_overnight_file_stream)
        self.overnight_test_button.disabled = False

    def send_overnight_payload(self):
        serial = self.calibration_db.get_serial_number()
        
        try:
            self.calibration_db.send_overnight_test_calibration(serial, self.x_vals, self.y_vals, self.z_vals)
            self.sent_data_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        except:
            self.sent_data_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
            print(traceback.format_exc())

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

        #sg_y1_motor loads with vector & pos
        self.y1_vals = []
        #raw y1 loads
        self.raw_y1_vals = []

        #sg_y2_motor loads with vector & pos
        self.y2_vals = []
        #raw y2 vals
        self.raw_y2_vals = []

    def back_to_fac_settings(self):
        self.systemtools_sm.open_factory_settings_screen()

    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('overnight_testing','overnight_testing')

    def start_overnight_test(self):

        self.overnight_test_button.disabled = True

        self.m.jog_absolute_xy(self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000)
        self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)

        Clock.schedule_once(self.stream_overnight_file, 5)

    def stream_overnight_file(self, dt):

        if self.m.state().startswith('Idle') and not self.overnight_running:

            self.overnight_running = True

            filename = './asmcnc/apps/systemTools_app/files/overnight_test.gc'

            with open(filename) as f:
                overnight_gcode_pre_scrubbed = f.readlines()

            overnight_gcode = [self.m.quick_scrub(line) for line in overnight_gcode_pre_scrubbed]

            print("Running overnight test...")

            self.m.s.run_skeleton_buffer_stuffer(overnight_gcode)
            self.poll_end_of_overnight_file_stream = Clock.schedule_interval(self.post_overnight_file_stream, 60)

        else:
            Clock.schedule_once(self.stream_overnight_file, 3)


    def post_overnight_file_stream(self, dt):

        if self.m.state().startswith('Idle'):

            if self.m.s.NOT_SKELETON_STUFF and not self.m.s.is_job_streaming and not self.m.s.is_stream_lines_remaining and not self.m.is_machine_paused: 
                Clock.unschedule(self.poll_end_of_overnight_file_stream)

                self.overnight_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
                self.overnight_running = False
                self.send_overnight_payload()
                self.retry_data_send.disabled = False
                self.overnight_test_button.disabled = False


    # def run_overnight_test(self):
    #     self.overnight_running = True
    #     self.overnight_test_button.disabled = True
    #     self.OVERNIGHT_TIME_TO_RUN = 21600 #21600

    #     X_TOTAL_TIME = MAX_X_DISTANCE / MAX_XY_SPEED

    #     Z_TOTAL_TIME = MAX_Z_DISTANCE / MAX_Z_SPEED

    #     Y_TOTAL_TIME = MAX_Y_DISTANCE / MAX_XY_SPEED 

    #     self.OVERNIGHT_RECTANGLE_TIME = (((X_TOTAL_TIME * 60) + (Z_TOTAL_TIME * 60) + (Y_TOTAL_TIME * 60)) * 2) + 10

    #     self.OVERNIGHT_TOTAL_RUNS = 0

    #     self.OVERNIGHT_REQUIRED_RUNS = math.ceil(self.OVERNIGHT_TIME_TO_RUN / self.OVERNIGHT_RECTANGLE_TIME)

    #     def run_rectangle(dt):

    #         if not self.overnight_running:
    #             Clock.unschedule(self.OVERNIGHT_CLOCK)
    #             return

    #         if self.OVERNIGHT_TOTAL_RUNS == self.OVERNIGHT_REQUIRED_RUNS:
    #             Clock.unschedule(self.OVERNIGHT_CLOCK)
    #             self.overnight_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
    #             self.overnight_running = False
    #             self.send_overnight_payload()
    #             self.retry_data_send.disabled = False
    #             self.overnight_test_button.disabled = False
    #             return


    #             self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit - MAX_Z_DISTANCE, MAX_Z_SPEED)
    #             self.m.jog_absolute_single_axis('Y', self.m.y_min_jog_abs_limit + MAX_Y_DISTANCE, MAX_XY_SPEED)
    #             self.m.jog_absolute_single_axis('X', self.m.x_min_jog_abs_limit + MAX_X_DISTANCE, MAX_XY_SPEED)

    #             self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, MAX_Z_SPEED)
    #             self.m.jog_absolute_single_axis('Y', self.m.y_min_jog_abs_limit, MAX_XY_SPEED)
    #             self.m.jog_absolute_single_axis('X', self.m.x_min_jog_abs_limit, MAX_XY_SPEED)

    #             self.OVERNIGHT_TIME_TO_RUN -= self.OVERNIGHT_RECTANGLE_TIME
    #             self.OVERNIGHT_TOTAL_RUNS += 1

    #             sleep(0.01)

    #         else:
    #             Clock.schedule_once(run_rectangle, 1)


    #     run_rectangle(None)
    #     self.OVERNIGHT_CLOCK = Clock.schedule_interval(run_rectangle, self.OVERNIGHT_RECTANGLE_TIME)

    def measure(self):
        if self.overnight_running:
            if not self.m.s.sg_z_motor_axis == "-999":
                if len(self.z_vals) > 0:
                    cur_pos = self.m.mpos_z()
                    if self.z_vals[len(self.z_vals)-1][1] <  cur_pos:
                        self.z_vals.append([1, float(self.m.mpos_z()), self.m.s.sg_z_motor_axis])
                    else:
                        self.z_vals.append([0, float(self.m.mpos_z()), self.m.s.sg_z_motor_axis])
                else:
                    self.z_vals.append([0, float(self.m.mpos_z()), self.m.s.sg_z_motor_axis])

                self.raw_z_vals.append(self.m.s.sg_z_motor_axis)
                self.z_peak_load.text = "Z: " + str(max(self.raw_z_vals))
                self.z_rt_load.text = "Z: " + str(self.m.s.sg_z_motor_axis)

            if not self.m.s.sg_y_axis == "-999":
                if len(self.y_vals) > 0:
                    cur_pos = self.m.mpos_y()
                    if self.y_vals[len(self.y_vals)-1][1] <  cur_pos:
                        self.y_vals.append([1, float(self.m.mpos_y()), self.m.s.sg_y_axis, self.m.s.sg_y1_motor, self.m.s.sg_y2_motor])
                    else:
                        self.y_vals.append([0, float(self.m.mpos_y()), self.m.s.sg_y_axis, self.m.s.sg_y1_motor, self.m.s.sg_y2_motor])
                else:
                    self.y_vals.append([0, float(self.m.mpos_y()), self.m.s.sg_y_axis, self.m.s.sg_y1_motor, self.m.s.sg_y2_motor])

                self.raw_y_vals.append(self.m.s.sg_y_axis)
                self.raw_y1_vals.append(self.m.s.sg_y1_motor)
                self.raw_y2_vals.append(self.m.s.sg_y2_motor)
                self.y_peak_load.text = "Y: " + str(max(self.raw_y_vals))
                self.y_rt_load.text = "Y: " + str(self.m.s.sg_y_axis)
                self.y1_peak_load.text = "Y: " + str(max(self.raw_y1_vals))
                self.y2_peak_load.text = "Y: " + str(max(self.raw_y2_vals))
                self.y1_rt_load.text = "Y: " + str(self.m.s.sg_y1_motor)
                self.y2_rt_load.text = "Y: " + str(self.m.s.sg_y2_motor)

            if not self.m.s.sg_x_motor_axis == "-999":
                if len(self.x_vals) > 0:
                    cur_pos = self.m.mpos_x()
                    if self.x_vals[len(self.x_vals)-1][1] <  cur_pos:
                        self.x_vals.append([1, float(self.m.mpos_x()), self.m.s.sg_x_motor_axis])
                    else:
                        self.x_vals.append([0, float(self.m.mpos_x()), self.m.s.sg_x_motor_axis])
                else:
                    self.x_vals.append([0, float(self.m.mpos_x()), self.m.s.sg_x_motor_axis])

                self.raw_x_vals.append(self.m.s.sg_x_motor_axis)
                self.x_peak_load.text = "X: " + str(max(self.raw_x_vals))
                self.x_rt_load.text = "X: " + str(self.m.s.sg_x_motor_axis)