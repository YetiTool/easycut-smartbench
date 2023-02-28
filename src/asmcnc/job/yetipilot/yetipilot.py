import json
from kivy.clock import Clock
from math import sqrt, floor
import time
from asmcnc.job.yetipilot.logging.yetipilot_logger import AutoPilotLogger
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


DEV_MODE = False


class YetiPilot(object):
    enabled = False
    logger = None

    digital_spindle_mains_voltage = None

    bias_for_feed_decrease = 2.0
    bias_for_feed_increase = 1.0
    m_coefficient = 1.0
    c_coefficient = 35.0
    cap_for_feed_increase = 20
    cap_for_feed_decrease = -40
    cap_for_feed_increase_during_z_movement = 0

    moving_in_z = False
    counter = 0
    statuses_per_adjustment = 2
    spindle_load_stack_size = 2
    digital_spindle_load_stack = []
    override_commands_per_adjustment = 2
    override_command_delay = 0.06
    tolerance_for_acceleration_detection = 50

    spindle_target_load_watts = 880
    target_spindle_speed = 25000

    available_profiles = []
    available_cutter_diameters = []
    available_cutter_types = []
    available_material_types = []

    active_profile = None

    use_yp = False

    def __init__(self, **kwargs):
        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']
        self.jd = kwargs['job_data']
        self.get_available_profiles()
        self.use_profile(self.available_profiles[0])

    # System
    def enable(self):
        self.use_yp = True

        if DEV_MODE:
            self.use_logger()

    def disable(self):
        self.use_yp = False

    def use_logger(self):
        job_name = '' if not self.sm.has_screen('go') else self.sm.get_screen('go').file_data_label.text
        self.logger = AutoPilotLogger(
            self.digital_spindle_mains_voltage, self.spindle_target_load_watts, self.bias_for_feed_increase,
            self.bias_for_feed_decrease,
            self.m_coefficient, self.c_coefficient, self.cap_for_feed_increase, self.cap_for_feed_decrease, job_name,
            self.m.get_smartbench_name(), self.spindle_load_stack_size, 0,
            self.cap_for_feed_increase_during_z_movement,
            self, None
        )

    def reset(self):
        if self.logger:
            self.logger.reset()

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
        if self.moving_in_z and multiplier > 0:
            return self.cap_for_feed_increase_during_z_movement

        if multiplier < self.cap_for_feed_decrease:
            return self.cap_for_feed_decrease

        if multiplier > self.cap_for_feed_increase:
            return self.cap_for_feed_increase

        return multiplier

    # placeholder - confirm that YP is running
    def add_to_stack(self, digital_spindle_ld_qdA, feed_override_percentage, feed_rate, current_line_number):
        if not self.use_yp or self.digital_spindle_mains_voltage is None or self.active_profile is None:
            return

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
                feed_override_percentage, feed_rate, current_line_number)

            adjustment, raw_multiplier, capped_multiplier = self.calculate_adjustment(average_digital_spindle_load,
                                                                                      constant_feed)

            g0_move = current_line_number in self.jd.g0_lines
            allow_feedup = not g0_move and constant_feed

            if allow_feedup or raw_multiplier < 0:
                self.do_adjustment(adjustment)

            if len(self.jd.spindle_speeds) > 0:
                if 0 < current_line_number - self.jd.spindle_speeds[0][0] < 3:
                    self.adjust_spindle_speed(self.jd.spindle_speeds[0][1])
                    self.jd.spindle_speeds.pop(0)

            # END OF LOGIC
            if not self.logger:
                return

            time_stamp = None

            if self.m.s.job_start_time is not None:
                now_time = time.time()
                time_stamp = format_time(now_time - self.m.s.job_start_time)

            self.logger.add_log(
                current_load=average_digital_spindle_load,
                feed_multiplier=capped_multiplier,
                time=time_stamp,
                raw_loads=self.digital_spindle_load_stack[-self.spindle_load_stack_size:],
                average_loads=self.digital_spindle_load_stack[-self.spindle_load_stack_size:],
                raw_multiplier=raw_multiplier,
                adjustment_list=adjustment[:self.override_commands_per_adjustment],
                feed_override_percentage=feed_override_percentage,
                moving_in_z=str(self.moving_in_z),
                sg_x_motor_axis=self.m.s.sg_x_motor_axis,
                sg_y_axis=self.m.s.sg_y_axis,
                sg_z_motor_axis=self.m.s.sg_z_motor_axis,
                sg_x1_motor=self.m.s.sg_x1_motor,
                sg_x2_motor=self.m.s.sg_x2_motor,
                sg_y1_motor=self.m.s.sg_y1_motor,
                sg_y2_motor=self.m.s.sg_y2_motor,
                target_load=self.spindle_target_load_watts,
                raw_spindle_load=self.m.s.digital_spindle_ld_qdA,
                spindle_voltage=self.m.s.digital_spindle_mains_voltage,
                feed_rate=feed_rate,
                constant_speed=constant_feed,
                line_number=current_line_number,
                gcode_feed=gcode_feed,
                target_feed=gcode_feed * feed_override_percentage / 100,
                g0_move=g0_move,
                allow_feedup=allow_feedup,
                target_spindle_speed=self.target_spindle_speed,
                spindle_override_percentage=self.m.s.speed_override_percentage,
                spindle_rpm=int(self.m.s.spindle_speed),
                gcode=self.jd.job_gcode_running[current_line_number]
            )

    # For simulating feed overrides
    def dummy_override(self):
        pass

    # SPINDLE SPEED ADJUSTMENTS
    def adjust_spindle_speed(self, current_speed):
        total_override_required = (self.target_spindle_speed / current_speed) * 100
        current_override = self.m.s.speed_override_percentage
        difference = total_override_required - current_override

        adjustments = get_adjustment(difference)

        self.do_spindle_adjustment(adjustments)

    def do_spindle_adjustment(self, adjustments):
        for i, adjustment in enumerate(adjustments):
            if not self.use_yp or not self.m.s.is_job_streaming or \
                    self.m.is_machine_paused or "Alarm" in self.m.state():
                continue

            if adjustment == 10:
                Clock.schedule_once(lambda dt: self.m.speed_override_up_10(), i * self.override_command_delay)
            elif adjustment == 1:
                Clock.schedule_once(lambda dt: self.m.speed_override_up_1(), i * self.override_command_delay)
            elif adjustment == -10:
                Clock.schedule_once(lambda dt: self.m.speed_override_down_10(), i * self.override_command_delay)
            elif adjustment == -1:
                Clock.schedule_once(lambda dt: self.m.speed_override_down_1(), i * self.override_command_delay)

    def stop_and_show_error(self):
        self.sm.get_screen('go').start_or_pause_button_press()
        self.disable()
        print("ERROR: Feed override percentage is too low.")

    def do_adjustment(self, adjustments):
        for i, adjustment in enumerate(adjustments):
            if i == self.override_commands_per_adjustment:
                break

            if self.m.s.feed_override_percentage + adjustment > 200 and adjustment == 10:
                adjustment = 1

            if self.m.s.feed_override_percentage + adjustment < 10:
                self.stop_and_show_error()
                return

            if not self.use_yp or not self.m.s.is_job_streaming or \
                    self.m.is_machine_paused or "Alarm" in self.m.state():
                continue

            if adjustment == 10:
                Clock.schedule_once(lambda dt: self.m.feed_override_up_10(), i * self.override_command_delay)
            elif adjustment == 1:
                Clock.schedule_once(lambda dt: self.m.feed_override_up_1(), i * self.override_command_delay)
            elif adjustment == -10:
                Clock.schedule_once(lambda dt: self.m.feed_override_down_10(), i * self.override_command_delay)
            elif adjustment == -1:
                Clock.schedule_once(lambda dt: self.m.feed_override_down_1(), i * self.override_command_delay)

    # USE THESE FUNCTIONS FOR ADVANCED PROFILE
    def set_target_power(self, target_power):
        self.spindle_target_load_watts = target_power

    def set_target_spindle_speed(self, target_spindle_speed):
        self.target_spindle_speed = target_spindle_speed

    # USE THESE FUNCTIONS FOR BASIC PROFILES
    def get_available_profiles(self):
        with open('asmcnc/job/yetipilot/config/profiles.json') as f:
            profiles_json = json.load(f)

        for profile_json in profiles_json:
            self.available_profiles.append(
                YetiPilotProfile(
                    cutter_diameter=profile_json["Cutter Diameter"],
                    cutter_type=profile_json["Cutter Type"],
                    material_type=profile_json["Material Type"],
                    parameters=profile_json["Parameters"]
                )
            )

        # Get available options for dropdowns
        self.available_cutter_diameters = {str(profile.cutter_diameter) for profile in self.available_profiles}
        self.available_material_types = {str(profile.material_type) for profile in self.available_profiles}
        self.available_cutter_types = {str(profile.cutter_type) for profile in self.available_profiles}

    def get_profile(self, cutter_diameter, cutter_type, material_type):
        for profile in self.available_profiles:
            if profile.cutter_diameter == cutter_diameter and \
                    profile.cutter_type == cutter_type and \
                    profile.material_type == material_type:
                return profile

    def use_profile(self, profile):
        self.active_profile = profile
        for parameter in profile.parameters:
            setattr(self, parameter["Name"], parameter["Value"])

    # USE THESE FUNCTIONS FOR BASIC PROFILE DROPDOWNS
    def get_available_cutter_diameters(self):
        return self.available_cutter_diameters

    def get_available_cutter_types(self):
        return self.available_cutter_types

    def get_available_material_types(self):
        return self.available_material_types
