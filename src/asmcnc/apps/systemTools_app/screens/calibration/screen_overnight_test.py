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

from asmcnc.apps.systemTools_app.screens.calibration import widget_sg_status_bar

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

    six_hour_wear_in_button : six_hour_wear_in_button
    six_hour_wear_in_checkbox : six_hour_wear_in_checkbox
    recalibration_button : recalibration_button
    recalibration_checkbox : recalibration_checkbox
    fully_calibrated_run_button : fully_calibrated_run_button
    fully_calibrated_run_checkbox : fully_calibrated_run_checkbox
    retry_six_hour_wear_in_data_send : retry_six_hour_wear_in_data_send
    sent_six_hour_wear_in_data : sent_six_hour_wear_in_data
    retry_recalibration_data_send : retry_recalibration_data_send
    sent_recalibration_data : sent_recalibration_data
    retry_fully_calibrated_run_data_send : retry_fully_calibrated_run_data_send
    sent_fully_recalibrated_run_data : sent_fully_recalibrated_run_data

    status_container : status_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: 0.92
            orientation: 'vertical'

            BoxLayout:
                orientation: 'vertical'
                size_hint_y: 0.5   

                BoxLayout: 
                    orientation: 'horizontal'
                    size_hint_y: 0.26

                    Button:
                        text: 'Back'
                        on_press: root.back_to_fac_settings()

                    Button:
                        text: 'Home'
                        on_press: root.home()
                        background_color: [0,0,1,1]

                    Button:
                        id: overnight_test_button
                        text: 'START'
                        on_press: root.start_overnight_test()
                        background_color: [0,1,0,1]

                    Button:
                        text: 'STOP'
                        background_color: [1,0,0,1]
                        on_press: root.stop()
                        background_normal: ''

                Label: 
                    text: "Overnight test stages"
                    markup: True
                    halign: "center"
                    size_hint_y: 0.11

                BoxLayout: 
                    orientation: 'horizontal'
                    size_hint_y: 0.26

                    BoxLayout: 
                        orientation: 'horizontal'

                        Button:
                            id: six_hour_wear_in_button
                            text: '6 hour wear-in'
                            size_hint_x: 0.7
                            on_press: root.start_six_hour_wear_in()



                        BoxLayout:
                            size_hint_x: 0.3

                            Image:
                                id: six_hour_wear_in_checkbox
                                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True

                    BoxLayout: 
                        orientation: 'horizontal'

                        Button:
                            id: recalibration_button
                            text: 're-calibration'
                            size_hint_x: 0.7
                            on_press: root.start_recalibration()


                        BoxLayout:
                            size_hint_x: 0.3

                            Image:
                                id: recalibration_checkbox
                                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                    BoxLayout: 
                        orientation: 'horizontal'

                        Button:
                            id: fully_calibrated_run_button
                            text: 'post-calibration run'
                            size_hint_x: 0.7
                            on_press: root.start_fully_calibrated_final_run()


                        BoxLayout:
                            size_hint_x: 0.3

                            Image:
                                id: fully_calibrated_run_checkbox
                                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True

                Label: 
                    text: "Data sends"
                    markup: True
                    halign: "center"
                    size_hint_y: 0.11

                BoxLayout: 
                    orientation: 'horizontal'
                    size_hint_y: 0.26

                    BoxLayout: 
                        orientation: 'horizontal'

                        Button:
                            id: retry_six_hour_wear_in_data_send
                            text: 'Retry'
                            size_hint_x: 0.7
                            on_press: root.send_six_hour_wear_in_data()


                        BoxLayout:
                            size_hint_x: 0.3

                            Image:
                                id: sent_six_hour_wear_in_data
                                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True

                    BoxLayout: 
                        orientation: 'horizontal'

                        Button:
                            id: retry_recalibration_data_send
                            text: 'Retry'
                            size_hint_x: 0.7
                            on_press: root.send_recalibration_data()


                        BoxLayout:
                            size_hint_x: 0.3

                            Image:
                                id: sent_recalibration_data
                                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                    BoxLayout: 
                        orientation: 'horizontal'

                        Button:
                            id: retry_fully_calibrated_run_data_send
                            text: 'Retry'
                            size_hint_x: 0.7
                            on_press: root.send_fully_calibrated_final_run_data()


                        BoxLayout:
                            size_hint_x: 0.3

                            Image:
                                id: sent_fully_recalibrated_run_data
                                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True


            GridLayout:
                cols: 4
                size_hint_y: 0.5

                GridLayout:
                    rows: 6

                    Label:
                        text: ''
                        halign: 'left'
                        markup: True

                    Label:
                        text: 'Y:'
                        halign: 'left'
                        markup: True

                    Label:
                        text: 'Y1:'
                        halign: 'left'
                        markup: True

                    Label:
                        text: 'Y2:'
                        halign: 'left'
                        markup: True

                    Label:
                        text: 'X:'
                        halign: 'left'
                        markup: True

                    Label:
                        text: 'Z:'
                        halign: 'left'
                        markup: True

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

                GridLayout:
                    rows: 6

                    Label:
                        text: 'Pass?'

                    Image:
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                    Image:
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                    Image:
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                    Image:
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                    Image:
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

        BoxLayout:
            size_hint_y: 0.08
            id: status_container

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

    checkbox_inactive = "./asmcnc/skavaUI/img/checkbox_inactive.png"
    red_cross = "./asmcnc/skavaUI/img/template_cancel.png"
    green_tick = "./asmcnc/skavaUI/img/file_select_select.png"

    mini_run_dev_mode = False


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
        self.stage = ""

        self.status_container.add_widget(widget_sg_status_bar.SGStatusBar(machine=self.m, screen_manager=self.systemtools_sm.sm))

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

        self.unweighted_data = []

    def on_enter(self):
        self.m.s.FINAL_TEST = True

    def on_leave(self):
        self.m.s.FINAL_TEST = False

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

        self.raw_x_vals.append(x_sg)
        self.raw_y_vals.append(y_sg)
        self.raw_y1_vals.append(y1_sg)
        self.raw_y2_vals.append(y2_sg)
        self.raw_z_vals.append(z_sg)

        self.x_peak_load.text = str(max(self.raw_x_vals, key=abs))
        self.x_rt_load.text = str(self.m.s.sg_x_motor_axis)

        self.y_peak_load.text = str(max(self.raw_y_vals, key=abs))
        self.y_rt_load.text = str(self.m.s.sg_y_axis)
        self.y1_peak_load.text = str(max(self.raw_y1_vals, key=abs))
        self.y2_peak_load.text = str(max(self.raw_y2_vals, key=abs))
        self.y1_rt_load.text = str(self.m.s.sg_y1_motor)            
        self.y2_rt_load.text = str(self.m.s.sg_y2_motor)
        self.z_peak_load.text = str(max(self.raw_z_vals, key=abs))
        self.z_rt_load.text = str(self.m.s.sg_z_motor_axis)

        timestamp = datetime.now()

        status = [self.stage, cur_pos_x, cur_pos_y, cur_pos_z, x_dir, y_dir, z_dir, x_sg, y_sg, y1_sg, y2_sg, z_sg, tmc_temp, pcb_temp, mot_temp, timestamp]

        if not self.calibration_db.insert_status_wrapper(status):
            self.statuses.append(status)

    def back_to_fac_settings(self):
        self.systemtools_sm.open_factory_settings_screen()

    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('overnight_testing','overnight_testing')

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)
        self.overnight_running = False

