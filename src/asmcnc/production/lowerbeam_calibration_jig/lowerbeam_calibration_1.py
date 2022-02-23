from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

import datetime

Builder.load_string("""
<LBCalibration1>:
    calibrate_time:calibrate_time
    user_text : user_text

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1.00

        GridLayout:
            cols: 1
            rows: 2

            Label:
                id: user_text
                text: "Getting ready..."
                font_size: dp(50)
            
            Label:
                id: calibrate_time
                text: ''
                font_size: dp(50)

""")

class LBCalibration1(Screen):

    timer_started = False
    seconds = 60*30

    def __init__(self, **kwargs):
        super(LBCalibration1, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    def on_enter(self):

        if self.seconds < 1:
            self.sm.current = 'lbc2'

        elif not self.timer_started:
            Clock.schedule_once(lambda dt: self.start_calibration_timer(60), 5)

    def start_calibration_timer(self, minutes):

        if self.state().startswith('Idle'):
            self.m.jog_absolute_xy(self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000)
            self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)
            self.m.jog_relative('X', 2, 6000)
            self.update_time(30 * 60) # 30 minutes
            self.timer_started = True

        else: 
            Clock.schedule_once(lambda dt: self.start_calibration_timer(60), 1)

    def update_time(self, time_left):

        self.user_text = 'Countdown to calibration...'

        seconds = time_left

        def count_down(seconds):
            if seconds == 0:
                if self.sm.current == self.name:
                    print('entering')
                    self.sm.current = 'lbc2'
                    return
            
            if seconds > 0:
                seconds -= 1
                self.seconds = seconds

            self.calibrate_time.text = str(datetime.timedelta(seconds=seconds))

            Clock.schedule_once(lambda dt: count_down(seconds), 1)

        Clock.schedule_once(lambda dt: count_down(seconds), 0)

