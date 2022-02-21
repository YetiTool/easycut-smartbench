'''
Created on 31 Jan 2018
@author: Ed
This module defines the machine's properties (e.g. travel), services (e.g. serial comms) and functions (e.g. move left)
'''

import logging, threading, re

from asmcnc.comms import serial_connection  # @UnresolvedImport
from asmcnc.comms.yeti_grbl_protocol import protocol
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from asmcnc.comms import motors

from kivy.clock import Clock
import sys, os, time
from datetime import datetime
import os.path
from os import path

from __builtin__ import True
from kivy.uix.switch import Switch
from pickle import TRUE

from asmcnc.skavaUI import popup_info


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))


class RouterMachine(object):

# SETUP
    
    s = None # serial object

    # This block of variables reflecting grbl settings (when '$$' is issued, serial reads settings and syncs these params)
    grbl_x_max_travel = 1500.0 # measured from true home
    grbl_y_max_travel = 3000.0 # measured from true home
    grbl_z_max_travel = 300.0 # measured from true home
    
    # how close do we allow the machine to get to its limit switches when requesting a move (so as not to accidentally trip them)
    # note this an internal UI setting, it is NOT grbl pulloff ($27)
    limit_switch_safety_distance = 1.0

    is_machine_completed_the_initial_squaring_decision = False
    is_machine_homed = False # status on powerup
    is_squaring_XY_needed_after_homing = True # starts True, therefore squares on powerup. Switched to false after initial home, so as not to repeat on next home.

    is_machine_paused = False

    # empty dictionary to hold TMC motors
    TMC_motor = {}


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
    device_label_file_path = '../../smartbench_name.txt' # this puts it above EC folder in filesystem
    device_location_file_path = '../../smartbench_location.txt' # this puts it above EC folder in filesystem

    ## LOCALIZATION
    persistent_language_path = smartbench_values_dir + 'user_language.txt'

    ## PROBE SETTINGS
    z_lift_after_probing = 20.0
    z_probe_speed = 60
    z_touch_plate_thickness = 1.53

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

    ## STYLUS SETTINGS
    is_stylus_enabled = True
    stylus_router_choice = 'router'

    ## BRUSH VALUES
    spindle_brush_use_seconds = 0
    spindle_brush_lifetime_seconds = float(120*3600)

    ## SPINDLE COOLDOWN OPTIONS
    spindle_brand = 'YETI' # String to hold brand name
    spindle_voltage = 230 # Options are 230V or 110V
    spindle_digital = True #spindle can be manual or digital
    spindle_cooldown_time_seconds = 10 # YETI value is 10 seconds
    spindle_cooldown_rpm = 12000 # YETI default value was 20k, but has been lowered to 12k
    
    amb_cooldown_rpm_default = 10000
    yeti_cooldown_rpm_default = 12000
    spindle_cooldown_rpm_override = False



    ## DEVICE LABEL
    device_label = "My SmartBench" #TODO needs tying to machine unique ID else all machines will refence this dataseries

    ## DEVICE LOCATION
    device_location = 'SmartBench location'

    reminders_enabled = True

    trigger_setup = False

    def __init__(self, win_serial_port, screen_manager, settings_manager, localization, job):

        self.sm = screen_manager
        self.sett = settings_manager
        self.l = localization
        self.jd = job
        self.set_jog_limits()

        # Establish 's'erial comms and initialise
        self.s = serial_connection.SerialConnection(self, self.sm, self.sett, self.l, self.jd)
        self.s.establish_connection(win_serial_port)

        # Object to construct and send custom YETI GRBL commands
        self.p = protocol.protocol_v2()

        # initialise sb_value files if they don't already exist (to record persistent maintenance values)
        self.check_presence_of_sb_values_files()
        self.get_persistent_values()

        # initialise all motors
        self.TMC_motor[TMC_X1] = motors.motor_class(TMC_X1)
        self.TMC_motor[TMC_X2] = motors.motor_class(TMC_X2)
        self.TMC_motor[TMC_Y1] = motors.motor_class(TMC_Y1)
        self.TMC_motor[TMC_Y2] = motors.motor_class(TMC_Y2)
        self.TMC_motor[TMC_Z] = motors.motor_class(TMC_Z)

