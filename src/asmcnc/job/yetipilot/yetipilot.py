import json
from kivy.clock import Clock
from datetime import datetime

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message))

class YetiPilot(object):

    ## COMMENTED OUT BC POSSIBLY SUBJECT TO CHANGE
    # # Algorithm Variables
    # digital_spindle_mains_voltage = None
    # bias_for_feed_decrease = 2.0
    # bias_for_feed_increase = 1.0
    # m_coefficient = 1.0
    # c_coefficient = 35.0
    # cap_for_feed_increase = 20
    # cap_for_feed_decrease = -40
    # cap_for_feed_increase_during_z_movement = 0
    # moving_in_z = False

    # # System Variables
    # enabled = False
    # logger = None
    # counter = 0
    # statuses_per_adjustment = 2
    # spindle_load_stack_size = 2
    # spindle_target_load_watts = 880
    # digital_spindle_load_stack = []
    # override_commands_per_adjustment = 2
    # override_command_delay = 0.06
    # tolerance_for_acceleration_detection = 50

    use_yp = False

    standard_profiles = True

    diameter = "3mm"
    tool = "2 flute upcut spiral"
    material = "MDF"

    target_ld = 700

    step_min = 3
    step_max = 6

    def __init__(self, **kwargs):
        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']
        self.jd = kwargs['job_data']

    def enable(self):
        self.load_parameters_from_json()
        self.use_yp = True

    def disable(self):
        self.use_yp = False

    def load_parameters_from_json(self):
        pass

    # placeholder - confirm that YP is running
    def add_to_stack(self):
        log("Hi it's YetiPilot, let's have a safe flight")
        Clock.schedule_once(lambda dt: self.feed_override_wrapper(self.dummy_override), 1)

    # Keep this - ensures that commands are only sent if job is streaming & not paused
    # Use it when scheduling feed overrides
    def feed_override_wrapper(self, feed_override_func):
        if self.use_yp and self.m.s.is_job_streaming and \
           not self.m.is_machine_paused and not "Alarm" in self.m.state():
            feed_override_func()

    # For simulating feed overrides
    def dummy_override(self):
        log("Pilot sends feed override")
