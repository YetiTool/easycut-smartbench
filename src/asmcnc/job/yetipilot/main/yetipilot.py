from math import sqrt, ceil, floor
from asmcnc.job.yetipilot.utils.yetipilot_logger import AutoPilotLogger
import time
import json
from kivy.clock import Clock


def format_time(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds)) + '.{:03d}'.format(int(seconds * 1000) % 1000)


def get_single_adjustment(adjustments):
    if isinstance(adjustments, int):
        return adjustments

    adjustments = sorted(adjustments, key=abs)
    return adjustments[0] if len(adjustments) > 0 else None


def get_adjustment(feed_multiplier):
    feed_multiplier = ceil(feed_multiplier) if feed_multiplier < 0 else floor(feed_multiplier)
    negative = feed_multiplier < 0
    feed_multiplier = abs(feed_multiplier) if negative else feed_multiplier

    tens = int(feed_multiplier // 10)
    ones = int(feed_multiplier % 10)

    return [-10 if negative else 10 for _ in range(tens)] + [-1 if negative else 1 for _ in range(ones)]


class YetiPilot:
    # Algorithm Variables
    digital_spindle_mains_voltage = None
    bias_for_feed_decrease = 2.0
    bias_for_feed_increase = 1.0
    m_coefficient = 1.0
    c_coefficient = 35.0
    cap_for_feed_increase = 20
    cap_for_feed_decrease = -40
    cap_for_feed_increase_during_z_movement = 0
    moving_in_z = False

    # System Variables
    enabled = False
    logger = None
    counter = 0
    counter_max = 2
    digital_spindle_stack_max = 2
    digital_spindle_target_watts = 880
    digital_spindle_load_stack = []
    adjustment_count = 2
    adjustment_delay = 0.06
    tolerance_for_acceleration_detection = 50

    def __init__(self, **kwargs):
        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']
        self.jd = kwargs['job_data']

    def start(self):
        self.enabled = True
        job_name = ''

        if self.sm.has_screen('go'):
            job_name = self.sm.get_screen('go').file_data_label.text

        self.load_parameters_from_json()

        self.logger = AutoPilotLogger(
            self.digital_spindle_mains_voltage, self.digital_spindle_target_watts, self.bias_for_feed_increase,
            self.bias_for_feed_decrease,
            self.m_coefficient, self.c_coefficient, self.cap_for_feed_increase, self.cap_for_feed_decrease, job_name,
            self.m.get_smartbench_name(), self.digital_spindle_stack_max, 0,
            self.cap_for_feed_increase_during_z_movement,
            self, None
        )

    def stop(self):
        self.enabled = False

    def set_enabled(self, enabled):
        if enabled:
            self.start()
        else:
            self.stop()

    def ldA_to_watts(self, load):
        return self.digital_spindle_mains_voltage * 0.1 * sqrt(load)

    def get_multiplier(self, digital_spindle_ld_w):
        multiplier = (float(
            self.bias_for_feed_decrease) if digital_spindle_ld_w > self.digital_spindle_target_watts else
                      float(self.bias_for_feed_increase)) * (
                                 float(self.digital_spindle_target_watts) - float(digital_spindle_ld_w)) \
                     / float(self.digital_spindle_target_watts) * float(self.m_coefficient) * float(self.c_coefficient)

        return multiplier

    def cap_multiplier(self, multiplier):
        if self.moving_in_z and multiplier > 0:
            return self.cap_for_feed_increase_during_z_movement

        if multiplier < self.cap_for_feed_decrease:
            return self.cap_for_feed_decrease

        if multiplier > self.cap_for_feed_increase:
            return self.cap_for_feed_increase

        return multiplier

    def calculate_adjustment(self, average_digital_spindle_load):
        multiplier = self.get_multiplier(average_digital_spindle_load)
        capped_multiplier = self.cap_multiplier(multiplier)

        adjustments = get_adjustment(capped_multiplier)

        return adjustments, multiplier, capped_multiplier

    def do_adjustment(self, adjustments):
        for i, adjustment in enumerate(adjustments):
            if i > self.adjustment_count:
                break

            if adjustment == 10:
                Clock.schedule_once(lambda dt: self.m.feed_override_up_10(), i * self.adjustment_delay)
            elif adjustment == 1:
                Clock.schedule_once(lambda dt: self.m.feed_override_up_1(), i * self.adjustment_delay)
            elif adjustment == -10:
                Clock.schedule_once(lambda dt: self.m.feed_override_down_10(), i * self.adjustment_delay)
            elif adjustment == -1:
                Clock.schedule_once(lambda dt: self.m.feed_override_down_1(), i * self.adjustment_delay)

    def get_is_constant_feed_rate(self, feed_override_percentage, feed_rate, current_line_number):
        last_modal_feed_rate = self.jd.find_last_feedrate(current_line_number)
        constant_feed_target = last_modal_feed_rate * feed_override_percentage / 100

        return abs(constant_feed_target - feed_rate) < 50, last_modal_feed_rate

    def add_to_stack(self, digital_spindle_ld_qdA, feed_override_percentage,
                     feed_rate, current_line_number):
        if not self.enabled or self.digital_spindle_mains_voltage is None:
            return

        digital_spindle_ld_w = self.ldA_to_watts(digital_spindle_ld_qdA)

        if len(self.digital_spindle_load_stack) == self.digital_spindle_stack_max:
            self.digital_spindle_load_stack.pop(0)

        self.digital_spindle_load_stack.append(digital_spindle_ld_w)
        self.counter += 1

        if len(self.digital_spindle_load_stack) > 1 and self.counter >= self.counter_max:
            self.counter = 0

            average_digital_spindle_load = sum(
                self.digital_spindle_load_stack[-self.digital_spindle_stack_max:]) / self.digital_spindle_stack_max

            adjustment, raw_multiplier, capped_multiplier = self.calculate_adjustment(average_digital_spindle_load)

            constant_feed, gcode_feed = self.get_is_constant_feed_rate(
                feed_override_percentage, feed_rate, current_line_number)

            if constant_feed:
                self.do_adjustment(adjustment)

            time_stamp = None

            if self.m.s.job_start_time is not None:
                now_time = time.time()
                time_stamp = format_time(now_time - self.m.s.job_start_time)

            g0_move = False
            allow_feedup = not g0_move and constant_feed

            self.logger.add_log(
                current_load=average_digital_spindle_load,
                feed_multiplier=capped_multiplier,
                time=time_stamp,
                raw_loads=self.digital_spindle_load_stack[-self.digital_spindle_stack_max:],
                average_loads=self.digital_spindle_load_stack[-self.digital_spindle_stack_max:],
                raw_multiplier=raw_multiplier,
                adjustment_list=adjustment[:self.adjustment_count],
                feed_override_percentage=feed_override_percentage,
                moving_in_z=str(self.moving_in_z),
                sg_x_motor_axis=self.m.s.sg_x_motor_axis,
                sg_y_axis=self.m.s.sg_y_axis,
                sg_z_motor_axis=self.m.s.sg_z_motor_axis,
                sg_x1_motor=self.m.s.sg_x1_motor,
                sg_x2_motor=self.m.s.sg_x2_motor,
                sg_y1_motor=self.m.s.sg_y1_motor,
                sg_y2_motor=self.m.s.sg_y2_motor,
                target_load=self.digital_spindle_target_watts,
                raw_spindle_load=self.m.s.digital_spindle_ld_qdA,
                spindle_voltage=self.m.s.digital_spindle_mains_voltage,
                feed_rate=feed_rate,
                constant_speed=constant_feed,
                line_number=current_line_number,
                gcode_feed=gcode_feed,
                target_feed=gcode_feed * feed_override_percentage / 100,
                g0_move=g0_move,
                allow_feedup=allow_feedup
            )

    def load_parameters_from_json(self, path_override=None):
        with open('asmcnc/job/yetipilot/main/yetipilot_parameters.json' if not path_override else path_override) as f:
            data = json.load(f)
            for item in data:
                try:
                    setattr(self, item["Name"], item["Value"])
                except:
                    print("Invalid parameter: " + item["Name"])

    def reset(self):
        self.digital_spindle_mains_voltage = None
        self.digital_spindle_load_stack[:] = []
        if self.logger:
            self.logger.reset()

    def set_target_power(self, target_power):
        self.digital_spindle_target_watts = target_power