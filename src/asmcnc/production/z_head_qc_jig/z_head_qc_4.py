from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.comms.logging import log_exporter

Builder.load_string("""
<ZHeadQC4>:

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
            font_size: app.get_scaled_width(50.0)
            text_size: root.width, None
            size: self.texture_size
            halign: 'center'

    
""")

class ZHeadQC4(Screen):

    poll_for_tuning_completion = None
    poll_for_calibration_check = None
    poll_for_calibration_completion = None

    def __init__(self, **kwargs):
        super(ZHeadQC4, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    def on_enter(self):
        if not self.m.run_calibration and not self.m.tuning_in_progress:
            self.calibration_label.text = "Calibrating..."
            self.run_calibration()

        else: 
            self.calibration_label.text = "Try later"
            Clock.schedule_once(self.enter_prev_screen, 3)

    def run_calibration(self):
        self.m.tune_X_and_Z_for_calibration()
        self.poll_for_tuning_completion = Clock.schedule_interval(self.start_calibrating, 5)

    def start_calibrating(self, dt):
        if not self.m.tuning_in_progress:
            Clock.unschedule(self.poll_for_tuning_completion)

            if not self.m.calibration_tuning_fail_info:
                self.m.calibrate_X_and_Z()
                self.poll_for_calibration_check = Clock.schedule_interval(self.check_calibration, 5)

            else:
                self.calibration_label.text = self.m.calibration_tuning_fail_info

    def check_calibration(self, dt):
        if not self.m.run_calibration:
            Clock.unschedule(self.poll_for_calibration_check)

            if not self.m.calibration_tuning_fail_info:
                self.m.start_measuring_running_data(stage=12)
                self.m.check_x_z_calibration()
                self.poll_for_calibration_completion = Clock.schedule_interval(self.finish_calibrating, 5)

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
        self.sm.current = 'qc5'

    def enter_prev_screen(self, dt):
        self.sm.current = 'qc2'

    def on_leave(self):
        if self.poll_for_tuning_completion != None: Clock.unschedule(self.poll_for_tuning_completion)
        if self.poll_for_calibration_check != None: Clock.unschedule(self.poll_for_calibration_check)
        if self.poll_for_calibration_completion != None: Clock.unschedule(self.poll_for_calibration_completion)