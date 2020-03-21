'''
Created on 31 Jan 2018
@author: Ed
This module defines the machine's properties (e.g. travel), services (e.g. serial comms) and functions (e.g. move left)
'''

from asmcnc.comms import serial_connection
from kivy.clock import Clock
import sys
from __builtin__ import True
from kivy.uix.switch import Switch


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
    
    z_lift_after_probing = 20.0
    z_probe_speed = 60
    z_touch_plate_thickness = 1.53

    is_machine_homed = False # status on powerup
    is_squaring_XY_needed_after_homing = True # starts True, therefore squares on powerup. Switched to false after initial home, so as not to repeat on next home.
    is_check_mode_enabled = False    

    is_machine_paused = False
            
    def __init__(self, win_serial_port, screen_manager):

        self.sm = screen_manager
        self.set_jog_limits()

        # Establish 's'erial comms and initialise
        self.s = serial_connection.SerialConnection(self, self.sm)
        self.s.establish_connection(win_serial_port)
        print "Serial connection status:", self.s.is_connected()
        self.s.initialise_grbl()


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
    Does not change LED state (coz that's cutom YETI).
    e.g. Door state --> Idle
    
    '''

    # REFACTORED START/STOP COMMANDS

    def resume_from_alarm(self):
        # Machine has stopped without warning and probably lost position
        self._stop_all_streaming()  # In case alarm happened during stream, stop that
        self._grbl_soft_reset()     # Reset to get out of Alarm mode. All buffers will be dumped.
        # Now grbl won't allow anything until machine is rehomed or unlocked
        # To prevent user frustration, we're allowing the machine to be unlocked and moved until we can add further user handling
        # The user should be prompted to home in the alarm message
        Clock.schedule_once(lambda dt: self._grbl_unlock(),0.1)
        Clock.schedule_once(lambda dt: self.set_led_blue(),0.2)


    def stop_from_gcode_error(self):
        # Note this should be a implementation of door functionality, but this is a fast implementation since there are multiple possible door calls which we need to manage.
        self._grbl_feed_hold()
        # Allow machine to decelerate in XYZ before resetting to kill spindle, or it'll alarm due to resetting in motion
        Clock.schedule_once(lambda dt: self._grbl_soft_reset(), 1.5)

    def resume_from_gcode_error(self):
        Clock.schedule_once(lambda dt: self.set_led_blue(),0.1)


    def stop_from_quick_command_reset(self):
        self._stop_all_streaming()
        self._grbl_soft_reset()
        Clock.schedule_once(lambda dt: self._grbl_unlock(),0.1)
        Clock.schedule_once(lambda dt: self.set_led_blue(),0.2) 
               

        
    def stop_for_a_stream_pause(self):
        self.set_pause(True)  # set serial_connection flag to pause streaming
        self.s.is_job_streaming = False
        self._grbl_door() # send a soft-door command

    def resume_after_a_stream_pause(self):
        self._grbl_resume()
        Clock.schedule_once(lambda dt: self.set_pause(False),0.1)
        self.s.is_job_streaming = True

    def set_pause(self, pauseBool):
        self.is_machine_paused = pauseBool


 
    def stop_from_soft_stop_cancel(self):
        self._stop_all_streaming()
        self._grbl_soft_reset()
        Clock.schedule_once(lambda dt: self._grbl_unlock(),0.1)
        Clock.schedule_once(lambda dt: self.set_led_blue(),0.2) 

        # Could be refined - don't know if delay needed, or indeed purpose of call               
        Clock.schedule_once(lambda dt: self.set_pause(False),0.1)

        

    
    # Internal calls

    # Cancel all streams to stop EC continuing to send stuff (required before a RESET)
    def _stop_all_streaming(self):
        if self.s.is_job_streaming == True: self.s.cancel_stream() 
        if self.s.is_sequential_streaming == True: self.s.cancel_sequential_stream() # Cancel sequential stream to stop it continuing to send stuff after reset

    def _grbl_resume(self):
        self.s.write_realtime('~', altDisplayText = 'Resume')

    def _grbl_feed_hold(self):
        self.s.write_realtime('!', altDisplayText = 'Resume')

    def _grbl_soft_reset(self):
        self.s.write_realtime("\x18", altDisplayText = 'Soft reset')

    def _grbl_door(self):
        self.s.write_realtime('\x84', altDisplayText = 'Door')
    
    def _grbl_unlock(self):
        self.s.write_command('$X')




    # LEGACY COMMANDS

    def soft_reset(self):
        if self.s.is_job_streaming == True: self.s.cancel_stream() # Cancel stream_file to stop it continuing to send stuff after reset
        if self.s.is_sequential_streaming == True: self.s.cancel_sequential_stream() # Cancel sequential stream to stop it continuing to send stuff after reset
        self._grbl_soft_reset()

    def hold(self):
        self.set_pause(True)
        if not self.state().startswith('Door'): self.door()
    
    def resume(self):
        Clock.schedule_once(lambda dt: self.set_pause(False),0.1)
        self._grbl_resume()
        self.led_restore()
        
    def unlock_after_alarm(self):
        self._grbl_unlock()
        # Restore LEDs
        if sys.platform != "win32":
            self.s.write_command('AL0', show_in_sys=False, show_in_console=False)
            self.s.write_command('ALB9', show_in_sys=False, show_in_console=False)

    def door(self):
        self._grbl_door()




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
        if not self.state().startswith('Check'):
            self.s.write_command('$C', altDisplayText = 'Check mode ON')
            self.is_check_mode_enabled = True
        else:
            print 'Check mode already enabled'
            self.is_check_mode_enabled = True           

    def disable_check_mode(self):
        if self.state().startswith('Check') \
            or (self.state().startswith('Alarm') and self.is_check_mode_enabled == True) \
            or (self.state().startswith('Error') and self.is_check_mode_enabled == True): 
            self.s.write_command('$C', altDisplayText = 'Check mode OFF')
            self.is_check_mode_enabled = False
        else:
            print 'Check mode already disabled'
            self.is_check_mode_enabled = False 

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


# POSITIONAL SETTERS

    def set_workzone_to_pos_xy(self):
        self.s.write_command('G10 L20 P1 X0 Y0')

    def set_standby_to_pos(self):
        self.s.write_command('G28.1')

    def set_jobstart_z(self):
        self.s.write_command('G10 L20 P1 Z0')
        self.get_grbl_status()

    def set_x_datum(self):
        self.s.write_command('G10 L20 P1 X0')

    def set_y_datum(self):
        self.s.write_command('G10 L20 P1 Y0')
                

    

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

    def feed_override_reset(self):
        self.s.write_realtime('\x90', altDisplayText = 'Feed override RESET')

    def feed_override_up_10(self, final_percentage=''):
        self.s.write_realtime('\x91', altDisplayText='Feed override UP ' + str(final_percentage))

    def feed_override_down_10(self, final_percentage=''):
        self.s.write_realtime('\x92', altDisplayText='Feed override DOWN ' + str(final_percentage))

    def go_x_datum(self):
        self.s.write_command('G0 G53 Z-' + str(self.limit_switch_safety_distance))
        self.s.write_command('G4 P0.1')
        self.s.write_command('G0 G54 X0')
 
    def go_y_datum(self):
        self.s.write_command('G0 G53 Z-' + str(self.limit_switch_safety_distance))
        self.s.write_command('G4 P0.1')
        self.s.write_command('G0 G54 Y0')

        
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

    def probe_z_detection_event(self, z_machine_coord_when_probed):

        self.s.write_command('G90 G1 G53 Z' + z_machine_coord_when_probed)
        self.s.write_command('G4 P0.5') 
        self.s.write_command('G10 L20 P1 Z' + str(self.z_touch_plate_thickness))
        self.s.write_command('G4 P0.5') 
        self.zUp()    

    def home_all(self):
        self.sm.current = 'homing'



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

    def set_led_colour_by_name(self, colour_name):

        if colour_name == 'red': self.s.write_realtime("*LFF0000\n")
        if colour_name == 'green': self.s.write_realtime("*L00FF00\n")
        if colour_name == 'blue': self.s.write_realtime("*L0000FF\n")
        if colour_name == 'white': self.s.write_realtime("*LFFFFFF\n")
        if colour_name == 'off' or colour_name == 'dark': self.s.write_realtime("*L000000\n")

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
        
    #### CONFIRMED ACTIVE LEDS CMDS    
        
    def set_led_blue(self):
        self.s.write_command('AL0', show_in_sys=False, show_in_console=False)
        self.s.write_command('ALB9', show_in_sys=False, show_in_console=False)        
    
    def set_led_red(self):
        self.s.write_command('AL0', show_in_sys=False, show_in_console=False)
        self.s.write_command('ALR9', show_in_sys=False, show_in_console=False)

    def led_restore(self):
        self.s.write_realtime('&', altDisplayText = 'LED restore')
