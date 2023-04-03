"""
@author Archie
YetiPilot Functionality
"""

import json
import time
from math import sqrt, floor

from kivy.clock import Clock

from asmcnc.job.yetipilot.config.yetipilot_profile import YetiPilotProfile


def format_time(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds)) + '.{:03d}'.format(int(seconds * 1000) % 1000)


def get_adjustment(feed_multiplier):
    feed_multiplier = floor(feed_multiplier)
    negative = feed_multiplier < 0
    feed_multiplier = abs(feed_multiplier) if negative else feed_multiplier

    tens = int(feed_multiplier // 10)
    ones = int(feed_multiplier % 10)

    return [-10 if negative else 10 for _ in range(tens)] + [-1 if negative else 1 for _ in range(ones)]


class YetiPilot(object):
    use_yp = False

    digital_spindle_mains_voltage = None

    bias_for_feed_decrease = 2.0
    bias_for_feed_increase = 1.0
    m_coefficient = 1.0
    c_coefficient = 35.0
    cap_for_feed_increase = 20
    cap_for_feed_decrease = -40
    cap_for_feed_increase_during_z_movement = 0

    counter = 0
    statuses_per_adjustment = 2
    spindle_load_stack_size = 1
    digital_spindle_load_stack = []
    override_commands_per_adjustment = 2
    override_command_delay = 0.06
    tolerance_for_acceleration_detection = 5

    spindle_target_load_watts = 700
    target_spindle_speed = 25000

    available_profiles = []
    available_cutter_diameters = []
    available_cutter_types = []
    available_material_types = []

    active_profile = None

    using_advanced_profile = False
    using_basic_profile = False

    waiting_for_feed_too_low_decision = False

    spindle_230v_correction_factor = 1350

    profiles_path = 'asmcnc/job/yetipilot/config/profiles.json'
    parameters_path = 'asmcnc/job/yetipilot/config/algorithm_parameters.json'

    adjusting_spindle_speed = False

    def __init__(self, **kwargs):
        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']
        self.jd = kwargs['job_data']
        self.l = kwargs['localization']

        if kwargs.get('test', False):
            self.profiles_path = 'src/' + self.profiles_path
            self.parameters_path = 'src/' + self.parameters_path

        self.get_all_profiles()
        self.load_parameters()

    # System
    def enable(self):
        self.use_yp = True

        if self.sm.has_screen('go'):
            self.sm.get_screen('go').feedOverride.set_widget_visibility(False)
            self.sm.get_screen('go').speedOverride.set_widget_visibility(False)

    def disable(self):
        self.use_yp = False

        if self.sm.has_screen('go'):
            self.sm.get_screen('go').yp_widget.switch_reflects_yp()
            if not self.active_profile: self.sm.get_screen('go').yp_widget.profile_selection.text = ""
            self.sm.get_screen('go').feedOverride.set_widget_visibility(True)
            self.sm.get_screen('go').speedOverride.set_widget_visibility(True)

        if self.m.s.feed_override_percentage > 100:
            self.m.feed_override_reset()

        self.m.speed_override_reset()

    # Utils
    def ldA_to_watts(self, load):
        return self.digital_spindle_mains_voltage * 0.1 * sqrt(load)

    def get_multiplier(self, digital_spindle_ld_w):
        multiplier = (float(
            self.bias_for_feed_decrease) if digital_spindle_ld_w > self.spindle_target_load_watts else
                      float(self.bias_for_feed_increase)) * (
                             float(self.spindle_target_load_watts) - float(digital_spindle_ld_w)) \
                     / float(self.spindle_target_load_watts) * float(self.m_coefficient) * float(self.c_coefficient)

        return multiplier

    def calculate_adjustment(self, average_digital_spindle_load, constant_feed):
        multiplier = self.get_multiplier(average_digital_spindle_load)
        capped_multiplier = self.cap_multiplier(multiplier)

        adjustments = get_adjustment(capped_multiplier)

        if not constant_feed and multiplier > 0:
            return [], multiplier, capped_multiplier

        return adjustments, multiplier, capped_multiplier

    def cap_multiplier(self, multiplier):
        if self.m.s.z_change and multiplier > 0:
            return self.cap_for_feed_increase_during_z_movement

        if multiplier < self.cap_for_feed_decrease:
            return self.cap_for_feed_decrease

        if multiplier > self.cap_for_feed_increase:
            return self.cap_for_feed_increase

        return multiplier

    def add_to_stack(self, digital_spindle_ld_qdA, feed_override_percentage, feed_rate, digital_spindle_mains_voltage):
        if not self.active_profile and not self.using_advanced_profile:
            return

        self.digital_spindle_mains_voltage = digital_spindle_mains_voltage

        digital_spindle_ld_w = self.ldA_to_watts(digital_spindle_ld_qdA)

        if len(self.digital_spindle_load_stack) == self.spindle_load_stack_size:
            self.digital_spindle_load_stack.pop(0)

        self.digital_spindle_load_stack.append(digital_spindle_ld_w)
        self.counter += 1

        if len(self.digital_spindle_load_stack) >= 1 and self.counter >= self.statuses_per_adjustment:
            self.counter = 0

            average_digital_spindle_load = sum(
                self.digital_spindle_load_stack[-self.spindle_load_stack_size:]) / self.spindle_load_stack_size

            constant_feed, gcode_feed = self.m.get_is_constant_feed_rate(
                self.jd.grbl_mode_tracker[0][1], feed_override_percentage, feed_rate,
                self.tolerance_for_acceleration_detection)

            adjustment, raw_multiplier, capped_multiplier = self.calculate_adjustment(average_digital_spindle_load,
                                                                                      constant_feed)

            g0_move = self.m.get_grbl_motion_mode() == 0
            allow_feedup = not g0_move and constant_feed

            if allow_feedup or raw_multiplier < 0:
                self.do_adjustment(adjustment)

            if not self.using_advanced_profile and not self.adjusting_spindle_speed:
                self.adjust_spindle_speed(self.jd.grbl_mode_tracker[0][2])

    # SPINDLE SPEED ADJUSTMENTS
    def adjust_spindle_speed(self, current_rpm):
        total_override_required = (self.target_spindle_speed / current_rpm) * 100
        current_override = self.m.s.speed_override_percentage
        difference = total_override_required - current_override
        adjustments = get_adjustment(difference)
        self.adjusting_spindle_speed = True
        self.do_spindle_adjustment(adjustments)

    def set_adjusting_spindle_speed(self, value):
        self.adjusting_spindle_speed = value

    def do_spindle_adjustment(self, adjustments):
        for i, adjustment in enumerate(adjustments):
            if self.m.s.speed_override_percentage == 200 and adjustment > 0:
                break

            if self.m.s.speed_override_percentage + adjustment > 200:
                adjustment = 1

            if adjustment == 10:
                Clock.schedule_once(lambda dt: self.feed_override_wrapper(self.m.speed_override_up_10),
                                    i * self.override_command_delay)
            elif adjustment == 1:
                Clock.schedule_once(lambda dt: self.feed_override_wrapper(self.m.speed_override_up_1),
                                    i * self.override_command_delay)
            elif adjustment == -10:
                Clock.schedule_once(lambda dt: self.feed_override_wrapper(self.m.speed_override_down_10),
                                    i * self.override_command_delay)
            elif adjustment == -1:
                Clock.schedule_once(lambda dt: self.feed_override_wrapper(self.m.speed_override_down_1),
                                    i * self.override_command_delay)
        Clock.schedule_once(lambda dt: self.set_adjusting_spindle_speed(False), len(adjustments) *
                            self.override_command_delay + 0.2)

    def stop_and_show_error(self):
        self.disable()
        self.m.stop_for_a_stream_pause('yetipilot_low_feed')

    def check_if_feed_too_low(self):
        if not(self.use_yp and self.m.s.is_job_streaming and
               not self.m.is_machine_paused and "Alarm" not in self.m.state()):
            self.waiting_for_feed_too_low_decision = False
            return

        if self.m.s.feed_override_percentage == 10:
            self.stop_and_show_error()
        self.waiting_for_feed_too_low_decision = False

    def feed_override_wrapper(self, feed_override_func):
        if self.use_yp and self.m.s.is_job_streaming and \
                not self.m.is_machine_paused and "Alarm" not in self.m.state():
            feed_override_func()

    def do_adjustment(self, adjustments):
        for i, adjustment in enumerate(adjustments):
            if i == self.override_commands_per_adjustment:
                break

            if self.m.s.feed_override_percentage == 200 and adjustment > 0:
                break

            if self.m.s.feed_override_percentage + adjustment > 200 and adjustment == 10:
                adjustment = 1

            if self.m.s.feed_override_percentage + adjustment < 10:
                if not self.waiting_for_feed_too_low_decision:
                    Clock.schedule_once(lambda dt: self.check_if_feed_too_low(), 4)
                    self.waiting_for_feed_too_low_decision = True

            if adjustment == 10:
                Clock.schedule_once(lambda dt: self.feed_override_wrapper(self.m.feed_override_up_10),
                                    i * self.override_command_delay)
            elif adjustment == 1:
                Clock.schedule_once(lambda dt: self.feed_override_wrapper(self.m.feed_override_up_1),
                                    i * self.override_command_delay)
            elif adjustment == -10:
                Clock.schedule_once(lambda dt: self.feed_override_wrapper(self.m.feed_override_down_10),
                                    i * self.override_command_delay)
            elif adjustment == -1:
                Clock.schedule_once(lambda dt: self.feed_override_wrapper(self.m.feed_override_down_1),
                                    i * self.override_command_delay)

    def load_parameters(self):
        with open(self.parameters_path) as f:
            parameters_json = json.load(f)["Parameters"]

            for parameter in parameters_json:
                setattr(self, parameter["Name"], parameter["Value"])

    # USE THESE FUNCTIONS FOR BASIC PROFILES
    def get_all_profiles(self):
        with open(self.profiles_path) as f:
            profiles_json = json.load(f)

        for profile_json in profiles_json["Profiles"]:
            self.available_profiles.append(
                YetiPilotProfile(
                    cutter_diameter=profile_json["Cutter Diameter"],
                    cutter_type=self.l.get_str(profile_json["Cutter Type"]),
                    material_type=self.l.get_str(profile_json["Material Type"]),
                    step_down=profile_json["Step Down"],
                    parameters=profile_json["Parameters"]
                )
            )

        # Get available options for dropdowns
        self.available_material_types = self.get_sorted_material_types(self.available_profiles)
        self.available_cutter_diameters = self.get_sorted_cutter_diameters(self.available_profiles)
        self.available_cutter_types = self.get_sorted_cutter_types(self.available_profiles)

    def get_sorted_cutter_diameters(self, profiles):
        return sorted({str(profile.cutter_diameter) for profile in profiles})

    def get_sorted_material_types(self, profiles):
        return sorted({self.l.get_str(str(profile.material_type)) for profile in profiles})

    def get_sorted_cutter_types(self, profiles):
        return sorted({self.l.get_str(str(profile.cutter_type)) for profile in profiles})

    def filter_available_profiles(self, material_type=None, cutter_diameter=None, cutter_type=None):
        filters = [cutter_diameter, cutter_type, material_type]

        if not any(filters):
            return self.available_profiles

        filtered_profiles = []

        for profile in self.available_profiles:

            if material_type and str(profile.material_type) != material_type:
                continue

            if cutter_diameter and str(profile.cutter_diameter) != cutter_diameter:
                continue

            if cutter_type and str(profile.cutter_type) != cutter_type:
                continue

            filtered_profiles.append(profile)

        return filtered_profiles


    def get_profile(self, cutter_diameter, cutter_type, material_type):
        self.using_basic_profile = True

        if self.sm.has_screen('go') and self.use_yp:
            self.sm.get_screen('go').speedOverride.set_widget_visibility(False)
            self.sm.get_screen('go').feedOverride.set_widget_visibility(False)

        for profile in self.available_profiles:
            if str(profile.cutter_diameter) == cutter_diameter and \
                    str(profile.cutter_type) == cutter_type and \
                    str(profile.material_type) == material_type:
                return profile

    def get_spindle_speed_correction(self, target_rpm):
        is_230v = self.m.spindle_voltage == 230

        if is_230v:
            return target_rpm - self.spindle_230v_correction_factor

        return (target_rpm - 12916) / 0.514

    def use_profile(self, profile):
        self.active_profile = profile
        self.using_advanced_profile = False
        self.using_basic_profile = True

        if not self.active_profile:
            return

        for parameter in profile.parameters:
            setattr(self, parameter["Name"], parameter["Value"])

        self.target_spindle_speed = self.get_spindle_speed_correction(self.target_spindle_speed)

    # USE THESE FUNCTIONS FOR BASIC PROFILE DROPDOWNS
    def get_available_cutter_diameters(self):
        return self.available_cutter_diameters

    def get_available_cutter_types(self):
        return self.available_cutter_types

    def get_available_material_types(self):
        return self.available_material_types

    def get_active_cutter_type(self):
        if self.active_profile:
            return self.active_profile.cutter_type
        return ""

    def get_active_cutter_diameter(self):
        if self.active_profile:
            return str(self.active_profile.cutter_diameter)
        return ""

    def get_active_material_type(self):
        if self.active_profile:
            return self.active_profile.material_type
        return ""

    def get_active_step_down(self):
        if self.active_profile:
            return self.active_profile.step_down
        return "N/A"

    def set_using_advanced_profile(self, using_advanced_profile):
        self.using_advanced_profile = using_advanced_profile

        if using_advanced_profile and self.use_yp:
            if self.sm.has_screen('go'):
                self.sm.get_screen('go').speedOverride.set_widget_visibility(True)
                self.sm.get_screen('go').feedOverride.set_widget_visibility(False)

            self.using_basic_profile = False

    def set_target_power(self, target_power):
        self.spindle_target_load_watts = target_power
        self.set_using_advanced_profile(True)

    def get_target_power(self):
        return self.spindle_target_load_watts

    spindle_free_load_watts = 0

    def set_free_load(self, free_load):
        self.spindle_free_load_watts = free_load

    def get_spindle_freeload(self):
        return self.spindle_free_load_watts
