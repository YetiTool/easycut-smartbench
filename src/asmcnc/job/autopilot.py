"""
Created on 9 Dec 2022
@author: Archie
"""

import json
from datetime import datetime
from math import sqrt, floor
import threading

from kivy.clock import Clock

from autopilot_logger import AutoPilotLogger


class Autopilot:
    # Algorithm Variables
    delay_between_feed_adjustments = 0.3
    do_remove_outliers = 1
    spindle_target_watts = 400
    outlier_tolerance = 100  # Value applied above and below the average of spindle power inputs to remove outliers
    bias_for_feed_decrease = 2.0
    bias_for_feed_increase = 1.0
    m_coefficient = 1.0  # see feed factor algorithm
    # https://docs.google.com/document/d/1twwDlSkzwoy__OZFrJK5IDz0GDaC2_08EKyNHk6_npI/edit#
    c_coefficient = 35  # see above
    cap_for_feed_increase = 20
    cap_for_feed_decrease = -40
    cap_for_feed_increase_during_z_movement = 1
    amount_of_values_in_stack = (delay_between_feed_adjustments * 10) // (0.1 * 10)

    # Instance Variables
    spindle_mains_voltage = None  # TODO: Find fix for getting voltage accurately
    setup = False
    spindle_load_stack = []
    reading_clock = None
    autopilot_logger = None
    moving_in_z = False
    dev_mode = True

    def __init__(self, **kwargs):
        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']

    def log(self, log, override=False):
        if override or self.dev_mode:
            print(log)

    def first_read_setup(self):
        job_name = self.sm.get_screen('go').file_data_label.text

        self.autopilot_logger = AutoPilotLogger(self.spindle_mains_voltage, self.spindle_target_watts, self.bias_for_feed_increase,
                                                self.bias_for_feed_decrease, self.m_coefficient, self.c_coefficient,
                                                self.cap_for_feed_increase, self.cap_for_feed_decrease,
                                                job_name, self.m.serial_number(), self.delay_between_feed_adjustments,
                                                self.outlier_tolerance, self.cap_for_feed_increase_during_z_movement)

        self.setup = True

    def get_best_adjustment(self, percentage):
        percentage = floor(percentage)

        negative = False

        if percentage < 0:
            negative = True
            percentage = abs(percentage)

        tens = int(percentage // 10)
        ones = int(percentage % 10)

        moves = []
        backward_moves = []

        if ones > 5:
            tens += 1

            for i in range(10 - ones):
                backward_moves.append(-1)

            ones = 0

        for _ in range(tens):
            moves.append(10)

        for _ in range(ones):
            moves.append(1)

        limit = int((self.delay_between_feed_adjustments * 100) / (0.05 * 100))

        moves.extend(backward_moves)
        moves = [-move if negative else move for move in moves]

        if len(moves) > limit:
            moves = moves[:limit]

        return moves

    def add_to_stack(self, value):
        if len(self.spindle_load_stack) == int(self.amount_of_values_in_stack):
            self.spindle_load_stack.pop(0)
        self.spindle_load_stack.append(value)

    def adjust(self, data_avg, raw_loads, average_loads):
        if self.m.wpos_z() > 0:
            return

        raw_multiplier = self.get_feed_multiplier(data_avg)

        capped_multiplier = self.cap_feed_multiplier(raw_multiplier, self.spindle_target_watts, data_avg)

        best_adjustment = self.get_best_adjustment(capped_multiplier)

        self.do_best_adjustment(best_adjustment)

        self.log('adjustment list: ' + str(best_adjustment), override=True)

        self.autopilot_logger.add_log(data_avg, capped_multiplier, datetime.now().strftime('%H:%M:%S:%f'),
                                      raw_loads, average_loads, raw_multiplier, best_adjustment,
                                      self.m.s.feed_override_percentage, str(self.moving_in_z),
                                      self.m.s.sg_x_motor_axis, self.m.s.sg_y_axis, self.m.s.sg_z_motor_axis,
                                      self.m.s.sg_x1_motor, self.m.s.sg_x2_motor, self.m.s.sg_y1_motor,
                                      self.m.s.sg_y2_motor)

    def remove_outliers(self, data):
        if len(data) == 0:
            return data

        outlier_list = list(data)
        avg = sum(outlier_list) / len(outlier_list)
        for value in outlier_list:
            if value > avg + self.outlier_tolerance or value < avg - self.outlier_tolerance:
                outlier_list.remove(value)
        return outlier_list

    def read(self, dt):
        if len(self.spindle_load_stack) < self.amount_of_values_in_stack or not self.setup:
            return

        raw_loads = self.load_qdas_to_watts(self.spindle_load_stack)

        loads_to_use = list(raw_loads)

        if self.do_remove_outliers:
            loads_to_use = self.remove_outliers(raw_loads)

            if len(loads_to_use) < 3:
                print('Data invalid - not enough values')
                return

        if len(loads_to_use) == 0:
            return

        data_avg = sum(loads_to_use) / len(loads_to_use)

        self.adjust(data_avg, raw_loads, loads_to_use)

    def start(self):
        self.load_parameters_from_json()
        self.amount_of_values_in_stack = (self.delay_between_feed_adjustments * 10) // (0.1 * 10)

        self.reading_clock = Clock.schedule_interval(self.read, self.delay_between_feed_adjustments)

        self.m.s.autopilot_instance = self
        self.m.s.autopilot_flag = True

    def stop(self):
        if self.reading_clock is not None:
            Clock.unschedule(self.reading_clock)
            self.m.s.autopilot_flag = False

    def export(self):
        self.autopilot_logger.export_to_gsheet()

    def load_qdas_to_watts(self, qdas):
        return [self.spindle_mains_voltage * 0.1 * sqrt(qda) for qda in qdas if qda is not None and qda > 0]

    def cap_feed_multiplier(self, multiplier, target_power, current_power):
        if self.moving_in_z and current_power < target_power:
            return -self.cap_for_feed_increase_during_z_movement \
                if current_power > target_power \
                else self.cap_for_feed_increase_during_z_movement

        if current_power > target_power:
            if multiplier < self.cap_for_feed_decrease:
                return self.cap_for_feed_decrease
            else:
                return multiplier

        if current_power < target_power:
            if multiplier > self.cap_for_feed_increase:
                return self.cap_for_feed_increase
            else:
                return multiplier

        return multiplier

    def get_feed_multiplier(self, current_power):
        multiplier = (float(self.bias_for_feed_decrease) if current_power > self.spindle_target_watts else float(self.bias_for_feed_increase)) * (
                float(self.spindle_target_watts) - float(current_power)) / float(self.spindle_target_watts) \
                     * float(self.m_coefficient) * float(self.c_coefficient)

        return multiplier

    def do_best_adjustment(self, adjustment_list):
        feed_override_widget = self.sm.get_screen('go').feedOverride

        if not feed_override_widget:
            return

        for i in range(len(adjustment_list)):
            if feed_override_widget.feed_override_percentage + adjustment_list[i] > 200 or \
                    feed_override_widget.feed_override_percentage - adjustment_list[i] < 10:
                continue

            if adjustment_list[i] == 10:
                feed_override_widget.feed_override_percentage += 10
                Clock.schedule_once(
                    lambda dt: self.m.feed_override_up_10(feed_override_widget.feed_override_percentage), 0.05 * i)
            elif adjustment_list[i] == 1:
                feed_override_widget.feed_override_percentage += 1
                Clock.schedule_once(lambda dt: self.m.feed_override_up_1(feed_override_widget.feed_override_percentage),
                                    0.05 * i)
            elif adjustment_list[i] == -10:
                feed_override_widget.feed_override_percentage -= 10
                Clock.schedule_once(
                    lambda dt: self.m.feed_override_down_10(feed_override_widget.feed_override_percentage), 0.05 * i)
            elif adjustment_list[i] == -1:
                feed_override_widget.feed_override_percentage -= 1
                Clock.schedule_once(
                    lambda dt: self.m.feed_override_down_1(feed_override_widget.feed_override_percentage), 0.05 * i)

    def load_parameters_from_json(self):
        with open('asmcnc/job/autopilot_parameters.json') as f:
            data = json.load(f)
            for item in data:
                try:
                    setattr(self, item["Name"], item["Value"])
                except:
                    print("Invalid parameter: " + item["Name"])

    def cancel_job(self):
        self.setup = False
        self.m.s.autopilot_flag = False
        self.export()

    def reset(self):
        self.spindle_mains_voltage = None
        self.spindle_load_stack = []
        self.autopilot_logger.reset()
