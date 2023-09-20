from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.comms.yeti_grbl_protocol.c_defines import *

Builder.load_string(
    """
<LBCalibration2>:

    calibration_label : calibration_label
    
    canvas:
        Color:
            rgba: hex('#1976d2ff')

        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'

        Label:
            id: calibration_label
            text: 'Calibrating...'
            font_size: dp(50)
            text_size: root.width, None
            size: self.texture_size
            halign: 'center'

    
"""
)


class LBCalibration2(Screen):
    poll_for_tuning_completion = None
    poll_for_calibration_check = None
    poll_for_calibration_completion = None

    def __init__(self, **kwargs):
        self.sm = kwargs.pop("sm")
        self.m = kwargs.pop("m")
        super(LBCalibration2, self).__init__(**kwargs)

    def on_enter(self):
        if not self.m.run_calibration and not self.m.tuning_in_progress:
            self.calibration_label.text = "Calibrating..."
            self.run_calibration()
        else:
            self.calibration_label.text = "Try later"
            Clock.schedule_once(self.reenter_screen, 3)

    def run_calibration(self):
        self.m.tune_Y_for_calibration()
        self.poll_for_tuning_completion = Clock.schedule_interval(
            self.start_calibrating, 5
        )

    def start_calibrating(self, dt):
        if not self.m.tuning_in_progress:
            Clock.unschedule(self.poll_for_tuning_completion)
            if not self.m.calibration_tuning_fail_info:
                self.m.calibrate_Y()
                self.poll_for_calibration_check = Clock.schedule_interval(
                    self.check_calibration, 5
                )
            else:
                self.calibration_label.text = self.m.calibration_tuning_fail_info

    def check_calibration(self, dt):
        if not self.m.run_calibration:
            Clock.unschedule(self.poll_for_calibration_check)
            if not self.m.calibration_tuning_fail_info:
                self.m.start_measuring_running_data(stage=13)
                self.m.check_y_calibration()
                self.poll_for_calibration_completion = Clock.schedule_interval(
                    self.finish_calibrating, 5
                )
            else:
                self.calibration_label.text = self.m.calibration_tuning_fail_info

    def finish_calibrating(self, dt):
        if not self.m.checking_calibration_in_progress:
            Clock.unschedule(self.poll_for_calibration_completion)
            self.m.stop_measuring_running_data()
            if not self.m.checking_calibration_fail_info:
                self.enter_next_screen()
            else:
                self.calibration_label.text = self.m.checking_calibration_fail_info

    def enter_next_screen(self):
        self.sm.current = "lbc3"

    def reenter_screen(self):
        self.sm.current = "lbc1"
        self.sm.current = "lbc2"

    def on_leave(self):
        if self.poll_for_tuning_completion != None:
            Clock.unschedule(self.poll_for_tuning_completion)
        if self.poll_for_calibration_check != None:
            Clock.unschedule(self.poll_for_calibration_check)
        if self.poll_for_calibration_completion != None:
            Clock.unschedule(self.poll_for_calibration_completion)
