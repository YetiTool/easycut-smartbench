from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
import datetime

Builder.load_string(
    """
<ZHeadQC3>:
    calibrate_time:calibrate_time
    user_text : user_text

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1.00

        Button:
            text: '<<< Back'
            on_press: root.enter_prev_screen()
            text_size: self.size
            markup: 'True'
            halign: 'left'
            valign: 'middle'
            padding: [dp(10),0]
            size_hint_y: 0.2
            size_hint_x: 0.5
            font_size: dp(20)

        BoxLayout: 
            orientation: "vertical"
            spacing: dp(10)

            Label:
                text: 'ENSURE COVER ON'
                font_size: dp(50)

            Label:
                id: user_text
                text: "Getting ready..."
                font_size: dp(50)
            
            Label:
                id: calibrate_time
                text: root.formatted_max
                font_size: dp(50)

"""
)


class ZHeadQC3(Screen):
    timer_started = False
    one_minute = 60
    max_minutes = 1.5
    seconds = one_minute * max_minutes
    formatted_max = str(datetime.timedelta(seconds=seconds))

    def __init__(self, **kwargs):
        self.sm = kwargs.pop("sm")
        self.m = kwargs.pop("m")
        super(ZHeadQC3, self).__init__(**kwargs)

    def on_enter(self):
        if self.seconds < 1:
            self.sm.current = "qc4"
        elif not self.timer_started:
            Clock.schedule_once(lambda dt: self.start_calibration_timer(), 1)

    def start_calibration_timer(self):
        if self.m.state().startswith("Idle"):
            self.m.jog_absolute_xy(
                self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000
            )
            self.m.jog_absolute_single_axis("Z", self.m.z_max_jog_abs_limit, 750)
            self.m.jog_relative("X", 30, 6000)
            self.m.jog_relative("X", -30, 6000)
            self.update_time(self.max_minutes * self.one_minute)
            self.timer_started = True
        else:
            Clock.schedule_once(lambda dt: self.start_calibration_timer(), 1)

    def update_time(self, time_left):
        self.user_text.text = "Countdown to calibration..."
        seconds = time_left

        def count_down(seconds):
            if self.timer_started:
                if seconds == 0:
                    if self.sm.current == self.name:
                        self.sm.current = "qc4"
                        return
                if seconds > 0:
                    seconds -= 1
                    self.seconds = seconds
                self.calibrate_time.text = str(datetime.timedelta(seconds=seconds))
                Clock.schedule_once(lambda dt: count_down(seconds), 1)

        Clock.schedule_once(lambda dt: count_down(seconds), 0)

    def enter_prev_screen(self):
        self.sm.current = "qc2"

    def reset_timer(self):
        self.seconds = self.one_minute * self.max_minutes
        self.timer_started = False
        self.user_text.text = "Getting ready..."
        self.calibrate_time.text = "0:30:00"
