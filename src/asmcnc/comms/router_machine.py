'''
Created on 31 Jan 2018
@author: Ed
This module defines the machine's properties (e.g. travel), services (e.g. serial comms) and functions (e.g. move left)
'''
import re
import threading
import traceback

from enum import Enum
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.comms.model_manager import ModelManagerSingleton, ProductCodes
from kivy.app import App

try:
    import pigpio
except:
    pass

from asmcnc.comms import serial_connection
from asmcnc.comms.yeti_grbl_protocol import protocol
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from asmcnc.comms import motors
from asmcnc.comms.grbl_settings_manager import GRBLSettingsManagerSingleton
from asmcnc.skavaUI import popup_info
from asmcnc.comms.coordinate_system import CoordinateSystem

from kivy.clock import Clock
from kivy.properties import NumericProperty, ListProperty
from kivy.event import EventDispatcher
import os, time


class Axis(Enum):
    X = 'X'
    Y = 'Y'
    Z = 'Z'


class RouterMachine(EventDispatcher):
    # SETUP

    s = None # serial object

    # This block of variables reflecting grbl settings (when '$$' is issued, serial reads settings and syncs these params)
    grbl_x_max_travel = 1500.0 # measured from true home
    grbl_y_max_travel = 3000.0 # measured from true home
    grbl_z_max_travel = 300.0 # measured from true home

    # how close do we allow the machine to get to its limit switches when requesting a move (so as not to accidentally trip them)
    # note this an internal UI setting, it is NOT grbl pulloff ($27)
    limit_switch_safety_distance = 1.0

    # put commonly used speed and pos values here (or any values that need to be easy to find :))
    Z_MAX_FEED_RATE = 750

    is_machine_completed_the_initial_squaring_decision = False
    is_machine_homed = False # status on powerup
    is_squaring_XY_needed_after_homing = True # starts True, therefore squares on powerup. Switched to false after initial home, so as not to repeat on next home.

    is_machine_paused = False
    reason_for_machine_pause = None

    # empty dictionary to hold TMC motors
    TMC_motor = {}

    # SG threshold
    default_stall_guard_threshold = 250 # 250

    starting_serial_connection = False    # Stops user from starting serial connections while starting already (for zhead cycle app)

    # PERSISTENT MACHINE VALUES

    ## PERSISTENT VALUES SETUP
    smartbench_values_dir = './sb_values/'

    ### Individual files to hold persistent values
    set_up_options_file_path = smartbench_values_dir + 'set_up_options.txt'
    z_touch_plate_thickness_file_path = smartbench_values_dir + 'z_touch_plate_thickness.txt'
    calibration_settings_file_path = smartbench_values_dir + 'calibration_settings.txt'
    z_head_maintenance_settings_file_path = smartbench_values_dir + 'z_head_maintenance_settings.txt'
    z_head_laser_offset_file_path = smartbench_values_dir + 'z_head_laser_offset.txt'
    spindle_brush_values_file_path = smartbench_values_dir + 'spindle_brush_values.txt'
    spindle_cooldown_settings_file_path = smartbench_values_dir + 'spindle_cooldown_settings.txt'
    spindle_cooldown_rpm_override_file_path = smartbench_values_dir + 'spindle_cooldown_rpm_override.txt'
    stylus_settings_file_path = smartbench_values_dir + 'stylus_settings.txt'
    spindle_health_check_file_path = smartbench_values_dir + 'spindle_health_check.txt'
    device_label_file_path = '../../smartbench_name.txt' # this puts it above EC folder in filesystem
    device_location_file_path = '../../smartbench_location.txt' # this puts it above EC folder in filesystem

    ## LOCALIZATION
    persistent_language_path = smartbench_values_dir + 'user_language.txt'

    ## PROBE SETTINGS
    z_lift_after_probing = 20.0
    z_probe_speed = 60
    z_touch_plate_thickness = 1.53
    z_probe_speed_fast = 400
    fast_probing = False

    ## CALIBRATION SETTINGS
    time_since_calibration_seconds = 0
    time_to_remind_user_to_calibrate_seconds = float(320*3600)

    ## Z HEAD MAINTENANCE SETTINGS
    time_since_z_head_lubricated_seconds = 0
    time_to_remind_user_to_lube_z_seconds = float(50*3600)

    ## LASER VALUES
    laser_offset_x_value = 0
    laser_offset_y_value = 0

    is_laser_on = False
    is_laser_enabled = False

    laser_offset_tool_clearance_to_access_edge_of_sheet = 5

    ## STYLUS SETTINGS
    is_stylus_enabled = True
    stylus_router_choice = 'router'

    ## BRUSH VALUES
    spindle_brush_use_seconds = 0
    spindle_brush_lifetime_seconds = float(120*3600)

    ## SPINDLE COOLDOWN OPTIONS
    spindle_brand = 'YETI SC1' # String to hold brand name
    spindle_voltage = 230 # Options are 230V or 110V
    spindle_digital = True #spindle can be manual or digital
    spindle_cooldown_time_seconds = 10 # YETI value is 10 seconds
    spindle_cooldown_rpm = 12000 # YETI default value was 20k, but has been lowered to 12k

    amb_cooldown_rpm_default = 10000
    yeti_cooldown_rpm_default = 12000
    spindle_cooldown_rpm_override = False

    # SPINDLE HEALTH CHECK SETTINGS
    is_spindle_health_check_enabled_as_default = False

    ## DEVICE LABEL
    device_label = "My SmartBench" #TODO needs tying to machine unique ID else all machines will refence this dataseries

    ## DEVICE LOCATION
    device_location = 'SmartBench location'

    reminders_enabled = True

    trigger_setup = False

    def __init__(self, win_serial_port, screen_manager, settings_manager, localization, job, *args, **kwargs):
        super(RouterMachine, self).__init__(*args, **kwargs)

        self.sm = screen_manager
        self.sett = settings_manager
        self.l = localization
        self.jd = job
        self.model_manager = ModelManagerSingleton()
        self.grbl_manager = GRBLSettingsManagerSingleton()
        self.set_jog_limits()
        self.user_settings_manager = App.get_running_app().user_settings_manager

        self.win_serial_port = win_serial_port   # Need to save so that serial connection can be reopened (for zhead cycle app)

        # Establish 's'erial comms and initialise
        self.s = serial_connection.SerialConnection(self, self.sm, self.sett, self.l, self.jd)
        self.s.establish_connection(win_serial_port)

        # Object to construct and send custom YETI GRBL commands
        self.p = protocol.protocol_v2()

        # Object to handle coordinate systems
        self.cs = CoordinateSystem(self)

        # initialise sb_value files if they don't already exist (to record persistent maintenance values)
        self.check_presence_of_sb_values_files()
        self.get_persistent_values()

        # initialise all motors
        self.TMC_motor[TMC_X1] = motors.motor_class(TMC_X1)
        self.TMC_motor[TMC_X2] = motors.motor_class(TMC_X2)
        self.TMC_motor[TMC_Y1] = motors.motor_class(TMC_Y1)
        self.TMC_motor[TMC_Y2] = motors.motor_class(TMC_Y2)
        self.TMC_motor[TMC_Z] = motors.motor_class(TMC_Z)

        if self.model_manager.is_machine_drywall():
            self.device_label = 'My SmartCNC'

    Z_AXIS_ACCESSIBLE_ABS_HEIGHT = -5
    Z_PROBE_SAFE_PULL_OFF = 1

    def raise_z_axis_for_collet_access(self):
        """
        Raise Z to a height that the user can access the spindle collet
        :return: None
        """
        self.s.write_command('G0 G53 Z' + str(self.Z_AXIS_ACCESSIBLE_ABS_HEIGHT))
        # self.jog_absolute_single_axis(Axis.Z.value, target=self.Z_AXIS_ACCESSIBLE_ABS_HEIGHT,
                                    #   speed=self.Z_MAX_FEED_RATE)

    def raise_z_axis_to_safe_height_after_probing(self):
        """
        Raise Z to a height that is slightly above the probe coordinate so the machine clears the stock
        :return: none
        """
        self.jog_relative(Axis.Z.value, self.Z_PROBE_SAFE_PULL_OFF, self.Z_MAX_FEED_RATE)

    # CREATE/DESTROY SERIAL CONNECTION (for cycle app)
    def reconnect_serial_connection(self):
        self.starting_serial_connection = True
        self.close_serial_connection(0)
        Logger.info("Reconnect serial connection")
        self.s.establish_connection(self.win_serial_port)

    def close_serial_connection(self, dt):
        if self.s.is_connected():
            Logger.info("Closing serial connection")
            self.s.s.close()
        self.clear_motor_registers()
        self.s.fw_version = ''
        self.s.hw_version = ''

# PERSISTENT MACHINE VALUES
    def check_presence_of_sb_values_files(self):

        # check folder exists
        if not os.path.exists(self.smartbench_values_dir):
            Logger.info("Creating sb_values dir...")
            os.mkdir(self.smartbench_values_dir)

        if not os.path.exists(self.set_up_options_file_path):
            Logger.info("Creating set up options file...")
            file = open(self.set_up_options_file_path, "w+")
            file.write(str(self.trigger_setup))
            file.close()

        if not os.path.exists(self.z_touch_plate_thickness_file_path):
            Logger.info("Creating z touch plate thickness file...")
            file = open(self.z_touch_plate_thickness_file_path, "w+")
            file.write(str(self.z_touch_plate_thickness))
            file.close()

        if not os.path.exists(self.z_head_laser_offset_file_path):
            Logger.info("Creating z head laser offset file...")
            file = open(self.z_head_laser_offset_file_path, "w+")
            file.write('False' + "\n" + "0" + "\n" + "0")
            file.close()

        if not os.path.exists(self.spindle_brush_values_file_path):
            Logger.info("Creating spindle brush values file...")
            file = open(self.spindle_brush_values_file_path, "w+")
            file.write(str(self.spindle_brush_use_seconds) + "\n" + str(self.spindle_brush_lifetime_seconds))
            file.close()

        if not os.path.exists(self.spindle_cooldown_rpm_override_file_path):
            Logger.info("Creating spindle cooldown_rpm override settings file...")
            file = open(self.spindle_cooldown_rpm_override_file_path, "w+")
            file.write(str(self.spindle_cooldown_rpm_override))
            file.close()

        if not os.path.exists(self.spindle_cooldown_settings_file_path):
            Logger.info("Creating spindle cooldown settings file...")
            file = open(self.spindle_cooldown_settings_file_path, "w+")
            file.write(
                str(self.spindle_brand) + "\n" +
                str(self.spindle_voltage) + "\n" +
                str(self.spindle_digital) + "\n" +
                str(self.spindle_cooldown_time_seconds) + "\n" +
                str(self.spindle_cooldown_rpm)
                )
            file.close()

        if not os.path.exists(self.stylus_settings_file_path):
            Logger.info("Creating stylus settings file...")
            file = open(self.stylus_settings_file_path, "w+")
            file.write(str(self.is_stylus_enabled))
            file.close()

        if not os.path.exists(self.calibration_settings_file_path):
            Logger.info('Creating calibration settings file...')
            file = open(self.calibration_settings_file_path, 'w+')
            file.write(str(self.time_since_calibration_seconds) + "\n" + str(self.time_to_remind_user_to_calibrate_seconds))
            file.close()

        if not os.path.exists(self.z_head_maintenance_settings_file_path):
            Logger.info('Creating z head maintenance settings file...')
            file = open(self.z_head_maintenance_settings_file_path, 'w+')
            file.write(str(self.time_since_z_head_lubricated_seconds))
            file.close()

        if not os.path.exists(self.spindle_health_check_file_path):
            Logger.info("Creating spindle health check settings file...")
            file = open(self.spindle_health_check_file_path, "w+")
            file.write(str(self.is_spindle_health_check_enabled_as_default))
            file.close()

        if not os.path.exists(self.device_label_file_path):
            Logger.info('Creating device label settings file...')
            file = open(self.device_label_file_path, 'w+')
            file.write(str(self.device_label))
            file.close()

        if not os.path.exists(self.device_location_file_path):
            Logger.info('Creating device location settings file...')
            file = open(self.device_location_file_path, 'w+')
            file.write(str(self.device_location))

        if not os.path.exists(self.persistent_language_path):
            Logger.info("Creating language settings file")
            file = open(self.persistent_language_path, 'w+')
            file.write('English (GB)')
            file.close()

    def get_persistent_values(self):
        self.read_set_up_options()
        self.read_z_touch_plate_thickness()
        self.read_calibration_settings()
        self.read_z_head_maintenance_settings()
        self.read_z_head_laser_offset_values()
        self.read_spindle_brush_values()
        self.read_spindle_cooldown_rpm_override_settings()
        self.read_spindle_cooldown_settings()
        self.read_stylus_settings()
        self.read_spindle_health_check_settings()
        self.read_device_label()
        self.read_device_location()


    def look_at(self, f):
        return os.path.isfile(f)

    ## SET UP OPTIONS
    def read_set_up_options(self):
        try:
            file = open(self.set_up_options_file_path, 'r')
            trigger_bool_string  = str(file.read())
            file.close()

            if trigger_bool_string == 'False' or not trigger_bool_string: self.trigger_setup = False
            else: self.trigger_setup = True

            Logger.info("Read in set up options")
            return True

        except:
            Logger.exception("Unable to read in set up options")
            return False

    def write_set_up_options(self, value):

        try:
            file = open(self.set_up_options_file_path, 'w+')
            file.write(str(value))
            file.close()

            self.trigger_setup = value
            Logger.info("set up options written to file")
            return True

        except:
            Logger.exception("Unable to write set up options")
            return False


    ## TOUCH PLATE THICKENESS
    def read_z_touch_plate_thickness(self):

        try:
            file = open(self.z_touch_plate_thickness_file_path, 'r')
            self.z_touch_plate_thickness  = float(file.read())
            file.close()

            Logger.info("Read in z touch plate thickness")
            return True

        except:
            Logger.exception("Unable to read in z touch plate thickness")
            return False

    def write_z_touch_plate_thickness(self, value):

        try:
            file = open(self.z_touch_plate_thickness_file_path, 'w+')
            file.write(str(value))
            file.close()

            self.z_touch_plate_thickness = float(value)
            Logger.info("z touch plate thickness written to file")
            return True

        except:
            Logger.exception("Unable to write z touch plate thickness")
            return False


    ## CALIBRATION SETTINGS

    def read_calibration_settings(self):

        try:
            file = open(self.calibration_settings_file_path, 'r')
            [read_time_since_calibration_seconds, read_time_to_remind_user_to_calibrate_seconds]  = file.read().splitlines()
            file.close()

            self.time_since_calibration_seconds = float(read_time_since_calibration_seconds)
            self.time_to_remind_user_to_calibrate_seconds = float(read_time_to_remind_user_to_calibrate_seconds)

            Logger.info("Read in calibration settings")
            return True

        except:
            Logger.exception("Unable to read calibration settings")
            return False

    def write_calibration_settings(self, since_calibration, remind_time):

        try:
            file = open(self.calibration_settings_file_path, 'w+')
            file.write(str(since_calibration) + "\n" + str(remind_time))
            file.close()

            self.time_since_calibration_seconds = float(since_calibration)
            self.time_to_remind_user_to_calibrate_seconds = float(remind_time)
            Logger.info("calibration settings written to file")
            return True

        except:
            Logger.exception("Unable to write calibration settings")
            return False

    ## Z HEAD MAINTENANCE SETTINGS REMINDER

    def read_z_head_maintenance_settings(self):

        try:
            file = open(self.z_head_maintenance_settings_file_path, 'r')
            self.time_since_z_head_lubricated_seconds  = float(file.read())
            file.close()

            Logger.info("Read in z head maintenance settings")
            return True

        except:
            Logger.exception("Unable to read z head maintenance settings")
            return False

    def write_z_head_maintenance_settings(self, value):

        try:
            file = open(self.z_head_maintenance_settings_file_path, 'w+')
            file.write(str(value))
            file.close()

            self.time_since_z_head_lubricated_seconds = float(value)

            Logger.info("Write z head maintenance settings")
            return True

        except:
            Logger.exception("Unable to write z head maintenance settings")
            return False

    ## LASER DATUM OFFSET
    def read_z_head_laser_offset_values(self):

        try:
            file = open(self.z_head_laser_offset_file_path, 'r')
            [read_is_laser_enabled, read_laser_offset_x_value, read_laser_offset_y_value] = file.read().splitlines()
            file.close()

            # file read brings value in as a string, so need to do conversions to appropriate variables: 
            if read_is_laser_enabled == "True": self.is_laser_enabled = True
            else: self.is_laser_enabled = False

            self.laser_offset_x_value = float(read_laser_offset_x_value)
            self.laser_offset_y_value = float(read_laser_offset_y_value)


            Logger.info("Read in z head laser offset values")
            return True

        except:
            Logger.exception("Unable to read z head laser offset values")
            return False

    def write_z_head_laser_offset_values(self, enabled, X, Y):
        try:
            file = open(self.z_head_laser_offset_file_path, "w")
            file.write(str(enabled) + "\n" + str(X) + "\n" + str(Y))
            file.close()
            self.laser_offset_x_value = float(X)
            self.laser_offset_y_value = float(Y)
            if enabled == "True" or enabled == True: self.is_laser_enabled = True
            else: self.is_laser_enabled = False

            return True

        except:
            Logger.exception("Unable to write z head laser offset values")
            return False

    ## SPINDLE BRUSH MONITOR
    def read_spindle_brush_values(self):

        try:
            file = open(self.spindle_brush_values_file_path, 'r')
            read_brush = file.read().splitlines()
            file.close()

            self.spindle_brush_use_seconds = float(read_brush[0])
            self.spindle_brush_lifetime_seconds = float(read_brush[1])

            Logger.info("Read in spindle brush use and lifetime")
            return True

        except:

            Logger.exception("Unable to read spindle brush use and lifetime values")
            return False

    def write_spindle_brush_values(self, use, lifetime):
        try:
            file = open(self.spindle_brush_values_file_path, "w")
            file.write(str(use) + "\n" + str(lifetime))
            file.close()

            self.spindle_brush_use_seconds = float(use)
            self.spindle_brush_lifetime_seconds = float(lifetime)

            Logger.info("Spindle brush use and lifetime written to file")
            return True

        except:
            Logger.exception("Unable to write spindle brush use and lifetime values")
            return False

    ## SPINDLE COOLDOWN RPM OVERRIDE
    def read_spindle_cooldown_rpm_override_settings(self):

        try:
            file = open(self.spindle_cooldown_rpm_override_file_path, 'r')
            read_rpm_override = file.read()
            file.close()

            if read_rpm_override == 'True':
                self.spindle_cooldown_rpm_override = True
            else:
                self.spindle_cooldown_rpm_override = False

            Logger.info("Read in spindle cooldown override settings")
            return True

        except:
            Logger.exception("Unable to read spindle cooldown override settings")
            return False

    def write_spindle_cooldown_rpm_override_settings(self, rpm_override):
        try:

            file = open(self.spindle_cooldown_rpm_override_file_path, "w")
            file.write(str(rpm_override))
            file.close()

            if rpm_override == 'True' or rpm_override == True:
                self.spindle_cooldown_rpm_override = True
            else:
                self.spindle_cooldown_rpm_override = False

            Logger.info("Spindle cooldown override settings written to file")
            return True

        except:
            Logger.exception("Unable to write spindle cooldown override settings")
            return False

    ## SPINDLE COOLDOWN OPTIONS
    def read_spindle_cooldown_settings(self):

        try:
            file = open(self.spindle_cooldown_settings_file_path, 'r')
            read_spindle = file.read().splitlines()
            file.close()

            self.spindle_brand = str(read_spindle[0])
            self.spindle_voltage = int(read_spindle[1])
            if read_spindle[2] == 'True': self.spindle_digital = True
            else: self.spindle_digital = False
            self.spindle_cooldown_time_seconds = int(read_spindle[3])

            # Account for old naming convention
            if self.spindle_brand == 'YETI':
                self.spindle_brand = 'YETI SC1'

            # only use spindle cooldown rpm from file if the default has been overridden,
            # otherwise use default values
            if self.spindle_cooldown_rpm_override:
                self.spindle_cooldown_rpm = int(read_spindle[4])

            elif "YETI" in self.spindle_brand:
                self.spindle_cooldown_rpm = self.yeti_cooldown_rpm_default

            elif "AMB" in self.spindle_brand:
                self.spindle_cooldown_rpm = self.amb_cooldown_rpm_default

            else:
                self.spindle_cooldown_rpm = self.amb_cooldown_rpm_default

            Logger.info("Read in spindle cooldown settings")
            return True

        except:
            Logger.exception("Unable to read spindle cooldown settings")
            return False

    def write_spindle_cooldown_settings(self, brand, voltage, digital, time_seconds, rpm):
        try:

            file = open(self.spindle_cooldown_settings_file_path, "w")

            file_string = str(brand) + "\n" + str(voltage) + "\n" + str(digital) + "\n" + str(time_seconds) + "\n" + str(rpm)

            file.write(file_string)
            file.close()


            self.spindle_brand = str(brand)
            self.spindle_voltage = int(voltage)
            if digital == 'True' or digital == True: self.spindle_digital = True
            else: self.spindle_digital = False

            self.spindle_cooldown_time_seconds = int(time_seconds)
            self.spindle_cooldown_rpm = int(rpm)

            Logger.info("Spindle cooldown settings written to file")
            return True

        except:
            Logger.exception("Unable to write spindle cooldown settings")
            return False

    ## STYLUS OPTIONS
    def read_stylus_settings(self):

        try:
            file = open(self.stylus_settings_file_path, 'r')
            read_stylus = file.read()
            file.close()

            if read_stylus == 'True':
                self.is_stylus_enabled = True
            else:
                self.is_stylus_enabled = False

            Logger.info("Read in stylus settings")
            return True

        except:
            Logger.exception("Unable to read stylus settings")
            return False

    def write_stylus_settings(self, stylus):
        try:
            file = open(self.stylus_settings_file_path, "w")
            file.write(str(stylus))
            file.close()

            if stylus == 'True' or stylus == True:
                self.is_stylus_enabled = True
            else:
                self.is_stylus_enabled = False

            Logger.info("Stylus settings written to file")
            return True

        except:
            Logger.exception("Unable to write stylus settings")
            return False

    ## SPINDLE HEALTH CHECK OPTIONS
    def read_spindle_health_check_settings(self):

        try:
            file = open(self.spindle_health_check_file_path, 'r')
            read_health_check = file.read()
            file.close()

            if read_health_check == 'True':
                self.is_spindle_health_check_enabled_as_default = True
            else:
                self.is_spindle_health_check_enabled_as_default = False

            Logger.info("Read in spindle health check settings")
            return True

        except:
            Logger.exception("Unable to read spindle health check settings")
            return False

    def write_spindle_health_check_settings(self, health_check):
        try:
            file = open(self.spindle_health_check_file_path, "w")
            file.write(str(health_check))
            file.close()

            if health_check == 'True' or health_check == True:
                self.is_spindle_health_check_enabled_as_default = True
            else:
                self.is_spindle_health_check_enabled_as_default = False

            Logger.info("Spindle health check settings written to file")
            return True

        except:
            Logger.exception("Unable to write spindle health check settings")
            return False

    ## DEVICE LABEL
    def read_device_label(self):

        try:
            file = open(self.device_label_file_path, 'r')
            self.device_label = str(file.read())
            file.close()

            Logger.info("Read in device label")
            return True

        except:
            Logger.exception("Unable to read device label")
            return False

    def write_device_label(self, value):

        try:
            file = open(self.device_label_file_path, 'w+')
            file.write(str(value))
            file.close()

            self.device_label = str(value)
            Logger.info("device label written to file")
            return True

        except:
            Logger.exception("Unable to write device label")
            return False

    ## DEVICE LOCATION
    def read_device_location(self):

        try:
            file = open(self.device_location_file_path, 'r')
            self.device_location = str(file.read())
            file.close()

            Logger.info("Read in device location")
            return True

        except:
            Logger.exception("Unable to read device location")
            return False

    def write_device_location(self, value):

        try:
            file = open(self.device_location_file_path, 'w+')
            file.write(str(value))
            file.close()

            self.device_location = str(value)
            Logger.info("Device location written to file")
            return True

        except:
            Logger.exception("Unable to write device location")
            return False

    sing_path = '../../multiply.txt'
    theateam_path =  '../../plus.txt'

