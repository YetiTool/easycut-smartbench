from math import ceil, floor
from kivy.clock import Clock
from asmcnc.job.yetipilot.utils.autopilot_logger import AutoPilotLogger
from datetime import datetime


def get_adjustment(feed_multiplier):
    feed_multiplier = ceil(feed_multiplier) if feed_multiplier < 0 else floor(feed_multiplier)
    negative = feed_multiplier < 0
    feed_multiplier = abs(feed_multiplier) if negative else feed_multiplier

    tens = int(feed_multiplier // 10)
    ones = int(feed_multiplier % 10)

    if tens > 0:
        return -10 if negative else 10

    if ones > 0:
        return -1 if negative else 1

    return 0


def limit_adjustments(adjustments):
    if isinstance(adjustments, int):
        return adjustments

    adjustments = sorted(adjustments, key=abs)
    return adjustments[0] if len(adjustments) > 0 else None


class YetiPilot:
    status_count_before_adjustment = 1

    # Algorithm Variables
    bias_for_feed_decrease = 2.0
    bias_for_feed_increase = 1.0
    m_coefficient = 1.0
    c_coefficient = 35.0
    cap_for_feed_increase = 20
    cap_for_feed_decrease = -40
    cap_for_feed_increase_during_z_movement = 1
    moving_in_z = False

    # Spindle Variables
    spindle_stack_max_length = 5
    spindle_mains_voltage = None
    spindle_load_stack = []
    spindle_target_watts = 400

    enabled = False
    counter = 0

    logger = None

    def __init__(self, **kwargs):
        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']

    def start(self):
        self.enabled = True

        job_name = self.sm.get_screen('go').file_data_label.text

        print("Creating logger")

        self.logger = AutoPilotLogger(
            self.spindle_mains_voltage, self.spindle_target_watts, self.bias_for_feed_increase, self.bias_for_feed_decrease,
            self.m_coefficient, self.c_coefficient, self.cap_for_feed_increase, self.cap_for_feed_decrease, job_name,
            self.m.serial_number(), self.status_count_before_adjustment, 0, self.cap_for_feed_increase_during_z_movement,
            self)

    def stop(self):
        self.enabled = False

        if self.logger is not None:
            self.logger.export_to_gsheet()

    def set_enabled(self, enabled):
        if enabled:
            self.start()
            return

        self.stop()

    def set_spindle_voltage(self, voltage):
        self.spindle_mains_voltage = voltage

    def set_target_power(self, power):
        self.spindle_target_watts = power
        print('Target power: ' + str(power))

    def add_to_stack(self, load):
        if not self.enabled or self.spindle_mains_voltage is None:
            return

        if len(self.spindle_load_stack) == self.spindle_stack_max_length:
            self.spindle_load_stack.pop(0)

        self.spindle_load_stack.append(load)

        self.counter += 1
        if self.counter == self.status_count_before_adjustment:
            self.do_adjustment(load)
            self.counter = 0

    def do_adjustment(self, load):
        feed_multiplier = self.get_feed_multiplier(load)
        adjustments = get_adjustment(feed_multiplier)
        adjustment = limit_adjustments(adjustments)

        self.logger.add_log(
            load, adjustment, datetime.now().strftime('%H:%M:%S:%f'), self.spindle_load_stack, self.spindle_load_stack,
            adjustment, adjustment, self.m.s.feed_override_percentage, str(self.moving_in_z), self.m.s.sg_x_motor_axis,
            self.m.s.sg_y_axis, self.m.s.sg_z_motor_axis, self.m.s.sg_x1_motor, self.m.s.sg_x2_motor, self.m.s.sg_y1_motor,
            self.m.s.sg_y2_motor)

        if adjustment is None:
            return

        if adjustment == 10:
            self.m.feed_override_up_10()
        elif adjustment == 1:
            self.m.feed_override_up_1()
        elif adjustment == -10:
            self.m.feed_override_down_10()
        elif adjustment == -1:
            self.m.feed_override_down_1()

    def get_feed_multiplier(self, current_power):
        multiplier = (float(self.bias_for_feed_decrease) if current_power > self.spindle_target_watts else
                      float(self.bias_for_feed_increase)) * (float(self.spindle_target_watts) - float(current_power)) \
                     / float(self.spindle_target_watts) * float(self.m_coefficient) * float(self.c_coefficient)

        return multiplier


