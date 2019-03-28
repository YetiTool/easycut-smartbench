'''
Created on 31 Jan 2018
@author: Ed
This module defines the machine's properties (e.g. travel), services (e.g. serial comms) and functions (e.g. move left)
'''

from asmcnc.comms import serial_connection
from kivy.clock import Clock


class RouterMachine(object):
    
    s = None # serial object
    is_machine_homed = False # status on powerup

    # This block of variables reflecting grbl settings (when '$$' is issued, serial reads settings and syncs these params)
    grbl_x_max_travel = 1500.0 # measured from true home
    grbl_y_max_travel = 3000.0 # measured from true home
    grbl_z_max_travel = 300.0 # measured from true home
    
    # how close do we allow the machine to get to its limit switches when requesting a move (so as not to accidentally trip them)
    # note this an internal UI setting, it is NOT grbl pulloff ($27)
    limit_switch_safety_distance = 1.0 
    
    z_lift_after_probing = 20.0
    z_probe_speed = 60
    z_touch_plate_thickness = 1.65

    is_squaring_XY_needed_after_homing = True # starts True, therefore squares on powerup. Switched to false after initial home, so as not to repeat on next home.
    
#     job_file_gcode = []

            
    def __init__(self, win_serial_port, screen_manager):

        self.sm = screen_manager
        self.set_jog_limits()

        # Establish 's'erial comms and initialise
        self.s = serial_connection.SerialConnection(self, self.sm)
        self.s.establish_connection(win_serial_port)
        print "Serial connection status:", self.s.is_connected()
        self.s.initialise_grbl()

        # Clock.schedule_interval(self.set_led_state, 0.25)
        #Clock.schedule_once(self.update_led_state, 4)

# SETUP

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


# HOMING

    # Home the Z axis by moving the cutter down until it touches the probe.
    # On touching, electrical contact is made, detected, and WPos Z0 set, factoring in probe plate thickness.
    def probe_z(self):

        self.s.expecting_probe_result = True
        probeZTarget =  -(self.grbl_z_max_travel) - self.mpos_z() + 0.1 # 0.1 added to prevent rounding error triggering soft limit
        self.s.write_command('G91 G38.2 Z' + str(probeZTarget) + ' F' + str(self.z_probe_speed))
        self.s.write_command('G90')

        # Serial module then looks for probe detection
        # On detection "probe_z_detection_event" is called (for a single immediate EEPROM write command)....
        # ... followed by a delayed call to "probe_z_post_operation" for any post-write actions.


    def probe_z_detection_event(self):

        self.s.write_command('G10 L20 P1 Z' + str(self.z_touch_plate_thickness))


    def probe_z_post_operation(self, dt):

        # Retract:
        # if deep enough to retract fully
        if self.mpos_z() + self.z_lift_after_probing < -self.limit_switch_safety_distance:
            self.s.write_command('G0 G54 Z' + str(self.z_lift_after_probing))

        # if to close to limit, only go to limit
        else:
            self.s.write_command('G0 G53 Z' + str(-(self.limit_switch_safety_distance)))


    def home_all(self):

        self.set_state('Home') # (grbl not very good at setting the 'home' state)
        self.is_machine_homed = True # status on powerup
        if self.is_squaring_XY_needed_after_homing: self.set_XY_square()
        else: self.s.write_command('$H') # HOME


    def set_XY_square(self):

        # This function is designed to square the machine's X&Y axes
        # It does this by killing the limit switches and driving the X frame into mechanical deadstops at the end of the Y axis.
        # The steppers will stall out, but the X frame will square against the mechanical deadstops.
        # Intended use is first home after power-up only, or the stalling noise will get annoying!

        self.is_squaring_XY_needed_after_homing = False # clear flag, so this function doesn't run again 

        # Because we're setting grbl configs (i.e.$x=n), we need to adopt the grbl config approach used in the serial module.
        # So no direct writing to serial here, we're waiting for grbl responses before we send each line:

        homing_sequence_part_1 =  [
                                  '$H',
                                  '$20=0', # soft limits off
                                  '$21=0', # hard limits off
                                  'G91', # relative coords
                                  'G1 Y-25 F500', # drive lower frame into legs, assumes it's starting from a 3mm pull off
                                  'G1 Y25', # re-enter work area
                                  'G90', # abs coords
                                  'G4 P5'
                                  ]
        self.s.start_sequential_stream(homing_sequence_part_1)

        self.idle_state_count_for_XY_square_post_ops = 0 # resetting count to detect when to do post_operatons (see 'set_XY_square_post_operations' function)
        self.square_post_op_event = Clock.schedule_interval(self.set_XY_square_post_operations, 0.5)


    def set_XY_square_post_operations(self, dt):

        # Make sure the machine is idle before re-homing (grbl wont listen to $ commands when running)
        # The state can ping into idle very briefly during, so we're setting a threshold detection with 'idle_state_count_for_XY_square_post_ops'
        print("set_XY_square_post_operations")
        if not self.s.is_sequential_streaming:
            print("Not streaming")
            if self.state() == "Idle":
                print("Idle")
                self.idle_state_count_for_XY_square_post_ops += 1

                if self.idle_state_count_for_XY_square_post_ops >= 1:
                    self.square_post_op_event.cancel()
                    homing_sequence_part_2 =  [
                                              '$21=1', # soft limits on
                                              '$20=1', # soft limits off
                                              '$H' # home
                                              ]
                    self.s.start_sequential_stream(homing_sequence_part_2)
                    self.set_state('Home') # Since homing op is part of seq stream_file, can't call regular function which would normally force the idle state (grbl not very good at setting the 'home' state)


