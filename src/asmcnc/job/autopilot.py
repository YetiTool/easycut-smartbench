"""
Created on 9 Dec 2022
@author: Archie
"""

from kivy.clock import Clock
from math import sqrt, floor
from autopilot_logger import AutoPilotLogger
from datetime import datetime


def get_best_adjustment(percentage):
    percentage = round(percentage)

    negative = percentage < 0

    percentage = abs(percentage)
    tens = percentage // 10
    ones = percentage % 10

    if ones < 5:
        moves = []
        for i in range(int(floor(tens))):
            moves.append(-10 if negative else 10)
        for i in range(int(floor(ones))):
            moves.append(-1 if negative else 1)
        return moves
    else:
        moves = []
        for i in range(int(floor(tens + 1))):
            moves.append(-10 if negative else 10)
        for i in range(int(floor(10 - ones))):
            moves.append(1 if negative else -1)
        return moves


class Autopilot:
    reading_clock = None

    adjustment_delay = 0.5

    spindle_v_main = None
    spindle_target_watts = 875
    spindle_target_percentage = 0.5

    old_spindle_load_stack = []
    spindle_load_stack = []

    outlier_percentage = 20
    outlier_amount = 100

    bias = 2.0
    m_coefficient = 1.0
    c_coefficient = 30 / 0.875
    increase_cap = 5
    decrease_cap = 5

    autopilot_logger = None

    setup = False

    def __init__(self, **kwargs):
        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']

    def first_read_setup(self):
        self.autopilot_logger = AutoPilotLogger(self.spindle_v_main, self.spindle_target_watts,
                                                self.bias, self.m_coefficient, self.c_coefficient,
                                                self.increase_cap, self.decrease_cap)
        # confirm 5290 with Boris
        self.spindle_target_watts = self.spindle_v_main * 0.1 * sqrt(5290)
        self.setup = True

    def add_to_stack(self, value):
        if len(self.spindle_load_stack) == 5:
            self.spindle_load_stack.pop(0)
        self.spindle_load_stack.append(value)

    def adjust(self, data_avg):
        if self.m.wpos_z() > 0:
            return

        adjustment_required = self.get_feed_multiplier(self.spindle_target_watts, data_avg)

        print(adjustment_required)

        best_adjustment = get_best_adjustment(adjustment_required)

        print(best_adjustment)

        self.do_best_adjustment(best_adjustment)
        self.autopilot_logger.add_log(data_avg, adjustment_required, datetime.now().strftime('%H:%M:%S'))

    def remove_outliers(self, data):
        avg = sum(data) / len(data)
        for value in data:
            if value > avg + self.outlier_amount or value < avg - self.outlier_amount:
                data.remove(value)
        return data

    def read(self, dt):
        if len(self.spindle_load_stack) < 5 or not self.setup:
            return

        data = self.load_qdas_to_watts(self.spindle_load_stack)

        data = self.remove_outliers(data)

        if len(data) < 3:
            print('Data invalid - not enough values')
            return

        data_avg = sum(data) / len(data)

        self.adjust(data_avg)

    def start(self):
        self.reading_clock = Clock.schedule_interval(self.read, self.adjustment_delay)

        self.m.s.autopilot_instance = self
        self.m.s.autopilot_flag = True

    def stop(self):
        if self.reading_clock is not None:
            Clock.unschedule(self.reading_clock)
            self.m.s.autopilot_flag = False
        self.autopilot_logger.export_to_gsheet()

    def load_qda_to_watts(self, qda):
        return self.spindle_v_main * 0.1 * sqrt(qda)

    def load_qdas_to_watts(self, qdas):
        return [self.spindle_v_main * 0.1 * sqrt(qda) for qda in qdas if qda is not None and qda > 0]

    def get_feed_multiplier(self, target_power, current_power):
        multiplier = self.bias * (float(target_power) - float(current_power)) / float(target_power) \
                     * self.m_coefficient * self.c_coefficient

        if current_power > target_power and abs(multiplier) > self.decrease_cap:
            return -self.decrease_cap
        elif current_power < target_power and multiplier > self.increase_cap:
            return self.increase_cap

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
                Clock.schedule_once(lambda dt: self.m.feed_override_up_10(feed_override_widget.feed_override_percentage), 0.05 * i)
            elif adjustment_list[i] == 1:
                feed_override_widget.feed_override_percentage += 1
                Clock.schedule_once(lambda dt: self.m.feed_override_up_1(feed_override_widget.feed_override_percentage), 0.05 * i)
            elif adjustment_list[i] == -10:
                feed_override_widget.feed_override_percentage -= 10
                Clock.schedule_once(lambda dt: self.m.feed_override_down_10(feed_override_widget.feed_override_percentage), 0.05 * i)
            elif adjustment_list[i] == -1:
                feed_override_widget.feed_override_percentage -= 1
                Clock.schedule_once(lambda dt: self.m.feed_override_down_1(feed_override_widget.feed_override_percentage), 0.05 * i)

