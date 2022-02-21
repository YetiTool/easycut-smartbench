from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

import datetime

Builder.load_string("""
<LBCalibration1>:
    calibrate_time:calibrate_time

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1.00

        GridLayout:
            cols: 1
            rows: 2

            Label:
                text: 'Countdown to calibration...'
                font_size: dp(50)
            
            Label:
                id: calibrate_time
                text: '00:30:00'
                font_size: dp(50)

""")

class LBCalibration1(Screen):
    def __init__(self, **kwargs):
        super(LBCalibration1, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

        self.update_time(30 * 60) # 30 minutes 

    def update_time(self, time_left):
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

    def on_enter(self):
        if self.seconds < 1:
            self.sm.current = 'lbc2'
