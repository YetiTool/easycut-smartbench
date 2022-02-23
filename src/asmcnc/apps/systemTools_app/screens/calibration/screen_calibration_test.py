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

    BoxLayout:
        orientation: 'vertical'

        GridLayout: 
            cols: 3

            Button:
                text: 'Back'
                on_press: root.back_to_fac_settings()

            Button:
                text: 'Home'
                on_press: root.home()

            Button:
                text: 'STOP'
                background_color: [1,0,0,1]
                on_press: root.stop()

            GridLayout:
                cols: 2

                Button:
                    id: unweighted_test_button
                    text: 'Run unweighted test'
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
                text: 'Send data to database'
                on_press: root.send_data()

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
        serial = self.calibration_db.get_serial_number()

        try:
            self.calibration_db.send_final_test_calibration(serial, self.unweighted_data[0], self.unweighted_data[1], self.unweighted_data[2], self.x_vals, self.y_vals, self.z_vals)
            self.sent_data_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        except:
            self.sent_data_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
            print(traceback.format_exc())

    def stop(self):
        self.x_running = False
        self.y_running = False
        self.z_running = False
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

    def disable_run_buttons(self):
        self.x_load_button.disabled = True
        self.y_load_button.disabled = True
        self.z_load_button.disabled = True
        self.unweighted_test_button.disabled = True

    def confirm_unweighted(self, dt):
        self.unweighted_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        self.unweighted_data.append(self.x_vals)
        self.unweighted_data.append(self.y_vals)
        self.unweighted_data.append(self.z_vals)

        self.enable_run_buttons()

    def confirm_x(self, dt):
        self.enable_run_buttons()
        self.x_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"

    def confirm_y(self, dt):
        self.enable_run_buttons()
        self.y_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"

    def confirm_z(self, dt):
        self.enable_run_buttons()
        self.z_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"

    def run_unweighted_test(self):

        self.disable_run_buttons()

        self.m.jog_absolute_xy(self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000)
        self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)

        self.run_unweighted_z()

        self.unweighted_event_x = Clock.schedule_once(self.run_unweighted_x, TIME_TO_RUN_Z + 10)

        self.unweighted_event_y = Clock.schedule_once(self.run_unweighted_y, TIME_TO_RUN_Z + TIME_TO_RUN_X + 20)

        self.confirm_event = Clock.schedule_once(self.confirm_unweighted, TIME_TO_RUN_Z + TIME_TO_RUN_X + TIME_TO_RUN_Y)

    def stop_all_procedures(self):
        self.disable_x_measurement(None)
        self.disable_y_measurement(None)
        self.disable_z_measurement(None)
        popup_info.PopupStop(self.m, self.sm, self.l)

        if self.next_run_event != None: Clock.unschedule(self.next_run_event)
        if self.unweighted_event_x != None: Clock.unschedule(self.unweighted_event_x)
        if self.unweighted_event_y != None: Clock.unschedule(self.unweighted_event_y)
        if self.confirm_event != None: Clock.unschedule(self.confirm_event)

        self.enable_run_buttons()

    def run_unweighted_z(self):
        self.z_vals = []
        self.raw_z_vals = []

        #total distance required
        TOTAL_DISTANCE = float(TIME_TO_RUN_Z / 60) * MAX_Z_SPEED

        self.z_distance_left = TOTAL_DISTANCE

        self.z_running = True

        def run(dt):

            if self.m.state().startswith('Idle'):

                if not self.z_running:
                    return

                if self.z_distance_left > MAX_Z_DISTANCE:
                    if self.m.mpos_z() > -30:
                        self.m.jog_relative('Z', -MAX_Z_DISTANCE, MAX_Z_SPEED)
                    else:
                        self.m.jog_relative('Z', MAX_Z_DISTANCE, MAX_Z_SPEED)

                    self.z_distance_left -= MAX_Z_DISTANCE 

                    TIME_FOR_MOVEMENT = float((float(MAX_Z_DISTANCE) / float(MAX_Z_SPEED)) * 60) + 2

                    self.next_run_event = Clock.schedule_once(run, TIME_FOR_MOVEMENT)
                else:
                    if self.m.mpos_z() > -30:
                        self.m.jog_relative('Z', -self.z_distance_left, MAX_Z_SPEED)
                    else:
                        self.m.jog_relative('Z', self.z_distance_left, MAX_Z_SPEED)

                    TIME_FOR_MOVEMENT = float((float(self.z_distance_left) / float(MAX_Z_SPEED)) * 60) + 2

                    self.z_distance_left = 0

                    Clock.schedule_once(self.disable_z_measurement, TIME_FOR_MOVEMENT)

            else:
                self.next_run_event = Clock.schedule_once(run, 2)


        self.next_run_event = Clock.schedule_once(run, 0.5)

    def run_z_procedure(self, dt):

        self.disable_run_buttons()

        self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)

        self.z_vals = []
        self.raw_z_vals = []

        #total distance required
        TOTAL_DISTANCE = float(TIME_TO_RUN_Z / 60) * MAX_Z_SPEED

        self.z_distance_left = TOTAL_DISTANCE

        self.z_running = True

        def run(dt):

            if self.m.state().startswith('Idle'):

                if not self.z_running:
                    return

                if self.z_distance_left > MAX_Z_DISTANCE:
                    if self.m.mpos_z() > -30:
                        self.m.jog_relative('Z', -MAX_Z_DISTANCE, MAX_Z_SPEED)
                    else:
                        self.m.jog_relative('Z', MAX_Z_DISTANCE, MAX_Z_SPEED)

                    self.z_distance_left -= MAX_Z_DISTANCE 

                    TIME_FOR_MOVEMENT = float((float(MAX_Z_DISTANCE) / float(MAX_Z_SPEED)) * 60) + 2

                    self.next_run_event = Clock.schedule_once(run, TIME_FOR_MOVEMENT)
                else:
                    if self.m.mpos_z() > -30:
                        self.m.jog_relative('Z', -self.z_distance_left, MAX_Z_SPEED)
                    else:
                        self.m.jog_relative('Z', self.z_distance_left, MAX_Z_SPEED)

                    TIME_FOR_MOVEMENT = float((float(self.z_distance_left) / float(MAX_Z_SPEED)) * 60) + 2

                    self.z_distance_left = 0

                    Clock.schedule_once(self.disable_z_measurement, TIME_FOR_MOVEMENT)
                    self.confirm_event = Clock.schedule_once(self.confirm_z, TIME_FOR_MOVEMENT)

            else:
                self.next_run_event = Clock.schedule_once(run, 2)

        self.next_run_event = Clock.schedule_once(run, 0.5)

    #change distances and speeds
    def run_y_procedure(self, dt):

        self.disable_run_buttons()

        self.m.jog_absolute_xy(-700, self.m.y_min_jog_abs_limit, 6000)

        self.y_vals = []
        self.raw_y_vals = []

        #total distance required
        TOTAL_DISTANCE = float(TIME_TO_RUN_Y / 60) * MAX_XY_SPEED

        self.y_distance_left = TOTAL_DISTANCE

        self.y_running = True

        def run(dt):

            if self.m.state().startswith('Idle'):

                if not self.y_running:
                    return

                if self.y_distance_left > MAX_Y_DISTANCE:
                    if self.m.mpos_y() < -2460:
                        self.m.jog_relative('Y', MAX_Y_DISTANCE, MAX_XY_SPEED)
                    else:
                        self.m.jog_relative('Y', -MAX_Y_DISTANCE, MAX_XY_SPEED)

                    self.y_distance_left -= MAX_Y_DISTANCE 

                    TIME_FOR_MOVEMENT = float((float(MAX_Y_DISTANCE) / float(MAX_XY_SPEED)) * 60) + 2

                    self.next_run_event = Clock.schedule_once(run, TIME_FOR_MOVEMENT)
                else:
                    if self.m.mpos_y() < -2460:
                        self.m.jog_relative('Y', self.y_distance_left, MAX_XY_SPEED)
                    else:
                        self.m.jog_relative('Y', -self.y_distance_left, MAX_XY_SPEED)

                    TIME_FOR_MOVEMENT = float((float(self.y_distance_left) / float(MAX_XY_SPEED)) * 60) + 2

                    self.y_distance_left = 0

                    Clock.schedule_once(self.disable_y_measurement, TIME_FOR_MOVEMENT)
                    self.confirm_event = Clock.schedule_once(self.confirm_y, TIME_FOR_MOVEMENT)

            else:
                self.next_run_event = Clock.schedule_once(run, 2)

        self.next_run_event = Clock.schedule_once(run, 0.5)

    def run_unweighted_y(self, dt):
        self.y_vals = []
        self.raw_y_vals = []

        #total distance required
        TOTAL_DISTANCE = float(TIME_TO_RUN_Y / 60) * MAX_XY_SPEED

        self.y_distance_left = TOTAL_DISTANCE

        self.y_running = True

        def run(dt):

            if self.m.state().startswith('Idle'):

                if not self.y_running:
                    return

                if self.y_distance_left > MAX_Y_DISTANCE:
                    if self.m.mpos_y() < -2460:
                        self.m.jog_relative('Y', MAX_Y_DISTANCE, MAX_XY_SPEED)
                    else:
                        self.m.jog_relative('Y', -MAX_Y_DISTANCE, MAX_XY_SPEED)

                    self.y_distance_left -= MAX_Y_DISTANCE 

                    TIME_FOR_MOVEMENT = float((float(MAX_Y_DISTANCE) / float(MAX_XY_SPEED)) * 60) + 2

                    self.next_run_event = Clock.schedule_once(run, TIME_FOR_MOVEMENT)
                else:
                    if self.m.mpos_y() < -2460:
                        self.m.jog_relative('Y', self.y_distance_left, MAX_XY_SPEED)
                    else:
                        self.m.jog_relative('Y', -self.y_distance_left, MAX_XY_SPEED)

                    TIME_FOR_MOVEMENT = float((float(self.y_distance_left) / float(MAX_XY_SPEED)) * 60) + 2

                    self.y_distance_left = 0

                    Clock.schedule_once(self.disable_y_measurement, TIME_FOR_MOVEMENT)

            else:
                self.next_run_event = Clock.schedule_once(run, 2)

        self.next_run_event = Clock.schedule_once(run, 0.5)

    #change distances and speeds
    def run_x_procedure(self, dt):

        self.disable_run_buttons()

        self.m.jog_absolute_xy(self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000)

        self.raw_x_vals = []
        self.x_vals = []

        #total distance required
        TOTAL_DISTANCE = float(TIME_TO_RUN_X / 60) * MAX_XY_SPEED

        self.x_distance_left = TOTAL_DISTANCE

        self.x_running = True

        def run(dt):

            if self.m.state().startswith('Idle'):
    
                if not self.x_running:
                    return
                
                if self.x_distance_left > MAX_X_DISTANCE:
                    if self.m.mpos_x() < -1260:
                        self.m.jog_relative('X', MAX_X_DISTANCE, MAX_XY_SPEED)
                    else:
                        self.m.jog_relative('X', -MAX_X_DISTANCE, MAX_XY_SPEED)

                    self.x_distance_left -= MAX_X_DISTANCE 

                    TIME_FOR_MOVEMENT = float((float(MAX_X_DISTANCE) / float(MAX_XY_SPEED)) * 60) + 2

                    self.next_run_event = Clock.schedule_once(run, TIME_FOR_MOVEMENT)
                else:
                    if self.m.mpos_x() < -1260:
                        self.m.jog_relative('X', self.x_distance_left, MAX_XY_SPEED)
                    else:
                        self.m.jog_relative('X', -self.x_distance_left, MAX_XY_SPEED)

                    TIME_FOR_MOVEMENT = float((float(self.x_distance_left) / float(MAX_XY_SPEED)) * 60) + 2

                    self.x_distance_left = 0

                    Clock.schedule_once(self.disable_x_measurement, TIME_FOR_MOVEMENT)
                    self.confirm_event = Clock.schedule_once(self.confirm_x, TIME_FOR_MOVEMENT)

            else:
                self.next_run_event = Clock.schedule_once(run, 2)

        self.next_run_event = Clock.schedule_once(run, 0.5)

    def run_unweighted_x(self, dt):
        self.raw_x_vals = []
        self.x_vals = []

        #total distance required
        TOTAL_DISTANCE = float(TIME_TO_RUN_X / 60) * MAX_XY_SPEED

        self.x_distance_left = TOTAL_DISTANCE

        self.x_running = True

        def run(dt):

            if self.m.state().startswith('Idle'):

                if not self.x_running:
                    return
                
                if self.x_distance_left > MAX_X_DISTANCE:
                    if self.m.mpos_x() < -1260:
                        self.m.jog_relative('X', MAX_X_DISTANCE, MAX_XY_SPEED)
                    else:
                        self.m.jog_relative('X', -MAX_X_DISTANCE, MAX_XY_SPEED)

                    self.x_distance_left -= MAX_X_DISTANCE 

                    TIME_FOR_MOVEMENT = float((float(MAX_X_DISTANCE) / float(MAX_XY_SPEED)) * 60) + 2

                    self.next_run_event = Clock.schedule_once(run, TIME_FOR_MOVEMENT)
                else:
                    if self.m.mpos_x() < -1260:
                        self.m.jog_relative('X', self.x_distance_left, MAX_XY_SPEED)
                    else:
                        self.m.jog_relative('X', -self.x_distance_left, MAX_XY_SPEED)

                    TIME_FOR_MOVEMENT = float((float(self.x_distance_left) / float(MAX_XY_SPEED)) * 60) + 2

                    self.x_distance_left = 0

                    Clock.schedule_once(self.disable_x_measurement, TIME_FOR_MOVEMENT)

            else:
                self.next_run_event = Clock.schedule_once(run, 2)

        self.next_run_event = Clock.schedule_once(run, 0.5)

    def measure(self):

        if self.z_running and self.m.feed_rate() < 80:

            if self.m.s.sg_z_motor_axis == -999:
                return

            if len(self.z_vals) > 0:
                cur_pos = self.m.mpos_z()
                if self.z_vals[len(self.z_vals)-1][1] <  cur_pos:
                    self.z_vals.append([1, float(self.m.mpos_z()), self.m.s.sg_z_motor_axis])
                else:
                    self.z_vals.append([0, float(self.m.mpos_z()), self.m.s.sg_z_motor_axis])
            else:
                self.z_vals.append([0, float(self.m.mpos_z()), self.m.s.sg_z_motor_axis])

            self.raw_z_vals.append(self.m.s.sg_z_motor_axis)
            self.z_peak_load.text = "Z: " + str(max(self.raw_z_vals, key=abs))
            self.z_rt_load.text = "Z: " + str(self.m.s.sg_z_motor_axis)

        elif self.x_running and self.m.feed_rate() < 1200:
            if self.m.s.sg_x_motor_axis == -999:
                return

            if len(self.x_vals) > 0:
                cur_pos = self.m.mpos_x()
                if self.x_vals[len(self.x_vals)-1][1] <  cur_pos:
                    self.x_vals.append([1, float(self.m.mpos_x()), self.m.s.sg_x_motor_axis])
                else:
                    self.x_vals.append([0, float(self.m.mpos_x()), self.m.s.sg_x_motor_axis])
            else:
                self.x_vals.append([0, float(self.m.mpos_x()), self.m.s.sg_x_motor_axis])

            self.raw_x_vals.append(self.m.s.sg_x_motor_axis)
            self.x_peak_load.text = "X: " + str(max(self.raw_x_vals, key=abs))
            self.x_rt_load.text = "X: " + str(self.m.s.sg_x_motor_axis)

        elif self.y_running and self.m.feed_rate() < 1200:
            if self.m.s.sg_y_axis == -999 or self.m.s.sg_y1_motor == -999 or self.m.s.sg_y2_motor == -999:
                return

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
            self.y_peak_load.text = "Y: " + str(max(self.raw_y_vals, key=abs))
            self.y_rt_load.text = "Y: " + str(self.m.s.sg_y_axis)
            self.y1_peak_load.text = "Y: " + str(max(self.raw_y1_vals, key=abs))
            self.y2_peak_load.text = "Y: " + str(max(self.raw_y2_vals, key=abs))
            self.y1_rt_load.text = "Y: " + str(self.m.s.sg_y1_motor)
            self.y2_rt_load.text = "Y: " + str(self.m.s.sg_y2_motor)