# PERSISTENT MACHINE VALUES
    def check_presence_of_sb_values_files(self):

        # check folder exists
        if not path.exists(self.smartbench_values_dir):
            log("Creating sb_values dir...")
            os.mkdir(self.smartbench_values_dir)

        if not path.exists(self.set_up_options_file_path):
            log("Creating set up options file...")
            file = open(self.set_up_options_file_path, "w+")
            file.write(str(self.trigger_setup))
            file.close()

        if not path.exists(self.z_touch_plate_thickness_file_path):
            log("Creating z touch plate thickness file...")
            file = open(self.z_touch_plate_thickness_file_path, "w+")
            file.write(str(self.z_touch_plate_thickness))
            file.close()

        if not path.exists(self.z_head_laser_offset_file_path):
            log("Creating z head laser offset file...")
            file = open(self.z_head_laser_offset_file_path, "w+")
            file.write('False' + "\n" + "0" + "\n" + "0")
            file.close()

        if not path.exists(self.spindle_brush_values_file_path):
            log("Creating spindle brush values file...")
            file = open(self.spindle_brush_values_file_path, "w+")
            file.write(str(self.spindle_brush_use_seconds) + "\n" + str(self.spindle_brush_lifetime_seconds))
            file.close()

        if not path.exists(self.spindle_cooldown_rpm_override_file_path):
            log("Creating spindle cooldown_rpm override settings file...")
            file = open(self.spindle_cooldown_rpm_override_file_path, "w+")
            file.write(str(self.spindle_cooldown_rpm_override))
            file.close()

        if not path.exists(self.spindle_cooldown_settings_file_path):
            log("Creating spindle cooldown settings file...")
            file = open(self.spindle_cooldown_settings_file_path, "w+")
            file.write(
                str(self.spindle_brand) + "\n" + 
                str(self.spindle_voltage) + "\n" + 
                str(self.spindle_digital) + "\n" + 
                str(self.spindle_cooldown_time_seconds) + "\n" +
                str(self.spindle_cooldown_rpm)
                )
            file.close()

        if not path.exists(self.stylus_settings_file_path):
            log("Creating stylus settings file...")
            file = open(self.stylus_settings_file_path, "w+")
            file.write(str(self.is_stylus_enabled))
            file.close()

        if not path.exists(self.calibration_settings_file_path):
            log('Creating calibration settings file...')
            file = open(self.calibration_settings_file_path, 'w+')
            file.write(str(self.time_since_calibration_seconds) + "\n" + str(self.time_to_remind_user_to_calibrate_seconds))
            file.close()

        if not path.exists(self.z_head_maintenance_settings_file_path):
            log('Creating z head maintenance settings file...')
            file = open(self.z_head_maintenance_settings_file_path, 'w+')
            file.write(str(self.time_since_z_head_lubricated_seconds))
            file.close()

        if not path.exists(self.device_label_file_path):
            log('Creating device label settings file...')
            file = open(self.device_label_file_path, 'w+')
            file.write(str(self.device_label))
            file.close()

        if not path.exists(self.device_location_file_path):
            log('Creating device location settings file...')
            file = open(self.device_location_file_path, 'w+')
            file.write(str(self.device_location))

        if not path.exists(self.persistent_language_path):
            log("Creating language settings file")
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
        self.read_device_label()
        self.read_device_location()


    ## SET UP OPTIONS
    def read_set_up_options(self):
        try: 
            file = open(self.set_up_options_file_path, 'r')
            trigger_bool_string  = str(file.read())
            file.close()

            if trigger_bool_string == 'False' or trigger_bool_string == False: self.trigger_setup = False
            else: self.trigger_setup = True

            log("Read in set up options")
            return True

        except:
            log("Unable to read in set up options")
            return False

    def write_set_up_options(self, value):

        try:
            file = open(self.set_up_options_file_path, 'w+')
            file.write(str(value))
            file.close()

            self.trigger_setup = value
            log("set up options written to file")
            return True

        except:
            log("Unable to write set up options")
            return False


    ## TOUCH PLATE THICKENESS
    def read_z_touch_plate_thickness(self):

        try: 
            file = open(self.z_touch_plate_thickness_file_path, 'r')
            self.z_touch_plate_thickness  = float(file.read())
            file.close()

            log("Read in z touch plate thickness")
            return True

        except:
            log("Unable to read in z touch plate thickness")
            return False

    def write_z_touch_plate_thickness(self, value):

        try:
            file = open(self.z_touch_plate_thickness_file_path, 'w+')
            file.write(str(value))
            file.close()

            self.z_touch_plate_thickness = float(value)
            log("z touch plate thickness written to file")
            return True

        except:
            log("Unable to write z touch plate thickness")
            return False


    ## CALIBRATION SETTINGS

    def read_calibration_settings(self):

        try: 
            file = open(self.calibration_settings_file_path, 'r')
            [read_time_since_calibration_seconds, read_time_to_remind_user_to_calibrate_seconds]  = file.read().splitlines()
            file.close()

            self.time_since_calibration_seconds = float(read_time_since_calibration_seconds)
            self.time_to_remind_user_to_calibrate_seconds = float(read_time_to_remind_user_to_calibrate_seconds)

            log("Read in calibration settings")
            return True

        except:
            log("Unable to read calibration settings")
            return False

    def write_calibration_settings(self, since_calibration, remind_time):

        try:
            file = open(self.calibration_settings_file_path, 'w+')
            file.write(str(since_calibration) + "\n" + str(remind_time))
            file.close()

            self.time_since_calibration_seconds = float(since_calibration)
            self.time_to_remind_user_to_calibrate_seconds = float(remind_time)
            log("calibration settings written to file")
            return True

        except:
            log("Unable to write calibration settings")
            return False

    ## Z HEAD MAINTENANCE SETTINGS REMINDER

    def read_z_head_maintenance_settings(self):

        try: 
            file = open(self.z_head_maintenance_settings_file_path, 'r')
            self.time_since_z_head_lubricated_seconds  = float(file.read())
            file.close()

            log("Read in z head maintenance settings")
            return True

        except: 
            log("Unable to read z head maintenance settings")
            return False

    def write_z_head_maintenance_settings(self, value):

        try:
            file = open(self.z_head_maintenance_settings_file_path, 'w+')
            file.write(str(value))
            file.close()

            self.time_since_z_head_lubricated_seconds = float(value)

            log("Write z head maintenance settings")
            return True

        except: 
            log("Unable to write z head maintenance settings")
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


            log("Read in z head laser offset values")
            return True

        except: 
            log("Unable to read z head laser offset values") 
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
            log("Unable to write z head laser offset values")
            return False

    ## SPINDLE BRUSH MONITOR
    def read_spindle_brush_values(self):

        try:
            file = open(self.spindle_brush_values_file_path, 'r')
            read_brush = file.read().splitlines()
            file.close()

            self.spindle_brush_use_seconds = float(read_brush[0])
            self.spindle_brush_lifetime_seconds = float(read_brush[1])

            log("Read in spindle brush use and lifetime")
            return True

        except: 

            log("Unable to read spindle brush use and lifetime values")
            return False

    def write_spindle_brush_values(self, use, lifetime):
        try:
            file = open(self.spindle_brush_values_file_path, "w")
            file.write(str(use) + "\n" + str(lifetime))
            file.close()

            self.spindle_brush_use_seconds = float(use)
            self.spindle_brush_lifetime_seconds = float(lifetime)

            log("Spindle brush use and lifetime written to file")
            return True

        except: 
            log("Unable to write spindle brush use and lifetime values")
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

            log("Read in spindle cooldown override settings")
            return True

        except: 
            log("Unable to read spindle cooldown override settings")
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

            log("Spindle cooldown override settings written to file")
            return True

        except: 
            log("Unable to write spindle cooldown override settings")
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

            log("Read in spindle cooldown settings")
            return True

        except: 
            log("Unable to read spindle cooldown settings")
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

            log("Spindle cooldown settings written to file")
            return True

        except: 
            log("Unable to write spindle cooldown settings")
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

            log("Read in stylus settings")
            return True

        except: 
            log("Unable to read stylus settings")
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

            log("Stylus settings written to file")
            return True

        except: 
            log("Unable to write stylus settings")
            return False

    ## DEVICE LABEL
    def read_device_label(self):

        try:
            file = open(self.device_label_file_path, 'r')
            self.device_label = str(file.read())
            file.close()

            log("Read in device label")
            return True

        except:
            log("Unable to read device label")
            return False

    def write_device_label(self, value):

        try:
            file = open(self.device_label_file_path, 'w+')
            file.write(str(value))
            file.close()

            self.device_label = str(value)
            log("device label written to file")
            return True

        except:
            log("Unable to write device label")
            return False

    ## DEVICE LOCATION
    def read_device_location(self):

        try:
            file = open(self.device_location_file_path, 'r')
            self.device_location = str(file.read())
            file.close()

            log("Read in device location")
            return True

        except:
            log("Unable to read device location")
            return False

    def write_device_location(self, value):

        try:
            file = open(self.device_location_file_path, 'w+')
            file.write(str(value))
            file.close()

            self.device_location = str(value)
            log("Device location written to file")
            return True

        except:
            log("Unable to write device location")
            return False

