from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from datetime import datetime
from asmcnc.skavaUI import popup_info
import math
import traceback
from time import sleep
import threading
from datetime import datetime

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
    sent_first_data_check:sent_first_data_check
    sent_second_data_check:sent_second_data_check
    retry_first_data_send:retry_first_data_send
    retry_second_data_send:retry_second_data_send

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
                cols: 3

                Label:
                    text: '6 hour data: '
                
                Image:
                    id: sent_first_data_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

                Button:
                    text: 'Retry'
                    on_press: root.send_first_overnight_payload()
                    id: retry_first_data_send

            GridLayout:
                cols: 3

                Label:
                    text: '1 hour data: '
                
                Image:
                    id: sent_second_data_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

                Button:
                    text: 'Retry'
                    on_press: root.send_overnight_post_recal_payload()
                    id: retry_second_data_send

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

    poll_end_of_first_overnight_file_stream = None
    poll_end_of_second_overnight_file_stream = None

    first_overnight_run_data = []
    second_overnight_run_data = []

    def __init__(self, **kwargs):
        super(OvernightTesting, self).__init__(**kwargs)

        self.m = kwargs['m']
        self.systemtools_sm = kwargs['systemtools']
        self.calibration_db = kwargs['calibration_db']
        self.sm = kwargs['sm']
        self.l = kwargs['l']

        self.setup_arrays()
        self.overnight_running = False

        self.statuses = []
        self.stage = "Overnight6HR"

    def on_enter(self):
        self.m.s.FINAL_TEST = True

    def on_leave(self):
        self.m.s.FINAL_TEST = False

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)
        self.overnight_running = False
        if self.poll_end_of_first_overnight_file_stream != None: Clock.unschedule(self.poll_end_of_first_overnight_file_stream)
        if self.poll_end_of_second_overnight_file_stream != None: Clock.unschedule(self.poll_end_of_second_overnight_file_stream)
        self.overnight_test_button.disabled = False

    def send_first_overnight_payload(self):
        serial = self.calibration_db.get_serial_number()
        
        try:
            self.calibration_db.send_overnight_test_calibration(serial, *self.first_overnight_run_data)
            self.sent_first_data_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        except:
            self.sent_first_data_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
            print(traceback.format_exc())


    def send_overnight_post_recal_payload(self):
        serial = self.calibration_db.get_serial_number()
        
        try:
            self.calibration_db.send_overnight_test_post_recalibration(serial, *self.second_overnight_run_data)
            self.sent_second_data_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        except:
            self.sent_second_data_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
            print(traceback.format_exc())

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
            # filename = './asmcnc/apps/systemTools_app/files/mini_run.gc'

            with open(filename) as f:
                overnight_gcode_pre_scrubbed = f.readlines()

            overnight_gcode = [self.m.quick_scrub(line) for line in overnight_gcode_pre_scrubbed]

            print("Running overnight test...")

            self.m.s.run_skeleton_buffer_stuffer(overnight_gcode)
            self.poll_end_of_first_overnight_file_stream = Clock.schedule_interval(self.post_overnight_first_file_stream, 60)

        else:
            Clock.schedule_once(self.stream_overnight_file, 3)


    def post_overnight_first_file_stream(self, dt):

        if self.m.state().startswith('Idle'):

            if self.m.s.NOT_SKELETON_STUFF and not self.m.s.is_job_streaming and not self.m.s.is_stream_lines_remaining and not self.m.is_machine_paused: 
                Clock.unschedule(self.poll_end_of_first_overnight_file_stream)

                self.overnight_running = False
                self.first_overnight_run_data = self.store_overnight_run_measurements()
                self.send_first_overnight_payload()
                self.retry_first_data_send.disabled = False


    def recalibrate_after_wear_in(self):
        self.m.calibrate_X_Y_and_Z()
        self.poll_for_recalibration_completion = Clock.schedule_interval(self.finish_recalibrating, 5)


    def finish_recalibrating(self, dt):
        if not self.m.run_calibration:
            Clock.unschedule(self.poll_for_recalibration_completion)

            if not self.m.calibration_tuning_fail_info:
                self.stream_post_recal_file(0)

            # else:
            #     self.calibration_label.text = self.m.calibration_tuning_fail_info



    def stream_post_recal_file(self, dt):

        if self.m.state().startswith('Idle') and not self.overnight_running:

            self.overnight_running = True

            filename = './asmcnc/apps/systemTools_app/files/post_recal_test.gc'
            # filename = './asmcnc/apps/systemTools_app/files/mini_run.gc'

            with open(filename) as f:
                post_recal_gcode_pre_scrubbed = f.readlines()

            post_recal_gcode = [self.m.quick_scrub(line) for line in post_recal_gcode_pre_scrubbed]

            print("Running overnight test...")

            self.m.s.run_skeleton_buffer_stuffer(post_recal_gcode)
            self.poll_end_of_second_overnight_file_stream = Clock.schedule_interval(self.post_overnight_second_file_stream, 60)

        else:
            Clock.schedule_once(self.stream_post_recal_file, 3)


    def post_overnight_second_file_stream(self, dt):

        if self.m.state().startswith('Idle'):

            if self.m.s.NOT_SKELETON_STUFF and not self.m.s.is_job_streaming and not self.m.s.is_stream_lines_remaining and not self.m.is_machine_paused: 
                Clock.unschedule(self.poll_end_of_second_overnight_file_stream)

                self.overnight_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
                self.overnight_running = False
                self.second_overnight_run_data = self.store_overnight_run_measurements()
                self.send_overnight_post_recal_payload()
                self.retry_second_data_send.disabled = False
                self.overnight_test_button.disabled = False

    # def store_overnight_run_measurements(self):

    #     persistent_array = [self.x_vals, self.y_vals, self.z_vals]
    #     self.setup_arrays()

    #     return persistent_array

    def measure(self):
        if not self.overnight_running:
            return

        cur_pos_x = self.m.mpos_x()
        cur_pos_y = self.m.mpos_y()
        cur_pos_z = self.m.mpos_z()

        x_dir = 0 if len(self.x_vals) > 0 and self.x_vals[len(self.x_vals - 1)][1] < cur_pos_x else 1
        y_dir = 0 if len(self.y_vals) > 0 and self.y_vals[len(self.y_vals - 1)][1] < cur_pos_y else 1
        z_dir = 1 if len(self.z_vals) > 0 and self.z_vals[len(self.z_vals - 1)][1] < cur_pos_z else 0

        x_sg = self.m.s.sg_x_motor_axis
        y_sg = self.m.s.sg_y_axis
        y1_sg = self.m.s.sg_y1_motor
        y2_sg = self.m.s.sg_y2_motor
        z_sg = self.m.s.sg_z_motor_axis

        tmc_temp = self.m.s.motor_driver_temp
        pcb_temp = self.m.s.pcb_temp
        mot_temp = self.m.s.transistor_heatsink_temp

        timestamp = datetime.now()

        status = [self.stage, cur_pos_x, cur_pos_y, cur_pos_z, x_dir, y_dir, z_dir, x_sg, y_sg, y1_sg, y2_sg, z_sg, tmc_temp, pcb_temp, mot_temp, timestamp]

        self.statuses.append(status)