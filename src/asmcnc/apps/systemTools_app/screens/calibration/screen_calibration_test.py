from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from datetime import datetime
from asmcnc.skavaUI import popup_info
import traceback

Builder.load_string("""
<CalibrationTesting>:
    y_rt_load:y_rt_load
    x_rt_load:x_rt_load
    z_rt_load:z_rt_load
    y1_rt_load:y1_rt_load
    y2_rt_load:y2_rt_load

    y_axis_fw_range : y_axis_fw_range
    y1_fw_range : y1_fw_range
    y2_fw_range : y2_fw_range
    x_fw_range : x_fw_range
    z_fw_range : z_fw_range
    y_axis_bw_range : y_axis_bw_range
    y1_bw_range : y1_bw_range
    y2_bw_range : y2_bw_range
    x_bw_range : x_bw_range
    z_bw_range : z_bw_range

    y_peak_load:y_peak_load
    x_peak_load:x_peak_load
    z_peak_load:z_peak_load
    y1_peak_load:y1_peak_load
    y2_peak_load:y2_peak_load

    x_test_check:x_test_check
    y_test_check:y_test_check
    z_test_check:z_test_check
    unweighted_test_check:unweighted_test_check
    sent_data_check:sent_data_check

    unweighted_test_button : unweighted_test_button
    x_load_button : x_load_button
    y_load_button : y_load_button
    z_load_button : z_load_button

    data_send_button : data_send_button

    home_button : home_button
    x0y0_jog_button : x0y0_jog_button
    x7y0_jog_button : x7y0_jog_button
    z0_jog_button : z0_jog_button

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.3

            BoxLayout:
                orientation: "horizontal"
                size_hint_x: 0.7

                Button:
                    text: 'Back'
                    on_press: root.back_to_fac_settings()

                Button:
                    id: home_button
                    text: 'Home'
                    on_press: root.home()

                Button:
                    id: x0y0_jog_button
                    text: 'X0Y0'
                    on_press: root.zero_x_and_y()

                Button:
                    id: x7y0_jog_button
                    text: 'X-700Y0'
                    on_press: root.mid_x_and_zero_y()

                Button:
                    id: z0_jog_button
                    text: 'Z0'
                    on_press: root.zero_Z()

            Button:
                text: 'STOP'
                background_color: [1,0,0,1]
                on_press: root.stop()
                size_hint_x: 0.3


        GridLayout: 
            cols: 3
            size_hint_y: 0.6

            GridLayout:
                cols: 2

                Button:
                    id: unweighted_test_button
                    text: 'Run XYZ 0kg'
                    on_press: root.run_unweighted_test()

                Image:
                    id: unweighted_test_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            GridLayout:
                cols: 2

                Button:
                    id: x_load_button
                    text: 'Run X (7.5kg)'
                    on_press: root.run_x_procedure(None)

                Image:
                    id: x_test_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            GridLayout:
                cols: 2

                Button:
                    id: y_load_button
                    text: 'Run Y (7.5kg)'
                    on_press: root.run_y_procedure(None)
                
                Image:
                    id: y_test_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            GridLayout:
                cols: 2

                Button:
                    id: z_load_button
                    text: 'Run Z (2kg)'
                    on_press: root.run_z_procedure(None)

                Image:
                    id: z_test_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            Button:
                id: data_send_button
                text: 'Send data to database'
                on_press: root.send_data()
                disabled: True

            GridLayout:
                cols: 2

                Label:
                    text: 'Sent data?'
                
                Image:
                    id: sent_data_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

        GridLayout:
            cols: 4

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
                    text: '<<--'

                Label:
                    id: y_axis_fw_range
                    text: 'Y:'

                Label:
                    id: y1_fw_range
                    text: 'Y1:'

                Label:
                    id: y2_fw_range
                    text: 'Y2:'

                Label:
                    id: x_fw_range
                    text: 'X:'

                Label:
                    id: z_fw_range
                    text: 'Z:'

            GridLayout:
                rows: 6

                Label:
                    text: '-->>'

                Label:
                    id: y_axis_bw_range
                    text: 'Y:'

                Label:
                    id: y1_bw_range
                    text: 'Y1:'

                Label:
                    id: y2_bw_range
                    text: 'Y2:'

                Label:
                    id: x_bw_range
                    text: 'X:'

                Label:
                    id: z_bw_range
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

MAX_XY_SPEED = 1186.0
MAX_Z_SPEED = 75.0

MAX_Z_DISTANCE = 115
MAX_X_DISTANCE = 1135
MAX_Y_DISTANCE = 2275

TIME_TO_RUN_Z = 241 #241
TIME_TO_RUN_X = 120 #120
TIME_TO_RUN_Y = 239 #239

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class CalibrationTesting(Screen):


    next_run_event = None
    unweighted_event_x = None
    unweighted_event_y = None
    confirm_event = None

    def __init__(self, **kwargs):
        super(CalibrationTesting, self).__init__(**kwargs)
        self.setup_arrays()

        self.m = kwargs['m']
        self.systemtools_sm = kwargs['systemtools']
        self.calibration_db = kwargs['calibration_db']
        self.sm = kwargs['sm']
        self.l = kwargs['l']

        # used to only measure axis in motion
        self.x_running = False
        self.y_running = False
        self.z_running = False

        self.stage = 'Unweighted'
        self.statuses = []

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

    def send_data(self):

        try:
            serial = self.calibration_db.get_serial_number()
            self.calibration_db.send_final_test_calibration(serial, self.unweighted_data[0], self.unweighted_data[1], self.unweighted_data[2], self.x_vals, self.y_vals, self.z_vals)
            self.sent_data_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        except:
            self.sent_data_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
            print(traceback.format_exc())

    def stop(self):
        self.x_running = False
        self.y_running = False
        self.z_running = False
        if self.next_run_event != None: Clock.unschedule(self.next_run_event)
        if self.unweighted_event_x != None: Clock.unschedule(self.unweighted_event_x)
        if self.unweighted_event_y != None: Clock.unschedule(self.unweighted_event_y)
        if self.confirm_event != None: Clock.unschedule(self.confirm_event)
        popup_info.PopupStop(self.m, self.sm, self.l)
        self.enable_run_buttons()

    def on_enter(self):
        self.m.s.FINAL_TEST = True
        if self.next_run_event != None: Clock.unschedule(self.next_run_event)
        if self.unweighted_event_x != None: Clock.unschedule(self.unweighted_event_x)
        if self.unweighted_event_y != None: Clock.unschedule(self.unweighted_event_y)
        if self.confirm_event != None: Clock.unschedule(self.confirm_event)
        self.enable_run_buttons()

    def on_leave(self):
        self.m.s.FINAL_TEST = False
        if self.next_run_event != None: Clock.unschedule(self.next_run_event)
        if self.unweighted_event_x != None: Clock.unschedule(self.unweighted_event_x)
        if self.unweighted_event_y != None: Clock.unschedule(self.unweighted_event_y)
        if self.confirm_event != None: Clock.unschedule(self.confirm_event)
        self.enable_run_buttons()

    def back_to_fac_settings(self):
        self.systemtools_sm.open_factory_settings_screen()

    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('calibration_testing','calibration_testing')

    def reset(self):
        if self.next_run_event != None: Clock.unschedule(self.next_run_event)
        if self.unweighted_event_x != None: Clock.unschedule(self.unweighted_event_x)
        if self.unweighted_event_y != None: Clock.unschedule(self.unweighted_event_y)
        if self.confirm_event != None: Clock.unschedule(self.confirm_event)

        self.m.resume_from_alarm()
        self.enable_run_buttons()


    def zero_x_and_y(self):
        self.m.jog_absolute_xy(self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000)

    def mid_x_and_zero_y(self):
        self.m.jog_absolute_xy(-700, self.m.y_min_jog_abs_limit, 6000)

    def zero_Z(self):
        self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)

    def disable_x_measurement(self, dt):
        self.x_running = False

    def disable_z_measurement(self, dt):
        self.z_running = False

    def disable_y_measurement(self, dt):
        self.y_running = False

    def enable_run_buttons(self):
        self.x_load_button.disabled = False
        self.y_load_button.disabled = False
        self.z_load_button.disabled = False
        self.unweighted_test_button.disabled = False
        self.home_button.disabled = False
        self.x0y0_jog_button.disabled = False
        self.x7y0_jog_button.disabled = False
        self.z0_jog_button.disabled = False        

    def disable_run_buttons(self):
        self.x_load_button.disabled = True
        self.y_load_button.disabled = True
        self.z_load_button.disabled = True
        self.unweighted_test_button.disabled = True
        self.home_button.disabled = True
        self.x0y0_jog_button.disabled = True
        self.x7y0_jog_button.disabled = True
        self.z0_jog_button.disabled = True

    def confirm_unweighted(self, dt):
        self.unweighted_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        self.unweighted_data.append(self.x_vals)
        self.unweighted_data.append(self.y_vals)
        self.unweighted_data.append(self.z_vals)

        self.enable_run_buttons()
        self.data_send_button.disabled = False

    def confirm_x(self, dt):
        self.enable_run_buttons()
        self.x_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"

    def confirm_y(self, dt):
        self.enable_run_buttons()
        self.y_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"

    def confirm_z(self, dt):
        if self.state().startswith('Idle'):
            self.z_running = False
            self.enable_run_buttons()
            self.z_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
    
    def measure(self):
        if (self.x_running and self.m.feed_rate() < 1200) or (self.y_running and self.m.feed_rate() < 1200) or (self.z_running and self.m.feed_rate() < 80):
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

        self.x_peak_load.text = "X: " + str(max(self.raw_x_vals, key=abs))
        self.x_rt_load.text = "X: " + str(self.m.s.sg_x_motor_axis)

        self.y_peak_load.text = "Y ax: " + str(max(self.raw_y_vals, key=abs))
        self.y_rt_load.text = "Y ax: " + str(self.m.s.sg_y_axis)
        self.y1_peak_load.text = "Y1: " + str(max(self.raw_y1_vals, key=abs))
        self.y2_peak_load.text = "Y2: " + str(max(self.raw_y2_vals, key=abs))
        self.y1_rt_load.text = "Y1: " + str(self.m.s.sg_y1_motor)            
        self.y2_rt_load.text = "Y2: " + str(self.m.s.sg_y2_motor)
        self.z_peak_load.text = "Z: " + str(max(self.raw_z_vals, key=abs))
        self.z_rt_load.text = "Z: " + str(self.m.s.sg_z_motor_axis)

        timestamp = datetime.now()

        status = [self.stage, cur_pos_x, cur_pos_y, cur_pos_z, x_dir, y_dir, z_dir, x_sg, y_sg, y1_sg, y2_sg, z_sg, tmc_temp, pcb_temp, mot_temp, timestamp]

        self.statuses.append(status)


    def show_expected_ranges(self, x_load, y_load, z_load):

        X_SG_to_kg_scaling = 13.7
        Y_SG_to_kg_scaling = 11.5
        Z_SG_to_kg_scaling = 5.0

        xy_friction = 5.0
        z_friction = 3.0

        tolerance = 0.8

        y_fw_expected_min = (xy_friction + float(y_load))*(1.0 - tolerance)
        y_fw_expected_max = (xy_friction + float(y_load))*(1.0 + tolerance)

        y_bw_expected_min = (xy_friction - float(y_load))*(1.0 - tolerance)
        y_bw_expected_max = (xy_friction - float(y_load))*(1.0 + tolerance)

        x_fw_expected_min = (xy_friction + float(x_load))*(1.0 - tolerance)
        x_fw_expected_max = (xy_friction + float(x_load))*(1.0 + tolerance)

        x_bw_expected_min = (xy_friction - float(x_load))*(1.0 - tolerance)
        x_bw_expected_max = (xy_friction - float(x_load))*(1.0 + tolerance)

        z_fw_expected_min = (z_friction + float(z_load))*(1.0 - tolerance)
        z_fw_expected_max = (z_friction + float(z_load))*(1.0 + tolerance)

        z_bw_expected_min = (z_friction - float(z_load))*(1.0 - tolerance)
        z_bw_expected_max = (z_friction - float(z_load))*(1.0 + tolerance)


        print(y_fw_expected_min)
        print(y_fw_expected_max)
        print(y_bw_expected_min)
        print(y_bw_expected_max)
        print(x_fw_expected_min)
        print(x_fw_expected_max)
        print(x_bw_expected_min)
        print(x_bw_expected_max)
        print(z_fw_expected_min)
        print(z_fw_expected_max)
        print(z_bw_expected_min)
        print(z_bw_expected_max)

        y_fw_range_text = str(y_fw_expected_min*Y_SG_to_kg_scaling) + "-" + str(y_fw_expected_max*Y_SG_to_kg_scaling)
        x_fw_range_text = str(x_fw_expected_min*X_SG_to_kg_scaling) + "-" + str(x_fw_expected_max*X_SG_to_kg_scaling)
        z_fw_range_text = str(z_fw_expected_min*Z_SG_to_kg_scaling) + "-" + str(z_fw_expected_max*Z_SG_to_kg_scaling)

        y_bw_range_text = str(y_bw_expected_min*Y_SG_to_kg_scaling) + "-" + str(y_bw_expected_max*Y_SG_to_kg_scaling)
        x_bw_range_text = str(x_bw_expected_min*X_SG_to_kg_scaling) + "-" + str(x_bw_expected_max*X_SG_to_kg_scaling)
        z_bw_range_text = str(z_bw_expected_min*Z_SG_to_kg_scaling) + "-" + str(z_bw_expected_max*Z_SG_to_kg_scaling)

        self.y_axis_fw_range.text = y_fw_range_text
        self.y1_fw_range.text = y_fw_range_text
        self.y2_fw_range.text = y_fw_range_text
        self.x_fw_range.text = x_fw_range_text
        self.z_fw_range.text = z_fw_range_text

        self.y_axis_bw_range.text = y_bw_range_text
        self.y1_bw_range.text = y_bw_range_text
        self.y2_bw_range.text = y_bw_range_text
        self.x_bw_range.text = x_bw_range_text
        self.z_bw_range.text = z_bw_range_text


    def run_z_procedure(self):

        # start run, run all the way down and then all the way back up. 

        self.disable_run_buttons()
        self.show_expected_ranges(0,0,2)

        self.z_vals = []
        self.raw_z_vals = []

        self.z_running = True

        self.m.send_any_gcode_command('G91 G1 Z-149 F75')
        self.m.send_any_gcode_command('G91 G1 Z149 F75')

        # poll to see when run is done
        self.confirm_event = Clock.schedule_interval(self.confirm_z, 5)


    def run_y_procedure(self):

        # start run, run all the way down and then all the way back up. 

        self.disable_run_buttons()
        self.show_expected_ranges(0,0,2)

        self.y_vals = []
        self.raw_y_vals = []

        self.y_running = True

        self.m.send_any_gcode_command('G91 G1 Y2500 F1186')
        self.m.send_any_gcode_command('G91 G1 Y-2500 F1186')

        # poll to see when run is done
        self.confirm_event = Clock.schedule_interval(self.confirm_y, 5)

    def run_x_procedure(self):

        # start run, run all the way down and then all the way back up. 

        self.disable_run_buttons()
        self.show_expected_ranges(0,0,2)

        self.x_vals = []
        self.raw_x_vals = []

        self.x_running = True

        self.m.send_any_gcode_command('G91 G1 x-1298 F1186')
        self.m.send_any_gcode_command('G91 G1 x1298 F1186')

        # poll to see when run is done
        self.confirm_event = Clock.schedule_interval(self.confirm_x, 5)


    def run_unweighted_test(self):
        pass



    # def run_unweighted_test(self):

    #     self.disable_run_buttons()

    #     self.show_expected_ranges(0,0,0)

    #     self.m.jog_absolute_xy(self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000)
    #     self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)

    #     self.run_unweighted_z()

    #     self.unweighted_event_x = Clock.schedule_once(self.run_unweighted_x, TIME_TO_RUN_Z + 10)

    #     self.unweighted_event_y = Clock.schedule_once(self.run_unweighted_y, TIME_TO_RUN_Z + TIME_TO_RUN_X + 20)

    #     self.confirm_event = Clock.schedule_once(self.confirm_unweighted, TIME_TO_RUN_Z + TIME_TO_RUN_X + TIME_TO_RUN_Y)

    # def stop_all_procedures(self):
    #     self.disable_x_measurement(None)
    #     self.disable_y_measurement(None)
    #     self.disable_z_measurement(None)
    #     popup_info.PopupStop(self.m, self.sm, self.l)

    #     if self.next_run_event != None: Clock.unschedule(self.next_run_event)
    #     if self.unweighted_event_x != None: Clock.unschedule(self.unweighted_event_x)
    #     if self.unweighted_event_y != None: Clock.unschedule(self.unweighted_event_y)
    #     if self.confirm_event != None: Clock.unschedule(self.confirm_event)

    #     self.enable_run_buttons()

    # def run_unweighted_z(self):
    #     self.z_vals = []
    #     self.raw_z_vals = []

    #     #total distance required
    #     TOTAL_DISTANCE = float(TIME_TO_RUN_Z / 60) * MAX_Z_SPEED

    #     self.z_distance_left = TOTAL_DISTANCE

    #     self.z_running = True

    #     def run(dt):

    #         if self.m.state().startswith('Idle'):

    #             if not self.z_running:
    #                 return

    #             if self.z_distance_left > MAX_Z_DISTANCE:
    #                 if self.m.mpos_z() > -30:
    #                     self.m.jog_relative('Z', -MAX_Z_DISTANCE, MAX_Z_SPEED)
    #                 else:
    #                     self.m.jog_relative('Z', MAX_Z_DISTANCE, MAX_Z_SPEED)

    #                 self.z_distance_left -= MAX_Z_DISTANCE 

    #                 TIME_FOR_MOVEMENT = float((float(MAX_Z_DISTANCE) / float(MAX_Z_SPEED)) * 60) + 2

    #                 self.next_run_event = Clock.schedule_once(run, TIME_FOR_MOVEMENT)
    #             else:
    #                 if self.m.mpos_z() > -30:
    #                     self.m.jog_relative('Z', -self.z_distance_left, MAX_Z_SPEED)
    #                 else:
    #                     self.m.jog_relative('Z', self.z_distance_left, MAX_Z_SPEED)

    #                 TIME_FOR_MOVEMENT = float((float(self.z_distance_left) / float(MAX_Z_SPEED)) * 60) + 2

    #                 self.z_distance_left = 0

    #                 Clock.schedule_once(self.disable_z_measurement, TIME_FOR_MOVEMENT)

    #         else:
    #             self.next_run_event = Clock.schedule_once(run, 2)


    #     self.next_run_event = Clock.schedule_once(run, 0.5)

    # def run_z_procedure(self, dt):

    #     self.disable_run_buttons()

    #     self.show_expected_ranges(0,0,2)

    #     self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)

    #     self.z_vals = []
    #     self.raw_z_vals = []

    #     #total distance required
    #     TOTAL_DISTANCE = float(TIME_TO_RUN_Z / 60) * MAX_Z_SPEED

    #     self.z_distance_left = TOTAL_DISTANCE

    #     self.z_running = True

    #     def run(dt):

    #         if self.m.state().startswith('Idle'):

    #             if not self.z_running:
    #                 return

    #             if self.z_distance_left > MAX_Z_DISTANCE:
    #                 if self.m.mpos_z() > -30:
    #                     self.m.jog_relative('Z', -MAX_Z_DISTANCE, MAX_Z_SPEED)
    #                 else:
    #                     self.m.jog_relative('Z', MAX_Z_DISTANCE, MAX_Z_SPEED)

    #                 self.z_distance_left -= MAX_Z_DISTANCE 

    #                 TIME_FOR_MOVEMENT = float((float(MAX_Z_DISTANCE) / float(MAX_Z_SPEED)) * 60) + 2

    #                 self.next_run_event = Clock.schedule_once(run, TIME_FOR_MOVEMENT)
    #             else:
    #                 if self.m.mpos_z() > -30:
    #                     self.m.jog_relative('Z', -self.z_distance_left, MAX_Z_SPEED)
    #                 else:
    #                     self.m.jog_relative('Z', self.z_distance_left, MAX_Z_SPEED)

    #                 TIME_FOR_MOVEMENT = float((float(self.z_distance_left) / float(MAX_Z_SPEED)) * 60) + 2

    #                 self.z_distance_left = 0

    #                 Clock.schedule_once(self.disable_z_measurement, TIME_FOR_MOVEMENT)
    #                 self.confirm_event = Clock.schedule_once(self.confirm_z, TIME_FOR_MOVEMENT)

    #         else:
    #             self.next_run_event = Clock.schedule_once(run, 2)

    #     self.next_run_event = Clock.schedule_once(run, 0.5)

    # #change distances and speeds
    # def run_y_procedure(self, dt):

    #     self.disable_run_buttons()

    #     self.show_expected_ranges(0,7.5,0)

    #     self.m.jog_absolute_single_axis('Y', self.m.y_min_jog_abs_limit, 6000)

    #     self.y_vals = []
    #     self.raw_y_vals = []

    #     #total distance required
    #     TOTAL_DISTANCE = float(TIME_TO_RUN_Y / 60) * MAX_XY_SPEED

    #     self.y_distance_left = TOTAL_DISTANCE

    #     self.y_running = True

    #     def run(dt):

    #         if self.m.state().startswith('Idle'):

    #             if not self.y_running:
    #                 return

    #             if self.y_distance_left > MAX_Y_DISTANCE:
    #                 if self.m.mpos_y() < -2460:
    #                     self.m.jog_relative('Y', MAX_Y_DISTANCE, MAX_XY_SPEED)
    #                 else:
    #                     self.m.jog_relative('Y', -MAX_Y_DISTANCE, MAX_XY_SPEED)

    #                 self.y_distance_left -= MAX_Y_DISTANCE 

    #                 TIME_FOR_MOVEMENT = float((float(MAX_Y_DISTANCE) / float(MAX_XY_SPEED)) * 60) + 2

    #                 self.next_run_event = Clock.schedule_once(run, TIME_FOR_MOVEMENT)
    #             else:
    #                 if self.m.mpos_y() < -2460:
    #                     self.m.jog_relative('Y', self.y_distance_left, MAX_XY_SPEED)
    #                 else:
    #                     self.m.jog_relative('Y', -self.y_distance_left, MAX_XY_SPEED)

    #                 TIME_FOR_MOVEMENT = float((float(self.y_distance_left) / float(MAX_XY_SPEED)) * 60) + 2

    #                 self.y_distance_left = 0

    #                 Clock.schedule_once(self.disable_y_measurement, TIME_FOR_MOVEMENT)
    #                 self.confirm_event = Clock.schedule_once(self.confirm_y, TIME_FOR_MOVEMENT)

    #         else:
    #             self.next_run_event = Clock.schedule_once(run, 2)

    #     self.next_run_event = Clock.schedule_once(run, 0.5)

    # def run_unweighted_y(self, dt):
    #     self.y_vals = []
    #     self.raw_y_vals = []

    #     #total distance required
    #     TOTAL_DISTANCE = float(TIME_TO_RUN_Y / 60) * MAX_XY_SPEED

    #     self.y_distance_left = TOTAL_DISTANCE

    #     self.y_running = True

    #     def run(dt):

    #         if self.m.state().startswith('Idle'):

    #             if not self.y_running:
    #                 return

    #             if self.y_distance_left > MAX_Y_DISTANCE:
    #                 if self.m.mpos_y() < -2460:
    #                     self.m.jog_relative('Y', MAX_Y_DISTANCE, MAX_XY_SPEED)
    #                 else:
    #                     self.m.jog_relative('Y', -MAX_Y_DISTANCE, MAX_XY_SPEED)

    #                 self.y_distance_left -= MAX_Y_DISTANCE 

    #                 TIME_FOR_MOVEMENT = float((float(MAX_Y_DISTANCE) / float(MAX_XY_SPEED)) * 60) + 2

    #                 self.next_run_event = Clock.schedule_once(run, TIME_FOR_MOVEMENT)
    #             else:
    #                 if self.m.mpos_y() < -2460:
    #                     self.m.jog_relative('Y', self.y_distance_left, MAX_XY_SPEED)
    #                 else:
    #                     self.m.jog_relative('Y', -self.y_distance_left, MAX_XY_SPEED)

    #                 TIME_FOR_MOVEMENT = float((float(self.y_distance_left) / float(MAX_XY_SPEED)) * 60) + 2

    #                 self.y_distance_left = 0

    #                 Clock.schedule_once(self.disable_y_measurement, TIME_FOR_MOVEMENT)

    #         else:
    #             self.next_run_event = Clock.schedule_once(run, 2)

    #     self.next_run_event = Clock.schedule_once(run, 0.5)

    # #change distances and speeds
    # def run_x_procedure(self, dt):

    #     self.disable_run_buttons()

    #     self.show_expected_ranges(7.5,0,0)

    #     self.m.jog_absolute_single_axis('X', self.m.x_min_jog_abs_limit, 6000)

    #     self.raw_x_vals = []
    #     self.x_vals = []

    #     #total distance required
    #     TOTAL_DISTANCE = float(TIME_TO_RUN_X / 60) * MAX_XY_SPEED

    #     self.x_distance_left = TOTAL_DISTANCE

    #     self.x_running = True

    #     def run(dt):

    #         if self.m.state().startswith('Idle'):
    
    #             if not self.x_running:
    #                 return
                
    #             if self.x_distance_left > MAX_X_DISTANCE:
    #                 if self.m.mpos_x() < -1260:
    #                     self.m.jog_relative('X', MAX_X_DISTANCE, MAX_XY_SPEED)
    #                 else:
    #                     self.m.jog_relative('X', -MAX_X_DISTANCE, MAX_XY_SPEED)

    #                 self.x_distance_left -= MAX_X_DISTANCE 

    #                 TIME_FOR_MOVEMENT = float((float(MAX_X_DISTANCE) / float(MAX_XY_SPEED)) * 60) + 2

    #                 self.next_run_event = Clock.schedule_once(run, TIME_FOR_MOVEMENT)
    #             else:
    #                 if self.m.mpos_x() < -1260:
    #                     self.m.jog_relative('X', self.x_distance_left, MAX_XY_SPEED)
    #                 else:
    #                     self.m.jog_relative('X', -self.x_distance_left, MAX_XY_SPEED)

    #                 TIME_FOR_MOVEMENT = float((float(self.x_distance_left) / float(MAX_XY_SPEED)) * 60) + 2

    #                 self.x_distance_left = 0

    #                 Clock.schedule_once(self.disable_x_measurement, TIME_FOR_MOVEMENT)
    #                 self.confirm_event = Clock.schedule_once(self.confirm_x, TIME_FOR_MOVEMENT)

    #         else:
    #             self.next_run_event = Clock.schedule_once(run, 2)

    #     self.next_run_event = Clock.schedule_once(run, 0.5)

    # def run_unweighted_x(self, dt):
    #     self.raw_x_vals = []
    #     self.x_vals = []

    #     #total distance required
    #     TOTAL_DISTANCE = float(TIME_TO_RUN_X / 60) * MAX_XY_SPEED

    #     self.x_distance_left = TOTAL_DISTANCE

    #     self.x_running = True

    #     def run(dt):

    #         if self.m.state().startswith('Idle'):

    #             if not self.x_running:
    #                 return
                
    #             if self.x_distance_left > MAX_X_DISTANCE:
    #                 if self.m.mpos_x() < -1260:
    #                     self.m.jog_relative('X', MAX_X_DISTANCE, MAX_XY_SPEED)
    #                 else:
    #                     self.m.jog_relative('X', -MAX_X_DISTANCE, MAX_XY_SPEED)

    #                 self.x_distance_left -= MAX_X_DISTANCE 

    #                 TIME_FOR_MOVEMENT = float((float(MAX_X_DISTANCE) / float(MAX_XY_SPEED)) * 60) + 2

    #                 self.next_run_event = Clock.schedule_once(run, TIME_FOR_MOVEMENT)
    #             else:
    #                 if self.m.mpos_x() < -1260:
    #                     self.m.jog_relative('X', self.x_distance_left, MAX_XY_SPEED)
    #                 else:
    #                     self.m.jog_relative('X', -self.x_distance_left, MAX_XY_SPEED)

    #                 TIME_FOR_MOVEMENT = float((float(self.x_distance_left) / float(MAX_XY_SPEED)) * 60) + 2

    #                 self.x_distance_left = 0

    #                 Clock.schedule_once(self.disable_x_measurement, TIME_FOR_MOVEMENT)

    #         else:
    #             self.next_run_event = Clock.schedule_once(run, 2)

    #     self.next_run_event = Clock.schedule_once(run, 0.5)