# GRBL SETTINGS
    def write_dollar_50_setting(self, serial_number):
        dollar_50_setting = [
                            '$50=' + str(serial_number),
                            '$$'
                            ]
        self.s.start_sequential_stream(dollar_50_setting, reset_grbl_after_stream=True)

    def bake_default_grbl_settings(self): # move to machine module
        grbl_settings = [
                    '$0=10',          #Step pulse, microseconds
                    '$1=255',         #Step idle delay, milliseconds
                    '$2=4',           #Step port invert, mask
                    '$3=1',           #Direction port invert, mask
                    '$4=0',           #Step enable invert, boolean
                    '$5=1',           #Limit pins invert, boolean
                    '$6=0',           #Probe pin invert, boolean
                    '$10=3',          #Status report, mask <----------------------
                    '$11=0.010',      #Junction deviation, mm
                    '$12=0.002',      #Arc tolerance, mm
                    '$13=0',          #Report inches, boolean
                    '$20=1',          #Soft limits, boolean <-------------------
                    '$21=1',          #Hard limits, boolean <------------------
                    '$22=1',          #Homing cycle, boolean <------------------------
                    '$23=3',          #Homing dir invert, mask
                    '$24=600.0',      #Homing feed, mm/min
                    '$25=3000.0',     #Homing seek, mm/min
                    '$26=250',        #Homing debounce, milliseconds
                    '$27=15.000',     #Homing pull-off, mm
                    '$30=25000.0',    #Max spindle speed, RPM
                    '$31=0.0',        #Min spindle speed, RPM
                    '$32=0',          #Laser mode, boolean
#                     '$100=56.649',    #X steps/mm
#                     '$101=56.665',    #Y steps/mm
#                     '$102=1066.667',  #Z steps/mm
                    '$110=8000.0',    #X Max rate, mm/min
                    '$111=6000.0',    #Y Max rate, mm/min
                    '$112=750.0',     #Z Max rate, mm/min
                    '$120=130.0',     #X Acceleration, mm/sec^2
                    '$121=130.0',     #Y Acceleration, mm/sec^2
                    '$122=200.0',     #Z Acceleration, mm/sec^2
                    '$130=1300.0',    #X Max travel, mm TODO: Link to a settings object
                    '$131=2502.0',    #Y Max travel, mm
                    '$132=150.0',     #Z Max travel, mm
                    '$$',             # Echo grbl settings, which will be read by sw, and internal parameters sync'd
                    '$#'              # Echo grbl parameter info, which will be read by sw, and internal parameters sync'd
            ]

        self.s.start_sequential_stream(grbl_settings, reset_grbl_after_stream=True)   # Send any grbl specific parameters

    def save_grbl_settings(self): # move to machine module

        self.send_any_gcode_command("$$")
        self.send_any_gcode_command("$#")

        try: self.s.setting_50
        except:
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
                        '$32=' + str(self.s.setting_32),           #Laser mode, boolean
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
        else:
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
                        '$32=' + str(self.s.setting_32),           #Laser mode, boolean
                        '$50=' + str(self.s.setting_50),     #Yeti custom serial number
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
        log('Saved grbl settings to file')

    def restore_grbl_settings_from_file(self, filename):

        try: 
            fileobject = open(filename, 'r')
            settings_to_restore = (fileobject.read()).split('\n')
            self.s.start_sequential_stream(settings_to_restore)   # Send any grbl specific parameters
            Clock.schedule_once(lambda dt: self.send_any_gcode_command("$$"), 1)
            Clock.schedule_once(lambda dt: self.send_any_gcode_command("$#"), 2)
            return True

        except:
            log('Could not read from file')
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


# HW/FW VERSION CAPABILITY

    def fw_can_operate_digital_spindle(self):
        # log("FW version to operate digital spindles doesn't exist yet, but it's coming!")
        return False

    # def fw_can_operate_laser_commands(self):
    #     output = self.is_machines_fw_version_equal_to_or_greater_than_version('1.1.2', 'laser commands AX and AZ')
    #     log('FW version able to operate laser commands AX and AZ: ' + str(output))
    #     return output      

    def hw_can_operate_laser_commands(self):
        output = self.is_machines_hw_version_equal_to_or_greater_than_version(8, 'laser commands AX and AZ') # Update to version 8, but need 6 to test on rig
        log('HW version able to operate laser commands AX and AZ: ' + str(output))
        return output


    def fw_can_operate_zUp_on_pause(self):

        log('FW version able to lift on pause: ' + str(self.is_machines_fw_version_equal_to_or_greater_than_version('1.0.13', 'Z up on pause')))
        return self.is_machines_fw_version_equal_to_or_greater_than_version('1.0.13', 'Z up on pause')
    

    def is_machines_fw_version_equal_to_or_greater_than_version(self, version_to_reference, capability_decription):  # ref_version_parts syntax "x.x.x"
        
        if sys.platform != 'win32' and sys.platform != 'darwin':

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
                log(error_description)

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

        else: return False

    def is_machines_hw_version_equal_to_or_greater_than_version(self, version_to_reference, capability_decription): 
        
        if sys.platform != 'win32' and sys.platform != 'darwin':
            try:
                if float(self.s.hw_version) >= version_to_reference:
                    return True
                else:
                    return False
            
            except:
                error_description = "Couldn't process machine hardware value when checking capability: " + str(capability_decription) + \
                ".\n\n Please check Z Head connection."
                log(error_description)

                return False

        else: return False

# HW/FW ADJUSTMENTS

    # Functions to convert spindle RPMs if using a 110V spindle
    # 'red' refers to 230V line (which is what electronics thinks spindle will be regardless of actual HW)
    # 'green' refers to 110V line

    def convert_from_110_to_230(self, rpm_green):
        if float(rpm_green) != 0:
            v_green = (float(rpm_green) - 9375)/1562.5
            rpm_red = (2187.5*float(v_green)) + 3125
            return float(rpm_red)
        else: return 0

    def convert_from_230_to_110(self, rpm_red):
        if float(rpm_red) != 0:
            v_red = (float(rpm_red) - 3125)/2187.5
            rpm_green = (1562.5*float(v_red)) + 9375
            return float(rpm_green)
        else: return 0

