"""
Created on 9 Dec 2022
@author: Archie
"""

from kivy.clock import Clock
from math import sqrt, floor
from autopilot_logger import AutoPilotLogger
from datetime import datetime
import json


def get_best_adjustment(percentage):
    moves = []

    tens = percentage // 10
    ones = percentage % 10

    for i in range(int(floor(tens))):
        moves.append(10)

    for i in range(int(floor(ones))):
        moves.append(1)

    return moves


class Autopilot:
    # Algorithm Variables

    delay_between_feed_adjustments = 0.5
    spindle_target_watts = 875
    outlier_amount = 100  # Value applied above and below the average of spindle power inputs to remove outliers
    bias_for_feed_decrease = 2.0
    m_coefficient = 1.0  # see feed factor algorithm
    # https://docs.google.com/document/d/1twwDlSkzwoy__OZFrJK5IDz0GDaC2_08EKyNHk6_npI/edit#
    c_coefficient = 30 / 0.875  # see above
    cap_for_feed_increase = 20
    cap_for_feed_decrease = -40

    # Instance Variables

    spindle_mains_voltage = None
    setup = False
    spindle_load_stack = []
    reading_clock = None
    autopilot_logger = None

    def __init__(self, **kwargs):
        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']

    def first_read_setup(self):
        job_name = self.sm.get_screen('go').file_data_label.text

        self.autopilot_logger = AutoPilotLogger(self.spindle_mains_voltage, self.spindle_target_watts,
                                                self.bias_for_feed_decrease, self.m_coefficient, self.c_coefficient,
                                                self.cap_for_feed_increase, self.cap_for_feed_decrease,
                                                job_name, self.m.serial_number(), self.delay_between_feed_adjustments,
                                                self.outlier_amount)
        # confirm 5290 with Boris
        self.spindle_target_watts = self.spindle_mains_voltage * 0.1 * sqrt(5290)
        self.setup = True

    def add_to_stack(self, value):
        if len(self.spindle_load_stack) == 5:
            self.spindle_load_stack.pop(0)
        self.spindle_load_stack.append(value)

    def adjust(self, data_avg, raw_loads, average_loads):
        if self.m.wpos_z() > 0:
            return

        raw_multiplier = self.get_feed_multiplier(self.spindle_target_watts, data_avg)

        capped_multiplier = self.cap_feed_multiplier(raw_multiplier)

        best_adjustment = get_best_adjustment(capped_multiplier)

        self.do_best_adjustment(best_adjustment)

        self.autopilot_logger.add_log(data_avg, capped_multiplier, datetime.now().strftime('%H:%M:%S:%f'),
                                      raw_loads, average_loads, raw_multiplier, best_adjustment,
                                      self.m.s.feed_override_percentage)

    def remove_outliers(self, data):
        avg = sum(data) / len(data)
        for value in data:
            if value > avg + self.outlier_amount or value < avg - self.outlier_amount:
                data.remove(value)
        return data

    def read(self, dt):
        if len(self.spindle_load_stack) < 5 or not self.setup:
            return

        raw_loads = self.load_qdas_to_watts(self.spindle_load_stack)

        average_loads = self.remove_outliers(raw_loads)

        if len(average_loads) < 3:
            print('Data invalid - not enough values')
            return

        data_avg = sum(average_loads) / len(average_loads)

        self.adjust(data_avg, raw_loads, average_loads)

    def start(self):
        self.load_parameters_from_json()

        self.reading_clock = Clock.schedule_interval(self.read, self.delay_between_feed_adjustments)

        self.m.s.autopilot_instance = self
        self.m.s.autopilot_flag = True

    def stop(self):
        if self.reading_clock is not None:
            Clock.unschedule(self.reading_clock)
            self.m.s.autopilot_flag = False

        Clock.schedule_once(lambda dt: self.autopilot_logger.export_to_gsheet(), 3)

    def load_qda_to_watts(self, qda):
        return self.spindle_mains_voltage * 0.1 * sqrt(qda)

    def load_qdas_to_watts(self, qdas):
        return [self.spindle_mains_voltage * 0.1 * sqrt(qda) for qda in qdas if qda is not None and qda > 0]

    def cap_feed_multiplier(self, multiplier, target_power, current_power):
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

    def get_feed_multiplier(self, target_power, current_power):
        multiplier = float(self.bias_for_feed_decrease) * (float(target_power) - float(current_power)) / float(target_power) \
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
        with open('asmcnc/job/parameters.json') as f:
            data = json.load(f)
            for item in data:
                try:
                    setattr(self, item["Name"], item["Value"])
                except:
                    print("Invalid parameter: " + item["Name"])
