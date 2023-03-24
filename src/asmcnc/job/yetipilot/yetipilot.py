"""
@author Archie
YetiPilot Functionality
"""

import json
import time
from math import sqrt

from kivy.clock import Clock

from asmcnc.job.yetipilot.config.yetipilot_profile import YetiPilotProfile
from asmcnc.job.yetipilot.logging.yetipilot_logger import AutoPilotLogger


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

    def __init__(self, **kwargs):
        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']
        self.jd = kwargs['job_data']

        if kwargs.get('test', False):
            self.profiles_path = 'src/' + self.profiles_path
            self.parameters_path = 'src/' + self.parameters_path

        self.get_available_profiles()
        self.load_parameters()

        self.logger = AutoPilotLogger(
            self.digital_spindle_mains_voltage, self.spindle_free_load_watts + self.spindle_tool_load_watts,
            self.bias_for_feed_increase, self.bias_for_feed_decrease,
            self.m_coefficient, self.c_coefficient, self.cap_for_feed_increase, self.cap_for_feed_decrease, "job_name",
            self.m.device_label, self.spindle_load_stack_size, 0,
            self.cap_for_feed_increase_during_z_movement,
            self, None
        )

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
            self.sm.get_screen('go').feedOverride.set_widget_visibility(True)
            self.sm.get_screen('go').speedOverride.set_widget_visibility(True)

        if self.m.s.feed_override_percentage > 100:
            self.m.feed_override_reset()

        self.m.speed_override_reset()

    # Utils
    def ldA_to_watts(self, load):
        return self.digital_spindle_mains_voltage * 0.1 * sqrt(load)

    def get_target_spindle_load(self):
        return self.spindle_free_load_watts + self.spindle_tool_load_watts

    def get_multiplier(self, load):
        if load > self.get_target_spindle_load():
            return self.bias_for_feed_decrease * (self.get_target_spindle_load() - load) / \
                   self.get_target_spindle_load() * self.m_coefficient * self.c_coefficient

        return self.bias_for_feed_increase * (self.get_target_spindle_load() - load) / \
               self.get_target_spindle_load() * self.m_coefficient * self.c_coefficient

    def get_feed_adjustment_percentage(self, average_spindle_load, constant_feed, gcode_mode, is_z_moving):
        feed_multiplier = self.get_multiplier(load=average_spindle_load)
        allowed_to_feed_up = constant_feed and gcode_mode != 0 and not is_z_moving

        # If not allowed to feed up
        if not allowed_to_feed_up:
            return 0 if feed_multiplier > 0 else feed_multiplier

        # If outside the limits of adjustment
        if not (self.cap_for_feed_decrease < feed_multiplier < self.cap_for_feed_increase):
            return self.cap_for_feed_decrease if feed_multiplier < 0 else self.cap_for_feed_increase

        # Only positive numbers within limits of adjustment should get this far
        return feed_multiplier

    def get_speed_adjustment_percentage(self):
        last_gcode_rpm = self.jd.grbl_mode_tracker[0][2]
        live_rpm = int(self.m.s.spindle_speed)

        if abs(live_rpm - last_gcode_rpm) >= 500:
            return ((self.target_spindle_speed / last_gcode_rpm) * 100) - self.m.s.speed_override_percentage
        return 0

    def is_feed_too_low_callback(self):
        # this needs to go after the resume from stop_and_show_error
        # self.waiting_for_feed_too_low_decision = False

        self.stop_and_show_error()

    def start_feed_too_low_check(self):
        self.waiting_for_feed_too_low_decision = True
        Clock.schedule_once(lambda dt: self.is_feed_too_low_callback(), 4)

    def do_override_adjustment(self, adjustment_percentage, command_dictionary, feed):
        # Skip if 0
        if adjustment_percentage == 0:
            return []

        adjustment_list = get_adjustment_list(adjustment_percentage)

        # If doing feed adjustments, limit the list
        if feed:
            adjustment_list = adjustment_list[:self.override_commands_per_adjustment]

        for i, adjustment in enumerate(adjustment_list):
            command_delay = self.override_command_delay * i

            if feed:
                if self.m.s.feed_override_percentage == 200:
                    return adjustment_list[:i]

                percentage_after_adjustments = adjustment + self.m.s.feed_override_percentage

                # If doing feed adjustments and the feed drops below 10% (theoretical), then start the low feed check
                if percentage_after_adjustments < 10:
                    if not self.waiting_for_feed_too_low_decision:
                        self.start_feed_too_low_check()

                # If the adjustment will exceed the limit of 200%, reduce to 1 to build up to max
                elif percentage_after_adjustments > 200:
                    adjustment = 1

            # Schedule the feed override command
            Clock.schedule_once(command_dictionary[adjustment], command_delay)

        return adjustment_list

    def get_command_dictionary(self, feed):
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

            average_spindle_load = sum(self.digital_spindle_load_stack) / self.spindle_load_stack_size

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
                print("YetiPilot: Feed Adjustments done: " + str(feed_adjustments))

            if not self.using_advanced_profile:
                speed_adjustment_percentage = self.get_speed_adjustment_percentage()
                speed_adjustments = self.do_override_adjustment(speed_adjustment_percentage,
                                                                self.get_command_dictionary(feed=False),
                                                                feed=False)

                if speed_adjustments:
                    print("YetiPilot: Speed Adjustments done: " + str(speed_adjustments))

                # Log data
                time_stamp = None

                if self.jd.job_start_time is not None:
                    now_time = time.time()
                    time_stamp = format_time(now_time - self.jd.job_start_time)

                allow_feedup = gcode_mode != 0 and not is_z_moving and constant_feed

                current_gcode = self.jd.job_gcode_running[self.m.s.grbl_ln] if len(
                    self.jd.job_gcode_running) - 1 >= self.m.s.grbl_ln else ''

                self.logger.add_log(
                    current_load=average_spindle_load,
                    feed_multiplier=feed_adjustment_percentage,
                    time=time_stamp,
                    raw_loads=self.digital_spindle_load_stack,
                    average_loads=self.digital_spindle_load_stack,
                    raw_multiplier=feed_adjustment_percentage,
                    adjustment_list=feed_adjustments,
                    feed_override_percentage=feed_override_percentage,
                    moving_in_z=is_z_moving,
                    sg_x_motor_axis=0,
                    sg_y_axis=0,
                    sg_z_motor_axis=0,
                    sg_x1_motor=0,
                    sg_x2_motor=0,
                    sg_y1_motor=0,
                    sg_y2_motor=0,
                    target_load=self.get_target_spindle_load(),
                    raw_spindle_load=digital_spindle_ld_qdA,
                    spindle_voltage=digital_spindle_mains_voltage,
                    feed_rate=feed_rate,
                    constant_speed=constant_feed,
                    line_number=self.m.s.grbl_ln,
                    gcode_feed=self.jd.grbl_mode_tracker[0][1],
                    target_feed=self.jd.grbl_mode_tracker[0][1] * feed_override_percentage / 100,
                    g0_move=gcode_mode == 0,
                    allow_feedup=allow_feedup,
                    target_spindle_speed=self.target_spindle_speed,
                    spindle_override_percentage=self.m.s.speed_override_percentage,
                    spindle_rpm=0,
                    gcode=current_gcode
                )

    def stop_and_show_error(self):
        self.disable()
        self.m.stop_for_a_stream_pause('yetipilot_low_feed')

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
    def get_available_profiles(self):
        with open(self.profiles_path) as f:
            profiles_json = json.load(f)

        for profile_json in profiles_json["Profiles"]:
            self.available_profiles.append(
                YetiPilotProfile(
                    cutter_diameter=profile_json["Cutter Diameter"],
                    cutter_type=profile_json["Cutter Type"],
                    material_type=profile_json["Material Type"],
                    step_down=profile_json["Step Down"],
                    parameters=profile_json["Parameters"]
                )
            )

        # Get available options for dropdowns
        self.available_cutter_diameters = sorted({str(profile.cutter_diameter) for profile in self.available_profiles})
        self.available_material_types = sorted({str(profile.material_type) for profile in self.available_profiles})
        self.available_cutter_types = sorted({str(profile.cutter_type) for profile in self.available_profiles})

    def get_profile(self, cutter_diameter, cutter_type, material_type):
        self.using_basic_profile = True

        if self.sm.has_screen('go'):
            self.sm.get_screen('go').speedOverride.set_widget_visibility(False)

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

        if using_advanced_profile:
            if self.sm.has_screen('go'):
                self.sm.get_screen('go').speedOverride.set_widget_visibility(True)

            self.using_basic_profile = False

    def set_target_power(self, target_power):
        self.spindle_tool_load_watts = target_power
        self.set_using_advanced_profile(True)

    def get_target_power(self):
        return self.spindle_tool_load_watts

    def set_spindle_free_load(self, spindle_free_load):
        self.spindle_free_load_watts = spindle_free_load
