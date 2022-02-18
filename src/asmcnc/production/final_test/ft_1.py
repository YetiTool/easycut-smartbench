from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from datetime import datetime
import math

Builder.load_string("""
<FinalTestScreenTest>:
    y_rt_load:y_rt_load
    y1_rt_load:y1_rt_load
    y2_rt_load:y2_rt_load
    x_rt_load:x_rt_load
    z_rt_load:z_rt_load

    z_peak_load:z_peak_load
    x_peak_load:x_peak_load
    y_peak_load:y_peak_load
    y1_peak_load:y1_peak_load
    y2_peak_load:y2_peak_load

    BoxLayout:
        orientation: 'vertical'

        GridLayout: 
            cols: 7
        
            Button:
                text: 'Home'
                on_press: root.home()
                
            Button:
                text: 'Reset'
                on_press: root.reset()

            Button:
                text: 'Run unweighted test'
                on_press: root.run_unweighted()

            Button:
                text: 'Run Z (2kg)'
                on_press: root.run_z_procedure(None)

            Button:
                text: 'Run X (5kg)'
                on_press: root.run_x_procedure(None)

            Button:
                text: 'Run Y (5kg)'
                on_press: root.run_y_procedure(None)

            Button:
                text: 'Run overnight'
                on_press: root.run_overnight_test()

        GridLayout:
            rows: 1
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

TIME_TO_RUN_Z = 241
TIME_TO_RUN_X = 120
TIME_TO_RUN_Y = 239

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class FinalTestScreenTest(Screen):
    def __init__(self, **kwargs):
        super(FinalTestScreenTest, self).__init__(**kwargs)

        self.m = kwargs['m']

        self.x_running = False
        self.y_running = False
        self.z_running = False
        self.x_vals = []
        self.y_vals = []
        self.z_vals = []
        self.raw_z_vals = []
        self.raw_x_vals = []
        self.raw_y_vals = []
        self.raw_y1_vals = []
        self.raw_y2_vals = []

    def on_enter(self):
        self.m.s.FINAL_TEST = True

    def on_leave(self):
        self.m.s.FINAL_TEST = False

    def run_overnight_test(self):
        #6 hours in seconds
        self.OVERNIGHT_TIME_TO_RUN = 21600
        X_TOTAL_TIME = MAX_X_DISTANCE / MAX_XY_SPEED #0.8431703204 mins
        Z_TOTAL_TIME = MAX_Z_DISTANCE / MAX_Z_SPEED #1.33333333333 mins
        Y_TOTAL_TIME = MAX_Y_DISTANCE / MAX_XY_SPEED #1.26475548061 mins
        self.OVERNIGHT_RECTANGLE_TIME = ((X_TOTAL_TIME * 60) + (Z_TOTAL_TIME * 60) + (Y_TOTAL_TIME * 60)) * 2 # 206.47554806 seconds
        self.OVERNIGHT_TOTAL_RUNS = 0
        self.OVERNIGHT_REQUIRED_RUNS = math.ceil(self.OVERNIGHT_TIME_TO_RUN / self.OVERNIGHT_RECTANGLE_TIME)

        def run_rectangle(dt):
            if self.OVERNIGHT_TOTAL_RUNS == self.OVERNIGHT_REQUIRED_RUNS:
                Clock.unschedule(self.OVERNIGHT_CLOCK)

            self.m.jog_relative('Z', -MAX_Z_DISTANCE, MAX_Z_SPEED)
            self.m.jog_relative('X', MAX_X_DISTANCE, MAX_XY_SPEED)
            self.m.jog_relative('Y', MAX_Y_DISTANCE, MAX_XY_SPEED)

            self.m.jog_relative('Z', MAX_Z_DISTANCE, MAX_Z_SPEED)
            self.m.jog_relative('X', -MAX_X_DISTANCE, MAX_XY_SPEED)
            self.m.jog_relative('Y', -MAX_Y_DISTANCE, MAX_XY_SPEED)

            self.OVERNIGHT_TIME_TO_RUN -= self.OVERNIGHT_RECTANGLE_TIME

        run_rectangle(None)
        self.OVERNIGHT_CLOCK = Clock.schedule_interval(run_rectangle, self.OVERNIGHT_RECTANGLE_TIME)

    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('ft','ft')

    def reset(self):
        self.m.resume_from_alarm()

    def disable_x_measurement(self, dt):
        print(self.x_vals)
        self.x_running = False

    def disable_z_measurement(self, dt):
        print(self.z_vals)
        self.z_running = False

    def disable_y_measurement(self, dt):
        print(self.y_vals)
        self.y_running = False

    def run_unweighted(self):
        self.run_z_procedure(None)

        Clock.schedule_once(self.run_x_procedure, TIME_TO_RUN_Z + 10)

        Clock.schedule_once(self.run_y_procedure, TIME_TO_RUN_Z + TIME_TO_RUN_X + 20)

    def stop_all_procedures(self):
        self.disable_x_measurement(None)
        self.disable_y_measurement(None)
        self.disable_z_measurement(None)

        log("Stopped all procedures")

    def run_z_procedure(self, dt):
        self.z_vals = []
        self.raw_z_vals = []

        #total distance required
        TOTAL_DISTANCE = float(TIME_TO_RUN_Z / 60) * MAX_Z_SPEED

        self.z_distance_left = TOTAL_DISTANCE

        self.z_running = True

        def run(dt):
            if not self.z_running:
                return

            if self.z_distance_left > MAX_Z_DISTANCE:
                if self.m.mpos_z() > -30:
                    self.m.jog_relative('Z', -MAX_Z_DISTANCE, MAX_Z_SPEED)
                else:
                    self.m.jog_relative('Z', MAX_Z_DISTANCE, MAX_Z_SPEED)

                self.z_distance_left -= MAX_Z_DISTANCE 

                TIME_FOR_MOVEMENT = float((float(MAX_Z_DISTANCE) / float(MAX_Z_SPEED)) * 60)

                Clock.schedule_once(run, TIME_FOR_MOVEMENT)
            else:
                if self.m.mpos_z() > -30:
                    self.m.jog_relative('Z', -self.z_distance_left, MAX_Z_SPEED)
                else:
                    self.m.jog_relative('Z', self.z_distance_left, MAX_Z_SPEED)

                TIME_FOR_MOVEMENT = float((float(self.z_distance_left) / float(MAX_Z_SPEED)) * 60)

                self.z_distance_left = 0

                Clock.schedule_once(self.disable_z_measurement, TIME_FOR_MOVEMENT)

        run(None)

    #change distances and speeds
    def run_y_procedure(self, dt):
        self.y_vals = []
        self.raw_y_vals = []

        #total distance required
        TOTAL_DISTANCE = float(TIME_TO_RUN_Y / 60) * MAX_XY_SPEED

        self.y_distance_left = TOTAL_DISTANCE

        self.y_running = True

        def run(dt):
            if not self.y_running:
                return

            if self.y_distance_left > MAX_Y_DISTANCE:
                if self.m.mpos_y() < -2460:
                    self.m.jog_relative('Y', MAX_Y_DISTANCE, MAX_XY_SPEED)
                else:
                    self.m.jog_relative('Y', -MAX_Y_DISTANCE, MAX_XY_SPEED)

                self.y_distance_left -= MAX_Y_DISTANCE 

                TIME_FOR_MOVEMENT = float((float(MAX_Y_DISTANCE) / float(MAX_XY_SPEED)) * 60)

                Clock.schedule_once(run, TIME_FOR_MOVEMENT)
            else:
                if self.m.mpos_y() < -2460:
                    self.m.jog_relative('Y', self.y_distance_left, MAX_XY_SPEED)
                else:
                    self.m.jog_relative('Y', -self.y_distance_left, MAX_XY_SPEED)

                TIME_FOR_MOVEMENT = float((float(self.y_distance_left) / float(MAX_XY_SPEED)) * 60)

                self.y_distance_left = 0

                Clock.schedule_once(self.disable_y_measurement, TIME_FOR_MOVEMENT)

        run(None)

    #change distances and speeds
    def run_x_procedure(self, dt):
        #total distance required
        TOTAL_DISTANCE = float(TIME_TO_RUN_X / 60) * MAX_XY_SPEED

        self.x_distance_left = TOTAL_DISTANCE

        self.x_running = True

        def run(dt):
            if not self.x_running:
                return
            
            if self.x_distance_left > MAX_X_DISTANCE:
                if self.m.mpos_x() < -1260:
                    self.m.jog_relative('X', MAX_X_DISTANCE, MAX_XY_SPEED)
                else:
                    self.m.jog_relative('X', -MAX_X_DISTANCE, MAX_XY_SPEED)

                self.x_distance_left -= MAX_X_DISTANCE 

                TIME_FOR_MOVEMENT = float((float(MAX_X_DISTANCE) / float(MAX_XY_SPEED)) * 60)

                Clock.schedule_once(run, TIME_FOR_MOVEMENT)
            else:
                if self.m.mpos_x() < -1260:
                    self.m.jog_relative('X', self.x_distance_left, MAX_XY_SPEED)
                else:
                    self.m.jog_relative('X', -self.x_distance_left, MAX_XY_SPEED)

                TIME_FOR_MOVEMENT = float((float(self.x_distance_left) / float(MAX_XY_SPEED)) * 60)

                self.x_distance_left = 0

                Clock.schedule_once(self.disable_x_measurement, TIME_FOR_MOVEMENT)

        run(None)

    def measure(self):
        if self.z_running:
            if self.m.s.z_motor_axis == "-999":
                return

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
        elif self.x_running:
            if self.m.s.x_motor_axis == "-999":
                return

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
        elif self.y_running:
            if self.m.s.y_axis == "-999" or self.m.s.y1_motor == "-999" or self.m.s.y2_motor == "-999":
                return

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