# STATUS            
        
    def is_connected(self):
        return self.s.is_connected()
    
    def is_job_streaming(self):
        return self.s.is_job_streaming
    
    def state(self):
        return self.s.m_state

    def set_state(self, temp_state):
        grbl_state_words = ['Idle', 'Run', 'Hold', 'Jog', 'Alarm', 'Door', 'Check', 'Home', 'Sleep']
        if temp_state in grbl_state_words:
            self.s.m_state = temp_state
    
    # 'Machine position'/mpos is the absolute position of the tooltip, wrt home
    
    def mpos_x(self):
        return float(self.s.m_x)
    
    def mpos_y(self):
        return float(self.s.m_y)
    
    def mpos_z(self):
        return float(self.s.m_z)
    
    def x_pos_str(self):
        return self.s.m_x
    
    def y_pos_str(self):
        return self.s.m_y
    
    def z_pos_str(self):
        return self.s.m_z
    

    
    # 'Work position'/wpos is the position of the tooltip relative to the datum position set for the job
    # WPos = MPos - WCO.
    def wpos_x(self):
        return float(self.s.m_x) - self.x_wco()
    
    def wpos_y(self):
        return float(self.s.m_y) - self.y_wco()
    
    def wpos_z(self):
        return float(self.s.m_z) - self.z_wco()
    
    # 'Work Co-ordinate offset'/wco is the definition of the datum position set for the job, wrt home
    # WPos = MPos - WCO
    def x_wco(self):
        return float(self.s.wco_x)
    
    def y_wco(self):
        return float(self.s.wco_y)
    
    def z_wco(self):
        return float(self.s.wco_z)
    
    # The G28 command moves the tooltip to an intermediate parking position. 
    # Potentially useful if you want the tool to go to a specific position before and after a job (for example to reload a part for batch work)
    def g28_x(self):
        return float(self.s.g28_x)
    
    def g28_y(self):
        return float(self.s.g28_y)
    
    def g28_z(self):
        return float(self.s.g28_z)
    