# GRBL SETTINGS
    def write_dollar_setting(self, setting_no, value, reset_grbl_after_stream=True):
        list_to_stream = [
            '$%s=%s' % (str(setting_no), str(value)),
            '$$'
        ]
        self.s.start_sequential_stream(list_to_stream, reset_grbl_after_stream)
        if setting_no in self.grbl_manager.settings_to_save:
            self.grbl_manager.save_console_specific_setting(setting_no, value)

    def bake_default_grbl_settings(self, z_head_qc_bake=False):

        z_max_travel_value = self.get_z_max_travel_to_bake(
            self.is_machines_fw_version_equal_to_or_greater_than_version('2.6.0', 'set Z travel'),
            self.TMC_motor[TMC_X1].ActiveCurrentScale
            )

        if not z_max_travel_value: return False

        grbl_settings = [
                    '$0=10',                                        #Step pulse, microseconds
                    '$1=255',                                       #Step idle delay, milliseconds
                    '$2=4',                                         #Step port invert, mask
                    '$3=1',                                         #Direction port invert, mask
                    '$4=0',                                         #Step enable invert, boolean
                    '$5=1',                                         #Limit pins invert, boolean
                    '$6=0',                                         #Probe pin invert, boolean
                    '$10=3',                                        #Status report, mask <----------------------
                    '$11=0.010',                                    #Junction deviation, mm
                    '$12=0.002',                                    #Arc tolerance, mm
                    '$13=0',                                        #Report inches, boolean
                    '$22=1',                                        #Homing cycle, boolean <------------------------
                    '$20=1',                                        #Soft limits, boolean <-------------------
                    '$21=1',                                        #Hard limits, boolean <------------------
                    '$23=3',                                        #Homing dir invert, mask
                    '$24=600.0',                                    #Homing feed, mm/min
                    '$25=3000.0',                                   #Homing seek, mm/min
                    '$26=250',                                      #Homing debounce, milliseconds
                    '$27=15.000',                                   #Homing pull-off, mm
                    '$30=25000.0',                                  #Max spindle speed, RPM
                    '$31=0.0',                                      #Min spindle speed, RPM
                    '$32=0',                                        #Laser mode, boolean
#                     '$100=56.649',                                #X steps/mm
#                     '$101=56.665',                                #Y steps/mm
#                     '$102=1066.667',                              #Z steps/mm
                    '$110=8000.0',                                  #X Max rate, mm/min
                    '$111=6000.0',                                  #Y Max rate, mm/min
                    '$112=750.0',                                   #Z Max rate, mm/min
                    '$120=130.0',                                   #X Acceleration, mm/sec^2
                    '$121=130.0',                                   #Y Acceleration, mm/sec^2
                    '$122=200.0',                                   #Z Acceleration, mm/sec^2
                    '$130=1300.0',                                  #X Max travel, mm TODO: Link to a settings object
                    '$131=2503.0',                                  #Y Max travel, mm
                    '$132=' + str(z_max_travel_value)  #Z Max travel, mm
            ]

        if self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'send $51 and $53 settings'):

            version_one_three_grbl_settings = [
                    '$51=0',          #Enable digital feedback spindle, boolean
                    '$53=0'           #Enable stall guard alarm operation, boolean
                    ]

            if self.is_machines_fw_version_equal_to_or_greater_than_version('2.5.0', 'send $54 setting'):

                if z_head_qc_bake:
                    version_one_three_grbl_settings.append('$54=1')           #Motor load (SG) values reporting type, boolean
                else:
                    version_one_three_grbl_settings.append('$54=0')           #Motor load (SG) values reporting type, boolean

            grbl_settings.extend(version_one_three_grbl_settings)

        grbl_settings.append('$$')     # Echo grbl settings, which will be read by sw, and internal parameters sync'd
        grbl_settings.append('$#')     # Echo grbl parameter info, which will be read by sw, and internal parameters sync'd

        self.s.start_sequential_stream(grbl_settings, reset_grbl_after_stream=True)   # Send any grbl specific parameters

        return True

    def get_z_max_travel_to_bake(self, fw_at_least_2_6, x_current):
        """
        If FW version >= 2.6 and the x_current is >= 27, it is likely that the ZH has:
          - double stack motors
          - shorter cage
        and therefore the max travel that can be baked should be 130.0.
        Prior to this change, the value should be 150.0.
        """

        if fw_at_least_2_6:
            if x_current >= 27:
                return 130.0
            elif x_current == 0:
                return False

        return 150.0


    def save_grbl_settings(self):

        self.send_any_gcode_command("$$")
        self.send_any_gcode_command("$#")

        grbl_settings_and_params = [
                    '$0=' + str(self.s.setting_0),    #Step pulse, microseconds
                    '$1=' + str(self.s.setting_1),    #Step idle delay, milliseconds
                    '$2=' + str(self.s.setting_2),           #Step port invert, mask
                    '$3=' + str(self.s.setting_3),           #Direction port invert, mask
                    '$4=' + str(self.s.setting_4),           #Step enable invert, boolean
                    '$5=' + str(self.s.setting_5),           #Limit pins invert, boolean
                    '$6=' + str(self.s.setting_6),           #Probe pin invert, boolean
                    '$10=' + str(self.s.setting_10),          #Status report, mask <----------------------
                    '$11=' + str(self.s.setting_11),      #Junction deviation, mm
                    '$12=' + str(self.s.setting_12),      #Arc tolerance, mm
                    '$13=' + str(self.s.setting_13),          #Report inches, boolean
                    '$22=' + str(self.s.setting_22),          #Homing cycle, boolean <------------------------
                    '$20=' + str(self.s.setting_20),          #Soft limits, boolean <-------------------
                    '$21=' + str(self.s.setting_21),          #Hard limits, boolean <------------------
                    '$23=' + str(self.s.setting_23),          #Homing dir invert, mask
                    '$24=' + str(self.s.setting_24),     #Homing feed, mm/min
                    '$25=' + str(self.s.setting_25),    #Homing seek, mm/min
                    '$26=' + str(self.s.setting_26),        #Homing debounce, milliseconds
                    '$27=' + str(self.s.setting_27),      #Homing pull-off, mm
                    '$30=' + str(self.s.setting_30),      #Max spindle speed, RPM
                    '$31=' + str(self.s.setting_31),         #Min spindle speed, RPM
                    '$32=' + str(self.s.setting_32)           #Laser mode, boolean
            ]

        if self.get_dollar_setting(50):
            grbl_settings_and_params.append('$50=' + str(self.s.setting_50))     #Yeti custom serial number
        if self.get_dollar_setting(51) != -1:
            grbl_settings_and_params.append('$51=' + str(self.s.setting_51))     #Enable digital feedback spindle, boolean

        try:
            grbl_settings_and_params.append('$53=' + str(self.s.setting_53))     #Enable stall guard alarm operation, boolean
            grbl_settings_and_params.append('$54=' + str(self.s.setting_54))     #Motor load (SG) values reporting type, boolean

        except:
            pass

        grbl_settings_and_params += [
                    '$100=' + str(self.s.setting_100),   #X steps/mm
                    '$101=' + str(self.s.setting_101),   #Y steps/mm
                    '$102=' + str(self.s.setting_102),   #Z steps/mm
                    '$110=' + str(self.s.setting_110),   #X Max rate, mm/min
                    '$111=' + str(self.s.setting_111),   #Y Max rate, mm/min
                    '$112=' + str(self.s.setting_112),   #Z Max rate, mm/min
                    '$120=' + str(self.s.setting_120),    #X Acceleration, mm/sec^2
                    '$121=' + str(self.s.setting_121),    #Y Acceleration, mm/sec^2
                    '$122=' + str(self.s.setting_122),    #Z Acceleration, mm/sec^2
                    '$130=' + str(self.s.setting_130),   #X Max travel, mm TODO: Link to a settings object
                    '$131=' + str(self.s.setting_131),   #Y Max travel, mm
                    '$132=' + str(self.s.setting_132)   #Z Max travel, mm
                    # 'G10 L2 P1 X' + str(self.m.s.g54_x) + ' Y' + str(self.m.s.g54_y) + ' Z' + str(self.m.s.g54_z) # tell GRBL what position it's in
            ]

        f = open('/home/pi/easycut-smartbench/src/sb_values/saved_grbl_settings_params.txt', 'w')
        f.write(('\n').join(grbl_settings_and_params))
        f.close()
        Logger.info('Saved grbl settings to file')

    def restore_grbl_settings_from_file(self, filename):

        try:
            fileobject = open(filename, 'r')
            settings_to_restore = (fileobject.read()).split('\n')
            settings_to_restore.append("$$")
            settings_to_restore.append("$#")
            self.s.start_sequential_stream(settings_to_restore)   # Send any grbl specific parameters
            return True

        except:
            Logger.exception('Could not read from file')
            return False

# ABSOLUTE MACHINE LIMITS

    # For manual moves, recalculate the absolute limits, factoring in the limit-switch safety distance (how close we want to get to the switches)
    def set_jog_limits(self):

        # XY home end
        self.x_min_jog_abs_limit = -self.grbl_x_max_travel + self.limit_switch_safety_distance
        self.y_min_jog_abs_limit = -self.grbl_y_max_travel + self.limit_switch_safety_distance

        # XY far end
        self.x_max_jog_abs_limit = -self.limit_switch_safety_distance
        self.y_max_jog_abs_limit = -self.limit_switch_safety_distance

        # Z 
        self.z_max_jog_abs_limit = -self.limit_switch_safety_distance
        self.z_min_jog_abs_limit = -self.grbl_z_max_travel


    # Functions to check which Y bench is being used based on y max travel
    def bench_is_short(self):
        return self.grbl_y_max_travel < 2000.0

    def bench_is_standard(self):
        return self.grbl_y_max_travel > 2000.0

    # def bench_is_long(self):
    #     return self.grbl_y_max_travel > 3000.0


# HW/FW VERSION CAPABILITY

    def is_using_sc2(self):
        return self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'SC2 capable') \
            and self.theateam() and self.get_dollar_setting(51) and self.stylus_router_choice != 'stylus'

    def is_spindle_health_check_active(self):
        return self.is_spindle_health_check_enabled_as_default

    spindle_health_check_failed = False
    spindle_health_check_passed = False

    def has_spindle_health_check_failed(self):
        return self.spindle_health_check_failed

    def has_spindle_health_check_passed(self):
        return self.spindle_health_check_passed

    def has_spindle_health_check_run(self):
        return self.has_spindle_health_check_passed() or self.has_spindle_health_check_failed()

    def get_spindle_freeload(self):
        return self.s.spindle_freeload

    # def fw_can_operate_laser_commands(self):
    #     output = self.is_machines_fw_version_equal_to_or_greater_than_version('1.1.2', 'laser commands AX and AZ')
    #     Logger.info('FW version able to operate laser commands AX and AZ: ' + str(output))
    #     return output      

    def hw_can_operate_laser_commands(self):
        output = self.is_machines_hw_version_equal_to_or_greater_than_version(8, 'laser commands AX and AZ') # Update to version 8, but need 6 to test on rig
        Logger.debug('HW version able to operate laser commands AX and AZ: ' + str(output))
        return output


    def fw_can_operate_zUp_on_pause(self):

        Logger.debug('FW version able to lift on pause: ' + str(self.is_machines_fw_version_equal_to_or_greater_than_version('1.0.13', 'Z up on pause')))
        return self.is_machines_fw_version_equal_to_or_greater_than_version('1.0.13', 'Z up on pause')


    def is_machines_fw_version_equal_to_or_greater_than_version(self, version_to_reference, capability_decription):  # ref_version_parts syntax "x.x.x"

        # NOTE: Would use "from packaging import version" but didn't ship as standard. So doing the hard way.
        try:
            machine_fw_parts = self.s.fw_version.split('.')[:3]  # [:3] take's only the first three split values (throw away the date field
            ref_version_parts = version_to_reference.split('.')[:3]

            # convert values to ints for comparison
            machine_fw_parts = [int(i) for i in machine_fw_parts]
            ref_version_parts = [int(i) for i in ref_version_parts]
        except:
            error_description = "Couldn't process Z head firmware value when checking capability: " + str(capability_decription) + \
            ".\n\n Please check Z Head connection."
            Logger.exception(error_description)

            return False

        if machine_fw_parts[0] > ref_version_parts[0]:
            return True
        elif machine_fw_parts[0] < ref_version_parts[0]:
            return False
        else: # equal so far
            if machine_fw_parts[1] > ref_version_parts[1]:
                return True
            elif machine_fw_parts[1] < ref_version_parts[1]:
                return False
            else: # equal so far
                if machine_fw_parts[2] > ref_version_parts[2]:
                    return True
                elif machine_fw_parts[2] < ref_version_parts[2]:
                    return False
                else:
                    return True # equal

    def is_machines_hw_version_equal_to_or_greater_than_version(self, version_to_reference, capability_decription):

        try:
            if float(self.s.hw_version) >= version_to_reference:
                return True
            else:
                return False

        except:
            error_description = "Couldn't process machine hardware value when checking capability: " + str(capability_decription) + \
            ".\n\n Please check Z Head connection."
            Logger.exception(error_description)

            return False

    def sing(self):
        return self.look_at(self.sing_path)

    def theateam(self):
        return self.look_at(self.theateam_path)

    def enable_theateam(self):
        self.write_dollar_setting(51, 1)
        open(self.theateam_path, 'a').close()

    def disable_theateam(self):
        self.write_dollar_setting(51, 0)
        os.remove(self.theateam_path)