# START UP SEQUENCES

    # BOOT UP SEQUENCE
    def bootup_sequence(self):
        log("Boot up machine, and get settings...")
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
    ## NEEDS TESTING
    handshake_event = None

    def tmc_handshake(self):

        if self.s.fw_version:

            if self.handshake_event: Clock.unschedule(self.handshake_event)

            if self.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'get TMC registers'):
                self.send_command_to_motor("GET REGISTERS", command=GET_REGISTERS)

        else: 
            # In case handshake is too soon, it keeps trying until it can read a FW version
            self.handshake_event = Clock.schedule_interval(lambda dt: self.tmc_handshake(), 1)

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
        Clock.schedule_once(lambda dt: self.vac_off(), 2.0)
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
        
    def stop_for_a_stream_pause(self):
        self.set_pause(True)
        self._grbl_door() # send a soft-door command

    def resume_after_a_stream_pause(self):
        self._grbl_resume()        
        Clock.schedule_once(lambda dt: self.set_pause(False),0.3)

    def set_pause(self, pauseBool):

        prev_state = self.is_machine_paused
        self.is_machine_paused = pauseBool # sets serial_connection flag to pause (allows a hard door to be detected)

        def record_pause_time(prev_state, pauseBool):
            # record pause time
            if prev_state == False and pauseBool == True:
                self.s.stream_pause_start_time = time.time()

            if prev_state == True and pauseBool == False and self.s.stream_pause_start_time != 0:
                self.s.stream_paused_accumulated_time = self.s.stream_paused_accumulated_time + (time.time() - self.s.stream_pause_start_time)
                self.s.stream_pause_start_time = 0

        Clock.schedule_once(lambda dt: record_pause_time(prev_state, pauseBool), 0.2)

    def stop_from_soft_stop_cancel(self):
        self.resume_from_alarm() 
        Clock.schedule_once(lambda dt: self.set_pause(False),0.6) 

    def resume_from_a_soft_door(self):
        self._grbl_resume()
        Clock.schedule_once(lambda dt: self.set_pause(False),0.4)

    def resume_after_a_hard_door(self):
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
        log('Streaming stopped.')
        if self.s.is_job_streaming == True: self.s.cancel_stream()
        if self.s.is_sequential_streaming == True: self.s.cancel_sequential_stream() # Cancel sequential stream to stop it continuing to send stuff after reset

    def _grbl_resume(self):
        log('grbl realtime cmd sent: ~ resume')
        self.s.write_realtime('~', altDisplayText = 'Resume')

    def _grbl_feed_hold(self):
        log('grbl realtime cmd sent: ! feed-hold')
        self.s.write_realtime('!', altDisplayText = 'Feed hold')

    def _grbl_soft_reset(self):
        log('grbl realtime cmd sent: \\x18 soft reset')
        self.s.write_realtime("\x18", altDisplayText = 'Soft reset')

    def _grbl_door(self):
        log('grbl realtime cmd sent: \\x84')
        self.s.write_realtime('\x84', altDisplayText = 'Door')
    
    def _grbl_unlock(self):
        log('grbl realtime cmd sent: $X unlock')
        self.s.write_command('$X', altDisplayText = 'Unlock: $X')


# COMMS

    def is_connected(self): return self.s.is_connected()
    def is_job_streaming(self): return self.s.is_job_streaming
    def state(self): return self.s.m_state
    def buffer_capacity(self): return self.s.serial_blocks_available


    def set_state(self, temp_state):
        grbl_state_words = ['Idle', 'Run', 'Hold', 'Jog', 'Alarm', 'Door', 'Check', 'Home', 'Sleep']
        if temp_state in grbl_state_words:
            self.s.m_state = temp_state

    def get_grbl_status(self):
        self.s.write_command('$#')

    def get_grbl_settings(self):
        self.s.write_command('$$')
        
    def send_any_gcode_command(self, gcode):
        self.s.write_command(gcode)
    
    def enable_check_mode(self):
        self._grbl_soft_reset()
        if self.s.m_state != "Check":
            Clock.schedule_once(lambda dt: self.s.write_command('$C', altDisplayText = 'Check mode ON'), 0.6)
        else:
            log('Check mode already enabled')

    def disable_check_mode(self):
        if self.s.m_state == "Check":
            self.s.write_command('$C', altDisplayText = 'Check mode OFF')
        else:
            log('Check mode already disabled')
        Clock.schedule_once(lambda dt: self._grbl_soft_reset(), 0.1)

    def get_switch_states(self):
        
        switch_states = []
        
        if self.s.limit_x == True: switch_states.append('limit_x') # convention: min is lower_case
        if self.s.limit_X == True: switch_states.append('limit_X') # convention: MAX is UPPER_CASE
        if self.s.limit_y == True: switch_states.append('limit_y')   
        if self.s.limit_Y == True: switch_states.append('limit_Y') 
        if self.s.limit_z == True: switch_states.append('limit_z') 
        if self.s.probe == True: switch_states.append('probe') 
        if self.s.dust_shoe_cover == True: switch_states.append('dust_shoe_cover') 
        if self.s.spare_door == True: switch_states.append('spare_door')
        
        return switch_states 
    
    def disable_limit_switches(self):

        #turn soft limits, hard limts OFF
        print 'switching soft limits & hard limts OFF'
        settings = ['$22=0','$20=0','$21=0']
        self.s.start_sequential_stream(settings)
    
    def enable_limit_switches(self):

        #turn soft limits, hard limts OFF
        print 'switching soft limits & hard limts ON'
        settings = ['$22=1','$20=1','$21=1']
        self.s.start_sequential_stream(settings)

# SETTINGS GETTERS
    def serial_number(self): 
        try: self.s.setting_50
        except: return 0
        else: return self.s.setting_50

    def z_head_version(self):
        try: self.s.setting_50
        except: return 0
        else: return str(self.s.setting_50)[-2] + str(self.s.setting_50)[-1]

# POSITONAL GETTERS            
        
    def x_pos_str(self): return self.s.m_x
    def y_pos_str(self): return self.s.m_y
    def z_pos_str(self): return self.s.m_z

    # 'Machine position'/mpos is the absolute position of the tooltip, wrt home
    def mpos_x(self): return float(self.s.m_x)
    def mpos_y(self): return float(self.s.m_y)
    def mpos_z(self): return float(self.s.m_z)
    
    # 'Work position'/wpos is the position of the tooltip relative to the datum position set for the job
    # WPos = MPos - WCO.
    def wpos_x(self): return float(self.s.m_x) - self.x_wco()
    def wpos_y(self): return float(self.s.m_y) - self.y_wco()
    def wpos_z(self): return float(self.s.m_z) - self.z_wco()
    
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

    def spindle_speed(self): 
        if self.spindle_voltage == 110: 
            # if not self.spindle_digital or not self.fw_can_operate_digital_spindle(): # this is only relevant much later on
            converted_speed = self.convert_from_230_to_110(self.s.spindle_speed)
            return int(converted_speed)
        else: 
            return int(self.s.spindle_speed)

    def spindle_load(self): 
        try:
            return int(self.s.spindle_load_voltage)
        except:
            return ''

