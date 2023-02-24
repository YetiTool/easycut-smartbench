import json
from kivy.clock import Clock

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

    # List for override events, that can be unscheduled/cleared when a job is paused or stopped
    scheduled_overrides = []

    def __init__(self, **kwargs):
        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']
        self.jd = kwargs['job_data']

    def start(self):
        self.load_parameters_from_json()
        self.use_yp = True

    def stop(self):
        self.use_yp = False

    # placeholder - confirm that YP is running
    def add_to_stack(self):
        log("Hi it's YetiPilot, let's have a safe flight")
        Clock.schedule_once(lambda dt: self.feed_override_wrapper(dummy_override), 1)

    # Keep this - ensures that commands are only sent if job is streaming & not paused
    def feed_override_wrapper(feed_override_func):
        if self.m.s.is_job_streaming and not self.m.is_machine_paused:
            feed_override_func()

    # For simulating feed overrides
    def dummy_override(self):
        log("Pilot sends feed override")