# HW/FW ADJUSTMENTS

    def correct_rpm_for_120(self, target_rpm, revert = False, log = True):
        """
        Compensates for the desparity in set and actual spindle RPM for a 120V spindle.

        Args:
            target_rpm (int): The target RPM to be corrected.
            revert (bool, optional): If True, the corrected RPM will be reverted back to the original requested RPM. Defaults to False.
            log (bool, optional): If True, compensating information will be logged.

        Returns:
            int: The corrected RPM value.
        """

        # For conversion maths see https://docs.google.com/spreadsheets/d/1Dbn6JmNCWaCNxpXMXxxNB2IKvNlhND6zz_qQlq60dQY/edit#gid=1507195715

        if 10000 <= target_rpm <= 25000:

            if revert:
                return int(round(0.6739 * target_rpm + 8658)) # Revert the corrected RPM back to the original requested RPM

            compensated_RPM = int(round((target_rpm - 8658) / 0.6739))

            if compensated_RPM < 0:
                if log:
                    Logger.info("Calculated RPM {} too low for 120V spindle, setting to 0".format(target_rpm))
                compensated_RPM = 0
            elif compensated_RPM > 25000:
                compensated_RPM = 25000

            return compensated_RPM

        else:
            if log:
                Logger.info("Requested RPM {} outside of range for 120V spindle (10000 - 25000)".format(target_rpm))
            return 0

    def correct_rpm_for_230(self, target_rpm, revert = False, log= True):
        """
        Compensates for the desparity in set and actual spindle RPM for a 230V spindle.

        Args:
            target_rpm (int): The target RPM to be corrected.
            revert (bool, optional): If True, the corrected RPM will be reverted back to the original requested RPM. Defaults to False.
            log (bool, optional): If True, compensating information will be logged.

        Returns:
            int: The corrected RPM value.
        """
        # For conversion maths see https://docs.google.com/spreadsheets/d/1Dbn6JmNCWaCNxpXMXxxNB2IKvNlhND6zz_qQlq60dQY/edit#gid=1507195715

        if 4000 <= target_rpm <= 25000:

            if revert:
                return int(round(0.95915 * target_rpm + 1886)) # Revert the corrected RPM back to the original requested RPM

            compensated_RPM = int(round((target_rpm - 1886) / 0.95915))

            if compensated_RPM < 0:
                if log:
                    Logger.info("Calculated RPM {} too low for 230V spindle, setting to 0".format(target_rpm))
                compensated_RPM = 0
            elif compensated_RPM > 25000:
                compensated_RPM = 25000

            return compensated_RPM

        else:
            if log:
                Logger.info("Requested RPM {} outside of range for 230V spindle (4000 - 25000)".format(target_rpm))
            return 0

    def correct_rpm(self, requested_rpm, spindle_voltage = None, revert = False, log = True):
        """
        Compensates for the desparity in set and actual spindle RPM for a spindle.

        For use outside of router_machine.py

        Args:
            requested_rpm (float): The RPM value to be corrected.
            voltage (int, optional): The spindle voltage. Defaults to spindle_voltage.
            revert (bool, optional): If True, the corrected RPM will be reverted back to the original requested RPM. Defaults to False.

        Returns:
            float: The corrected RPM value.

        Raises:
            ValueError: If the spindle voltage is not recognised.
        """

        if spindle_voltage is None:
            spindle_voltage = self.spindle_voltage # Use spindle voltage set by user in maintenance app

        if spindle_voltage in [110, 120]:
            rpm_to_set = self.correct_rpm_for_120(requested_rpm, revert, log)

        elif spindle_voltage in [230, 240]:
            rpm_to_set = self.correct_rpm_for_230(requested_rpm, revert, log)

        else:
            raise ValueError('Spindle voltage: {} not recognised'.format(spindle_voltage))

        if revert:
            if log:
                Logger.info("Requested RPM: "+ str(requested_rpm) +
                            " Reverted RPM: " + str(rpm_to_set) +
                            " Voltage: " + str(spindle_voltage))
        else:
            if log:
                Logger.info("Requested RPM: "+ str(requested_rpm) +
                            " Compensated RPM: " + str(rpm_to_set) +
                            " Voltage: " + str(spindle_voltage))

        return rpm_to_set

    def turn_on_spindle_for_data_read(self):
        """
        Turns on the spindle at 0 RPM. Used to read spindle data.

        :return: None
        """
        self.turn_on_spindle(rpm=0)

    def turn_on_spindle(self, rpm=12000, run_at_grbl_speed=False):
        """
        This method sends the command 'M3' to the Z Head to turn on the spindle at a given speed.

        No RPM compensation occurs in this command as this is captured and handled by compensate_spindle_speed_command() in the SerialConnection object

        :param rpm: The RPM to turn the spindle on at. Defaults to 12,000.
        :param run_at_grbl_speed: If True, the spindle will run at the last GRBL speed. Defaults to False.
        :return: None
        """
        dust_shoe_detection = self.user_settings_manager.get_value('dust_shoe_detection')
        if dust_shoe_detection and not self.s.dustshoe_is_closed:
            self.sm.pm.show_dustshoe_warning_popup()
            return
        if run_at_grbl_speed:
            self.s.write_command("M3")
        else:
            self.s.write_command("M3 S" + str(rpm))

    def turn_off_spindle(self):
        """
        This method sends the command 'M5' to the Z Head to turn off the spindle.

        :return: None
        """
        self.s.write_command("M5")

    def minimum_spindle_speed(self, spindle_voltage = None):
        """
        Returns the minimum spindle speed for a given spindle voltage.

        For use outside of router_machine.py

        Args:
            spindle_voltage (int, optional): The spindle voltage. Defaults to spindle_voltage.

        Returns:
            int: The minimum spindle speed.
        """

        if spindle_voltage is None:
            spindle_voltage = self.spindle_voltage # Use spindle voltage set by user in maintenance app

        if spindle_voltage in [110, 120]:
            return 10000 # Defined by Mafell spindle HW

        elif spindle_voltage in [230, 240]:
            return 4000 # Defined by Mafell spindle HW

        else:
            raise ValueError('Spindle voltage: {} not recognised'.format(spindle_voltage))

    def maximum_spindle_speed(self):
        return 25000

    def is_spindle_on(self):
        return float(self.s.spindle_speed) > 0


# START UP SEQUENCES

    # BOOT UP SEQUENCE
    def bootup_sequence(self):
        Logger.info("Boot up machine, and get settings...")
        self._stop_all_streaming()  # In case alarm happened during boot, stop that
        self._grbl_soft_reset()     # Reset to get out of Alarm mode.
        # Now grbl won't allow anything until machine is rehomed or unlocked, so...
        Clock.schedule_once(lambda dt: self._grbl_unlock(),0.1)
        # Set lights
        Clock.schedule_once(lambda dt: self.set_led_colour('YELLOW'),0.31)
        # Get grbl firmware version loaded into serial comms
        Clock.schedule_once(lambda dt: self.send_any_gcode_command('$I'), 1.5)
        # Turn laser off (if it is on)
        Clock.schedule_once(lambda dt: self.laser_off(bootup=True), 1.7)
        # Get grbl settings loaded into serial comms
        Clock.schedule_once(lambda dt: self.get_grbl_settings(), 1.9)
        # do TMC motor controller handshake (if FW > 2.2.8), load params into serial comms
        Clock.schedule_once(lambda dt: self.tmc_handshake(), 3)


    # TMC MOTOR CONTROLLER HANDSHAKE
    handshake_event = None

    def tmc_handshake(self):

        self.clear_motor_registers()

        if self.s.fw_version and self.state().startswith('Idle'):

            if self.handshake_event: Clock.unschedule(self.handshake_event)

            if self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'get TMC registers'):
                self.send_command_to_motor("GET REGISTERS", command=GET_REGISTERS)

        else:
            # In case handshake is too soon, it tries one more time to see if it can read a FW version
            self.handshake_event = Clock.schedule_once(lambda dt: self.tmc_handshake(), 10)


# CRITICAL START/STOP

    '''
    
    Working doc (WARNING, may not be updated):
    https://docs.google.com/document/d/1iEII2Yl9jmwNsMWgSrnNJ-6phimv7sJFLdcrkriSAb0/edit#heading=h.jjpupza6jss
    
    Understanding what start/stop commands to use:
    
    DOOR (SOFT).
    Realtime command. Puts machine in door state.
    Use case: decelerates the XYZ to stop and turns the spindle off. This is better than a feed hold because a hold doesn't stop the spindle (and you can't do a manual gcode spindle off/on command during a stream)
    To resume: use RESUME 
    Important note: in door state, the machine will not process either the char or line buffer. It only accepts realtime commands. 
    If chars are sent, they will simply get added to the buffer (assuming there is space). Therefore ONLY send realtime commands when in this state.
    e.g. Door triggered. LED colour sent. Nothing happens, buffer capacity reduces by 5 chars. Resume triggered. LED colour activates, buffer clears.
    
    DOOR (HARD)
    Same as door soft, but triggered from the pin (hard switch). In addition it activates the yeti flashing red light - which is a problem (see below)
    
    YETI flashing red light:
    In YETI grbl 1.0.7 the hard door switch also triggers a flashing red light, operated from within grbl, which has a bug. 
    Flashing red light mode is not cleared by realtime '&' command (normally sets LED to white).
    Instead, issuing this '&' command at any point after flashing has been initiated, simply freezes it on either red or nothing. 
    To resume normal LED functions (when not in door state any more) send a normal LED command. Obviously this is a problem when streaming.
    
    RESUME:
    Realtime command.
    Use case: Intended for use in resuming from a door state. Spindle will fire up for a few seconds before continuing to operate the line buffer.
    
    INCOMING ALARM:
    Suspends Grbl
    Firstly, needs a RESET. So impossible to recover a stream since the buffer gets lost - it's time to start again.
    THEN, in addition, the machine must HOME or UNLOCK
    
    UNLOCK:
    Not realtime: '$X'
    If the machine has been REST after an ALARM, then it isn't allowed to move unless it is unlocked or homed
    It has no other function
    
    RESET:
    Realtime
    Completely clears grbl, including buffers and state.
    If done during motion, will thro ALARM. Otherwise normal operations resume (no homing req etc).
    Does not change LED state (coz that's cutosm YETI).
    e.g. Door state --> Idle
    
    '''

    # START/STOP COMMANDS

    def reset_from_alarm(self):
        # Machine has stopped without warning and probably lost position
        self._stop_all_streaming()  # In case alarm happened during stream, stop that
        self._grbl_soft_reset()     # Reset to get out of Alarm mode. All buffers will be dumped.

    def resume_from_alarm(self):
        # Machine has stopped without warning and probably lost position
        self._stop_all_streaming()  # In case alarm happened during stream, stop that
        self._grbl_soft_reset()     # Reset to get out of Alarm mode. All buffers will be dumped.
        # Now grbl won't allow anything until machine is rehomed or unlocked
        # To prevent user frustration, we're allowing the machine to be unlocked and moved until we can add further user handling
        Clock.schedule_once(lambda dt: self._grbl_unlock(),0.1)
        Clock.schedule_once(lambda dt: self.led_restore(),0.3)
        Clock.schedule_once(lambda dt: self.set_led_colour('GREEN'),0.5)

    def stop_from_gcode_error(self):
        # Note this should be a implementation of door functionality, but this is a fast implementation since there are multiple possible door calls which we need to manage.
        self._grbl_feed_hold()
        self._stop_all_streaming()  # In case alarm happened during stream, stop that

        # Allow machine to decelerate in XYZ before resetting to kill spindle, or it'll alarm due to resetting in motion
        Clock.schedule_once(lambda dt: self._grbl_soft_reset(), 1.5)

        # Sulk
        Clock.schedule_once(lambda dt: self.turn_off_vacuum(), 2.0)
        Clock.schedule_once(lambda dt: self.set_led_colour('RED'),2.1)

    def resume_from_gcode_error(self):
        Clock.schedule_once(lambda dt: self.set_led_colour('GREEN'),0.1)

    def soft_stop(self):
        self.set_pause(True)
        self._grbl_door()

    def stop_from_quick_command_reset(self):
        self._stop_all_streaming()
        self._grbl_soft_reset()
        Clock.schedule_once(lambda dt: self._grbl_unlock(),0.1)
        Clock.schedule_once(lambda dt: self.set_led_colour('GREEN'),0.2)

    def stop_for_a_stream_pause(self, reason_for_pause=None):
        self.set_pause(True, reason_for_pause=reason_for_pause)
        self._grbl_door()

    def resume_after_a_stream_pause(self):
        self.reason_for_machine_pause = "Resuming"
        self._grbl_resume()
        Clock.schedule_once(lambda dt: self.set_pause(False),0.3)

    def set_pause(self, pauseBool, reason_for_pause=None):

        prev_state = self.is_machine_paused
        self.is_machine_paused = pauseBool # sets serial_connection flag to pause (allows a hard door to be detected)
        if not pauseBool: reason_for_pause=None # ideally, don't include a reason when setting to False, but this is here in case
        self.reason_for_machine_pause = reason_for_pause

        def record_pause_time(prev_state, pauseBool):
            # record pause time
            if not prev_state and pauseBool:
                self.s.stream_pause_start_time = time.time()

            if prev_state and not pauseBool and self.s.stream_pause_start_time != 0:
                self.s.stream_paused_accumulated_time = self.s.stream_paused_accumulated_time + (time.time() - self.s.stream_pause_start_time)
                self.s.stream_pause_start_time = 0

        Clock.schedule_once(lambda dt: record_pause_time(prev_state, pauseBool), 0.2)

    def stop_from_soft_stop_cancel(self):
        self.resume_from_alarm()
        Clock.schedule_once(lambda dt: self.set_pause(False),0.6)

    def resume_from_a_soft_door(self):
        self.reason_for_machine_pause = "Resuming"
        self._grbl_resume()
        Clock.schedule_once(lambda dt: self.set_pause(False),0.4)

    def resume_after_a_hard_door(self):
        self.reason_for_machine_pause = "Resuming"
        self._grbl_resume()
        Clock.schedule_once(lambda dt: self.set_pause(False),0.4)

    def cancel_after_a_hard_door(self):
        self.resume_from_alarm()
        Clock.schedule_once(lambda dt: self.set_pause(False),0.4)

    def reset_after_sequential_stream(self):
        self._stop_all_streaming()
        self._grbl_soft_reset()

    def reset_pre_homing(self):
        self._stop_all_streaming()
        self._grbl_soft_reset()
        Clock.schedule_once(lambda dt: self._grbl_unlock(),0.1) # if awaking from an alarm state, to allow other calls to process prior to the ineveitable $H which would normally clear it
        Clock.schedule_once(lambda dt: self.set_led_colour("ORANGE"),0.2)
        # Then allow 0.2 seconds for grbl to become receptive after reset

    def reset_on_cancel_homing(self):
        self._stop_all_streaming()
        self._grbl_soft_reset()
        Clock.schedule_once(lambda dt: self.set_led_colour("BLUE"),0.2)


    # Internal calls

    def _stop_all_streaming(self):
        # Cancel all streams to stop EC continuing to send stuff (required before a RESET)
        Logger.info('Streaming stopped.')
        if self.s.is_job_streaming: self.s.cancel_stream()
        if self.s.is_sequential_streaming: self.s.cancel_sequential_stream() # Cancel sequential stream to stop it continuing to send stuff after reset

    def _grbl_resume(self):
        Logger.info('grbl realtime cmd sent: ~ resume')
        self.s.write_realtime('~', altDisplayText = 'Resume')

    def _grbl_feed_hold(self):
        Logger.info('grbl realtime cmd sent: ! feed-hold')
        self.s.write_realtime('!', altDisplayText = 'Feed hold')

    def _grbl_soft_reset(self):
        Logger.info('grbl realtime cmd sent: \\x18 soft reset')
        self.s.grbl_waiting_for_reset = True
        self.s.write_realtime("\x18", altDisplayText = 'Soft reset')

    def _grbl_door(self):
        Logger.info('grbl realtime cmd sent: \\x84')
        self.s.write_realtime('\x84', altDisplayText = 'Door')

    def _grbl_unlock(self):
        Logger.info('grbl realtime cmd sent: $X unlock')
        self.s.write_command('$X', altDisplayText = 'Unlock: $X')


# COMMS

    def is_connected(self): return self.s.is_connected()
    def is_job_streaming(self): return self.s.is_job_streaming
    def state(self): return self.s.m_state
    def buffer_capacity(self): return self.s.serial_blocks_available
    def is_grbl_waiting_for_reset(self): return self.s.grbl_waiting_for_reset


# GRBL STATES AND SETTINGS

    def set_state(self, temp_state):
        grbl_state_words = ['Idle', 'Run', 'Hold', 'Jog', 'Alarm', 'Door', 'Check', 'Home', 'Sleep']
        if temp_state in grbl_state_words:
            self.s.m_state = temp_state

    # Query if smartbench_is_busy: don't send commands yet :) 
    def smartbench_is_busy(self):

        if not self.state().startswith("Idle"):
            return True

        if self.s.is_sequential_streaming:
            return True

        if self.s.is_job_streaming:
            return True

        if self.s.write_command_buffer:
            return True

        if self.s.write_realtime_buffer:
            return True

        if self.s.write_protocol_buffer:
            return True

        if int(self.s.serial_blocks_available) != self.s.GRBL_BLOCK_SIZE:
            return True

        if int(self.s.serial_chars_available) != self.s.RX_BUFFER_SIZE:
            return True

        if self.s.grbl_waiting_for_reset:
            return True

        if self.is_machine_paused:
            return True

        return False

    def get_grbl_status(self):
        self.s.write_command('$#')

    def get_grbl_settings(self):
        self.s.write_command('$$')

    def get_grbl_motion_mode(self):
        return self.jd.grbl_mode_tracker[0][0] if self.jd.grbl_mode_tracker else None

    def send_any_gcode_command(self, gcode):
        self.s.write_command(gcode)

    def enable_check_mode(self):
        self._grbl_soft_reset()
        if self.s.m_state != "Check":
            Clock.schedule_once(lambda dt: self.s.write_command('$C', altDisplayText = 'Check mode ON'), 0.6)
        else:
            Logger.info('Check mode already enabled')

    def disable_check_mode(self):
        if self.s.m_state == "Check":
            self.s.write_command('$C', altDisplayText = 'Check mode OFF')
        else:
            Logger.info('Check mode already disabled')
        Clock.schedule_once(lambda dt: self._grbl_soft_reset(), 0.1)

    def get_switch_states(self):

        switch_states = []

        if self.s.limit_x: switch_states.append('limit_x') # convention: min is lower_case
        if self.s.limit_X: switch_states.append('limit_X') # convention: MAX is UPPER_CASE
        if self.s.limit_y: switch_states.append('limit_y')
        if self.s.limit_Y: switch_states.append('limit_Y')
        if self.s.limit_z: switch_states.append('limit_z')
        if self.s.probe: switch_states.append('probe')
        if self.s.dustshoe_is_closed: switch_states.append('dustshoe_is_closed')
        if self.s.spare_door: switch_states.append('spare_door')

        return switch_states

    def disable_limit_switches(self):

        #turn soft limits, hard limts OFF
        Logger.info('switching soft limits & hard limts OFF')
        settings = ['$22=0','$20=0','$21=0']
        self.s.start_sequential_stream(settings)

    def enable_limit_switches(self):

        #turn soft limits, hard limts OFF
        Logger.info('switching soft limits & hard limts ON')
        settings = ['$22=1','$20=1','$21=1']
        self.s.start_sequential_stream(settings)

    def disable_only_hard_limits(self):

        Logger.info("TURNING OFF HARD LIMITS")
        settings = ['$21=0']
        self.s.start_sequential_stream(settings)

    def enable_only_hard_limits(self):

        Logger.info("TURNING ON HARD LIMITS")
        settings = ['$21=1']
        self.s.start_sequential_stream(settings)

    def disable_only_soft_limits(self):

        Logger.info("TURNING OFF SOFT LIMITS")
        settings = ['$20=0']
        self.s.start_sequential_stream(settings)

    def enable_only_soft_limits(self):

        Logger.info("TURNING ON SOFT LIMITS")
        settings = ['$20=1']
        self.s.start_sequential_stream(settings)

    # settings for v1.3 and above

    def disable_x_motors(self):
        if self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'Disable x motors'):
            self.send_command_to_motor("Disable X1 motor", motor=TMC_X1, command=SET_MOTOR_ENERGIZED, value=0)
            self.send_command_to_motor("Disable X2 motor", motor=TMC_X2, command=SET_MOTOR_ENERGIZED, value=0)

    def enable_x_motors(self):
        if self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'Enable x motors'):
            self.send_command_to_motor("Enable X1 motor", motor=TMC_X1, command=SET_MOTOR_ENERGIZED, value=1)
            self.send_command_to_motor("Enable X2 motor", motor=TMC_X2, command=SET_MOTOR_ENERGIZED, value=1)

    def disable_y_motors(self):
        if self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'Disable y motors'):
            self.send_command_to_motor("Disable Y1 motor", motor=TMC_Y1, command=SET_MOTOR_ENERGIZED, value=0)
            self.send_command_to_motor("Disable Y2 motor", motor=TMC_Y2, command=SET_MOTOR_ENERGIZED, value=0)

    def enable_y_motors(self, dt=0):
        if self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'Enable y motors'):
            self.send_command_to_motor("Enable Y1 motor", motor=TMC_Y1, command=SET_MOTOR_ENERGIZED, value=1)
            self.send_command_to_motor("Enable Y2 motor", motor=TMC_Y2, command=SET_MOTOR_ENERGIZED, value=1)

    def disable_z_motor(self):
        if self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'Disable z motor'):
            self.send_command_to_motor("Disable Z motor", motor=TMC_Z, command=SET_MOTOR_ENERGIZED, value=0)

    def enable_z_motor(self):
        if self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'Enable z motor'):
            self.send_command_to_motor("Enable Z motor", motor=TMC_Z, command=SET_MOTOR_ENERGIZED, value=1)

    def disable_stall_detection(self):
        if self.get_dollar_setting(53) and self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'Disable SG'):
            self.send_command_to_motor("SET SG ALARM: 0", command=SET_SG_ALARM)

    def enable_stall_detection(self, dt=0):
        if self.get_dollar_setting(53) and self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'Disable SG'):
            self.send_command_to_motor("SET SG ALARM: 1", command=SET_SG_ALARM, value=1)