# POSITIONAL SETTERS

    def set_workzone_to_pos_xy(self):
        self.s.write_command('G10 L20 P1 X0 Y0')
        Clock.schedule_once(lambda dt: self.strobe_led_playlist("datum_has_been_set"), 0.2)

    def set_x_datum(self):
        self.s.write_command('G10 L20 P1 X0')
        Clock.schedule_once(lambda dt: self.strobe_led_playlist("datum_has_been_set"), 0.2)

    def set_y_datum(self):
        self.s.write_command('G10 L20 P1 Y0')
        Clock.schedule_once(lambda dt: self.strobe_led_playlist("datum_has_been_set"), 0.2)

    def set_workzone_to_pos_xy_with_laser(self):
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
        self.s.write_command('G10 L20 P1 Z0')
        Clock.schedule_once(lambda dt: self.strobe_led_playlist("datum_has_been_set"), 0.2)
        self.get_grbl_status()

    def set_standby_to_pos(self):
        self.s.write_command('G28.1')
        Clock.schedule_once(lambda dt: self.strobe_led_playlist("standby_pos_has_been_set"), 0.2)

    

# MOVEMENT/ACTION

    def jog_absolute_single_axis(self, axis, target, speed):
        self.s.write_command('$J=G53 ' + axis + str(target) + ' F' + str(speed))
    
    def jog_absolute_xy(self, x_target, y_target, speed):
        self.s.write_command('$J=G53 X' + str(x_target) + ' Y' + str(y_target) + ' F' + str(speed))  
 
    def jog_relative(self, axis, dist, speed):
        self.s.write_command('$J=G91 ' + axis + str(dist) + ' F' + str(speed))
    
    def quit_jog(self):
        self.s.write_realtime('\x85', altDisplayText = 'Quit jog')

    def spindle_on(self):
        self.s.write_command('M3 S25000')
    
    def spindle_off(self):
        self.s.write_command('M5')

    def cooldown_zUp_and_spindle_on(self):
        self.s.write_command('AE')
        if self.spindle_voltage == 230:
            self.s.write_command('M3 S' + str(self.spindle_cooldown_rpm))
        else:
            cooldown_rpm = self.convert_from_110_to_230(self.spindle_cooldown_rpm)
            self.s.write_command('M3 S' + str(cooldown_rpm))
        self.zUp()

    def laser_on(self):
        if self.is_laser_enabled == True: 

            if self.hw_can_operate_laser_commands():
                self.s.write_command('AZ')
            self.set_led_colour('BLUE')

            self.is_laser_on = True

    def laser_off(self, bootup=False):
        self.is_laser_on = False
        if self.hw_can_operate_laser_commands():
            self.s.write_command('AX')
        if bootup == True:
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
        
    def zUp(self):
        self.s.write_command('G0 G53 Z-' + str(self.s.setting_27))

    def vac_on(self):
        self.s.write_command('AE')

    def vac_off(self):
        self.s.write_command('AF')

    def go_x_datum(self):
        self.s.write_command('G0 G53 Z-' + str(self.limit_switch_safety_distance))
        self.s.write_command('G4 P0.1')
        self.s.write_command('G0 G54 X0')
 
    def go_y_datum(self):
        self.s.write_command('G0 G53 Z-' + str(self.limit_switch_safety_distance))
        self.s.write_command('G4 P0.1')
        self.s.write_command('G0 G54 Y0')

    def jog_spindle_to_laser_datum(self, axis):

        if axis == 'X' or axis == 'XY' or axis == 'YX':

            # Keep this is for beta testing, as 
            print("Laser offset value: " + str(self.laser_offset_x_value))
            print("Pos value: " + str(self.mpos_x()))

            print("Try to move to: " + str(self.mpos_x() + float(self.laser_offset_x_value)))
            print("Limit at: " + str(float(self.x_min_jog_abs_limit)))

            # Check that movement is within bounds before jogging
            if (self.mpos_x() + float(self.laser_offset_x_value) <= float(self.x_max_jog_abs_limit)
            and self.mpos_x() + float(self.laser_offset_x_value) >= float(self.x_min_jog_abs_limit)):

                self.jog_relative('X', self.laser_offset_x_value, 6000.0)

            else: return False

        if axis == 'Y' or axis == 'XY' or axis == 'YX':
            # Check that movement is within bounds before jogging
            if (self.mpos_y() + float(self.laser_offset_y_value) <= float(self.y_max_jog_abs_limit)
            and self.mpos_y() + float(self.laser_offset_y_value) >= float(self.y_min_jog_abs_limit)):

                self.jog_relative('Y', self.laser_offset_y_value, 6000.0)

            else: return False

        return True

    # Realtime XYZ feed adjustment
    def feed_override_reset(self):
        self.s.write_realtime('\x90', altDisplayText = 'Feed override RESET')

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

        
# HOMING

    # ensure that return and cancel args match the names of the screen names defined in the screen manager
    def request_homing_procedure(self, return_to_screen_str, cancel_to_screen_str):

        self.sm.get_screen('squaring_decision').return_to_screen = return_to_screen_str
        self.sm.get_screen('squaring_decision').cancel_to_screen = cancel_to_screen_str
        self.sm.current = 'squaring_decision'


    # Home the Z axis by moving the cutter down until it touches the probe.
    # On touching, electrical contact is made, detected, and WPos Z0 set, factoring in probe plate thickness.
    def probe_z(self):

        if self.state() == 'Idle':
            self.set_led_colour("WHITE")
            self.s.expecting_probe_result = True
            probeZTarget =  -(self.grbl_z_max_travel) - self.mpos_z() + 0.1 # 0.1 added to prevent rounding error triggering soft limit
            self.s.write_command('G91 G38.2 Z' + str(probeZTarget) + ' F' + str(self.z_probe_speed))
            self.s.write_command('G90')
            # Serial module then looks for probe detection
            # On detection "probe_z_detection_event" is called (for a single immediate EEPROM write command)....
            # ... followed by a delayed call to "probe_z_post_operation" for any post-write actions.


    def probe_z_detection_event(self, z_machine_coord_when_probed):

        self.s.write_command('G90 G1 G53 Z' + z_machine_coord_when_probed)
        self.s.write_command('G4 P0.5') 
        self.s.write_command('G10 L20 P1 Z' + str(self.z_touch_plate_thickness))
        self.s.write_command('G4 P0.5') 
        Clock.schedule_once(lambda dt: self.strobe_led_playlist("datum_has_been_set"), 0.5)
        self.zUp()    



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
         
        else: print ("LED Colour denied because streaming: " + colour_name + "\n")


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

        else: print "Strobe situation: " + situation + " not recognised"
            
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
                log("Sending command to motor: " + str(motor) + ", cmd: " + str(cmd) + ", val: " + hex(val))

        else:
            # throw an error, command is not valid
            log("ERROR: unknown command in send_command_to_motor: " + str(motor) + ", cmd: " + str(command) + ", val: " + hex(value))

        return out

    def setShadowReg(self, motor, register, value, mask, shift):
        self.TMC_motor[motor].shadowRegisters[register] = self.TMC_motor[motor].shadowRegisters[register] & ~ (           mask   << shift) #clear
        self.TMC_motor[motor].shadowRegisters[register] = self.TMC_motor[motor].shadowRegisters[register] |   ( ( value & mask ) << shift) #set
        return self.TMC_motor[motor].shadowRegisters[register]

    #####################################################################
    # CALIBRATION AND TUNNING PROCEDURES
    #####################################################################

    # CALL THESE FROM MAIN APP

    # QUERY THIS FLAG AFTER CALLING TUNING FUNCTIONS, TO SEE IF TUNING HAS FINISHED
    tuning_in_progress = False

    def tune_X_and_Z_for_calibration(self):

        self.tuning_in_progress = True
        log("Tuning X and Z...")
        self.prepare_for_tuning()
        # THEN JOG AWAY AT MAX SPEED
        log("Jog to check SG values")
        self.tuning_jog_forwards_fast(X = True, Y = False, Z = True)
        self.check_SGs_rezero_and_go_to_next_checks_then_tune(X = True, Y = False, Z = True)

    def tune_Y_for_calibration(self):

        self.tuning_in_progress = True
        log("Tuning Y...")
        self.prepare_for_tuning()
        # THEN JOG AWAY AT MAX SPEED
        log("Jog to check SG values")
        self.tuning_jog_forwards_fast(X = False, Y = True, Z = False)
        self.check_SGs_rezero_and_go_to_next_checks_then_tune(X = False, Y = True, Z = False)

    # QUERY THIS FLAG AFTER CALLING CALIBRATION FUNCTIONS, TO SEE IF CALIBRATION HAS FINISHED
    run_calibration = False

    def calibrate_X_and_Z(self):

        self.run_calibration = True
        log("Calibrating X and Z...")
        self.initialise_calibration(X = True, Y = False, Z = True)

    def calibrate_Y(self):

        self.run_calibration = True
        log("Calibrating Y...")
        self.initialise_calibration(X = False, Y = True, Z = False)


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

    temp_toff = 2
    temp_sgt = 0

    toff_max = 10 # 10
    sgt_max = 20 # 20

    reference_temp = 45.0


    def reset_tuning_flags(self):

        log("Reset tuning flags")

        self.toff_and_sgt_found = False
        self.tuning_poll = None
        self.x_toff_tuned = None
        self.x_sgt_tuned = None
        self.y1_toff_tuned = None
        self.y1_sgt_tuned = None
        self.y2_toff_tuned = None
        self.y2_sgt_tuned = None
        self.z_toff_tuned = None
        self.z_sgt_tuned = None

        self.temp_sg_array = []

        self.temp_toff = 2
        self.temp_sgt = 0

    # ALL MOTORS ARE FREE RUNNING
    def prepare_for_tuning(self):

        log("Prepare for tuning")

        self.s.write_command('$20=0')

        # Enable raw SG reporting: command REPORT_RAW_SG
        self.send_command_to_motor("REPORT RAW SG SET", command=REPORT_RAW_SG, value=1) # is there a way to check this has sent? 

        self.reset_tuning_flags()

        # Zero position
        log("Zero position")
        self.jog_absolute_xy(self.x_min_jog_abs_limit, self.y_min_jog_abs_limit, 6000)
        self.jog_absolute_single_axis('Z', self.z_max_jog_abs_limit, 750)

        self.time_to_check_for_tuning_prep = time.time()

    # CHECK SG VALUES FIRST (TO MAKE SURE THEY'RE RAW)
    def check_SGs_rezero_and_go_to_next_checks_then_tune(self, X = False, Y = False, Z = False):

        SG_to_check = None

        if Z: SG_to_check = self.s.sg_z_motor_axis
        elif X: SG_to_check = self.s.sg_x_motor_axis
        elif Y: SG_to_check = self.s.sg_y1_motor


        if 200 < SG_to_check < 800:

            self.quit_jog()

            log("SG values in range - re-zero")

            self.jog_absolute_xy(self.x_min_jog_abs_limit, self.y_min_jog_abs_limit, 6000)
            self.jog_absolute_single_axis('Z', self.z_max_jog_abs_limit, 750)

            self.time_to_check_for_tuning_prep = time.time()
            Clock.schedule_once(lambda dt: self.check_temps_and_then_go_to_idle_check_then_tune(X=X, Y=Y, Z=Z), 2)


        elif (self.time_to_check_for_tuning_prep + 180) < time.time():
            # raise error popup
            log("RAW SG VALUES NOT ENABLED")

        else: 
            if self.state().startswith('Idle'):
                self.tuning_jog_back_fast(X=X, Y=Y, Z=Z)
                self.tuning_jog_forwards_fast(X=X, Y=Y, Z=Z)

            Clock.schedule_once(lambda dt: self.check_SGs_rezero_and_go_to_next_checks_then_tune(X=X, Y=Y, Z=Z), 1)



    def check_temps_and_then_go_to_idle_check_then_tune(self, X = False, Y = False, Z = False):

        if ((self.reference_temp - 15) <= self.s.motor_driver_temp <= (self.reference_temp + 15)):

            log("Temperature reads valid, check machine is Idle...")

            self.time_to_check_for_tuning_prep = time.time()
            Clock.schedule_once(lambda dt: self.is_machine_idle_for_tuning(X=X, Y=Y, Z=Z), 2)

        elif (self.time_to_check_for_tuning_prep + 15) < time.time():
            # raise error popup
            log("TEMPS AREN'T RIGHT?? TEMP: " + str(self.s.motor_driver_temp))


        else: 
            Clock.schedule_once(lambda dt: self.check_temps_and_then_go_to_idle_check_then_tune(X=X, Y=Y, Z=Z), 3)


    # NEED TO ADD IN WHAT HAPPENS IF TIME RUNS OUT ELSES HERE ALSO
    def is_machine_idle_for_tuning(self, X = False, Y = False, Z = False):

        if self.state().startswith('Idle'):

            log("Ready for tuning, start slow jog...")
            log("Start tuning...")
            self.start_tuning(X,Y,Z)

        elif (self.time_to_check_for_tuning_prep + 120) < time.time():
            # raise error popup
            log("STILL NOT IDLE ??")

        else: 
            Clock.schedule_once(lambda dt: self.is_machine_idle_for_tuning(X=X, Y=Y, Z=Z), 5)



    def start_slow_tuning_jog(self, X = False, Y = False, Z = False):

        # 3. Start long jogging in the axis of interest at 300mm/min for X and Y or for 30mm/min for Z

        if X and Z and not Y: 
            self.s.write_command('$J = G91 X2000 Z-200 F301.5')

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
            self.s.write_command('$J=G53 X' + str(self.x_min_jog_abs_limit) + ' Z ' + str(self.z_max_jog_abs_limit) + ' F6029.9')

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
        self.tuning_poll = Clock.schedule_interval(lambda dt: self.apply_tuned_settings(X=X, Y=Y, Z=Z), 10)


    def do_tuning(self, X, Y, Z):

        # ORDER IS: 
        # self.sg_z_motor_axis = int(sg_values[0])
        # self.sg_x_motor_axis = int(sg_values[1])
        # self.sg_y_axis = int(sg_values[2]) (this depends on y1 and y2 motors)
        # self.sg_y1_motor = int(sg_values[3])
        # self.sg_y2_motor = int(sg_values[4])

        time.sleep(0.5)
        tuning_array, current_temp = self.sweep_toff_and_sgt_and_motor_driver_temp(X = X, Y = Y, Z = Z)

        log("Sweep finished")

        try: 

            if X: 
                X_target_SG = self.get_target_SG_from_current_temperature('X', current_temp)
                self.x_toff_tuned, self.x_sgt_tuned = self.find_best_combo_per_motor_or_axis(tuning_array, X_target_SG, 1)

            if Y: 
                Y_target_SG = self.get_target_SG_from_current_temperature('Y', current_temp)
                self.y1_toff_tuned, self.y1_sgt_tuned = self.find_best_combo_per_motor_or_axis(tuning_array, Y_target_SG, 3)
                self.y2_toff_tuned, self.y2_sgt_tuned = self.find_best_combo_per_motor_or_axis(tuning_array, Y_target_SG, 4)

            if Z: 
                Z_target_SG =self.get_target_SG_from_current_temperature('Z', current_temp)
                self.z_toff_tuned, self.z_sgt_tuned = self.find_best_combo_per_motor_or_axis(tuning_array, Z_target_SG, 0)

        except: 

            log("Could not complete tuning! Check log for errors")
            Clock.unschedule(self.tuning_poll)


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
                self.send_command_to_motor("SET TOFF X " + str(self.temp_toff), motor = TMC_X1, command = SET_TOFF, value = self.temp_toff)
                time.sleep(0.1)
            if Y: 
                self.send_command_to_motor("SET TOFF Y1 " + str(self.temp_toff), motor = TMC_Y1, command = SET_TOFF, value = self.temp_toff)
                self.send_command_to_motor("SET TOFF Y2 " + str(self.temp_toff), motor = TMC_Y2, command = SET_TOFF, value = self.temp_toff)
                time.sleep(0.2)
            if Z: 
                self.send_command_to_motor("SET TOFF Z " + str(self.temp_toff), motor = TMC_Z, command = SET_TOFF, value = self.temp_toff)
                time.sleep(0.1)

            while self.temp_sgt <= self.sgt_max:

                if X: 
                    self.send_command_to_motor("SET SGT X " + str(self.temp_sgt), motor = TMC_X1, command = SET_SGT, value = self.temp_sgt)
                    time.sleep(0.1)
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
                        log('Idle - restart jogs')
                        self.s.tuning_flag = False
                        self.temp_sg_array = []
                        self.tuning_jog_back_fast(X=X, Y=Y, Z=Z)
                        self.start_slow_tuning_jog(X=X, Y=Y, Z=Z)
                        time.sleep(0.01)

                    # But don't measure the backwards fast jogs!
                    elif self.feed_rate() > 303:
                        log('Feed rate too high, skipping')
                        self.s.tuning_flag = False
                        self.temp_sg_array = []
                        time.sleep(1)

                    # Record if conditions are good :)
                    else:
                        self.s.tuning_flag = True
                        time.sleep(0.01)

                self.s.tuning_flag = False

                tuning_array[self.temp_toff][self.temp_sgt] = self.temp_sg_array[8:16]
                self.temp_sg_array = []

                log("SWEPT TOFF AND SGT: " + str(self.temp_toff) + ", " + str(self.temp_sgt))

                temperature_list.append(self.s.motor_driver_temp)

                self.temp_sgt = self.temp_sgt + 1

            self.temp_sgt = 0
            self.temp_toff = self.temp_toff + 1

        try:
            avg_temperature = sum(temperature_list) / len(temperature_list)
            log("Average temperature: " + str(avg_temperature))
            return tuning_array, avg_temperature

        except: 
            log("BAD TEMPERATURES! CAN'T CALIBRATE")


    def find_best_combo_per_motor_or_axis(self, tuning_array, target_SG, idx):

        # idx is motor/axis index

        log("Find best combo for axis idx: " + str(idx) + ", target: " + str(target_SG))

        # toff, sgt, dsg
        prev_best = [None, None, None]

        for toff in range(2,self.toff_max + 1):
            for sgt in range(0,self.sgt_max + 1):

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
        log("FOUND FOR IDX: " + str(idx) + ":" + str(prev_best[0]) + "," + str(prev_best[1]) + "," + str(prev_best[2]))

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

        if ((self.reference_temp - 15) > current_temperature > (self.reference_temp + 15)):

            log("Temperatures out of expected range! Check set-up!")
            return

        reference_SG = 500

        if motor == 'X':
            gradient_per_Celsius = 4000.0
            rpm = 300.0/(3200/(170/3))

        elif motor == 'Y':
            gradient_per_Celsius = 1500.0
            rpm = 300.0/(3200/(170/3))

        elif motor == 'Z':
            gradient_per_Celsius = 4000.0
            rpm = 30.0/(3200/(1066.67))

        delta_to_current_temperature = self.reference_temp - current_temperature
        step_us = 60000000 / (rpm * 3200)
        compensation_SG_offset = gradient_per_Celsius/1000000 * delta_to_current_temperature * step_us
        target_SG = reference_SG + int(compensation_SG_offset)

        log("Calculate target SG " + str(motor) + ": " + str(target_SG))

        return target_SG


    def apply_tuned_settings(self, X = False, Y = False, Z = False):

        # NB: ALL THE SETTINGS HERE WILL TAKE A FEW SECONDS TO COMPLETE

        if self.toff_and_sgt_found:

            log("TOFF and SGT found - applying settings")

            if not self.tuning_poll: Clock.unschedule(self.tuning_poll)

            # Stop slow jog
            self.quit_jog()

            # Apply found TOFF and SGT values to the motor: commands SET_CHOPCONF and SET_SGCSCONF

            if X: 
                self.send_command_to_motor("SET TOFF X " + str(self.x_toff_tuned), motor = TMC_X1, command = SET_TOFF, value = self.x_toff_tuned)
                self.send_command_to_motor("SET SGT X " + str(self.x_sgt_tuned), motor = TMC_X1, command = SET_SGT, value = self.x_sgt_tuned)
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

        log("Storing TMC parameters in EEPROM")

        # Store the motors settings in the EEPROM: command STORE_TMC_PARAMS
        self.send_command_to_motor("STORE TMC PARAMS IN EEPROM", command = STORE_TMC_PARAMS)

        # Disable raw SG reporting: command REPORT_RAW_SG
        self.send_command_to_motor("REPORT RAW SG SET", command=REPORT_RAW_SG, value=0)

        # Read registers back in
        self.send_command_to_motor("GET REGISTERS", command=GET_REGISTERS)

        Clock.schedule_once(self.finish_tuning, 3) # Give settings plenty of time to be sent and parsed


    def finish_tuning(self, dt):

        self.s.write_command('$20=1')

        log("Tuning complete")

        self.reset_tuning_flags()
        self.tuning_in_progress = False


    # MEAT OF CALIBRATION FUNCTIONS - DON'T CALL FROM MAIN APP

    x_ready_to_calibrate = False
    y_ready_to_calibrate = False
    z_ready_to_calibrate = False

    poll_for_x_ready = None
    poll_for_y_ready = None
    poll_for_z_ready = None

    time_to_check_for_calibration_prep = 0

    def initialise_calibration(self, X=False, Y=False, Z=False):

        log("Initialise Calibration")

        self.s.write_command('$20=0')

        self.s.write_command('$J=G53 X0 F6000')
        self.s.write_command('$J=G53 Y0 F6000')
        self.s.write_command('$J=G53 Z0 F750')

        if X: self.poll_for_x_ready = Clock.schedule_interval(self.do_calibrate_x, 2)
        if Y: self.poll_for_y_ready = Clock.schedule_interval(self.do_calibrate_y, 2)
        if Z: self.poll_for_z_ready = Clock.schedule_interval(self.do_calibrate_z, 2)

        # Only sets one ready to begin with
        if X: self.x_ready_to_calibrate = True
        elif Y: self.y_ready_to_calibrate = True
        elif Z: self.z_ready_to_calibrate = True


    def do_calibrate_x(self, dt):

        if self.x_ready_to_calibrate:

            log("Calibrate X")

            Clock.unschedule(self.poll_for_x_ready)
            self.poll_for_x_ready = None
            self.x_ready_to_calibrate = False
            self.time_to_check_for_calibration_prep = time.time()
            self.check_idle_and_buffer_then_start_calibration('X')

    def do_calibrate_y(self, dt):

        if self.y_ready_to_calibrate:

            log("Calibrate Y")

            Clock.unschedule(self.poll_for_y_ready)
            self.poll_for_y_ready = None
            self.y_ready_to_calibrate = False
            self.time_to_check_for_calibration_prep = time.time()
            self.check_idle_and_buffer_then_start_calibration('Y')


    def do_calibrate_z(self, dt):

        if self.z_ready_to_calibrate:

            log("Calibrate Z")

            Clock.unschedule(self.poll_for_z_ready)
            self.poll_for_z_ready = None
            self.z_ready_to_calibrate = False
            self.time_to_check_for_calibration_prep = time.time()
            self.check_idle_and_buffer_then_start_calibration('Z')

    def check_idle_and_buffer_then_start_calibration(self, axis): 

        if self.state().startswith('Idle') and not self.s.write_protocol_buffer:

            if axis == 'X': 
                calibrate_mode = 32
                calibration_file = './asmcnc/production/calibration_gcode_files/X_cal.gc' # need to sest these up
                altDisplayText = "CALIBRATE X AXIS"

            if axis == 'Y': 
                calibrate_mode = 64
                calibration_file = './asmcnc/production/calibration_gcode_files/Y_cal.gc' # need to sest these up
                altDisplayText = "CALIBRATE Y AXIS"

            if axis == 'Z': 
                calibrate_mode = 128
                calibration_file = './asmcnc/production/calibration_gcode_files/Z_cal.gc' # need to sest these up
                altDisplayText = "CALIBRATE Z AXIS"

            self.send_command_to_motor(altDisplayText, command=SET_CALIBR_MODE, value=calibrate_mode)
            Clock.schedule_once(lambda dt: self.stream_calibration_file(calibration_file), 10)

        elif (self.time_to_check_for_calibration_prep + 120) < time.time():

            # gives error message to popup
            log("MACHINE STILL NOT IDLE OR BUFFER FULL - CAN'T CALIBRATE")

        else: 
            Clock.schedule_once(lambda dt: self.check_idle_and_buffer_then_start_calibration(axis), 2)


    def stream_calibration_file(self, filename):

        with open(filename) as f:
            calibration_gcode_pre_scrubbed = f.readlines()

        calibration_gcode = [self.quick_scrub(line) for line in calibration_gcode_pre_scrubbed]

        log("Calibrating...")

        self.s.run_skeleton_buffer_stuffer(calibration_gcode)
        self.poll_end_of_calibration_file_stream = Clock.schedule_interval(self.post_calibration_file_stream, 5)

    def quick_scrub(self, line):

        l_block = re.sub('\s|\(.*?\)', '', (line.strip()).upper())
        return l_block


    def post_calibration_file_stream(self, dt):

        if self.state().startswith('Idle'):

            if self.s.NOT_SKELETON_STUFF and not self.s.is_job_streaming and not self.s.is_stream_lines_remaining and not self.is_machine_paused: 
                Clock.unschedule(self.poll_end_of_calibration_file_stream)
                self.send_command_to_motor("COMPUTE THIS CALIBRATION", command=SET_CALIBR_MODE, value=2)
                
                # FW needs 5 seconds to compute & store after calibration
                Clock.schedule_once(lambda dt: self.do_next_axis_or_finish_calibration_sequence(), 5)


    def do_next_axis_or_finish_calibration_sequence(self):

            # X is always first, so check y and then z
            if self.poll_for_y_ready != None: self.y_ready_to_calibrate = True
            elif self.poll_for_z_ready != None: self.z_ready_to_calibrate = True
            else: self.save_calibration_coefficients_to_motor_classes()


    def save_calibration_coefficients_to_motor_classes(self):

        self.s.write_command('$20=1')
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

        log("Calibration complete")


    # UPLOADING CALIBRATION TO FW:
    calibration_upload_in_progress = False

    def upload_Z_calibration_settings_from_motor_class(self):

        self.calibration_upload_in_progress = True
        Clock.schedule_once(lambda dt: self.initialise_calibration_upload('Z'), 0.5)

    time_to_check_for_upload_prep = 0

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

            Clock.schedule_once(lambda dt: self.initialise_calibration_upload(axis), 2)

        else: 
            log("PROBLEM! Can't initialise calibration upload")


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
        Clock.schedule_once(lambda dt: self.complete_calibration(), 1)


    def complete_calibration(self):
        self.time_to_check_for_upload_prep = 0
        self.calibration_upload_in_progress = False
        log("Calibration upload complete")


