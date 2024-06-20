"""
@author Archie
YetiPilot Functionality
"""

import json
import time
from math import sqrt

from asmcnc.comms.logging_system.logging_system import Logger
from kivy.clock import Clock

from asmcnc.job.yetipilot.config.yetipilot_profile import YetiPilotProfile

def format_time(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds)) + '.{:03d}'.format(int(seconds * 1000) % 1000)


def get_adjustment_list(feed_adjustment_percentage):
    feed_adjustment_percentage = int(round(feed_adjustment_percentage))
    tens = [10 if feed_adjustment_percentage > 0 else -10 for _ in range(abs(feed_adjustment_percentage) // 10)]
    ones = [1 if feed_adjustment_percentage > 0 else -1 for _ in range(abs(feed_adjustment_percentage) % 10)]
    return tens + ones


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

    status_per_adjustment_counter = 0
    statuses_per_adjustment = 2
    spindle_load_stack_size = 1
    digital_spindle_load_stack = []
    override_commands_per_adjustment = 2
    override_command_delay = 0.06
    spindle_override_command_delay = 0.1
    tolerance_for_acceleration_detection = 5

    spindle_free_load_watts = 0
    spindle_tool_load_watts = 0

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
        self.m = kwargs['machine']

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

    def get_multiplier(self, load):
        if load > self.get_total_target_power():
            return self.bias_for_feed_decrease * (self.get_total_target_power() - load) / \
                   self.get_total_target_power() * self.m_coefficient * self.c_coefficient

        return self.bias_for_feed_increase * (self.get_total_target_power() - load) / \
               self.get_total_target_power() * self.m_coefficient * self.c_coefficient

    def get_feed_adjustment_percentage(self, average_spindle_load, constant_feed, gcode_mode, is_z_moving,
                                       feed_multiplier=None):
        """
        Calculates the correct feed adjustment percentage
        :param average_spindle_load: the average spindle load
        :param constant_feed: whether the feed rate is constant
        :param gcode_mode: which gcode mode is being used
        :param is_z_moving: whether the z axis is moving
        :param feed_multiplier: overrides the calculated feed multiplier (used for unit tests only)
        :return:
        """

        feed_multiplier = self.get_multiplier(load=average_spindle_load) if not feed_multiplier else feed_multiplier
        allowed_to_feed_up = constant_feed and gcode_mode != 0 and not is_z_moving

        # If not allowed to feed up
        if not allowed_to_feed_up and feed_multiplier > 0:
            return 0

        # If outside the limits of adjustment
        if not (self.cap_for_feed_decrease < feed_multiplier < self.cap_for_feed_increase):
            return self.cap_for_feed_decrease if feed_multiplier < 0 else self.cap_for_feed_increase

        # Only positive numbers within limits of adjustment should get this far
        return feed_multiplier

    def get_speed_adjustment_percentage(self):
        last_gcode_rpm = self.jd.grbl_mode_tracker[0][2]
        target_rpm = self.target_spindle_speed
        spindle_minimum_rpm = self.m.minimum_spindle_speed()

        if abs(last_gcode_rpm - target_rpm) > 100:
            target_speed_multiplier = ((target_rpm-spindle_minimum_rpm)/(last_gcode_rpm-spindle_minimum_rpm)) * 0.9 + 0.1
            adjustment_percentage = (target_speed_multiplier - 1) * 100
            return adjustment_percentage
        return 0

    def start_feed_too_low_check(self):
        self.waiting_for_feed_too_low_decision = True
        Clock.schedule_once(lambda dt: self.check_if_feed_too_low(), 4)

    def set_adjusting_spindle_speed(self, adjusting):
        self.adjusting_spindle_speed = adjusting

    def do_override_adjustment(self, adjustment_percentage, command_dictionary, feed):
        """
        Schedules the override adjustments
        :param adjustment_percentage: the percentage to adjust by
        :param command_dictionary: the respective command dictionary
        :param feed: whether the adjustment is for feed (False for speed)
        :return: the list of adjustments made
        """

        # Skip if 0
        if adjustment_percentage == 0:
            return []

        adjustment_list = get_adjustment_list(adjustment_percentage)

        # If doing feed adjustments, limit the list
        if feed:
            adjustment_list = adjustment_list[:self.override_commands_per_adjustment]

        if not feed:
            self.set_adjusting_spindle_speed(True)
            # Clock.schedule_once(lambda dt: self.set_adjusting_spindle_speed(False),
            #                     self.override_command_delay * len(adjustment_list) + 0.2)

        for i, adjustment in enumerate(adjustment_list):
            command_delay = (self.override_command_delay if feed else self.spindle_override_command_delay) * i

            if feed:
                if self.m.s.feed_override_percentage == 200 and adjustment > 0:
                    return adjustment_list[:i]

                percentage_after_adjustments = adjustment + self.m.s.feed_override_percentage

                # If doing feed adjustments and the feed drops below 10% (theoretical), then start the low feed check
                if percentage_after_adjustments < 30:
                    if not self.waiting_for_feed_too_low_decision:
                        self.start_feed_too_low_check()

                # If the adjustment will exceed the limit of 200%, reduce to 1 to build up to max
                elif percentage_after_adjustments > 200:
                    adjustment = 1

            # Schedule the feed override command
            Clock.schedule_once(command_dictionary[adjustment], command_delay)

        return adjustment_list

    def get_command_dictionary(self, feed):
        """
        Get command dictionary for feed or speed adjustments
        :param feed: whether the adjustment is for feed (False for speed)
        :return: the command dictionary
        """

        if feed:
            return {
                10: lambda dt: self.feed_override_wrapper(self.m.feed_override_up_10),
                1: lambda dt: self.feed_override_wrapper(self.m.feed_override_up_1),
                -1: lambda dt: self.feed_override_wrapper(self.m.feed_override_down_1),
                -10: lambda dt: self.feed_override_wrapper(self.m.feed_override_down_10)
            }

        return {
            10: lambda dt: self.feed_override_wrapper(self.m.speed_override_up_10),
            1: lambda dt: self.feed_override_wrapper(self.m.speed_override_up_1),
            -1: lambda dt: self.feed_override_wrapper(self.m.speed_override_down_1),
            -10: lambda dt: self.feed_override_wrapper(self.m.speed_override_down_10)
        }

    def add_status_to_yetipilot(self, digital_spindle_ld_qdA, digital_spindle_mains_voltage,
                                feed_override_percentage, feed_rate):
        """
        Adds a status to the yetipilot algorithm
        :param digital_spindle_ld_qdA: the digital spindle load in qdA
        :param digital_spindle_mains_voltage: the digital spindle mains voltage
        :param feed_override_percentage: the current feed override percentage
        :param feed_rate: the current feed rate
        """

        self.digital_spindle_mains_voltage = digital_spindle_mains_voltage
        digital_spindle_ld_w = self.ldA_to_watts(digital_spindle_ld_qdA)

        # Keep stack to its max size
        if len(self.digital_spindle_load_stack) == self.spindle_load_stack_size:
            self.digital_spindle_load_stack.pop(0)
        self.digital_spindle_load_stack.append(digital_spindle_ld_w)

        self.status_per_adjustment_counter += 1
        if self.status_per_adjustment_counter >= self.statuses_per_adjustment:
            self.status_per_adjustment_counter = 0

            # Gather required stats

            average_spindle_load = sum(self.digital_spindle_load_stack) / len(self.digital_spindle_load_stack)

            constant_feed, gcode_feed = self.m.get_is_constant_feed_rate(self.jd.grbl_mode_tracker[0][1],
                                                                         feed_override_percentage, feed_rate,
                                                                         self.tolerance_for_acceleration_detection)

            gcode_mode = self.m.get_grbl_motion_mode()

            is_z_moving = self.m.s.z_change

            feed_adjustment_percentage = self.get_feed_adjustment_percentage(average_spindle_load, constant_feed,
                                                                             gcode_mode, is_z_moving)

            # Adjust feeds & speeds

            feed_adjustments = self.do_override_adjustment(feed_adjustment_percentage,
                                                           self.get_command_dictionary(feed=True),
                                                           feed=True)

            if feed_adjustments:
                Logger.info("YetiPilot: Feed Adjustments done: " + str(feed_adjustments))

            if not self.using_advanced_profile and not self.adjusting_spindle_speed:
                speed_adjustment_percentage = self.get_speed_adjustment_percentage()
                speed_adjustments = self.do_override_adjustment(speed_adjustment_percentage,
                                                                self.get_command_dictionary(feed=False),
                                                                feed=False)

                if speed_adjustments:
                    Logger.info("YetiPilot: Speed Adjustments done: " + str(speed_adjustments))

    def stop_and_show_error(self):
        self.disable()
        self.m.stop_for_a_stream_pause('yetipilot_low_feed')

    def check_if_feed_too_low(self):
        if not(self.use_yp and self.m.s.is_job_streaming and
               not self.m.is_machine_paused and "Alarm" not in self.m.state()):
            self.waiting_for_feed_too_low_decision = False
            return

        if self.m.s.feed_override_percentage == 30:
            self.stop_and_show_error()
        self.waiting_for_feed_too_low_decision = False

    def feed_override_wrapper(self, feed_override_func):
        if self.use_yp and self.m.s.is_job_streaming and \
                not self.m.is_machine_paused and "Alarm" not in self.m.state():
            feed_override_func()

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
                    cutter_diameter=profile_json["Cutter Diameter"].encode('utf-8'),
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
        self.using_advanced_profile = False

        if self.sm.has_screen('go') and self.use_yp:
            self.sm.get_screen('go').speedOverride.set_widget_visibility(False)
            self.sm.get_screen('go').feedOverride.set_widget_visibility(False)

        for profile in self.available_profiles:
            if str(profile.cutter_diameter) == cutter_diameter and \
                    str(profile.cutter_type) == cutter_type and \
                    str(profile.material_type) == material_type:
                return profile

    def use_profile(self, profile):
        if self.active_profile != profile:
            self.m.speed_override_reset()
            self.set_adjusting_spindle_speed(False)

        self.active_profile = profile
        self.using_advanced_profile = False
        self.using_basic_profile = True

        if not self.active_profile:
            return

        for parameter in profile.parameters:
            setattr(self, parameter["Name"], parameter["Value"])


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

    # GETTERS AND SETTERS FOR TARGET POWERS

    def get_total_target_power(self):
        return self.get_free_load() + self.get_tool_load()

    def get_free_load(self):
        return self.spindle_free_load_watts

    def get_tool_load(self):
        return self.spindle_tool_load_watts

    def set_free_load(self, free_load):
        self.spindle_free_load_watts = free_load

    def set_tool_load(self, tool_load):
        self.spindle_tool_load_watts = tool_load
