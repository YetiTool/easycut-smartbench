'''
Created on 31 Jan 2018
@author: Ed
This module defines the machine's properties (e.g. travel), services (e.g. serial comms) and functions (e.g. move left)
'''

from asmcnc.comms import serial_connection  # @UnresolvedImport
from kivy.clock import Clock
import sys, os
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


    # PERSISTENT MACHINE VALUES


    ## PERSISTENT VALUES SETUP
    smartbench_values_dir = '/home/pi/easycut-smartbench/src/sb_values/'
    
    ### Individual files to hold persistent values
    set_up_options_file_path = smartbench_values_dir + 'set_up_options.txt'
    z_touch_plate_thickness_file_path = smartbench_values_dir + 'z_touch_plate_thickness.txt'
    calibration_settings_file_path = smartbench_values_dir + 'calibration_settings.txt'
    z_head_maintenance_settings_file_path = smartbench_values_dir + 'z_head_maintenance_settings.txt'   
    z_head_laser_offset_file_path = smartbench_values_dir + 'z_head_laser_offset.txt'
    spindle_brush_values_file_path = smartbench_values_dir + 'spindle_brush_values.txt'
    spindle_cooldown_settings_file_path = smartbench_values_dir + 'spindle_cooldown_settings.txt'

    ## PROBE SETTINGS
    z_lift_after_probing = 20.0
    z_probe_speed = 60
    z_touch_plate_thickness = 1.53

    ## CALIBRATION SETTINGS
    time_since_calibration_seconds = 0
    time_to_remind_user_to_calibrate_seconds = float(320*3600)

    ## Z HEAD MAINTENANCE SETTINGS
    time_since_z_head_lubricated_seconds = 0

    ## LASER VALUES
    laser_offset_x_value = 0
    laser_offset_y_value = 0

    is_laser_on = False
    is_laser_enabled = False

    ## BRUSH VALUES
    spindle_brush_use_seconds = 0
    spindle_brush_lifetime_seconds = float(120*3600)

    ## SPINDLE COOLDOWN OPTIONS
    spindle_brand = 'YETI' # String to hold brand name
    spindle_voltage = 230 # Options are 230V or 110V
    spindle_digital = True #spindle can be manual or digital
    spindle_cooldown_time_seconds = 10 # YETI value is 10 seconds
    spindle_cooldown_rpm = 20000 # YETI value is 20k 

    reminders_enabled = True

    trigger_setup = False
            
    def __init__(self, win_serial_port, screen_manager):

        self.sm = screen_manager
        self.set_jog_limits()

        # Establish 's'erial comms and initialise
        self.s = serial_connection.SerialConnection(self, self.sm)
        self.s.establish_connection(win_serial_port)

        # initialise sb_value files if they don't already exist (to record persistent maintenance values)
        if sys.platform != "win32" and sys.platform != "darwin":
            self.check_presence_of_sb_values_files()
            self.get_persistent_values()

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

    def get_persistent_values(self):
        self.read_set_up_options()
        self.read_z_touch_plate_thickness()
        self.read_calibration_settings()
        self.read_z_head_maintenance_settings()
        self.read_z_head_laser_offset_values()
        self.read_spindle_brush_values()
        self.read_spindle_cooldown_settings()


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


    ## SPINDLE COOLDOWN OPTIONS
    def read_spindle_cooldown_settings(self):

        try:
            file = open(self.spindle_cooldown_settings_file_path, 'r')
            # this might throw errors, not sure? might need to define list first and then read but let's try
            read_spindle = file.read().splitlines()
            file.close()

            self.spindle_brand = str(read_spindle[0])
            self.spindle_voltage = int(read_spindle[1])
            if read_spindle[2] == 'True': self.spindle_digital = True
            else: self.spindle_digital = False
            self.spindle_cooldown_time_seconds = int(read_spindle[3])
            self.spindle_cooldown_rpm = int(read_spindle[4])

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