# SETTINGS GETTERS
    def serial_number(self):
        return self.s.setting_50

    def get_product_code(self):
        """takes the last two digits of $50 and converts them to a ProductCode."""
        if self.s.setting_50 == 0.0:
            return ProductCodes.UNKNOWN
        else:
            pc = str(self.s.setting_50)[-2] + str(self.s.setting_50)[-1]
            return ProductCodes(int(pc))

    def firmware_version(self):
        try: self.s.fw_version
        except: return 0
        else: return self.s.fw_version


    def bench_is_dwt(self):
        return self.get_product_code() is ProductCodes.DRYWALLTEC

    def smartbench_model(self):
        # recommend refactoring models into an enum, relying on strings is error-prone
        pc = self.get_product_code()
        if pc is ProductCodes.DRYWALLTEC:
            return "DRYWALLTEC SmartCNC"
        elif pc == ProductCodes.PRECISION_PRO_X:
            return "SmartBench V1.3 PrecisionPro X"
        elif pc is ProductCodes.PRECISION_PRO_PLUS:
            return "SmartBench V1.3 PrecisionPro Plus"
        elif pc is ProductCodes.PRECISION_PRO:
            if self.bench_is_short():
                return "SmartBench Mini V1.3 PrecisionPro"
            elif self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'Smartbench model'):
                return "SmartBench V1.3 PrecisionPro CNC Router"
            elif self.is_machines_fw_version_equal_to_or_greater_than_version('1.4.0', 'Smartbench model'):
                return "SmartBench V1.2 PrecisionPro CNC Router"
            else:
                return "SmartBench V1.2 Precision CNC Router"
        elif pc is ProductCodes.STANDARD:
            return "SmartBench V1.2 Standard CNC Router"
        elif pc is ProductCodes.FIRST_VERSION:
            if self.is_machines_hw_version_equal_to_or_greater_than_version(5, 'Smartbench model'):
                return "SmartBench V1.1 CNC Router"
            else:
                return "SmartBench V1.0 CNC Router"

        Logger.error("SmartBench model detection failed")
        return "SmartBench model detection failed"

    def get_dollar_setting(self, setting_num):
        return getattr(self.s, "setting_" + str(setting_num), 0)

# POSITONAL GETTERS

    def x_pos_str(self): return str(self.s.m_x)
    def y_pos_str(self): return str(self.s.m_y)
    def z_pos_str(self): return str(self.s.m_z)

    # 'Machine position'/mpos is the absolute position of the tooltip, wrt home
    def mpos_x(self): return self.s.m_x
    def mpos_y(self): return self.s.m_y
    def mpos_z(self): return self.s.m_z

    # 'Work position'/wpos is the position of the tooltip relative to the datum position set for the job
    # WPos = MPos - WCO.
    def wpos_x(self): return self.s.m_x - self.x_wco()
    def wpos_y(self): return self.s.m_y - self.y_wco()
    def wpos_z(self): return self.s.m_z - self.z_wco()

    # 'Work Co-ordinate offset'/wco is the definition of the datum position set for the job, wrt home
    # WPos = MPos - WCO
    def x_wco(self): return float(self.s.wco_x)
    def y_wco(self): return float(self.s.wco_y)
    def z_wco(self): return float(self.s.wco_z)

    # The G28 command moves the tooltip to an intermediate parking position. 
    # Potentially useful if you want the tool to go to a specific position before and after a job (for example to reload a part for batch work)
    def g28_x(self): return float(self.s.g28_x)
    def g28_y(self): return float(self.s.g28_y)
    def g28_z(self): return float(self.s.g28_z)

# SPEED AND FEED GETTERS
    def feed_rate(self): return int(self.s.feed_rate)

    def get_is_constant_feed_rate(self, last_modal_feed_rate, feed_override_percentage, current_feed_rate, tolerance_for_acceleration_detection):
        constant_feed_target = last_modal_feed_rate * feed_override_percentage / 100
        return abs(constant_feed_target - current_feed_rate) <= tolerance_for_acceleration_detection, last_modal_feed_rate

    def spindle_load(self):
        try:
            return int(self.s.spindle_load_voltage)
        except:
            return ''

# LOAD GETTERS

    # Stall guard loads - this is the relative load on a motor or axis, which is monitored to guard against a stall
    def x_sg(self): return self.s.sg_x_motor_axis
    def y_sg(self): return self.s.sg_y_axis
    def y1_sg(self): return self.s.sg_y1_motor
    def y2_sg(self): return self.s.sg_y2_motor
    def z_sg(self): return self.s.sg_z_motor_axis
    def x1_sg(self): return self.s.sg_x1_motor
    def x2_sg(self): return self.s.sg_x2_motor

# POSITIONAL SETTERS

    datum_position = ListProperty([0, 0])

    def set_workzone_to_pos_xy(self):
        self.set_datum(x=0, y=0)
        self.datum_position = [self.s.m_x, self.s.m_y]
        Clock.schedule_once(lambda dt: self.strobe_led_playlist("datum_has_been_set"), 0.2)

    def set_x_datum(self):
        self.set_datum(x=0)
        Clock.schedule_once(lambda dt: self.strobe_led_playlist("datum_has_been_set"), 0.2)

    def set_y_datum(self):
        self.set_datum(y=0)
        Clock.schedule_once(lambda dt: self.strobe_led_playlist("datum_has_been_set"), 0.2)

    def set_workzone_to_pos_xy_with_laser(self, jog_to_datum=True):
        if jog_to_datum:
            if self.jog_spindle_to_laser_datum('XY'):

                def wait_for_movement_to_complete(dt):
                    if not self.state() == 'Jog':
                        Clock.unschedule(xy_poll_for_success)
                        self.set_workzone_to_pos_xy()

                xy_poll_for_success = Clock.schedule_interval(wait_for_movement_to_complete, 0.5)

            else:
                error_message = (
                    self.l.get_str("Laser crosshair is out of bounds!") + \
                    "\n\n" + \
                    self.l.get_str("Datum has not been set.") + " " + \
                    self.l.get_str("Please choose a different datum using the laser crosshair.")
                    )
                popup_info.PopupError(self.sm, self.l, error_message)
        else:
            self.set_datum(x=-self.laser_offset_x_value, y=-self.laser_offset_y_value)

    def set_x_datum_with_laser(self):
        if self.jog_spindle_to_laser_datum('X'):

            def wait_for_movement_to_complete(dt):
                if not self.state() == 'Jog':
                    Clock.unschedule(x_poll_for_success)
                    self.set_x_datum()

            x_poll_for_success = Clock.schedule_interval(wait_for_movement_to_complete, 0.5)

        else:
            error_message = (
                self.l.get_str("Laser crosshair is out of bounds!") + \
                "\n\n" + \
                self.l.get_str("Datum has not been set.") + \
                self.l.get_str("Please choose a different datum using the laser crosshair.")
                )
            popup_info.PopupError(self.sm, self.l, error_message)

    def set_y_datum_with_laser(self):
        if self.jog_spindle_to_laser_datum('Y'):

            def wait_for_movement_to_complete(dt):
                if not self.state() == 'Jog':
                    Clock.unschedule(y_poll_for_success)
                    self.set_y_datum()

            y_poll_for_success = Clock.schedule_interval(wait_for_movement_to_complete, 0.5)

        else:
            error_message = (
                self.l.get_str("Laser crosshair is out of bounds!") + \
                "\n\n" + \
                self.l.get_str("Datum has not been set.") + \
                self.l.get_str("Please choose a different datum using the laser crosshair.")
                )
            popup_info.PopupError(self.sm, self.l, error_message)


    def set_jobstart_z(self):
        self.set_datum(z=0)
        Clock.schedule_once(lambda dt: self.strobe_led_playlist("datum_has_been_set"), 0.2)

    def set_standby_to_pos(self):
        self.s.write_command('G28.1')
        Clock.schedule_once(lambda dt: self.strobe_led_playlist("standby_pos_has_been_set"), 0.2)

    def set_datum(self, x=None, y=None, z=None, relative=False):
        if relative:
            datum_command = 'G10 L2'
        else:
            datum_command = 'G10 L20 P1'

        if x is not None:
            datum_command += " X" + str(x)
        if y is not None:
            datum_command += " Y" + str(y)
        if z is not None:
            datum_command += " Z" + str(z)

        self.s.write_command(datum_command)
        self.get_grbl_status()



# MOVEMENT/ACTION

    def jog_absolute_single_axis(self, axis, target, speed):
        self.s.write_command('$J=G53 ' + axis + str(target) + ' F' + str(speed))

    def jog_absolute_xy(self, x_target, y_target, speed):
        self.s.write_command('$J=G53 X' + str(x_target) + ' Y' + str(y_target) + ' F' + str(speed))

    def jog_relative(self, axis, dist, speed):
        self.s.write_command('$J=G91 ' + axis + str(dist) + ' F' + str(speed))

    def quit_jog(self):
        self.s.write_realtime('\x85', altDisplayText = 'Quit jog')

    def cooldown_zUp_and_spindle_on(self):
        self.turn_off_vacuum()
        self.turn_on_spindle(self.spindle_cooldown_rpm)
        self.raise_z_axis_for_collet_access()

    def laser_on(self):
        if self.is_laser_enabled:

            if self.hw_can_operate_laser_commands():
                self.s.write_command('AZ')
            self.set_led_colour('BLUE')

            self.is_laser_on = True

    def laser_off(self, bootup=False):
        self.is_laser_on = False
        if self.hw_can_operate_laser_commands():
            self.s.write_command('AX')
        if bootup:
            self.set_led_colour('YELLOW')
        else:
            self.set_led_colour('GREEN')

    def toggle_spindle_off_overide(self, dt):
        self.s.write_realtime('\x9e', altDisplayText = 'Spindle stop override')

    def go_to_jobstart_xy(self):
        self.s.write_command('G0 G53 Z-' + str(self.limit_switch_safety_distance))
        self.s.write_command('G4 P0.1')
        self.s.write_command('G0 G54 X0 Y0')

    def go_to_standby(self):
        self.s.write_command('G0 G53 Z-' + str(self.limit_switch_safety_distance))
        self.s.write_command('G4 P0.1')
        self.s.write_command('G28')

    def go_to_jobstart_z(self):
        self.s.write_command('G0 G54 Z0')

    def turn_on_vacuum(self):
        """
        Turns the vacuum on by sending the 'AE' command.
        :return: None
        """
        self.s.write_command("AE")

    def turn_off_vacuum(self):
        """
        Turns the vacuum off by sending the 'AF' command.
        :return: None
        """
        self.s.write_command("AF")

    def go_x_datum(self):
        self.s.write_command('G0 G53 Z-' + str(self.limit_switch_safety_distance))
        self.s.write_command('G4 P0.1')
        self.s.write_command('G0 G54 X0')

    def go_y_datum(self):
        self.s.write_command('G0 G53 Z-' + str(self.limit_switch_safety_distance))
        self.s.write_command('G4 P0.1')
        self.s.write_command('G0 G54 Y0')

    def go_xy_datum(self):
        self.s.write_command('G0 G53 Z-' + str(self.limit_switch_safety_distance))
        self.s.write_command('G4 P0.1')
        self.s.write_command('G0 G54 X0 Y0')

    def go_xy_datum_with_laser(self):
        self.s.write_command('G0 G53 Z-' + str(self.limit_switch_safety_distance))
        self.s.write_command('G4 P0.1')
        self.s.write_command('G0 G54 X{} Y{}'.format(-self.laser_offset_x_value, -self.laser_offset_y_value))

    def jog_spindle_to_laser_datum(self, axis):

        if 'X' in axis:

            # Keep this is for beta testing, as 
            Logger.debug("Laser offset value: " + str(self.laser_offset_x_value))
            Logger.debug("Pos value: " + str(self.s.m_x))

            Logger.debug("Try to move to: " + str(self.s.m_x + float(self.laser_offset_x_value)))
            Logger.debug("Limit at: " + str(float(self.x_min_jog_abs_limit)))

            # Check that movement is within bounds before jogging
            if (self.s.m_x + float(self.laser_offset_x_value) <= float(self.x_max_jog_abs_limit)
            and self.s.m_x + float(self.laser_offset_x_value) >= float(self.x_min_jog_abs_limit)):

                self.jog_relative('X', self.laser_offset_x_value, 6000.0)

            else: return False

        if 'Y' in axis:
            # Check that movement is within bounds before jogging
            if (self.s.m_y + float(self.laser_offset_y_value) <= float(self.y_max_jog_abs_limit)
            and self.s.m_y + float(self.laser_offset_y_value) >= float(self.y_min_jog_abs_limit)):

                self.jog_relative('Y', self.laser_offset_y_value, 6000.0)

            else: return False

        return True

    # Realtime XYZ feed adjustment
    def feed_override_reset(self):
        self.s.write_realtime('\x90', altDisplayText = 'Feed override RESET')

    def feed_override_up_10(self, final_percentage=''):
        self.s.write_realtime('\x91', altDisplayText='Feed override UP ' + str(final_percentage))

    def feed_override_down_10(self, final_percentage=''):
        self.s.write_realtime('\x92', altDisplayText='Feed override DOWN ' + str(final_percentage))

    def feed_override_up_1(self, final_percentage=''):
        self.s.write_realtime('\x93', altDisplayText='Feed override UP ' + str(final_percentage))

    def feed_override_down_1(self, final_percentage=''):
        self.s.write_realtime('\x94', altDisplayText='Feed override DOWN ' + str(final_percentage))

    # Realtime spindle speed adjustment
    def speed_override_reset(self):
        self.s.write_realtime('\x99', altDisplayText = 'Speed override RESET')

    def speed_override_up_1(self, final_percentage=''):
        self.s.write_realtime('\x9C', altDisplayText='Speed override UP ' + str(final_percentage))

    def speed_override_down_1(self, final_percentage=''):
        self.s.write_realtime('\x9D', altDisplayText='Speed override DOWN ' + str(final_percentage))

    def speed_override_up_10(self, final_percentage=''):
        self.s.write_realtime('\x9A', altDisplayText='Speed override UP ' + str(final_percentage))

    def speed_override_down_10(self, final_percentage=''):
        self.s.write_realtime('\x9B', altDisplayText='Speed override DOWN ' + str(final_percentage))


# HOMING

    """
    These functions control all stages covered by the homing sequence. 
    All of the "component" functions are independent of one another, and can be called as stand-alone commands
    that do not link into any other functions. 

    Component functions are called by specific sequencing functions that are set up to run through the list of 
    component functions. 

    To change the homing function sequence, you must update: 

    auto_squaring_idx (only needs to be changed if the index for auto-squaring is changed)
    homing_seq_first_delay (list of delays between functions)
    homing_funcs_list (ordered list of functions in sequence)

    """

    # ensure that return and cancel args match the names of the screen names defined in the screen manager
    # this calls the first screen in the homing sequence
    def request_homing_procedure(self, return_to_screen_str, cancel_to_screen_str):
        self.sm.get_screen('squaring_decision').return_to_screen = return_to_screen_str
        self.sm.get_screen('squaring_decision').cancel_to_screen = cancel_to_screen_str
        self.sm.current = 'squaring_decision'

    homing_initial_delay_after_reset = 0.5

    # Call this function for whole sequence
    def do_standard_homing_sequence(self):
        self.homing_interrupted = False
        self.homing_in_progress = True
        Logger.info("Start homing sequence")
        self.reset_homing_sequence_flags()
        self.reset_pre_homing()
        self.setup_homing_funcs_list()
        self.schedule_homing_event(self.next_homing_task_wrapper, self.homing_initial_delay_after_reset)
        self.schedule_homing_event(self.do_next_task_in_sequence, self.homing_initial_delay_after_reset + 0.1)
        self.schedule_homing_event(self.complete_homing_task, self.homing_initial_delay_after_reset + 0.2)

    # check this function from screens to determine whether auto-squaring is happening
    def i_am_auto_squaring(self):

        if self.homing_task_idx != self.auto_squaring_idx:
            return False

        if not self.s.is_sequential_streaming:
            return False

        if len(self.s._sequential_stream_buffer) < 2:
            return False

        return True

    # components of homing sequence
    def start_homing(self, dt=0):
        Logger.info("Start GRBL Homing")
        self.set_state('Home')
        self.s.start_sequential_stream(['$H'])

    def start_auto_squaring(self, dt=0):
        '''
        This function is designed to square the machine's X&Y axes
        It does this by killing the limit switches and driving the X frame into mechanical deadstops at the end of the Y axis.
        The steppers will stall out, but the X frame will square against the mechanical deadstops.
        Intended use is first home after power-up only.
        We're waiting for grbl responses before we send each line, as we're editing GRBL dollar settings
        Delays after $ settings will be auto-inserted by serial connection module
        '''
        if not self.is_squaring_XY_needed_after_homing:
            Logger.info("Skip auto squaring")
            return

        Logger.info("Start auto squaring")

        square_homing_sequence =  [
                                  '$20=0', # soft limits off
                                  '$21=0', # hard limits off
                                  'G53 G0 X-400', # position zHead to put CoG of X beam on the mid plane (mX: -400)
                                  'G91', # relative coords
                                  'G1 Y-28 F700', # drive lower frame into legs, assumes it's starting from a 3mm pull off
                                  'G1 Y28', # re-enter work area
                                  'G90', # abs coords
                                  'G53 G0 X-1285', # position zHead to put CoG of X beam on the mid plane (mX: -400)
                                  'G4 P0.5', # delay, which is needed solely for it's "blocking ok" response
                                  '$21=1', # soft limits on
                                  '$20=1', # hard limits on
                                  'G4 P0.5', # delay, which is needed solely for it's "blocking ok" response
                                  '$H'
                                  ]
        self.s.start_sequential_stream(square_homing_sequence, reset_grbl_after_stream=True)

    def query_grbl_settings_modes_and_info(self, dt=0):
        query_grbl_list_to_stream = [
                    '$$', # Echo grbl settings, which will be read by sw, and internal parameters sync'd
                    '$#', # Echo grbl modes, which will be read by sw, and internal parameters sync'd
                    '$I' # Echo grbl version info, which will be read by sw, and internal parameters sync'd
                    ]
        self.s.start_sequential_stream(query_grbl_list_to_stream)

    def move_to_accommodate_laser_offset(self, dt=0):
        if not self.is_laser_enabled: return
        Logger.info("Move to laser offset")
        self.jog_absolute_single_axis('X', float(self.x_min_jog_abs_limit) + 5 - self.laser_offset_x_value, 3000)

    # final component is always complete homing sequence
    def complete_homing_sequence(self, dt=0):
        self.set_led_colour("GREEN")
        self.reset_homing_sequence_flags()
        self.is_machine_completed_the_initial_squaring_decision = True
        self.is_machine_homed = True
        self.homing_interrupted = False
        self.homing_in_progress = False
        Logger.info("Complete homing sequence")

        if self.model_manager.is_machine_drywall():
            self.cs.drywall_tec_laser_position.move_to_dwl(dwl_x=0, dwl_y=0)
            Logger.info("Moving laser to machine's 0, 0")

    # sequence control variables and functions
    homing_in_progress = False
    homing_interrupted = False
    homing_task_idx = 0
    completed_homing_tasks = []
    homing_seq_events = []
    homing_funcs_list = []
    auto_squaring_idx = 2

    # these are the initial delay in the clock scheduling between the event that's just completed
    # and the event that will be called next - mostly used for protocol commands
    homing_seq_first_delay = [
        0,    # 0: null
        0,    # 1: start_homing - disable_stall_detection_before_auto_squaring
        0.1,  # 2: disable_stall_detection_before_auto_squaring - start_auto_squaring
        0,    # 3: start_auto_squaring - query_grbl_settings_modes_and_info
        0,    # 4: query_grbl_settings_modes_and_info - start_calibrating_after_homing
        0,    # 5: start_calibrating_after_homing - enable_stall_detection_after_calibrating
        0.1,  # 6: enable_stall_detection_after_calibrating - move_to_accommodate_laser_offset
        0,    # 7: move_to_accommodate_laser_offset - raise_z_axis_for_collet_access
        0,    # 8: raise_z_axis_for_collet_access - complete_homing_sequence
    ]

    def setup_homing_funcs_list(self):

        self.homing_funcs_list = [

            self.start_homing,                                  # 0
            self.disable_stall_detection,                       # 1
            self.start_auto_squaring,                           # 2
            self.query_grbl_settings_modes_and_info,            # 3
            self.calibrate_all_three_axes,                      # 4
            self.enable_stall_detection,                        # 5
            self.move_to_accommodate_laser_offset,              # 6
            self.raise_z_axis_for_collet_access,                # 7
            self.complete_homing_sequence                       # 8

            ]

        self.completed_homing_tasks = [False]*(len(self.homing_funcs_list)-1)

    def schedule_homing_event(self, func, delay=0.2):
        self.homing_seq_events = [x for x in self.homing_seq_events if func != x.get_callback()]
        self.homing_seq_events.append(Clock.schedule_once(func, delay))

    def reschedule_homing_task_if_busy(self, func, delay=0.2):

        if self.state().startswith("Alarm") or self.state().startswith("Door"):
            self.cancel_homing_sequence()
            Logger.info("Cancel homing from router_machine due to: " + self.state())
            return True

        if self.smartbench_is_busy() or self.run_calibration:
            self.schedule_homing_event(func, delay)
            return True

    def unschedule_homing_events(self):
        for event in self.homing_seq_events:
            if event: event.cancel()

        del self.homing_seq_events[:]

    ## use flags to track progress through sequence
    def reset_homing_sequence_flags(self):
        self.unschedule_homing_events()
        self.completed_homing_tasks = []
        self.homing_task_idx = 0
        self.homing_funcs_list = []

    ## handle all events in homing sequence
    def complete_homing_task(self, dt=0):
        if self.reschedule_homing_task_if_busy(self.complete_homing_task): return
        self.set_current_homing_task_complete()

    def if_last_task_complete(self):
        if self.get_current_homing_task_complete():
            self.homing_task_idx+=1
            return True

    def do_next_task_in_sequence(self, dt=0):
        if self.if_last_task_complete():
            self.schedule_homing_event(self.next_homing_task_wrapper, self.homing_seq_first_delay[self.homing_task_idx])
            if not self.homing_task_idx: return
            self.schedule_homing_event(self.complete_homing_task, self.homing_seq_first_delay[self.homing_task_idx])

        self.schedule_homing_event(self.do_next_task_in_sequence)

    def next_homing_task_wrapper(self, dt=0):
        if self.reschedule_homing_task_if_busy(self.next_homing_task_wrapper): return
        self.homing_funcs_list[self.homing_task_idx]()

    def set_current_homing_task_complete(self):
        try: self.completed_homing_tasks[self.homing_task_idx] = True
        except:
            Logger.exception("Could not set completed homing task")

    def get_current_homing_task_complete(self):
        try: return self.completed_homing_tasks[self.homing_task_idx]
        except:
            Logger.exception("Could not get completed homing task")
            return False

    def cancel_homing_sequence(self):
        self.reset_on_cancel_homing()
        self.reset_homing_sequence_flags()
        self.homing_interrupted = True
        self.reset_on_cancel_homing()
        if self.run_calibration: self.cancel_triple_axes_calibration() # If mid calibration, want to do a hard PCB reset
        self.is_machine_homed = False
        self.set_led_colour("YELLOW")
        self.homing_in_progress = False
        Logger.info("Cancel homing sequence")


