from math import ceil, floor, sqrt
from asmcnc.job.yetipilot.utils.autopilot_logger import AutoPilotLogger
import time
import json


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


def format_time(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds)) + '.{:03d}'.format(int(seconds * 1000) % 1000)


class YetiPilot:
    status_count_before_adjustment = 2

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
    spindle_sample_stack = []
    spindle_sample_count = 2

    enabled = False
    counter = 0

    logger = None

    def __init__(self, **kwargs):
        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']

    def start(self):
        self.enabled = True

        job_name = ''

        if self.sm.has_screen('go'):
            job_name = self.sm.get_screen('go').file_data_label.text

        self.load_parameters_from_json()

        self.logger = AutoPilotLogger(
            self.spindle_mains_voltage, self.spindle_target_watts, self.bias_for_feed_increase, self.bias_for_feed_decrease,
            self.m_coefficient, self.c_coefficient, self.cap_for_feed_increase, self.cap_for_feed_decrease, job_name,
            self.m.serial_number(), self.status_count_before_adjustment, 0, self.cap_for_feed_increase_during_z_movement,
            self)

    def stop(self):
        self.enabled = False

    def set_enabled(self, enabled):
        if enabled:
            self.start()
            return

        self.stop()

    def set_spindle_voltage(self, voltage):
        self.spindle_mains_voltage = voltage
        self.logger.spindle_v_main = voltage

    def set_target_power(self, power):
        self.spindle_target_watts = power

    def lda_to_watts(self, load):
        return self.spindle_mains_voltage * 0.1 * sqrt(load)

    def add_to_stack(self, load):
        if not self.enabled or self.spindle_mains_voltage is None:
            return

        load = self.lda_to_watts(load)

        if len(self.spindle_load_stack) == self.spindle_stack_max_length:
            self.spindle_load_stack.pop(0)

        if len(self.spindle_sample_stack) == self.spindle_sample_count:
            self.spindle_sample_stack.pop(0)

        self.spindle_sample_stack.append(load)
        self.spindle_load_stack.append(load)

        avg = sum(self.spindle_sample_stack) / len(self.spindle_sample_stack)

        self.counter += 1
        if self.counter == self.status_count_before_adjustment:
            self.do_adjustment(avg)
            self.counter = 0

    def cap_multiplier(self, multiplier):
        if self.moving_in_z and multiplier > 0:
            return self.cap_for_feed_increase_during_z_movement

        if multiplier < self.cap_for_feed_decrease:
            return self.cap_for_feed_decrease

        if multiplier > self.cap_for_feed_increase:
            return self.cap_for_feed_increase

        return multiplier

    def do_adjustment(self, load):
        feed_multiplier = self.get_feed_multiplier(load)
        adjustments = get_adjustment(feed_multiplier)
        adjustment = limit_adjustments(adjustments)
        adjustment = self.cap_multiplier(adjustment)

        time_stamp = None

        if self.m.s.job_start_time is not None:
            now_time = time.time()
            time_stamp = format_time(now_time - self.m.s.job_start_time)

        self.logger.add_log(
            load, adjustment, time_stamp, self.spindle_load_stack[:], self.spindle_load_stack[:],
            adjustment, adjustment, self.m.s.feed_override_percentage, str(self.moving_in_z), self.m.s.sg_x_motor_axis,
            self.m.s.sg_y_axis, self.m.s.sg_z_motor_axis, self.m.s.sg_x1_motor, self.m.s.sg_x2_motor, self.m.s.sg_y1_motor,
            self.m.s.sg_y2_motor, self.spindle_target_watts, self.m.s.digital_spindle_ld_qdA, self.m.s.digital_spindle_mains_voltage,
            self.m.s.feed_rate)

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

    def reset(self):
        self.spindle_mains_voltage = None
        self.spindle_load_stack[:] = []
        if self.logger:
            self.logger.reset()

    def load_parameters_from_json(self):
        with open('asmcnc/job/yetipilot/main/yetipilot_parameters.json') as f:
            data = json.load(f)
            for item in data:
                try:
                    setattr(self, item["Name"], item["Value"])
                except:
                    print("Invalid parameter: " + item["Name"])