## COMMENTED OUT OLD VERSION

        # if self.poll_end_of_first_overnight_file_stream != None: Clock.unschedule(self.poll_end_of_first_overnight_file_stream)
        # if self.poll_end_of_second_overnight_file_stream != None: Clock.unschedule(self.poll_end_of_second_overnight_file_stream)
        # self.overnight_test_button.disabled = False


    # def send_first_overnight_payload(self):
    #     serial = self.calibration_db.get_serial_number()
        
    #     try:
    #         self.calibration_db.send_overnight_test_calibration(serial, *self.first_overnight_run_data)
    #         self.sent_first_data_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
    #     except:
    #         self.sent_first_data_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
    #         print(traceback.format_exc())


    # def send_overnight_post_recal_payload(self):
    #     serial = self.calibration_db.get_serial_number()
        
    #     try:
    #         self.calibration_db.send_overnight_test_post_recalibration(serial, *self.second_overnight_run_data)
    #         self.sent_second_data_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
    #     except:
    #         self.sent_second_data_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
    #         print(traceback.format_exc())



    # def start_overnight_test(self):

    #     self.overnight_test_button.disabled = True

    #     self.m.jog_absolute_xy(self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000)
    #     self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)

    #     Clock.schedule_once(self.stream_overnight_file, 5)

    # def stream_overnight_file(self, dt):

    #     if self.m.state().startswith('Idle') and not self.overnight_running:

    #         self.overnight_running = True

    #         filename = './asmcnc/apps/systemTools_app/files/overnight_test.gc'
    #         # filename = './asmcnc/apps/systemTools_app/files/mini_run.gc'

    #         with open(filename) as f:
    #             overnight_gcode_pre_scrubbed = f.readlines()

    #         overnight_gcode = [self.m.quick_scrub(line) for line in overnight_gcode_pre_scrubbed]

    #         print("Running overnight test...")

    #         self.m.s.run_skeleton_buffer_stuffer(overnight_gcode)
    #         self.poll_end_of_first_overnight_file_stream = Clock.schedule_interval(self.post_overnight_first_file_stream, 60)

    #     else:
    #         Clock.schedule_once(self.stream_overnight_file, 3)


    # def post_overnight_first_file_stream(self, dt):

    #     if self.m.state().startswith('Idle'):

    #         if self.m.s.NOT_SKELETON_STUFF and not self.m.s.is_job_streaming and not self.m.s.is_stream_lines_remaining and not self.m.is_machine_paused: 
    #             Clock.unschedule(self.poll_end_of_first_overnight_file_stream)

    #             self.overnight_running = False
    #             self.first_overnight_run_data = self.store_overnight_run_measurements()
    #             self.send_first_overnight_payload()
    #             self.retry_first_data_send.disabled = False


    # def recalibrate_after_wear_in(self):
    #     self.m.calibrate_X_Y_and_Z()
    #     self.poll_for_recalibration_completion = Clock.schedule_interval(self.finish_recalibrating, 5)


    # def finish_recalibrating(self, dt):
    #     if not self.m.run_calibration:
    #         Clock.unschedule(self.poll_for_recalibration_completion)

    #         if not self.m.calibration_tuning_fail_info:
    #             self.stream_post_recal_file(0)

    #         # else:
    #         #     self.calibration_label.text = self.m.calibration_tuning_fail_info



    # def stream_post_recal_file(self, dt):

    #     if self.m.state().startswith('Idle') and not self.overnight_running:

    #         self.overnight_running = True

    #         filename = './asmcnc/apps/systemTools_app/files/post_recal_test.gc'
    #         # filename = './asmcnc/apps/systemTools_app/files/mini_run.gc'

    #         with open(filename) as f:
    #             post_recal_gcode_pre_scrubbed = f.readlines()

    #         post_recal_gcode = [self.m.quick_scrub(line) for line in post_recal_gcode_pre_scrubbed]

    #         print("Running overnight test...")

    #         self.m.s.run_skeleton_buffer_stuffer(post_recal_gcode)
    #         self.poll_end_of_second_overnight_file_stream = Clock.schedule_interval(self.post_overnight_second_file_stream, 60)

    #     else:
    #         Clock.schedule_once(self.stream_post_recal_file, 3)


    # def post_overnight_second_file_stream(self, dt):

    #     if self.m.state().startswith('Idle'):

    #         if self.m.s.NOT_SKELETON_STUFF and not self.m.s.is_job_streaming and not self.m.s.is_stream_lines_remaining and not self.m.is_machine_paused: 
    #             Clock.unschedule(self.poll_end_of_second_overnight_file_stream)

    #             self.overnight_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
    #             self.overnight_running = False
    #             self.second_overnight_run_data = self.store_overnight_run_measurements()
    #             self.send_overnight_post_recal_payload()
    #             self.retry_second_data_send.disabled = False
    #             self.overnight_test_button.disabled = False

    # # def store_overnight_run_measurements(self):

    # #     persistent_array = [self.x_vals, self.y_vals, self.z_vals]
    # #     self.setup_arrays()

    # #     return persistent_array


    ## OVERNIGHT TEST CONTROL
    def start_full_overnight_test(self):

        # Schedule stages #2 and #3, and then run the first stage (6 hour wear in)
        poll_for_recalibration_stage = Clock.schedule_interval(self.ready_for_recalibration, 10)
        poll_for_fully_calibrated_final_run_stage = Clock.schedule_interval(self.ready_for_fully_calibrated_final_run, 10)
        self.start_six_hour_wear_in()


    ## RUNNING FUNCTIONS - THESE ARE ALL PARTS OF "OVERNIGHT TEST"

    # These functions also need to set the STAGE, so each bit of sent data knows what it's for

    # This should start, stream the 6 hour wear-in file, and then do any post 6 hour wear-in
    def start_six_hour_wear_in(self):

        self.m.jog_absolute_xy(self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000)
        self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)

        Clock.schedule_once(self.run_six_hour_wear_in, 5)


    def run_six_hour_wear_in(self):

        if self._not_ready_to_stream():
            Clock.schedule_once(self.run_six_hour_wear_in, 3)
            return

        self.stage = "Overnight6HR"
        self._stream_overnight_file('six_hour_rectangle')
        self.poll_end_of_six_hour_wear_in = Clock.schedule_interval(self.post_six_hour_wear_in, 60)

        print("Running six hour wear-in...")


    def post_six_hour_wear_in(self): # This should also trigger the payload data send for any data that did not succeed in sending

        if self._not_finished_streaming(self.poll_end_of_six_hour_wear_in):
            return

        self.tick_checkbox(self.six_hour_wear_in_checkbox, True)
        self.send_six_hour_wear_in_data()


    def ready_for_recalibration(self, dt):
        
        if self.is_step_ticked(self.six_hour_wear_in_checkbox) and self.is_step_complete(self.sent_six_hour_wear_in_data):

            if self.poll_for_recalibration_stage != None: Clock.unschedule(self.poll_for_recalibration_stage)
            self.start_recalibration()


    def start_recalibration(self):
        pass

    def run_recalibration(self):
        pass

    def post_recalibration(self):
        pass


    # This should run the post-calibration 1 hour file to harvest SG values/run data when machine is fully calibrated. 

    def ready_for_fully_calibrated_final_run(self):
        
        if self.is_step_ticked(self.recalibration_checkbox) and self.is_step_complete(self.sent_recalibration_data):

            if self.poll_for_fully_calibrated_final_run_stage != None: Clock.unschedule(self.poll_for_fully_calibrated_final_run_stage)
            self.start_fully_calibrated_final_run()


    def start_fully_calibrated_final_run(self):

        self.m.jog_absolute_xy(self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000)
        self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)

        Clock.schedule_once(self.run_fully_calibrated_final_run, 5)


    def run_fully_calibrated_final_run(self):

        if self._not_ready_to_stream():
            Clock.schedule_once(self.run_fully_calibrated_final_run, 3)
            return

        self.stage = "FullyCalibrated1HR"
        self._stream_overnight_file('one_hour_rectangle')
        self.poll_end_of_fully_calibrated_final_run = Clock.schedule_interval(self.post_fully_calibrated_final_run, 60)

        print("Running fully calibrated final run...")


    def post_fully_calibrated_final_run(self):

        if self._not_finished_streaming(self.poll_end_of_fully_calibrated_final_run):
            return

        self.tick_checkbox(self.fully_calibrated_run_checkbox, True)
        self.send_fully_calibrated_final_run_data()


    # STREAMING FUNCTIONS

    def _not_ready_to_stream(self):
        if self.m.state().startswith('Idle') and not self.overnight_running:
            return False

        else: 
            return True


    def _stream_overnight_file(self, filename_end):

        self.overnight_running = True

        if self.mini_run_dev_mode: filename_end = 'mini_run'

        else:
            filename = './asmcnc/apps/systemTools_app/files/' + filename_end + '.gc'

        with open(filename) as f:
            gcode_prescrubbed = f.readlines()

        gcode = [self.m.quick_scrub(line) for line in gcode_prescrubbed]

        self.m.s.run_skeleton_buffer_stuffer(gcode)


    def _not_finished_streaming(self, poll_to_unschedule):

        if not self.m.state().startswith('Idle'):
            return True

        if self.m.s.NOT_SKELETON_STUFF and not self.m.s.is_job_streaming and not self.m.s.is_stream_lines_remaining and not self.m.is_machine_paused: 
            
            if self.poll_to_unschedule != None: Clock.unschedule(self.poll_to_unschedule)
            self.overnight_running = False

            return False

        return True



    ## DATA STREAMS

    # These actually only need to send any data that hasn't already been sent - for completion, check when arrays are empty

    # Add all statuses to same array - and then for each function/check, see if any of the stages are in the lists. 

    def send_six_hour_wear_in_data(self):
        self._has_data_been_sent("Overnight6HR", self.sent_six_hour_wear_in_data)


    def send_recalibration_data(self):
        self._has_data_been_sent("CalibrationCheckOT", self.sent_recalibration_data)


    def send_fully_calibrated_final_run_data(self):
        self._has_data_been_sent("FullyCalibrated1HR", self.sent_fully_recalibrated_run_data)


    def _send_remaining_statuses(self):

        self.statuses[:] = [status for status in self.statuses if not self.calibration_db.insert_status_wrapper(status)]

        if not self.statuses:
            return True

        return False


    def _has_data_been_sent(self, stage, checkbox_id):

        if not self.statuses or self._send_remaining_statuses():
            self.tick_checkbox(self.checkbox_id, True)
        
        elif any(stage in status for status in self.statuses):
            self.tick_checkbox(self.checkbox_id, False)


    ## SET TICKS
    def tick_checkbox(self, checkbox_id, tick):

        if tick: 
            self.checkbox_id.source = self.green_tick

        else: 
            self.checkbox_id.source = self.red_cross

    ## GET TICKS
    def is_step_complete(self, checkbox_id):

        if not self.checkbox_id.source == self.checkbox_inactive:
            return True

        else: 
            return False

    def is_step_ticked(self, checkbox_id):

        if not self.checkbox_id.source == self.green_tick:
            return True

        else: 
            return False


    # ## CALIBRATION FUNCTIONS

    # def _check_peak_loads():


    #     self.x_peak_load.text
    #     self.y_peak_load.text
    #     self.y1_peak_load.text
    #     self.y2_peak_load.text
    #     self.z_peak_load.text