# Z PROBE

    # Home the Z axis by moving the cutter down until it touches the probe.
    # On touching, electrical contact is made, detected, and WPos Z0 set, factoring in probe plate thickness.
    def probe_z(self, fast_probe=False):

        if self.state() == 'Idle':
            self.set_led_colour("WHITE")
            self.s.expecting_probe_result = True
            probe_z_target =  -(self.grbl_z_max_travel) - self.s.m_z + 0.1 # 0.1 added to prevent rounding error triggering soft limit
            probe_speed = self.z_probe_speed_fast if fast_probe else self.z_probe_speed
            self.fast_probing = fast_probe
            fast_travel_distance = 60  # mm to go fast and not probing yet
            min_probing_distance = 30  # have at least 30mm safety margin for probing
            if fast_probe and abs(probe_z_target) > fast_travel_distance + min_probing_distance:
                self.s.write_command('G0 G53 Z-' + str(fast_travel_distance))
                probe_z_target += fast_travel_distance # adjust max travel for the 60mm traveled in G0
            self.s.write_command('G91 G38.2 Z' + str(probe_z_target) + ' F' + str(probe_speed))
            self.s.write_command('G90')
            # Serial module then looks for probe detection
            # On detection "probe_z_detection_event" is called (for a single immediate EEPROM write command)....
            # ... followed by a delayed call to "probe_z_post_operation" for any post-write actions.


    probe_z_coord = NumericProperty()

    def probe_z_detection_event(self, z_machine_coord_when_probed):
        """
        This function is called by the serial module when the probe detection is detected.
        :param z_machine_coord_when_probed: the machine's Z coordinate when the probe is detected
        :return: None
        """
        self.probe_z_coord = z_machine_coord_when_probed
        self.s.write_command('G90 G1 G53 Z' + z_machine_coord_when_probed)
        self.s.write_command('G4 P0.5')
        self.s.write_command('G10 L20 P1 Z' + str(self.z_touch_plate_thickness))
        self.s.write_command('G4 P0.5')
        Clock.schedule_once(lambda dt: self.strobe_led_playlist("datum_has_been_set"), 0.5)

        if self.fast_probing:
            self.jog_relative('Z', 5, 750)
            self.fast_probing = False
        else:
            # Ensure that it doesn't go down to -5 if the probe was detected higher than that
            if float(z_machine_coord_when_probed) < self.Z_AXIS_ACCESSIBLE_ABS_HEIGHT:
                self.raise_z_axis_for_collet_access()
            else:
                # Raise z axis by 1mm to ensure it's clear of the probe plate
                self.raise_z_axis_to_safe_height_after_probing()

    # LIGHTING

    led_colour_status = "none"

    def set_led_colour(self, colour_name):

        # NEVER SEND MID-JOB. Chars defining RGB will fill up the serial buffer unless handled somehow
        if not self.s.is_job_streaming and not self.s.is_sequential_streaming:

            self.led_colour_status = colour_name

            if colour_name == 'RED':        self.s.write_command("*LFF0000")
            elif (colour_name == 'GREEN'and self.is_machine_homed):    self.s.write_command("*L11FF00")
            elif (colour_name == 'GREEN'and not self.is_machine_homed):    self.s.write_command("*LFFFF00")
            elif colour_name == 'BLUE':     self.s.write_command("*L1100FF")
            elif colour_name == 'WHITE':    self.s.write_command("*LFFFFFF")
            elif colour_name == 'YELLOW':   self.s.write_command("*LFFFF00")
            elif colour_name == 'ORANGE':   self.s.write_command("*LFF8000")
            elif colour_name == 'MAGENTA':  self.s.write_command("*LFF00FF")
            elif colour_name == 'OFF':      self.s.write_command("*L110000")

        else: Logger.warning("LED Colour denied because streaming: " + colour_name + "\n")


    def led_restore(self):
        # this is special
        # A: It's a realtime command which can be useful when streaming, or grbl is suspended
        # B: It's exception is a bug - when the machine is in suspended DOOR mode, triggered from a hard switch:
        # Send the command at this point means that the flashing will freeze
        # This can be unfrozen by sending any normal led command (assuming that the grbl has been released from suspension ie. with a RESUME)
        self.s.write_realtime('&', altDisplayText = 'LED restore')



    def strobe_led_playlist(self, situation):

        # Can be used to generate all manners of temporary lighting effects. Well most of them anyway.

        if situation == "datum_has_been_set":
            strobe_colour1 = 'GREEN'
            strobe_colour2 = 'GREEN'
            colour_1_period = 0.5
            colour_2_period = 0.5
            cycles = 1
            end_on_colour = self.led_colour_status
            self._strobe_loop(strobe_colour1, strobe_colour2, colour_1_period, colour_2_period, cycles, end_on_colour)

        elif situation == "standby_pos_has_been_set":
            strobe_colour1 = 'MAGENTA'
            strobe_colour2 = 'MAGENTA'
            colour_1_period = 0.5
            colour_2_period = 0.5
            cycles = 1
            end_on_colour = self.led_colour_status
            self._strobe_loop(strobe_colour1, strobe_colour2, colour_1_period, colour_2_period, cycles, end_on_colour)

        elif situation == "green_pulse":
            strobe_colour1 = 'GREEN'
            strobe_colour2 = 'OFF'
            colour_1_period = 0.2
            colour_2_period = 0.2
            cycles = 3
            end_on_colour = self.led_colour_status
            self._strobe_loop(strobe_colour1, strobe_colour2, colour_1_period, colour_2_period, cycles, end_on_colour)

        else: Logger.warning("Strobe situation: " + situation + " not recognised")

    strobe_cycle_count = 0

    def _strobe_loop(self, strobe_colour1, strobe_colour2, colour_1_period, colour_2_period, cycles, end_on_colour):
        self.set_led_colour(strobe_colour1)
        Clock.schedule_once(lambda dt: self.set_led_colour(strobe_colour2), colour_1_period)
        self.strobe_cycle_count += 1
        if self.strobe_cycle_count < cycles:
            Clock.schedule_once(lambda dt: self._strobe_loop(strobe_colour1, strobe_colour2, colour_1_period, colour_2_period, cycles, end_on_colour), colour_1_period + colour_2_period)
        else:
            self.strobe_cycle_count = 0
            Clock.schedule_once(lambda dt: self.set_led_colour(end_on_colour), colour_1_period + colour_2_period)

    # LED DISCO inferno

    rainbow_delay = 0.03
    led_rainbow_ending_green = [
        'B0','G0','R0','R1','R2','R3','R4','R5','R6','R7','R8','R9','R8','R7','R6','R5','R4','R3','R2','R1','R0',
        # 'B1','B2','B3','B4','B5','B6','B7','B8','B9','B8','B7','B6','B5','B4','B3','B2','B1','B0'
        'G1','G2','G3','G4','G5','G6','G7','G8','G9'
        ]


    rainbow_cycle_count = 0
    rainbow_cycle_limit = len(led_rainbow_ending_green)

    def run_led_rainbow_ending_green(self):

        if self.state().startswith('Idle'):

            self.set_rainbow_cycle_led(self.led_rainbow_ending_green[self.rainbow_cycle_count])
            self.rainbow_cycle_count += 1

            if self.rainbow_cycle_count < self.rainbow_cycle_limit:
                Clock.schedule_once(lambda dt: self.run_led_rainbow_ending_green(), self.rainbow_delay)
            else:
                self.rainbow_cycle_count = 0 # reset for next rainbow call

    def set_rainbow_cycle_led(self, command):
        self.s.write_command('AL' + command, show_in_sys=False, show_in_console=False)


    # PRINT REGISTERS Logger.info("0x{:08X}".format(
    def print_tmc_registers(self, motor_idx):

        TMC_registers_report_string = (
        "-------------------------------------" + "\n" + \
        "MOTOR ID: " + str(motor_idx) + "\n" + \
        "Driver Control Reg: " + "0x{:08X}".format(self.TMC_motor[int(motor_idx)].shadowRegisters[0]) + "\n" + \
        "Chopper Config Reg: " + "0x{:08X}".format(self.TMC_motor[int(motor_idx)].shadowRegisters[1]) + "\n" + \
        "CoolStep Config Reg: " + "0x{:08X}".format(self.TMC_motor[int(motor_idx)].shadowRegisters[2]) + "\n" + \
        "Stall Guard Config Reg: " + "0x{:08X}".format(self.TMC_motor[int(motor_idx)].shadowRegisters[3]) + "\n" + \
        "Driver Config Reg: " + "0x{:08X}".format(self.TMC_motor[int(motor_idx)].shadowRegisters[4]) + "\n" + \
        "Active Current Scale: " + str(self.TMC_motor[int(motor_idx)].ActiveCurrentScale) + "\n" + \
        "Idle Current Scale: " + str(self.TMC_motor[int(motor_idx)].standStillCurrentScale) + "\n" + \
        "Stall Guard Threshold: " + str(self.TMC_motor[int(motor_idx)].stallGuardAlarmThreshold) + "\n" + \
        "Max Stall Guard Step: " + str(self.TMC_motor[int(motor_idx)].max_step_period_us_SG) + "\n" + \
        "Thermal Coefficient: " + str(self.TMC_motor[int(motor_idx)].temperatureCoefficient) + "\n" + \
        "-------------------------------------"
        )

        map(Logger.info, TMC_registers_report_string.split("\n"))

    #####################################################################
    # PROTOCOL MOTOR FUNCTIONS - USE THIS TO SEND ANY MOTOR COMMANDS
    #####################################################################

    def send_command_to_motor(self, altDisplayText, motor=TMC_X1, command=SET_ACTIVE_CURRENT, value=0, printlog=True):

        len = 999;

        # global commands:
        if command == SET_SG_ALARM          :   cmd = command;      len = TMC_GBL_CMD_LENGTH;       val = value
        if command == SET_CALIBR_MODE       :   cmd = command;      len = TMC_GBL_CMD_LENGTH;       val = value
        if command == RESTORE_TMC_DEFAULTS  :   cmd = command;      len = TMC_GBL_CMD_LENGTH;       val = 0
        if command == STORE_TMC_PARAMS      :   cmd = command;      len = TMC_GBL_CMD_LENGTH;       val = 0
        if command == GET_REGISTERS         :   cmd = command;      len = TMC_GBL_CMD_LENGTH;       val = 0
        if command == WDT_TMC_TEST          :   cmd = command;      len = TMC_GBL_CMD_LENGTH;       val = value
        if command == REPORT_STALLS         :   cmd = command;      len = TMC_GBL_CMD_LENGTH;       val = 0
        if command == UPLOAD_CALIBR_VALUE   :   cmd = command;      len = TMC_REG_CMD_LENGTH;       val = value
        if command == REPORT_RAW_SG         :   cmd = command;      len = TMC_GBL_CMD_LENGTH;       val = value



        # individual motor commands
        if command == SET_IDLE_CURRENT:         cmd = command;      len = TMC_GBL_CMD_LENGTH;       val = value
        if command == SET_ACTIVE_CURRENT:       cmd = command;      len = TMC_GBL_CMD_LENGTH;       val = value; val = self.setShadowReg(motor, SGCSCONF, value, CS_MASK     , CS_SHIFT          )
        if command == SET_MOTOR_ENERGIZED:      cmd = command;      len = TMC_GBL_CMD_LENGTH;       val = value
        if command == SET_SG_ALARM_TRSHLD:      cmd = command;      len = TMC_REG_CMD_LENGTH;       val = value; self.TMC_motor[motor].stallGuardAlarmThreshold   = value # 4 bytes value
        if command == SET_THERMAL_COEFF:        cmd = command;      len = TMC_REG_CMD_LENGTH;       val = value; self.TMC_motor[motor].temperatureCoefficient     = value # 4 bytes value
        if command == SET_MAX_SG_STEP_US:       cmd = command;      len = TMC_REG_CMD_LENGTH;       val = value; self.TMC_motor[motor].max_step_period_us_SG      = value # 4 bytes value


        # DRVCTRL register
        if command == SET_MRES      : len = TMC_REG_CMD_LENGTH; cmd = SET_DRVCTRL; val = self.setShadowReg(motor, DRVCTRL, value, MRES_MASK     , MRES_SHIFT        )
        if command == SET_DEDGE     : len = TMC_REG_CMD_LENGTH; cmd = SET_DRVCTRL; val = self.setShadowReg(motor, DRVCTRL, value, DEDGE_MASK    , DEDGE_SHIFT       )
        if command == SET_INTERPOL  : len = TMC_REG_CMD_LENGTH; cmd = SET_DRVCTRL; val = self.setShadowReg(motor, DRVCTRL, value, INTERPOL_MASK , INTERPOL_SHIFT    )
        if command == SET_CACB      : len = TMC_REG_CMD_LENGTH; cmd = SET_DRVCTRL; val = value

        # CHOPCONF register
        if command == SET_TOFF      : len = TMC_REG_CMD_LENGTH; cmd = SET_CHOPCONF; val = self.setShadowReg(motor, CHOPCONF, value, TOFF_MASK   , TOFF_SHIFT        )
        if command == SET_HSTRT     : len = TMC_REG_CMD_LENGTH; cmd = SET_CHOPCONF; val = self.setShadowReg(motor, CHOPCONF, value, HSTRT_MASK  , HSTRT_SHIFT       )
        if command == SET_HEND      : len = TMC_REG_CMD_LENGTH; cmd = SET_CHOPCONF; val = self.setShadowReg(motor, CHOPCONF, value, HEND_MASK   , HEND_SHIFT        )
        if command == SET_HDEC      : len = TMC_REG_CMD_LENGTH; cmd = SET_CHOPCONF; val = self.setShadowReg(motor, CHOPCONF, value, HDEC_MASK   , HDEC_SHIFT        )
        if command == SET_RNDTF     : len = TMC_REG_CMD_LENGTH; cmd = SET_CHOPCONF; val = self.setShadowReg(motor, CHOPCONF, value, RNDTF_MASK  , RNDTF_SHIFT       )
        if command == SET_CHM       : len = TMC_REG_CMD_LENGTH; cmd = SET_CHOPCONF; val = self.setShadowReg(motor, CHOPCONF, value, CHM_MASK    , CHM_SHIFT         )
        if command == SET_TBL       : len = TMC_REG_CMD_LENGTH; cmd = SET_CHOPCONF; val = self.setShadowReg(motor, CHOPCONF, value, TBL_MASK    , TBL_SHIFT         )

        # SMARTEN register
        if command == SET_SEMIN     : len = TMC_REG_CMD_LENGTH; cmd = SET_SMARTEN; val = self.setShadowReg(motor, SMARTEN, value, SEMIN_MASK    , SEMIN_SHIFT       )
        if command == SET_SEUP      : len = TMC_REG_CMD_LENGTH; cmd = SET_SMARTEN; val = self.setShadowReg(motor, SMARTEN, value, SEUP_MASK     , SEUP_SHIFT        )
        if command == SET_SEMAX     : len = TMC_REG_CMD_LENGTH; cmd = SET_SMARTEN; val = self.setShadowReg(motor, SMARTEN, value, SEMAX_MASK    , SEMAX_SHIFT       )
        if command == SET_SEDN      : len = TMC_REG_CMD_LENGTH; cmd = SET_SMARTEN; val = self.setShadowReg(motor, SMARTEN, value, SEDN_MASK     , SEDN_SHIFT        )
        if command == SET_SEIMIN    : len = TMC_REG_CMD_LENGTH; cmd = SET_SMARTEN; val = self.setShadowReg(motor, SMARTEN, value, SEIMIN_MASK   , SEIMIN_SHIFT      )

        # SGCSCONF register
        #if command == SET_CS        : len = TMC_REG_CMD_LENGTH; cmd = SET_SGCSCONF; val = self.setShadowReg(motor, SGCSCONF, value, CS_MASK     , CS_SHIFT          )
        if command == SET_SGT       : len = TMC_REG_CMD_LENGTH; cmd = SET_SGCSCONF; val = self.setShadowReg(motor, SGCSCONF, value, SGT_MASK    , SGT_SHIFT         )
        if command == SET_SFILT     : len = TMC_REG_CMD_LENGTH; cmd = SET_SGCSCONF; val = self.setShadowReg(motor, SGCSCONF, value, SFILT_MASK  , SFILT_SHIFT       )

        # DRVCONF register                                                                                                                                          
        if command == SET_RDSEL      : len = TMC_REG_CMD_LENGTH; cmd = SET_DRVCONF; val = self.setShadowReg(motor, DRVCONF, value, RDSEL_MASK   , RDSEL_SHIFT       )
        if command == SET_VSENSE     : len = TMC_REG_CMD_LENGTH; cmd = SET_DRVCONF; val = self.setShadowReg(motor, DRVCONF, value, VSENSE_MASK  , VSENSE_SHIFT      )
        if command == SET_SDOFF      : len = TMC_REG_CMD_LENGTH; cmd = SET_DRVCONF; val = self.setShadowReg(motor, DRVCONF, value, SDOFF_MASK   , SDOFF_SHIFT       )
        if command == SET_TS2G       : len = TMC_REG_CMD_LENGTH; cmd = SET_DRVCONF; val = self.setShadowReg(motor, DRVCONF, value, TS2G_MASK    , TS2G_SHIFT        )
        if command == SET_DISS2G     : len = TMC_REG_CMD_LENGTH; cmd = SET_DRVCONF; val = self.setShadowReg(motor, DRVCONF, value, DISS2G_MASK  , DISS2G_SHIFT      )
        if command == SET_SLPL       : len = TMC_REG_CMD_LENGTH; cmd = SET_DRVCONF; val = self.setShadowReg(motor, DRVCONF, value, SLPL_MASK    , SLPL_SHIFT        )
        if command == SET_SLPH       : len = TMC_REG_CMD_LENGTH; cmd = SET_DRVCONF; val = self.setShadowReg(motor, DRVCONF, value, SLPH_MASK    , SLPH_SHIFT        )
        if (command == SET_SLPL or command == SET_SLPH):                            val = self.setShadowReg(motor, DRVCONF, value > 3, SLP2_MASK, SLP2_SHIFT        ) # hadle slope control MSB:
        if command == SET_TST        : len = TMC_REG_CMD_LENGTH; cmd = SET_DRVCONF; val = self.setShadowReg(motor, DRVCONF, value, TST_MASK     , TST_SHIFT         )
        if command == SET_SDOFF      : len = TMC_REG_CMD_LENGTH; cmd = SET_DRVCONF; val = self.setShadowReg(motor, DRVCONF, value, SDOFF_MASK   , SDOFF_SHIFT       )


        if len < 999:
            if cmd < (MOTOR_OFFSET+1)*TOTAL_TMCS:
                cmd = cmd + motor * MOTOR_OFFSET # if individual command shift it by the motor index

            out = self.s.write_protocol(self.p.constructTMCcommand(cmd, val, len), altDisplayText)

            if printlog:
                Logger.info("Sending command to motor: " + str(motor) + ", cmd: " + str(cmd) + ", val: " + hex(val))

        else:
            # throw an error, command is not valid
            Logger.error("ERROR: unknown command in send_command_to_motor: " + str(motor) + ", cmd: " + str(command) + ", val: " + hex(value))

        return out

    def setShadowReg(self, motor, register, value, mask, shift):
        self.TMC_motor[motor].shadowRegisters[register] = self.TMC_motor[motor].shadowRegisters[register] & ~ (           mask   << shift) #clear
        self.TMC_motor[motor].shadowRegisters[register] = self.TMC_motor[motor].shadowRegisters[register] |   ( ( value & mask ) << shift) #set
        return self.TMC_motor[motor].shadowRegisters[register]

    #####################################################################
    # CALIBRATION AND TUNING PROCEDURES
    #####################################################################

    # IT IS ASSUMED THAT FUNCTIONS THAT TUNE/CALIBRATE JUST X AND Z OR JUST Y ARE FOR FREE MOTORS IN SPACE
    # IT IS ASSUMED THAT FUNCTIONS THAT TUNE/CALIBRATE ALL THREE AXIS ARE DOING IT ON AN ASSEMBLED MACHINE, WITH ENGAGED MOTORS

    # CALL THESE FROM MAIN APP

    calibration_tuning_fail_info = ''

    # QUERY THIS FLAG AFTER CALLING TUNING FUNCTIONS, TO SEE IF TUNING HAS FINISHED
    tuning_in_progress = False

    def tune_X_and_Z_for_calibration(self):

        self.tuning_in_progress = True
        Logger.info("Tuning X and Z...")
        self.prepare_for_tuning()
        # THEN JOG AWAY AT MAX SPEED
        Logger.info("Jog to check SG values")
        self.tuning_jog_forwards_fast(X = True, Y = False, Z = True)
        self.check_SGs_rezero_and_go_to_next_checks_then_tune(X = True, Y = False, Z = True)

    def tune_Y_for_calibration(self):

        self.tuning_in_progress = True
        Logger.info("Tuning Y...")
        self.prepare_for_tuning()
        # THEN JOG AWAY AT MAX SPEED
        Logger.info("Jog to check SG values")
        self.tuning_jog_forwards_fast(X = False, Y = True, Z = False)
        self.check_SGs_rezero_and_go_to_next_checks_then_tune(X = False, Y = True, Z = False)

    def tune_X_Y_Z_for_calibration(self):

        self.tuning_in_progress = True
        Logger.info("Tuning X Y and Z...")
        self.prepare_for_tuning()
        # THEN JOG AWAY AT MAX SPEED
        Logger.info("Jog to check SG values")
        self.tuning_jog_forwards_fast(X = True, Y = True, Z = True)
        self.check_SGs_rezero_and_go_to_next_checks_then_tune(X = True, Y = True, Z = True)

    # QUERY THIS FLAG AFTER CALLING CALIBRATION FUNCTIONS, TO SEE IF CALIBRATION HAS FINISHED
    run_calibration = False

    def calibrate_all_three_axes(self):

        if  self.is_machines_fw_version_equal_to_or_greater_than_version('2.6.0', 'triple axis calibration') and self.sing() and \
            self.get_dollar_setting(53):
            self.run_calibration = True
            Logger.info("Calibrating all axes together...")
            self.prep_triple_axes_calibration()
            return True

    def calibrate_X(self, zero_position=True, mod_soft_limits=True, fast=False):

        self.run_calibration = True
        Logger.info("Calibrating X...")
        self.initialise_calibration(X = True, Y = False, Z = False, zero_position=zero_position, mod_soft_limits=mod_soft_limits, quick_calibration=fast)

    def calibrate_Y(self, zero_position=True, mod_soft_limits=True, fast=False):

        self.run_calibration = True
        Logger.info("Calibrating Y...")
        self.initialise_calibration(X = False, Y = True, Z = False, zero_position=zero_position, mod_soft_limits=mod_soft_limits, quick_calibration=fast)

    def calibrate_Z(self, zero_position=True, mod_soft_limits=True, fast=False):

        self.run_calibration = True
        Logger.info("Calibrating Z...")
        self.initialise_calibration(X = False, Y = False, Z = True, zero_position=zero_position, mod_soft_limits=mod_soft_limits, quick_calibration=fast)

    def calibrate_X_and_Z(self, zero_position=True, mod_soft_limits=True, fast=False):

        self.run_calibration = True
        Logger.info("Calibrating X and Z...")
        self.initialise_calibration(X = True, Y = False, Z = True, zero_position=zero_position, mod_soft_limits=mod_soft_limits, quick_calibration=fast)

    def calibrate_X_Y_and_Z(self, zero_position=True, mod_soft_limits=True, fast=False):

        self.run_calibration = True
        Logger.info("Calibrating X, Y, and Z...")
        self.initialise_calibration(X = True, Y = True, Z = True, zero_position=zero_position, mod_soft_limits=mod_soft_limits, quick_calibration=fast)

    # MEAT OF TUNING - DON'T CALL FROM MAIN APP

    # Zero position
    # Enable raw SG reporting: command REPORT_RAW_SG
    # Check that machine is reporting sensible temperatures
    # Check that machine is Idle
    # Start long jogging in the axis of interest at 300mm/min for X and Y or for 30mm/min for Z
    # Sweep TOFF in the range 2-10
    # Sweep SGT in the range 0-20
    # For each TOFF/SGT combination read SG 15 times (every 100ms, usual status report rate), skip the first 7 points as they are settling points and not valid. Average the remaining 8 points. 
    # Adjust target SG based on temperature (example)
    # Find the TOFF/SGT combination which gives the SG reading nearest to target SG (500 in this case)
    # Apply found TOFF and SGT values to the motor: commands SET_CHOPCONF and SET_SGCSCONF
    # Store the motors settings in the EEPROM: command STORE_TMC_PARAMS 
    # Disable raw SG reporting: command REPORT_RAW_SG


    toff_and_sgt_found = False
    tuning_poll = None
    x_toff_tuned = None
    x_sgt_tuned = None
    y1_toff_tuned = None
    y1_sgt_tuned = None
    y2_toff_tuned = None
    y2_sgt_tuned = None
    z_toff_tuned = None
    z_sgt_tuned = None

    temp_sg_array = []

    time_to_check_for_tuning_prep = 0

    toff_min = 4 # 2
    sgt_min = 0 # 0

    toff_max = 10 # 10
    sgt_max = 20 # 20

    temp_toff = toff_min
    temp_sgt = sgt_min

    reference_temp = 45.0
    temp_tolerance = 20.0
    upper_temp_limit = reference_temp + temp_tolerance
    lower_temp_limit = reference_temp - (temp_tolerance + 15) # it gets cold in the factory


    def reset_tuning_flags(self):

        Logger.info("Reset tuning flags")

        self.toff_and_sgt_found = False
        self.tuning_poll = None
        self.x1_toff_tuned = None
        self.x1_sgt_tuned = None
        self.x2_toff_tuned = None
        self.x2_sgt_tuned = None
        self.y1_toff_tuned = None
        self.y1_sgt_tuned = None
        self.y2_toff_tuned = None
        self.y2_sgt_tuned = None
        self.z_toff_tuned = None
        self.z_sgt_tuned = None

        self.temp_sg_array = []

        self.temp_toff = self.toff_min
        self.temp_sgt = self.sgt_min

    def motor_driver_temp_in_range(self, temp_to_assess):
        return (self.lower_temp_limit <= temp_to_assess <= self.upper_temp_limit)

    # ALL MOTORS ARE FREE RUNNING
    def prepare_for_tuning(self):

        Logger.info("Prepare for tuning")
        self.calibration_tuning_fail_info = ''

        Logger.info("Pos x: " + self.x_pos_str())
        Logger.info("Pos y: " + self.y_pos_str())
        Logger.info("Pos z: " + self.z_pos_str())

        self.s.write_command('$20=0')

        # Enable raw SG reporting: command REPORT_RAW_SG
        self.send_command_to_motor("REPORT RAW SG SET", command=REPORT_RAW_SG, value=1) # is there a way to check this has sent?
        self.reset_tuning_flags()

        # Zero position
        Logger.info("Zero position")
        self.jog_absolute_xy(self.x_min_jog_abs_limit, self.y_min_jog_abs_limit, 6000)
        self.jog_absolute_single_axis('Z', self.z_max_jog_abs_limit, 750)

        self.time_to_check_for_tuning_prep = time.time()

    # CHECK SG VALUES FIRST (TO MAKE SURE THEY'RE RAW)
    def check_SGs_rezero_and_go_to_next_checks_then_tune(self, X = False, Y = False, Z = False):

        SG_to_check = None

        if Z: SG_to_check = self.s.sg_z_motor_axis
        elif X: SG_to_check = self.s.sg_x_motor_axis
        elif Y: SG_to_check = self.s.sg_y1_motor


        if 200 < SG_to_check < 950:

            self.quit_jog()

            Logger.info("SG values in range - re-zero")

            self.jog_absolute_xy(self.x_min_jog_abs_limit, self.y_min_jog_abs_limit, 6000)
            self.jog_absolute_single_axis('Z', self.z_max_jog_abs_limit, 750)

            self.time_to_check_for_tuning_prep = time.time()
            Clock.schedule_once(lambda dt: self.check_temps_and_then_go_to_idle_check_then_tune(X=X, Y=Y, Z=Z), 2)


        elif (self.time_to_check_for_tuning_prep + 180) < time.time():
            # raise error popup
            Logger.warning("RAW SG VALUES NOT ENABLED")
            self.calibration_tuning_fail_info = "Raw SG values are still not enabled or reads are bad after 3 mins"
            Clock.schedule_once(self.finish_tuning, 0.1)

        else:
            if self.state().startswith('Idle'):
                self.tuning_jog_back_fast(X=X, Y=Y, Z=Z)
                self.tuning_jog_forwards_fast(X=X, Y=Y, Z=Z)

            Clock.schedule_once(lambda dt: self.check_SGs_rezero_and_go_to_next_checks_then_tune(X=X, Y=Y, Z=Z), 1)



    def check_temps_and_then_go_to_idle_check_then_tune(self, X = False, Y = False, Z = False):

        if self.motor_driver_temp_in_range(self.s.motor_driver_temp):

            Logger.info("Temperature reads valid, check machine is Idle...")

            self.time_to_check_for_tuning_prep = time.time()
            Clock.schedule_once(lambda dt: self.is_machine_idle_for_tuning(X=X, Y=Y, Z=Z), 2)

        elif (self.time_to_check_for_tuning_prep + 15) < time.time():
            # raise error popup
            Logger.warning("TEMPS AREN'T RIGHT?? TEMP: " + str(self.s.motor_driver_temp))
            self.calibration_tuning_fail_info = (
                "Temps aren't in expected range" + \
                "(" + str(int(self.lower_temp_limit)) + \
                "-" + \
                str(int(self.upper_temp_limit)) + "), " + \
                "motor_driver_temp is: " + str(self.s.motor_driver_temp)
                )

            Clock.schedule_once(self.finish_tuning, 0.1)


        else:
            Clock.schedule_once(lambda dt: self.check_temps_and_then_go_to_idle_check_then_tune(X=X, Y=Y, Z=Z), 3)


    # NEED TO ADD IN WHAT HAPPENS IF TIME RUNS OUT ELSES HERE ALSO
    def is_machine_idle_for_tuning(self, X = False, Y = False, Z = False):

        if self.state().startswith('Idle'):

            Logger.info("Ready for tuning, start slow jog...")
            Logger.info("Start tuning...")
            self.start_tuning(X,Y,Z)

        elif (self.time_to_check_for_tuning_prep + 120) < time.time():
            # raise error popup
            Logger.warning("STILL NOT IDLE ??")
            self.calibration_tuning_fail_info = "Machine not IDLE after 2 mins - check for alarms etc"
            Clock.schedule_once(self.finish_tuning, 0.1)

        else:
            Clock.schedule_once(lambda dt: self.is_machine_idle_for_tuning(X=X, Y=Y, Z=Z), 5)



    def start_slow_tuning_jog(self, X = False, Y = False, Z = False):

        # 3. Start long jogging in the axis of interest at 300mm/min for X and Y or for 30mm/min for Z

        if X and Z and not Y:
            self.s.write_command('$J = G91 X2000 Z-200 F301.5')

        elif X and Y and Z:
            self.s.write_command('$J = G91 X1270 Y1270 Z-127 F425.3')

        elif Y:
            self.s.write_command('$J = G91 Y2000 F300')

        elif X:
            self.s.write_command('$J = G91 X2000 F300')

        elif Z:
            self.s.write_command('$J = G91 Z-200 F30')

        # does not yet handle: 
        # - X, Y, Z
        # - X and Y
        # - Y and Z

    def tuning_jog_back_fast(self, X=False, Y=False, Z=False):

        if X and Z and not Y:
            self.s.write_command('$J=G53 X' + str(self.x_min_jog_abs_limit) + ' Z' + str(self.z_max_jog_abs_limit) + ' F6029.9')

        elif X and Y and Z:
            self.s.write_command('$J=G53 X' + str(self.x_min_jog_abs_limit) + ' Y' + str(self.y_min_jog_abs_limit) + ' Z' + str(self.z_max_jog_abs_limit) + ' F8518.3')

        elif Y:
            self.jog_absolute_single_axis('Y', self.y_min_jog_abs_limit, 6000)

        elif X:
            self.jog_absolute_single_axis('X', self.x_min_jog_abs_limit, 6000)

        elif Z:
            self.jog_absolute_single_axis('Z', self.z_max_jog_abs_limit, 750)

        # does not yet handle: 
        # - X, Y, Z
        # - X and Y
        # - Y and Z

    def tuning_jog_forwards_fast(self, X=False, Y=False, Z=False):

        if X and Z and not Y:
            self.s.write_command('$J=G53 X-1192 Z-149 F6046')

        elif X and Y and Z:
            self.s.write_command('$J = G91 X-1270 Y-1270 Z127 F8518.3')

        elif Y:
            self.jog_absolute_single_axis('Y', self.y_max_jog_abs_limit, 6000)

        elif X:
            self.jog_absolute_single_axis('X', self.x_max_jog_abs_limit, 6000)

        elif Z:
            self.jog_absolute_single_axis('Z', self.z_min_jog_abs_limit, 750)

        # does not yet handle: 
        # - X, Y, Z
        # - X and Y
        # - Y and Z

    def start_tuning(self, X, Y, Z):

        # start thread
        tune_thread = threading.Thread(target=self.do_tuning, args=(X, Y, Z))
        tune_thread.daemon = True
        tune_thread.start()

        # start poll - this will check when toff and sgt parameters have been found, and then apply settings
        self.tuning_poll = Clock.schedule_once(lambda dt: self.apply_tuned_settings(X=X, Y=Y, Z=Z), 10)


    def do_tuning(self, X, Y, Z):

        # ORDER IS: 
        # self.sg_z_motor_axis = int(sg_values[0])
        # self.sg_x_motor_axis = int(sg_values[1])
        # self.sg_y_axis = int(sg_values[2]) (this depends on y1 and y2 motors)
        # self.sg_y1_motor = int(sg_values[3])
        # self.sg_y2_motor = int(sg_values[4])

        # AND for 5 driver PCBS:
        # self.sg_x1_motor = int(sg_values[5])
        # self.sg_x2_motor = int(sg_values[6])

        time.sleep(0.5)

        self.print_tmc_registers(0)
        self.print_tmc_registers(1)
        self.print_tmc_registers(2)
        self.print_tmc_registers(3)
        self.print_tmc_registers(4)

        try:

            tuning_array, current_temp = self.sweep_toff_and_sgt_and_motor_driver_temp(X = X, Y = Y, Z = Z)
            Logger.info("Sweep finished")

            if X:
                X_target_SG = self.get_target_SG_from_current_temperature('X', current_temp)
                if (self.s.sg_x1_motor != None) and (self.s.sg_x2_motor != None):
                    self.x1_toff_tuned, self.x1_sgt_tuned = self.find_best_combo_per_motor_or_axis(tuning_array, X_target_SG, 5)
                    self.x2_toff_tuned, self.x2_sgt_tuned = self.find_best_combo_per_motor_or_axis(tuning_array, X_target_SG, 6)

                else:
                    self.x1_toff_tuned, self.x1_sgt_tuned = self.x2_toff_tuned, self.x2_sgt_tuned = self.find_best_combo_per_motor_or_axis(tuning_array, X_target_SG, 1)

            if Y:
                Y_target_SG = self.get_target_SG_from_current_temperature('Y', current_temp)
                self.y1_toff_tuned, self.y1_sgt_tuned = self.find_best_combo_per_motor_or_axis(tuning_array, Y_target_SG, 3)
                self.y2_toff_tuned, self.y2_sgt_tuned = self.find_best_combo_per_motor_or_axis(tuning_array, Y_target_SG, 4)

            if Z:
                Z_target_SG =self.get_target_SG_from_current_temperature('Z', current_temp)
                self.z_toff_tuned, self.z_sgt_tuned = self.find_best_combo_per_motor_or_axis(tuning_array, Z_target_SG, 0)

        except:

            Logger.exception("Could not complete tuning! Check log for errors")
            Clock.unschedule(self.tuning_poll)
            Clock.schedule_once(self.finish_tuning, 0.1)
            return


        self.toff_and_sgt_found = True


    def sweep_toff_and_sgt_and_motor_driver_temp(self, X = False, Y = False, Z = False):

        temperature_list = []

        # Sweep TOFF in the range 2-10
        # Sweep SGT in the range 0-20
        # For each TOFF/SGT combination read SG 15 times (every 100ms, usual status report rate), skip the first 7 points as they are settling points and not valid.

        # having empty initial values, so that running through indices with 
        # self.temp_toff and self.temp_sgt is easy and readable :) 

        tuning_array = [[[] for sgt_holder in xrange(self.sgt_max + 1)] for toff_holder in xrange(self.toff_max + 1)]


        while self.temp_toff <= self.toff_max:

            # Commands have to be sent at least 0.05 s apart, so sleeps after commands are sent give time for each command to be sent and recieved

            if X:
                self.send_command_to_motor("SET TOFF X1 " + str(self.temp_toff), motor = TMC_X1, command = SET_TOFF, value = self.temp_toff)
                self.send_command_to_motor("SET TOFF X2 " + str(self.temp_toff), motor = TMC_X2, command = SET_TOFF, value = self.temp_toff)
                time.sleep(0.2)
            if Y:
                self.send_command_to_motor("SET TOFF Y1 " + str(self.temp_toff), motor = TMC_Y1, command = SET_TOFF, value = self.temp_toff)
                self.send_command_to_motor("SET TOFF Y2 " + str(self.temp_toff), motor = TMC_Y2, command = SET_TOFF, value = self.temp_toff)
                time.sleep(0.2)
            if Z:
                self.send_command_to_motor("SET TOFF Z " + str(self.temp_toff), motor = TMC_Z, command = SET_TOFF, value = self.temp_toff)
                time.sleep(0.1)

            while self.temp_sgt <= self.sgt_max:

                if X:
                    self.send_command_to_motor("SET SGT X1 " + str(self.temp_sgt), motor = TMC_X1, command = SET_SGT, value = self.temp_sgt)
                    self.send_command_to_motor("SET SGT X2 " + str(self.temp_sgt), motor = TMC_X2, command = SET_SGT, value = self.temp_sgt)
                    time.sleep(0.2)
                if Y:
                    self.send_command_to_motor("SET SGT Y1 " + str(self.temp_sgt), motor = TMC_Y1, command = SET_SGT, value = self.temp_sgt)
                    self.send_command_to_motor("SET SGT Y2 " + str(self.temp_sgt), motor = TMC_Y2, command = SET_SGT, value = self.temp_sgt)
                    time.sleep(0.2)
                if Z:
                    self.send_command_to_motor("SET SGT Z " + str(self.temp_sgt), motor = TMC_Z, command = SET_SGT, value = self.temp_sgt)
                    time.sleep(0.1)

                while len(self.temp_sg_array) <= 15:

                    # Keep jogging!
                    if self.state().startswith('Idle'):
                        Logger.info('Idle - restart jogs')
                        self.s.record_sg_values_flag = False
                        self.temp_sg_array = []
                        self.tuning_jog_back_fast(X=X, Y=Y, Z=Z)
                        self.start_slow_tuning_jog(X=X, Y=Y, Z=Z)
                        time.sleep(0.01)

                    # But don't measure the backwards fast jogs!
                    elif self.feed_rate() > 430:
                        Logger.info('Feed rate too high, skipping')
                        self.s.record_sg_values_flag = False
                        self.temp_sg_array = []
                        time.sleep(1)

                    # Record if conditions are good :)
                    else:
                        self.s.record_sg_values_flag = True
                        time.sleep(0.01)

                self.s.record_sg_values_flag = False

                tuning_array[self.temp_toff][self.temp_sgt] = self.temp_sg_array[8:16]
                self.temp_sg_array = []

                Logger.info("SWEPT TOFF AND SGT: " + str(self.temp_toff) + ", " + str(self.temp_sgt))

                temperature_list.append(self.s.motor_driver_temp)

                self.temp_sgt = self.temp_sgt + 1

            self.temp_sgt = self.sgt_min
            self.temp_toff = self.temp_toff + 1

        try:
            avg_temperature = sum(temperature_list) / len(temperature_list)
            Logger.info("Average temperature: " + str(avg_temperature))
            return tuning_array, avg_temperature

        except:
            self.calibration_tuning_fail_info = "Bad temps during tuning!"
            Logger.exception("BAD TEMPERATURES! CAN'T CALIBRATE")


    def find_best_combo_per_motor_or_axis(self, tuning_array, target_SG, idx):

        # idx is motor/axis index

        Logger.info("Find best combo for axis idx: " + str(idx) + ", target: " + str(target_SG))

        # toff, sgt, dsg
        prev_best = [None, None, None]

        for toff in range(self.toff_min, self.toff_max + 1):
            for sgt in range(self.sgt_min, self.sgt_max + 1):

                try_dsg = self.average_points_in_sub_array(tuning_array[toff][sgt], idx) - target_SG

                # compare delta sg (between read in and target)
                # if it's smaller than any values found previously, then it's better, so save it
                try:
                    if abs(try_dsg) < abs(prev_best[2]):
                        prev_best = [toff, sgt, try_dsg]

                except:
                    if prev_best[2] == None:
                        prev_best = [toff, sgt, try_dsg]

        # at end of loop, prev_best == best
        Logger.info("FOUND FOR IDX: " + str(idx) + ":" + str(prev_best[0]) + "," + str(prev_best[1]) + "," + str(prev_best[2]))

        return prev_best[0], prev_best[1]


    def average_points_in_sub_array(self, sub_array, index):
        # Average the remaining 8 points. 
        just_idx_sgs = [sg_arr[index] for sg_arr in sub_array]
        avg_idx = sum(just_idx_sgs) / len(just_idx_sgs)
        return avg_idx


    def get_target_SG_from_current_temperature(self, motor, current_temperature):
        # To start with lets stick to
        # target temp = 45C
        # gradient_per_Celsius values (4000 for X and Z, 1500 for Y)
        # use "Motor Driver temperature"

        if not self.motor_driver_temp_in_range(current_temperature):

            Logger.warning("Temperatures out of expected range! Check set-up!")
            self.calibration_tuning_fail_info = "Temperatures out of expected range! Check set-up!"
            return

        reference_SG = 500

        if motor == 'X':
            gradient_per_Celsius = 5000.0
            rpm = 300.0/(3200/(170/3))

        elif motor == 'Y':
            gradient_per_Celsius = 5000.0
            rpm = 300.0/(3200/(170/3))

        elif motor == 'Z':
            gradient_per_Celsius = 10000.0
            rpm = 30.0/(3200/(1066.67))

        delta_to_current_temperature = self.reference_temp - current_temperature
        step_us = 60000000 / (rpm * 3200)
        compensation_SG_offset = gradient_per_Celsius/1000000 * delta_to_current_temperature * step_us
        target_SG = reference_SG + int(compensation_SG_offset)

        Logger.info("Calculate target SG " + str(motor) + ": " + str(target_SG))

        return target_SG


    def apply_tuned_settings(self, X = False, Y = False, Z = False):

        # NB: ALL THE SETTINGS HERE WILL TAKE A FEW SECONDS TO COMPLETE

        if not self.toff_and_sgt_found:

            self.tuning_poll = Clock.schedule_once(lambda dt: self.apply_tuned_settings(X=X, Y=Y, Z=Z), 10)
            return

        Logger.info("TOFF and SGT found - applying settings")

        # Stop slow jog
        self.quit_jog()

        # Apply found TOFF and SGT values to the motor: commands SET_CHOPCONF and SET_SGCSCONF

        if X:
            self.send_command_to_motor("SET TOFF X1 " + str(self.x1_toff_tuned), motor = TMC_X1, command = SET_TOFF, value = self.x1_toff_tuned)
            self.send_command_to_motor("SET TOFF X2 " + str(self.x2_toff_tuned), motor = TMC_X2, command = SET_TOFF, value = self.x2_toff_tuned)
            self.send_command_to_motor("SET SGT X1 " + str(self.x1_sgt_tuned), motor = TMC_X1, command = SET_SGT, value = self.x1_sgt_tuned)
            self.send_command_to_motor("SET SGT X2 " + str(self.x2_sgt_tuned), motor = TMC_X2, command = SET_SGT, value = self.x2_sgt_tuned)
        if Y:
            self.send_command_to_motor("SET TOFF Y1 " + str(self.y1_toff_tuned), motor = TMC_Y1, command = SET_TOFF, value = self.y1_toff_tuned)
            self.send_command_to_motor("SET TOFF Y2 " + str(self.y2_toff_tuned), motor = TMC_Y2, command = SET_TOFF, value = self.y2_toff_tuned)
            self.send_command_to_motor("SET SGT Y1 " + str(self.y1_sgt_tuned), motor = TMC_Y1, command = SET_SGT, value = self.y1_sgt_tuned)
            self.send_command_to_motor("SET SGT Y2 " + str(self.y2_sgt_tuned), motor = TMC_Y2, command = SET_SGT, value = self.y2_sgt_tuned)
        if Z:
            self.send_command_to_motor("SET TOFF Z " + str(self.z_toff_tuned), motor = TMC_Z, command = SET_TOFF, value = self.z_toff_tuned)
            self.send_command_to_motor("SET SGT Z " + str(self.z_sgt_tuned), motor = TMC_Z, command = SET_SGT, value = self.z_sgt_tuned)

        Clock.schedule_once(self.store_tuned_settings_and_unset_raw_SG_reporting, 5) # Give settings plenty of time to be sent and parsed


    def store_tuned_settings_and_unset_raw_SG_reporting(self, dt):

        Logger.info("Storing TMC parameters in EEPROM")

        # Store the motors settings in the EEPROM: command STORE_TMC_PARAMS
        self.send_command_to_motor("STORE TMC PARAMS IN EEPROM", command = STORE_TMC_PARAMS)

        # Disable raw SG reporting: command REPORT_RAW_SG
        self.send_command_to_motor("REPORT RAW SG SET", command=REPORT_RAW_SG, value=0)

        # Read registers back in
        self.send_command_to_motor("GET REGISTERS", command=GET_REGISTERS)

        Clock.schedule_once(self.send_final_tuning_commands, 3) # Give settings plenty of time to be sent and parsed


    def send_final_tuning_commands(self, dt):

        self.s.write_command('$20=1')
        Logger.info("Tuning complete")
        self.reset_tuning_flags()
        Clock.schedule_once(self.finish_tuning, 3) # Give settings plenty of time to be sent and parsed


    def finish_tuning(self, dt):

        # Check SB is Idle and all buffers are empty

        if  self.state().startswith('Idle') and \
            not self.s.write_command_buffer and \
            not self.s.write_protocol_buffer:

            self.tuning_in_progress = False


    # MEAT OF CALIBRATION FUNCTIONS - DON'T CALL FROM MAIN APP

    x_ready_to_calibrate = False
    y_ready_to_calibrate = False
    z_ready_to_calibrate = False

    poll_for_x_ready = None
    poll_for_y_ready = None
    poll_for_z_ready = None

    time_to_check_for_calibration_prep = 0
    disable_and_enable_soft_limits = True
    quick_calibration = False

    calibration_files_folder_path = './asmcnc/comms/motor_baselining_files/'

    ## Functions to calibrate each axis separately (fast or slow)

    def initialise_calibration(self, X=False, Y=False, Z=False, zero_position=True, mod_soft_limits=True, quick_calibration=False):

        Logger.info("Initialise Calibration")
        self.calibration_tuning_fail_info = ''
        self.disable_and_enable_soft_limits = mod_soft_limits
        self.quick_calibration = quick_calibration

        if self.disable_and_enable_soft_limits:
            self.s.write_command('$20=0')

        if zero_position:
            Logger.info("Zero position")
            self.jog_absolute_xy(self.x_min_jog_abs_limit, self.y_min_jog_abs_limit, 6000)
            self.jog_absolute_single_axis('Z', self.z_max_jog_abs_limit, 750)

        # Only sets one ready to begin with
        if X: self.x_ready_to_calibrate = True
        elif Y: self.y_ready_to_calibrate = True
        elif Z: self.z_ready_to_calibrate = True

        if X: self.poll_for_x_ready = Clock.schedule_interval(self.do_calibrate_x, 1)
        if Y: self.poll_for_y_ready = Clock.schedule_interval(self.do_calibrate_y, 1)
        if Z: self.poll_for_z_ready = Clock.schedule_interval(self.do_calibrate_z, 1)

    def do_calibrate_x(self, dt):

        if self.x_ready_to_calibrate:

            Logger.info("Calibrate X")

            Clock.unschedule(self.poll_for_x_ready)
            self.poll_for_x_ready = None
            self.x_ready_to_calibrate = False
            self.time_to_check_for_calibration_prep = time.time()
            self.check_idle_and_buffer_then_start_calibration('X')

    def do_calibrate_y(self, dt):

        if self.y_ready_to_calibrate:

            Logger.info("Calibrate Y")

            Clock.unschedule(self.poll_for_y_ready)
            self.poll_for_y_ready = None
            self.y_ready_to_calibrate = False
            self.time_to_check_for_calibration_prep = time.time()
            self.check_idle_and_buffer_then_start_calibration('Y')

    def do_calibrate_z(self, dt):

        if self.z_ready_to_calibrate:

            Logger.info("Calibrate Z")

            Clock.unschedule(self.poll_for_z_ready)
            self.poll_for_z_ready = None
            self.z_ready_to_calibrate = False
            self.time_to_check_for_calibration_prep = time.time()
            self.check_idle_and_buffer_then_start_calibration('Z')

    def check_idle_and_buffer_then_start_calibration(self, axis):

        if self.state().startswith('Idle') and not self.s.write_protocol_buffer:

            if self.quick_calibration: path_end = '_cal_quick_n_coarse.gc'
            else: path_end = '_cal.gc'
            calibration_file = self.calibration_files_folder_path + axis + path_end

            if axis == 'X':
                calibrate_mode = 32
                altDisplayText = "CALIBRATE X AXIS"

            if axis == 'Y':
                calibrate_mode = 64
                altDisplayText = "CALIBRATE Y AXIS"

            if axis == 'Z':
                calibrate_mode = 128
                altDisplayText = "CALIBRATE Z AXIS"

            self.send_command_to_motor(altDisplayText, command=SET_CALIBR_MODE, value=calibrate_mode)
            Clock.schedule_once(lambda dt: self.stream_calibration_file(calibration_file), 0.5)

        elif (self.time_to_check_for_calibration_prep + 120) < time.time():

            # gives error message to popup
            Logger.warning("MACHINE STILL NOT IDLE OR BUFFER FULL - CAN'T CALIBRATE")
            self.calibration_tuning_fail_info = "Machine not IDLE after 2 mins - check for alarms etc"
            Clock.schedule_once(lambda dt: self.complete_calibration(), 0.1)

        else:
            Clock.schedule_once(lambda dt: self.check_idle_and_buffer_then_start_calibration(axis), 0.1)


    ## Function to quickly calibrate all three axes in one go (FW v2.6 and up)

    def prep_triple_axes_calibration(self):

        if not self.run_calibration: return

        if not self.state().startswith('Idle') or self.s.write_protocol_buffer:
            Clock.schedule_once(lambda dt: self.prep_triple_axes_calibration(), 0.1)
            return

        self.calibration_tuning_fail_info = ''
        self.disable_and_enable_soft_limits = False
        self.send_command_to_motor("CALIBRATE ALL AXES", command=SET_CALIBR_MODE, value=TMC_CALIBRATION_INIT_ALL)

        calibration_file = self.calibration_files_folder_path + 'triple_axis_baselining.gc'
        Clock.schedule_once(lambda dt: self.stream_calibration_file(calibration_file), 0.5)


    ## Functions for all calibration modes

    def stream_calibration_file(self, filename):

        if not self.run_calibration: return

        with open(filename) as f:
            calibration_gcode_pre_scrubbed = f.readlines()

        calibration_gcode = [self.quick_scrub(line) for line in calibration_gcode_pre_scrubbed]

        Logger.info("Calibrating...")

        if not self.run_calibration: return
        self.s.run_skeleton_buffer_stuffer(calibration_gcode)
        self.poll_end_of_calibration_file_stream = Clock.schedule_once(self.post_calibration_file_stream, 0.5)


    def quick_scrub(self, line):

        l_block = re.sub('\s|\(.*?\)', '', (line.strip()).upper())
        return l_block


    def post_calibration_file_stream(self, dt):

        if not self.run_calibration: return

        if self.state().startswith('Idle') and self.s.NOT_SKELETON_STUFF and not self.s.is_job_streaming and not self.s.is_stream_lines_remaining and not self.is_machine_paused:
            Clock.unschedule(self.poll_end_of_calibration_file_stream)
            self.send_command_to_motor("COMPUTE THIS CALIBRATION", command=SET_CALIBR_MODE, value=2)

            # FW needs 5 seconds to compute & store after calibration
            Clock.schedule_once(lambda dt: self.do_next_axis_or_finish_calibration_sequence(), 5)

        else:
            self.poll_end_of_calibration_file_stream = Clock.schedule_once(self.post_calibration_file_stream, 0.5)


    def do_next_axis_or_finish_calibration_sequence(self):

        if not self.run_calibration: return

        # X is always first, so check y and then z
        if self.poll_for_y_ready != None: self.y_ready_to_calibrate = True
        elif self.poll_for_z_ready != None: self.z_ready_to_calibrate = True
        else: self.save_calibration_coefficients_to_motor_classes()


    def save_calibration_coefficients_to_motor_classes(self):

        if not self.run_calibration: return

        if self.disable_and_enable_soft_limits: self.s.write_command('$20=1')
        self.send_command_to_motor("OUTPUT CALIBRATION COEFFICIENTS", command=SET_CALIBR_MODE, value=4)
        Clock.schedule_once(lambda dt: self.complete_calibration(), 1)


    def complete_calibration(self):

        self.x_ready_to_calibrate = False
        self.y_ready_to_calibrate = False
        self.z_ready_to_calibrate = False

        self.poll_for_x_ready = None
        self.poll_for_y_ready = None
        self.poll_for_z_ready = None

        self.time_to_check_for_calibration_prep = 0

        self.run_calibration = False

        Logger.info("Calibration complete")

    # Don't use for all the different states yet, this is a quick hack solution
    # Ideally want to refactor the whole sequence
    def cancel_triple_axes_calibration(self):
        self.run_calibration = False
        self.complete_calibration()
        self._stop_all_streaming()
        self.hard_reset_pcb_sequence()


    # UPLOADING CALIBRATION TO FW:
    calibration_upload_in_progress = False
    calibration_upload_fail_info = ''

    def upload_Z_calibration_settings_from_motor_class(self):

        self.calibration_upload_in_progress = True
        self.calibration_upload_fail_info = ''
        self.set_sgt_and_toff_calibrated_at_settings(TMC_Z)
        Clock.schedule_once(lambda dt: self.initialise_calibration_upload('Z'), 1)

    def upload_Y_calibration_settings_from_motor_classes(self):
        self.calibration_upload_in_progress = True
        self.calibration_upload_fail_info = ''
        self.set_sgt_and_toff_calibrated_at_settings(TMC_Y1)
        self.set_sgt_and_toff_calibrated_at_settings(TMC_Y2)
        Clock.schedule_once(lambda dt: self.initialise_calibration_upload('Y'), 2)


    time_to_check_for_upload_prep = 0


    def set_sgt_and_toff_calibrated_at_settings(self, motor_index):

        display_text = "SET CALIBRATED AT FOR MOTOR " + str(motor_index) + ", "
        sgt_val = self.TMC_motor[int(motor_index)].calibrated_at_sgt_setting
        toff_val = self.TMC_motor[int(motor_index)].calibrated_at_toff_setting
        self.send_command_to_motor(display_text + "SGT " + str(sgt_val), motor = motor_index, command = SET_SGT, value = sgt_val)
        self.send_command_to_motor(display_text + "TOFF " + str(toff_val), motor = motor_index, command = SET_TOFF, value = toff_val)


    def initialise_calibration_upload(self, axis):

        if self.state().startswith('Idle') and not self.s.write_protocol_buffer:

            if axis == 'X':
                calibrate_mode = 32
                altDisplayText = "UPLOAD CALIBRATION TO X AXIS"
                motor_index = TMC_X1

            if axis == 'Y':
                calibrate_mode = 64
                altDisplayText = "UPLOAD CALIBRATION TO Y AXIS"
                motor_index = TMC_Y1

            if axis == 'Z':
                calibrate_mode = 128
                altDisplayText = "UPLOAD CALIBRATION TO Z AXIS"
                motor_index = TMC_Z

            self.send_command_to_motor(altDisplayText, command=SET_CALIBR_MODE, value=calibrate_mode)

            upload_cal_thread = threading.Thread(target=self.do_calibration_upload, args=(motor_index,))
            upload_cal_thread.daemon = True
            upload_cal_thread.start()

        elif (self.time_to_check_for_upload_prep + 120) < time.time():
            Logger.warning("PROBLEM! Can't initialise calibration upload")
            self.calibration_upload_fail_info = "Machine not IDLE after 2 mins - check for alarms etc"
            Clock.schedule_once(lambda dt: self.complete_calibration_upload(), 0.1)

        else:
            Clock.schedule_once(lambda dt: self.initialise_calibration_upload(axis), 2)


    def do_calibration_upload(self, motor_index):

        # # CALIBRATION PARAMS
        # calibration_dataset_SG_values   = []
        # calibrated_at_current_setting   = 0
        # calibrated_at_sgt_setting       = 0
        # calibrated_at_toff_setting      = 0
        # calibrated_at_temperature       = 0

        time.sleep(5) # allow time for calibration mode to initialise
        second_motor = None

        if (motor_index == TMC_X1) or (motor_index == TMC_Y1): # second motor

            second_motor = motor_index + 1

        data_length = len(self.TMC_motor[int(motor_index)].calibration_dataset_SG_values) + 4

        for idx in range(data_length - 4):
            self.send_one_calibration_upload_value(motor_index, idx, self.TMC_motor[int(motor_index)].calibration_dataset_SG_values[idx])

            if second_motor:
                self.send_one_calibration_upload_value(second_motor, idx, self.TMC_motor[int(second_motor)].calibration_dataset_SG_values[idx])

        self.send_calibration_parameters(motor_index, data_length)
        if second_motor: self.send_calibration_parameters(second_motor, data_length)

        Clock.schedule_once(lambda dt: self.tell_FW_to_finish_calibration_upload(), 5)


    def send_calibration_parameters(self, motor_index, data_length):

        self.send_one_calibration_upload_value(motor_index, data_length - 4, self.TMC_motor[int(motor_index)].calibrated_at_current_setting)
        self.send_one_calibration_upload_value(motor_index, data_length - 3, self.TMC_motor[int(motor_index)].calibrated_at_sgt_setting)
        self.send_one_calibration_upload_value(motor_index, data_length - 2, self.TMC_motor[int(motor_index)].calibrated_at_toff_setting)
        self.send_one_calibration_upload_value(motor_index, data_length - 1, self.TMC_motor[int(motor_index)].calibrated_at_temperature)


    def send_one_calibration_upload_value(self, motor_index, idx, val):

        altDisplayText = "UPLOAD CAL: M" + str(motor_index) + ":I" + str(idx) + ":COEFF " + str(val)

        constructed_value  = (motor_index << 24)      & 0xFF000000
        constructed_value |= (idx   << 16)      & 0x00FF0000
        constructed_value |= (val)              & 0x0000FFFF

        self.send_command_to_motor(altDisplayText, motor = motor_index, command=UPLOAD_CALIBR_VALUE, value = constructed_value)
        time.sleep(0.1)


    def tell_FW_to_finish_calibration_upload(self):
        self.send_command_to_motor("FINISH UPLOAD", command=SET_CALIBR_MODE, value=2)
        Clock.schedule_once(lambda dt: self.output_uploaded_coefficients(), 5)


    def output_uploaded_coefficients(self):
        self.send_command_to_motor("OUTPUT CALIBRATION COEFFICIENTS", command=SET_CALIBR_MODE, value=4)
        Clock.schedule_once(lambda dt: self.output_registers_to_check(), 2)


    def output_registers_to_check(self):
        self.send_command_to_motor("GET REGISTERS", command=GET_REGISTERS)
        Clock.schedule_once(lambda dt: self.complete_calibration_upload(), 2)


    def complete_calibration_upload(self):

        # Ensure last commmands have actually been sent through buffer
        if self.state().startswith('Idle') and not self.s.write_protocol_buffer:

            self.time_to_check_for_upload_prep = 0
            self.calibration_upload_in_progress = False
            Logger.info("Calibration upload complete")

        else:
            Clock.schedule_once(lambda dt: self.complete_calibration_upload(), 1)



    ## CHECKING CALIBRATION FILE STREAMS

    checking_calibration_in_progress = False
    checking_calibration_fail_info = ''

    cal_check_threshold_x_min = -201
    cal_check_threshold_x_max = 201

    cal_check_threshold_y_min = -201
    cal_check_threshold_y_max = 201

    cal_check_threshold_z_min = -201
    cal_check_threshold_z_max = 201

    refind_position_after_reset = False

    poll_end_of_calibration_check = None

    def check_x_y_z_calibration(self, do_reset=False, assembled=True):
        self.do_calibration_check(['X', 'Y', 'Z'], do_reset, assembled)

    def check_x_z_calibration(self, do_reset=True, assembled=False):
        self.do_calibration_check(['X', 'Z'], do_reset, assembled)

    def check_y_calibration(self, do_reset=True, assembled=False):
        self.do_calibration_check(['Y'], do_reset, assembled)


    def reset_cal_check_pass_thresholds(self):
        self.cal_check_threshold_x_min = -201
        self.cal_check_threshold_x_max = 201

        self.cal_check_threshold_y_min = -201
        self.cal_check_threshold_y_max = 201

        self.cal_check_threshold_z_min = -201
        self.cal_check_threshold_z_max = 201


    def do_calibration_check(self, axes, do_reset, assembled):

        if not self.prep_calibration_check(axes, do_reset):
            return

        if self.state().startswith('Alarm'):
            self.checking_calibration_fail_info = "Stuck in alarm state"
            self.poll_end_of_calibration_check = Clock.schedule_interval(lambda dt: self.post_calibration_check(axes), 0.5)
            return

        if not self.state().startswith('Idle') or not self.TMC_registers_have_been_read_in() or \
            self.s.is_sequential_streaming or not self.s.setting_132:
            Clock.schedule_once(lambda dt: self.do_calibration_check(axes, do_reset, assembled), 0.5)
            return

        if self.refind_position_after_reset:
            self.refind_position_after_reset = False
            if assembled: self.start_homing()
            else: self.free_travel_to_home_positions(axes)
            Clock.schedule_once(lambda dt: self.do_calibration_check(axes, do_reset, assembled), 0.5)
            return

        if not self.calibration_coefficients_have_been_read_in():
            self.send_command_to_motor("OUTPUT CALIBRATION COEFFICIENTS", command=SET_CALIBR_MODE, value=4)
            Clock.schedule_once(lambda dt: self.do_calibration_check(axes, do_reset, assembled), 5)
            return

        self.stream_calibration_check_files(axes)


    def prep_calibration_check(self, axes, do_reset):

        if self.checking_calibration_in_progress:
            return True

        self.checking_calibration_in_progress = True

        if not do_reset:
            self.refind_position_after_reset = False
            return True

        # Toggle FW reset pin before starting 
        if self.hard_reset_pcb_sequence():
            self.refind_position_after_reset = True
            return True

        self.checking_calibration_fail_info = "Pin toggle fail"
        self.poll_end_of_calibration_check = Clock.schedule_interval(lambda dt: self.post_calibration_check(axes), 0.5)
        return False

    def free_travel_to_home_positions(self, axes):

        free_travel_seq = []

        if "X" in axes: free_travel_seq.append("G53 " + "X" + str(float(-1*self.s.setting_130) + float(self.limit_switch_safety_distance))) #X Max travel
        if "Y" in axes: free_travel_seq.append("G53 " + "Y" + str(float(-1*self.s.setting_131) + float(self.limit_switch_safety_distance))) #Y Max travel
        if "Z" in axes: free_travel_seq.append("G53 " + "Z" + str(-1)) #Z Max travel

        self.s.start_sequential_stream(free_travel_seq)


    def stream_calibration_check_files(self, axes):

        check_calibration_gcode_pre_scrubbed = []

        for axis in axes:

            with open(self.construct_calibration_check_file_path(axis)) as f:
                check_calibration_gcode_pre_scrubbed.extend(f.readlines())

        check_calibration_gcode = [self.quick_scrub(line) for line in check_calibration_gcode_pre_scrubbed]

        Logger.info("Checking calibration...")

        self.checking_calibration_fail_info = ""
        self.temp_sg_array = []
        self.s.record_sg_values_flag = True

        self.s.run_skeleton_buffer_stuffer(check_calibration_gcode)
        self.poll_end_of_calibration_check = Clock.schedule_once(lambda dt: self.post_calibration_check(axes), 5)


    def post_calibration_check(self, axes):

        if  self.state().startswith('Idle') and self.TMC_registers_have_been_read_in() and \
            self.s.NOT_SKELETON_STUFF and not self.s.is_job_streaming and not self.s.is_stream_lines_remaining and not self.is_machine_paused:
            if self.poll_end_of_calibration_check != None: Clock.unschedule(self.poll_end_of_calibration_check)
            self.s.record_sg_values_flag = False
            self.are_sg_values_in_range_after_calibration(axes)
            self.temp_sg_array = []
            self.reset_cal_check_pass_thresholds()
            if self.checking_calibration_fail_info: Logger.info(self.checking_calibration_fail_info)
            self.checking_calibration_in_progress = False
            Logger.info("Calibration check complete")
        else:
            self.poll_end_of_calibration_check = Clock.schedule_once(lambda dt: self.post_calibration_check(axes), 0.5)


    def construct_calibration_check_file_path(self, axis):
        return './asmcnc/production/calibration_check_gcode_files/' + str(axis) + '_cal_check.gc'


    def are_sg_values_in_range_after_calibration(self, axes):

        x_both_max = None
        x1_max = None
        x2_max = None
        y_both_max = None
        y1_max = None
        y2_max = None
        z_both_max = None

        try:

            if 'X' in axes:

                x_both_max = self.get_abs_maximums_from_sg_array(self.temp_sg_array, 1)

                if not self.cal_check_threshold_x_min < x_both_max < self.cal_check_threshold_x_max:
                    self.checking_calibration_fail_info += "X SG values out of expected range: " + str(x_both_max) + "| "

            if 'Y' in axes:

                y_both_max = self.get_abs_maximums_from_sg_array(self.temp_sg_array, 2)

                if not self.cal_check_threshold_y_min < y_both_max < self.cal_check_threshold_y_max:
                    self.checking_calibration_fail_info += "Y SG values out of expected range: " + str(y_both_max) + "| "

            if 'Z' in axes:

                z_both_max = self.get_abs_maximums_from_sg_array(self.temp_sg_array, 0)

                if not self.cal_check_threshold_z_min < z_both_max < self.cal_check_threshold_z_max:
                    self.checking_calibration_fail_info += "Z SG values out of expected range, max: " + str(z_both_max) + "|"

        except:
            if not self.checking_calibration_fail_info: self.checking_calibration_fail_info += "Unexpected error"

        return x_both_max, y_both_max, z_both_max

    def get_abs_maximums_from_sg_array(self, sub_array, index):

        just_idx_sgs = [sg_arr[index] for sg_arr in sub_array if sg_arr[index] != -999]
        try:
            abs_max_idx = max(just_idx_sgs, key=abs)
        except:
            Logger.exception("Failed to get abs maximums from sg array")
            self.checking_calibration_fail_info = "All values -999 for idx: " + str(index)
        return abs_max_idx


    ## SET SMART FEATURES

    def set_sg_threshold(self, motor, threshold):
        if self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'set SG alarm threshold'):
            display_text = "SET SG ALARM THRESHOLD, " + "MTR: " + str(motor) + ", THR: " + str(threshold)
            self.send_command_to_motor(display_text, motor=motor, command=SET_SG_ALARM_TRSHLD, value=int(threshold))

    def set_threshold_for_axis(self, axis, threshold):

        if axis == "X":
            self.set_sg_threshold(TMC_X1, threshold)
            self.set_sg_threshold(TMC_X2, threshold)
            return

        if axis == "Y":
            self.set_sg_threshold(TMC_Y1, threshold)
            self.set_sg_threshold(TMC_Y2, threshold)
            return

        if axis == "Z": self.set_sg_threshold(TMC_Z, threshold)


    def set_motor_current(self, axis, current):

        if  (self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'setting current') and \
            self.state().startswith('Idle')):

            motors = []

            if "Z" in axis: motors.append(TMC_Z)

            if "X1" in axis or "X2" in axis:
                if "X1" in axis: motors.append(TMC_X1)
                if "X2" in axis: motors.append(TMC_X2)
            elif "X" in axis:
                motors.extend([TMC_X1, TMC_X2])

            if "Y1" in axis or "Y2" in axis:
                if "Y1" in axis: motors.append(TMC_Y1)
                if "Y2" in axis: motors.append(TMC_Y2)
            elif "Y" in axis:
                motors.extend([TMC_Y1, TMC_Y2])

            for motor in motors:

                altDisplayText = 'SET ACTIVE CURRENT: ' + axis + ': ' + "TMC: " + str(motor) + ", I: " + str(current)
                self.send_command_to_motor(altDisplayText, motor=motor, command=SET_ACTIVE_CURRENT, value=current)
                altDisplayText = 'SET IDLE CURRENT: ' + axis + ': ' + "TMC: " + str(motor) + ", I: " + str(current)
                self.send_command_to_motor(altDisplayText, motor=motor, command=SET_IDLE_CURRENT, value=current)

            return True

        else:
            return False


    def set_thermal_coefficients(self, axis, value):

        if  self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'setting thermal coefficients') and \
            self.state().startswith('Idle'):

            if "X" in axis: motors = [TMC_X1, TMC_X2]
            if "Y" in axis: motors = [TMC_Y1, TMC_Y2]
            if "Z" in axis: motors = [TMC_Z]

            for motor in motors:

                altDisplayText = 'SET THERMAL COEFF: ' + axis + ': ' + "TMC: " + str(motor) + ", " + str(value)
                self.send_command_to_motor(altDisplayText, motor=motor, command=SET_THERMAL_COEFF, value=value)

            return True

        else:
            return False


    def clear_motor_registers(self):

        self.TMC_motor[TMC_X1].reset_registers()
        self.TMC_motor[TMC_X2].reset_registers()
        self.TMC_motor[TMC_Y1].reset_registers()
        self.TMC_motor[TMC_Y2].reset_registers()
        self.TMC_motor[TMC_Z].reset_registers()


    def TMC_registers_have_been_read_in(self):

        if not self.TMC_motor[TMC_X1].got_registers: return False
        if not self.TMC_motor[TMC_X2].got_registers: return False
        if not self.TMC_motor[TMC_Y1].got_registers: return False
        if not self.TMC_motor[TMC_Y2].got_registers: return False
        if not self.TMC_motor[TMC_Z].got_registers: return False
        return True

    def calibration_coefficients_have_been_read_in(self):
        if not self.TMC_motor[TMC_X1].got_calibration_coefficients: return False
        if not self.TMC_motor[TMC_X2].got_calibration_coefficients: return False
        if not self.TMC_motor[TMC_Y1].got_calibration_coefficients: return False
        if not self.TMC_motor[TMC_Y2].got_calibration_coefficients: return False
        if not self.TMC_motor[TMC_Z].got_calibration_coefficients: return False
        return True

    def store_tmc_params_in_eeprom(self):
        self.send_command_to_motor("STORE TMC PARAMS IN EEPROM", command = STORE_TMC_PARAMS)
        time.sleep(1)

    def store_tmc_params_in_eeprom_and_handshake(self):
        self.store_tmc_params_in_eeprom()
        self.tmc_handshake()
        time.sleep(1)


    ## FIRMWARE UPDATES

    def hard_reset_pcb_sequence(self):

        try:
            pi = pigpio.pi()
            pi.stop()

        except:
            Logger.exception("Check pigpio daemon!")
            return False

        # Functions that use this function will need to check that serial comms has finished reconnecting after
        self.stop_serial_comms()
        toggle_outcome = self.toggle_reset_pin()
        self.do_connection()
        return toggle_outcome

    def toggle_reset_pin(self):

        try:

            pi = pigpio.pi()
            if int(pi.get_mode(17)) != 7:
                if not self.set_mode_of_reset_pin(): return False
            time.sleep(0.5)
            original_setting = pi.read(17)
            pi.write(17,int(not original_setting))
            time.sleep(1)
            new_setting = pi.read(17)
            pi.write(17,int(original_setting))
            restored_setting = pi.read(17)
            Logger.info("Toggled 17 to " + str(int(not original_setting)) + " and back to " + str(int(original_setting)))
            pi.stop()
            time.sleep(1)
            return int(original_setting) == int(restored_setting) == int(not new_setting)

        except:
            Logger.exception("Couldn't toggle reset pin, maybe check the pigio daemon?")
            return False

    def set_mode_of_reset_pin(self):

        try:
            # Toggle reset pin
            pi = pigpio.pi()
            pi.set_mode(17, pigpio.ALT3)
            new_pin_mode = int(pi.get_mode(17))
            Logger.info("Set GPIO 17 to mode ALT3: " + str(new_pin_mode))
            pi.stop()

            if new_pin_mode == 7: return True
            else: return False

        except:
            Logger.exception("Couldn't set mode of reset pin, maybe check the pigio daemon?")
            return False


    def stop_serial_comms(self):

        while self.state() != "Off": # yes, this is naughty.
            self.s.grbl_scanner_running = False
            time.sleep(0.2)
        self.close_serial_connection(0)
        time.sleep(0.5)

    def do_connection(self):

        self.reconnect_serial_connection()
        self.poll_for_reconnection = Clock.schedule_interval(self.try_start_services, 0.4)

    def try_start_services(self, dt):
        if self.s.is_connected():
            Clock.unschedule(self.poll_for_reconnection)
            Clock.schedule_once(self.s.start_services, 1)


    ## MEASURING STATUS DATA

    def measured_running_data(self):
        if not self.s.measure_running_data and self.s.running_data:
            return self.s.running_data

        else:
            return False

    def start_measuring_running_data(self, stage = 0):
        self.s.running_data = []
        self.s.measurement_stage = stage
        self.s.measure_running_data = True

    def stop_measuring_running_data(self):
        self.s.measure_running_data = False

    def continue_measuring_running_data(self):
        self.s.measure_running_data = True

    def change_stage_measuring_running_data(self, stage):
        self.s.measurement_stage = stage

    def clear_measured_running_data(self):
        self.s.measure_running_data = False
        self.s.running_data = []