# ACTION

    # "Reset" refers to a soft-reset
    # On soft-reset, grbl is locked - that means it won't do anything until homed
    # ... unless it is unlocked
    def soft_reset(self):
        if self.s.is_job_streaming == True: self.s.cancel_stream() # Cancel stream_file to stop it continuing to send stuff after reset
        self.s.write_realtime("\x18", show_in_sys=False, show_in_console=False) # Soft-reset. This forces the need to home when the controller starts up
        print '>>> GRBL RESET'
    
    def jog_absolute_single_axis(self, axis, target, speed):
        self.s.write_command('$J=G53 ' + axis + str(target) + ' F' + str(speed))
    
    def jog_absolute_xy(self, x_target, y_target, speed):
        self.s.write_command('$J=G53 X' + str(x_target) + ' Y' + str(y_target) + ' F' + str(speed))  
 
    def jog_relative(self, axis, dist, speed):
        self.s.write_command('$J=G91 ' + axis + str(dist) + ' F' + str(speed))
    
    def quit_jog(self):
        self.s.write_realtime('\x85', show_in_console=False)       

    def hold(self):
        self.door()
    
    def resume(self):
        self.s.write_realtime('~')       
    
    def spindle_on(self):
        self.s.write_command('M3 S25000')
    
    def spindle_off(self):
        self.s.write_command('M5')
    
    def buffer_capacity(self):
        return self.s.serial_blocks_available
    
    def set_workzone_to_pos_xy(self):
        self.s.write_command('G10 L20 P1 X0 Y0')

    def set_standby_to_pos(self):
        self.s.write_command('G28.1')
    
    def get_grbl_status(self):
        self.s.write_command('$#')

    def get_grbl_settings(self):
        self.s.write_command('$$')
        
    def send_any_gcode_command(self, gcode):
        self.s.write_command(gcode)

    def unlock_after_alarm(self):
        self.s.write_command('AL0', show_in_sys=False, show_in_console=False)
        self.s.write_command('ALB9', show_in_sys=False, show_in_console=False)
        self.s.write_command('$X')
    
    def go_to_jobstart_xy(self):
        self.s.write_command('G0 G54 X0 Y0')
    
    def go_to_standby(self):
        self.s.write_command('G28')
    
    def go_to_jobstart_z(self):
        self.s.write_command('G0 G54 Z0')
    
    def set_jobstart_z(self):
        self.s.write_command('G10 L20 P1 Z0')
        self.get_grbl_status()

    def test(self):
        print 'test'
        
    def zUp(self):
        self.s.write_command('G0 G53 Z-' + str(self.limit_switch_safety_distance))

    def led_ring_off(self):
        # self.s.write_command('AL0', show_in_sys=False, show_in_console=False)
        pass
    
#     def stream_file(self, job_file_path):
#         self.s.stream_file(job_file_path)

    def vac_on(self):
        self.s.write_command('AE')

    def vac_off(self):
        self.s.write_command('AF')

    def feed_override_reset(self):
        self.s.write_realtime('\x90', altDisplayText='Feed override RESET')

    def feed_override_up_10(self, final_percentage=''):
        self.s.write_realtime('\x91', altDisplayText='Feed override UP ' + str(final_percentage))

    def feed_override_down_10(self, final_percentage=''):
        self.s.write_realtime('\x92', altDisplayText='Feed override DOWN ' + str(final_percentage))

    is_check_mode_enabled = False

    def enable_check_mode(self):
        if self.is_check_mode_enabled == False:
            self.is_check_mode_enabled = True
            self.s.write_command('$C', altDisplayText = 'Check mode ON')

    def disable_check_mode(self):
        if self.is_check_mode_enabled == True:
            self.is_check_mode_enabled = False
            self.s.write_command('$C', altDisplayText = 'Check mode OFF')

    def set_x_datum(self):
        self.s.write_command('G10 L20 P1 X0')

    def set_y_datum(self):
        self.s.write_command('G10 L20 P1 Y0')
        
    def go_x_datum(self):
        self.s.write_command('G0 G54 X0')
 
    def go_y_datum(self):
        self.s.write_command('G0 G54 Y0')
        
    def toggle_spindle_off_overide(self, dt):
        self.s.write_realtime('\x9e', altDisplayText = 'Spindle stop override')

    def door(self):
        self.s.write_realtime('\x84', altDisplayText = 'Door')