# GRBL SETTINGS

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

    def restore_grbl_settings_from_file(self, filename):

        try: 
            fileobject = open(filename, 'r')
            settings_to_restore = (fileobject.read()).split('\n')
            self.s.start_sequential_stream(settings_to_restore)   # Send any grbl specific parameters
            self.send_any_gcode_command("$$")
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
        output = self.is_machines_hw_version_equal_to_or_greater_than_version('8', 'laser commands AX and AZ') # Update to version 8, but need 6 to test on rig
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
                if self.s.hw_version >= version_to_reference:
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

    # REFACTORED START/STOP COMMANDS

    def bootup_sequence(self):
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
        self.s.is_job_streaming = False
        self._grbl_door() # send a soft-door command

    def resume_after_a_stream_pause(self):
        Clock.schedule_once(lambda dt: self.set_pause(False),0.1)
        self.s.is_job_streaming = True
        self._grbl_resume()

    def set_pause(self, pauseBool):
        self.is_machine_paused = pauseBool  # sets serial_connection flag to pause (allows a hard door to be detected)
 
    def stop_from_soft_stop_cancel(self):
        self.resume_from_alarm() 
        Clock.schedule_once(lambda dt: self.set_pause(False),0.2) 

    def resume_from_a_soft_door(self):
        self._grbl_resume()
        Clock.schedule_once(lambda dt: self.set_pause(False),0.2)

    def resume_after_a_hard_door(self):
        self._grbl_resume()
        Clock.schedule_once(lambda dt: self.set_pause(False),0.2)

    def cancel_after_a_hard_door(self):
        self.resume_from_alarm() 
        Clock.schedule_once(lambda dt: self.set_pause(False),0.2) 
   
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
            Clock.schedule_once(lambda dt: self.s.write_command('$C', altDisplayText = 'Check mode ON'), 0.2)
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
            popup_info.PopupError(self.sm, "Laser datum is out of bounds!\n\nDatum has not been set. Please choose a different datum using the laser crosshair.")

    def set_x_datum_with_laser(self):
        if self.jog_spindle_to_laser_datum('X'): 

            def wait_for_movement_to_complete(dt):
                if not self.state() == 'Jog':
                    Clock.unschedule(x_poll_for_success)
                    self.set_x_datum()

            x_poll_for_success = Clock.schedule_interval(wait_for_movement_to_complete, 0.5)

        else: 
            popup_info.PopupError(self.sm, "Laser datum is out of bounds!\n\nDatum has not been set. Please choose a different datum using the laser crosshair.")

    def set_y_datum_with_laser(self):
        if self.jog_spindle_to_laser_datum('Y'): 

            def wait_for_movement_to_complete(dt):
                if not self.state() == 'Jog':
                    Clock.unschedule(y_poll_for_success)
                    self.set_y_datum()

            y_poll_for_success = Clock.schedule_interval(wait_for_movement_to_complete, 0.5)

        else: 
            popup_info.PopupError(self.sm, "Laser datum is out of bounds!\n\nDatum has not been set. Please choose a different datum using the laser crosshair.")


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
        self.s.write_command('G0 G53 Z-' + str(self.limit_switch_safety_distance))

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
        self.s.write_command('G0 G53 Z-' + str(self.limit_switch_safety_distance))

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
    def request_homing_procedure(self, return_to_screen_str, cancel_to_screen_str, force_squaring_decision = False):
        
        # Force user to decide between manual/auto squaring
        if force_squaring_decision: self.is_machine_completed_the_initial_squaring_decision = False
 
        # If squaring has already been completed and decision isn't getting forced again       
        if self.is_machine_completed_the_initial_squaring_decision:
            self.sm.get_screen('prepare_to_home').return_to_screen = return_to_screen_str
            self.sm.get_screen('prepare_to_home').cancel_to_screen = cancel_to_screen_str
            self.sm.current = 'prepare_to_home'  

        # If decision needs to be made again (either via forced arg, or because it's never been attempted or completed fully)
        else:
            self.sm.get_screen('squaring_decision').return_to_screen = return_to_screen_str
            self.sm.get_screen('squaring_decision').cancel_to_screen = cancel_to_screen_str
            self.sm.current = 'squaring_decision'


    # Home the Z axis by moving the cutter down until it touches the probe.
    # On touching, electrical contact is made, detected, and WPos Z0 set, factoring in probe plate thickness.
    def probe_z(self):

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


