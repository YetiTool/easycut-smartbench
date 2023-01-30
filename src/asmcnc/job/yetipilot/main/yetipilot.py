from math import ceil, floor
from kivy.clock import Clock


def get_adjustment(feed_multiplier):
    feed_multiplier = ceil(feed_multiplier) if feed_multiplier < 0 else floor(feed_multiplier)
    negative = feed_multiplier < 0
    feed_multiplier = abs(feed_multiplier) if negative else feed_multiplier

    tens = int(feed_multiplier // 10)
    ones = int(feed_multiplier % 10)
    moves = [[], []]

    if ones > 5:
        tens += 1
        for _ in range(10 - ones):
            moves[1].append(-1)
        ones = 0

    for _ in range(tens):
        moves.append(10)

    for _ in range(ones):
        moves.append(1)

    moves[0].extend(moves[1])
    moves[0] = [-move if negative else move for move in moves[0]]

    return moves[0]


def limit_adjustments(adjustments):
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

    feed_adjustment_delay_ms = 60

    def __init__(self, **kwargs):
        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']

    def start(self):
        self.enabled = True

    def stop(self):
        self.enabled = False

    def toggle(self):
        if self.enabled:
            self.stop()
            return

        self.start()

    def set_spindle_voltage(self, voltage):
        self.spindle_mains_voltage = voltage

    def set_target_power(self, power):
        self.spindle_target_watts = power

    def add_to_stack(self, load):
        if not self.enabled:
            print('Not enabled')
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

        if adjustment is None:
            return

        print('Adjusting: ' + str(adjustment))

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