# LIGHTING

    def set_led_state(self, dt):
        # Idle, Run, Hold, Jog, Alarm, Door, Check, Home, Sleep
        
        # Don't poll if in run, economise on comms
        if self.state().startswith('Idle'):
            self.s.write_command('AL0', show_in_sys=False, show_in_console=False)
            self.s.write_command('ALB9', show_in_sys=False, show_in_console=False)
        elif self.state().startswith('Hold'):
            pass # Once on hold, can't hear command
        elif self.state().startswith('Jog'):
            self.s.write_command('AL0', show_in_sys=False, show_in_console=False)
            self.s.write_command('ALG9', show_in_sys=False, show_in_console=False)        
        elif self.state().startswith('Door'):
            self.s.write_command('AL0', show_in_sys=False, show_in_console=False)
            self.s.write_command('ALR9', show_in_sys=False, show_in_console=False)        
            self.s.write_command('ALG9', show_in_sys=False, show_in_console=False)        
        elif self.state().startswith('Sleep'):
            self.s.write_command('AL0', show_in_sys=False, show_in_console=False)
        elif self.state().startswith('Alarm'):
            self.s.write_command('AL0', show_in_sys=False, show_in_console=False)
            self.s.write_command('ALR9', show_in_sys=False, show_in_console=False)
        elif self.state().startswith('Unknown'):
            self.s.write_command('AL0', show_in_sys=False, show_in_console=False)
            self.s.write_command('ALR9', show_in_sys=False, show_in_console=False)
            self.s.write_command('ALB9', show_in_sys=False, show_in_console=False)
        elif self.state().startswith('Home'):
            self.s.write_command('AL0', show_in_sys=False, show_in_console=False)
            self.s.write_command('ALR9', show_in_sys=False, show_in_console=False)
            self.s.write_command('ALG9', show_in_sys=False, show_in_console=False)
            self.s.write_command('ALB9', show_in_sys=False, show_in_console=False)


    led_state = 0
    led_states = [
        # Red bright > dim
        'R1',
        'R2',
        'R3',
        'R4',
        'R5',
        'R6',
        'R7',
        'R8',
        'R9',
        'R8',
        'R7',
        'R6',
        'R5',
        'R4',
        'R3',
        'R2',
        'R1',
        'R0',
        
        # Green bright > dim
        'G1',
        'G2',
        'G3',
        'G4',
        'G5',
        'G6',
        'G7',
        'G8',
        'G9',
        'G8',
        'G7',
        'G6',
        'G5',
        'G4',
        'G3',
        'G2',
        'G1',
        'G0',
        
        # Blue bright > dim
        'B1',
        'B2',
        'B3',
        'B4',
        'B5',
        'B6',
        'B7',
        'B8',
        'B9',
        'B8',
        'B7',
        'B6',
        'B5',
        'B4',
        'B3',
        'B2',
        'B1',
        'B0',
        
        # Red and green bright > dim
        'R1 G1',
        'R2 G2',
        'R3 G3',
        'R4 G4',
        'R5 G5',
        'R6 G6',
        'R7 G7',
        'R8 G8',
        'R9 G9',
        'R8 G8',
        'R7 G7',
        'R6 G6',
        'R5 G5',
        'R4 G4',
        'R3 G3',
        'R2 G2',
        'R1 G1',
        'R0 G0',
        
        # Loops back to start
        ]


    def update_led_state(self, dt):

        if self.state().startswith('Idle'):
            led_commands = self.led_states[self.led_state].split(' ')
            for led_command in led_commands:
                self.set_led(led_command)

            self.led_state += 1
            if self.led_state == len(self.led_states):
                self.led_state = 0
        Clock.schedule_once(self.update_led_state, 0.1)


    def set_led(self, command):
        self.s.write_command('AL' + command, show_in_sys=False, show_in_console=False)
        
    def set_led_blue(self):
        self.s.write_command('ALB9', show_in_sys=False, show_in_console=False)

