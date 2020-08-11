'''
Created on 31 Jan 2018
@author: Ed
Module to manage all serial comms between pi (EasyCut s/w) and realtime arduino chip (GRBL f/w)

THIS LOOKS FOR PORT ttyAMA not ttyS - incompatible with older platforms.
'''

from kivy.config import Config
from __builtin__ import True

# Set the Kivy "Clock" to tick at its fastest.
# # Clock usually used to establish consistent framerate for animations, but we need it to tick much faster (e.g. than 25fps) for serial refreshing
# Config.set('graphics', 'maxfps', '30')
# Config.write()

import serial, sys, time, string, threading
from datetime import datetime
from os import listdir
from kivy.clock import Clock

import re
from functools import partial
from serial.serialutil import SerialException


BAUD_RATE = 115200
ENABLE_STATUS_REPORTS = True
GRBL_SCANNER_MIN_DELAY = 0.01 # Delay between checking for response from grbl. Needs to be hi-freq for quick streaming, e.g. 0.01 = 100Hz

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))


class SerialConnection(object):

    STATUS_INTERVAL = 0.1 # How often to poll general status to update UI (0.04 = 25Hz = smooth animation)

    s = None    # Serial comms object
    sm = None   # Screen manager object

    grbl_out = ""
    job_gcode = []
    response_log = []
    suppress_error_screens = False
    suppress_alarm_screens = False
    suppress_door_screens = False
    FLUSH_FLAG = False
    
    write_command_buffer = []
    write_realtime_buffer = []
    
    monitor_text_buffer = ""
    overload_state = 0
    is_ready_to_assess_spindle_for_shutdown = True

    # For Z Head Diagnostics only:
    overload_pin_mV = 0

    def __init__(self, machine, screen_manager):

        self.sm = screen_manager   
        self.m = machine
        
    def __del__(self):
        print 'Destructor'

    def get_serial_screen(self, serial_error):

        if self.sm.current != 'serialScreen' and self.sm.current != 'rebooting':
            self.sm.get_screen('serialScreen').error_description = serial_error
            self.sm.current = 'serialScreen'

    def establish_connection(self, win_port):

        log('Start to establish connection...')
        # Parameter 'win'port' only used for windows dev e.g. "COM4"
        if sys.platform == "win32":
            try:
                self.s = serial.Serial(win_port, BAUD_RATE, timeout = 6, writeTimeout = 20)
                self.suppress_error_screens = True
            except:
                Clock.schedule_once(lambda dt: self.get_serial_screen('Could not establish a connection on startup.'), 2) # necessary bc otherwise screens not initialised yet      

        elif sys.platform == "darwin":
            self.suppress_error_screens = True
            try:
                filesForDevice = listdir('/dev/') # put all device files into list[]
                for line in filesForDevice: # run through all files
                    if (line.startswith('tty.usbmodem')): # look for...   
                        # When platform is updated, this needs to be moved across to the AMA0 port :)
                        devicePort = line # take whole line (includes suffix address e.g. ttyACM0
                        self.s = serial.Serial('/dev/' + str(devicePort), BAUD_RATE, timeout = 6, writeTimeout = 20) # assign
            except:
                Clock.schedule_once(lambda dt: self.get_serial_screen('Could not establish a connection on startup.'), 2) # necessary bc otherwise screens not initialised yet      

        else:
            try:
                filesForDevice = listdir('/dev/') # put all device files into list[]
                for line in filesForDevice: # run through all files

                    # FLAG: This if statement is only relevant in linux environment. 
                    # EITHER: USB Comms hardware
                    # if (line[:6] == 'ttyUSB' or line[:6] == 'ttyACM'): # look for prefix of known success (covers both Mega and Uno)
                    # OR: UART Comms hardware
                    if (line[:4] == 'ttyS' or line[:6] == 'ttyACM'): # look for...   
                        # When platform is updated, this needs to be moved across to the AMA0 port :)
                        devicePort = line # take whole line (includes suffix address e.g. ttyACM0
                        self.s = serial.Serial('/dev/' + str(devicePort), BAUD_RATE, timeout = 6, writeTimeout = 20) # assign

                    # elif (line[:6] == 'ttyAMA'): # in the case that in /boot/config.txt, dtoverlay=pi3-disable-bt
                    
                    #     devicePort = line # take whole line (includes suffix address e.g. ttyACM0
                    #     self.s = serial.Serial('/dev/' + str(devicePort), BAUD_RATE, timeout = 6, writeTimeout = 20) # assign
                    #     return True
                        
                    elif (line[:12] == 'tty.usbmodem'): # look for...   
                        devicePort = line # take whole line (includes suffix address e.g. ttyACM0
                        self.s = serial.Serial('/dev/' + str(devicePort), BAUD_RATE, timeout = 6, writeTimeout = 20) # assign

            except:
                Clock.schedule_once(lambda dt: self.get_serial_screen('Could not establish a connection on startup.'), 2) # necessary bc otherwise screens not initialised yet      

        log("Serial connection status: " + str(self.is_connected()))

        if self.is_connected():
            log('Initialising grbl...')
            self.write_direct("\r\n\r\n", realtime = False, show_in_sys = False, show_in_console = False)    # Wakes grbl

    # is serial port connected?
    def is_connected(self):

        if self.s != None:
            return True
        else: 
            return False


    # called by first kivy screen when safe to assume kivy processing is completed, to ensure correct clock scheduling
    def start_services(self, dt):

        log('Starting services')
        self.s.flushInput()  # Flush startup text in serial input
        self.next_poll_time = time.time()
        t = threading.Thread(target=self.grbl_scanner)
        t.daemon = True
        t.start()
        
        # Clear any hard switch presses that may have happened during boot
        self.m.bootup_sequence()  



# SCANNER: listens for responses from Grbl

    # "Response" is a message from GRBL saying how a line of gcode went (either 'ok', or 'error') when it was loaded from the serial buffer into the line buffer
    # When streaming, monitoring the response from GRBL is essential for EasyCut to know when to send the next line
    # Full docs: https://github.com/gnea/grbl/wiki/Grbl-v1.1-Interface

    # "Push" is for messages from GRBL to provide more general feedback on what Grbl is doing (e.g. status)

    VERBOSE_ALL_PUSH_MESSAGES = False
    VERBOSE_ALL_RESPONSE = False
    VERBOSE_STATUS = False


    def grbl_scanner(self):
        
        log('Running grbl_scanner thread')

        while True:

                         
            if self.FLUSH_FLAG == True:
                self.s.flushInput()
                self.FLUSH_FLAG = False
            
            # Polling 
            if self.next_poll_time < time.time():
                self.write_direct('?', realtime = True, show_in_sys = False, show_in_console = False)
                self.next_poll_time = time.time() + self.STATUS_INTERVAL

            # Process anything in the write_command and write_realtime lists,
            # i.e. everything else.
            
            command_counter = 0
            for command in self.write_command_buffer:
                self.write_direct(*command)
                command_counter += 1
                
            del self.write_command_buffer[0:(command_counter+1)]
            
            realtime_counter = 0
            for realtime_command in self.write_realtime_buffer:
                self.write_direct(realtime_command[0], altDisplayText = realtime_command[1], realtime = True)
                realtime_counter += 1
                
            del self.write_realtime_buffer[0:(realtime_counter+1)]

            
            # If there's a message received, deal with it depending on type:
            if self.s.inWaiting():
                # Read line in from serial buffer
                try:
                    rec_temp = self.s.readline().strip() #Block the executing thread indefinitely until a line arrives
                    self.grbl_out = rec_temp;
                    # print self.grbl_out
                except Exception as e:
                    log('serial.readline exception:\n' + str(e))
                    rec_temp = ''
                    self.get_serial_screen('Could not read line from serial buffer.')
            else: 
                rec_temp = ''

            # If something received from serial buffer, process it. 
            if len(rec_temp):  
            

                #if not rec_temp.startswith('<Alarm|MPos:') and not rec_temp.startswith('<Idle|MPos:'):
                if self.VERBOSE_ALL_RESPONSE: 
                    if rec_temp.startswith('<'):
                        log(rec_temp)
                    else:
                        log('< ' + rec_temp)
    
                # Update the gcode monitor (may not be initialised) and console:
                try:
                    self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('rec', rec_temp)
                except:
                    pass
    
                # Process the GRBL response:
                # NB: Sequential streaming is controlled through process_grbl_response
                try:
                    # If RESPONSE message (used in streaming, counting processed gcode lines)
                    if rec_temp.startswith(('ok', 'error')):
                        self.process_grbl_response(rec_temp)
                    # If PUSH message
                    else:
                        self.process_grbl_push(rec_temp)
                except Exception as e:
                    log('Process response exception:\n' + str(e))
                    self.get_serial_screen('Could not process grbl response. Grbl scanner has been stopped.')
                    raise # HACK allow error to cause serial comms thread to exit
                    # What happens here? 
                        # - this bit grinds to a halt presumably
                        # - need to send instructions to the GUI (prior to raise?) 
    
                # Job streaming: stuff butter
                if self.is_job_streaming:
                    if self.is_stream_lines_remaining:
                        self.stuff_buffer()
                    else: 
                        if self.g_count == self.l_count:
                            self.end_stream()
                    
        # Loop this method
        #Clock.schedule_once(self.grbl_scanner, GRBL_SCANNER_MIN_DELAY)



# STREAMING: sending gcode, using character counting protocol described here:
# https://github.com/gnea/grbl/wiki/Grbl-v1.1-Interface


    # streaming variables
    GRBL_BLOCK_SIZE = 35    # max number of gcode lines which GRBL can put in its 'BLOCK' or look ahead buffer
    RX_BUFFER_SIZE = 256    # serial buffer which gets filled by EasyCut. GRBL grabs from this when there is block space

    is_job_streaming = False
    is_stream_lines_remaining = False
    is_job_finished = False

    g_count = 0 # gcodes processed (ok/error'd) by grbl (gcodes may not get processed immediately after being sent)
    l_count = 0 # lines sent to grbl
    c_line = [] # char count of blocks/lines in grbl's serial buffer
    
    stream_start_time = 0
    stream_end_time = 0
    buffer_monitor_file = None
    
    def check_job(self, job_object):
        
        log('Checking job...')

        self.m.enable_check_mode()
        
        # Sleep to ensure check mode ok isn't included in log
        time.sleep(0.1)
        
        # Set up error logging
        self.suppress_error_screens = True
        self.response_log = []
        
        # run job as per normal, if_check_enabled has been set to true
        self.run_job(job_object)

        # get error log back to the checking screen when it's ready
        Clock.schedule_interval(partial(self.return_check_outcome, job_object),0.1)

    def return_check_outcome(self, job_object,dt):
        if len(self.response_log) >= len(job_object): # + 2
            self.suppress_error_screens = False
            self.sm.get_screen('check_job').error_log = self.response_log
            return False
        
    def run_job(self, job_object):
        
        self.is_job_finished = False
        
        # TAKE IN THE FILE
        self.job_gcode = job_object
        log('Job starting...')
        # SET UP FOR BUFFER STUFFING ONLY: 
        ### (if not initialised - come back to this one later w/ pausing functionality)

        def set_streaming_flags_to_true():
            self.is_stream_lines_remaining = True
            self.is_job_streaming = True    # allow grbl_scanner() to start stuffing buffer
            log('Job running')           

        if self.initialise_job() and self.job_gcode:
            Clock.schedule_once(lambda dt: set_streaming_flags_to_true(), 2)
                                       
        elif not self.job_gcode:
            log('Could not start job: File empty')
            self.sm.get_screen('go').reset_go_screen_prior_to_job_start()
            self.is_job_finished = True
        return

    def initialise_job(self):
            
        if not self.m.is_check_mode_enabled:
            # Move head out of the way before moving to the job datum in XY.
# >>>>>>> revert-196-vac_fix
            # self.m.prepare_machine() #PROBLEM
            self.m.set_led_colour('GREEN')
            self.m.zUp()
  
        self.FLUSH_FLAG = True
        
        time.sleep(0.1)
        
        self._reset_counters()

        return True


    def _reset_counters(self):
        
        # Reset counters & flags
        self.l_count = 0
        self.g_count = 0
        self.c_line = []
        self.stream_start_time = time.time();

    
    def stuff_buffer(self): # attempt to fill GRBLS's serial buffer, if there's room      

        while self.l_count < len(self.job_gcode):
            
            line_to_go = self.job_gcode[self.l_count]
            serial_space = self.RX_BUFFER_SIZE - sum(self.c_line)
    
            # if there's room in the serial buffer, send the line
            if len(line_to_go) + 1 <= serial_space:
                self.c_line.append(len(line_to_go) + 1) # Track number of characters in grbl serial read buffer
                self.write_direct(line_to_go, show_in_sys = True, show_in_console = False) # Send g-code block to grbl
                self.l_count += 1 # lines sent to grbl           
            else:
                return
 
        self.is_stream_lines_remaining = False

    # if 'ok' or 'error' rec'd from GRBL
    def process_grbl_response(self, message):    
        if self.suppress_error_screens == True:
            self.response_log.append(message)

        if message.startswith('error'):
            log('ERROR from GRBL: ' + message)
            
            if self.suppress_error_screens == False and self.sm.current != 'errorScreen':
                self.sm.get_screen('errorScreen').message = message
                
                if self.sm.current == 'alarmScreen':
                    self.sm.get_screen('errorScreen').return_to_screen = self.sm.get_screen('alarmScreen').return_to_screen
                else:
                    self.sm.get_screen('errorScreen').return_to_screen = self.sm.current
                self.sm.current = 'errorScreen'

        # This is a special condition, used only at startup to set EEPROM settings
        if self.is_sequential_streaming:
            self._send_next_sequential_stream()
            
        elif self.is_job_streaming:
            self.g_count += 1 # Iterate g-code counter
            if self.c_line != []:
                del self.c_line[0] # Delete the block character count corresponding to the last 'ok'



    # After streaming is completed
    def end_stream(self):

        # Reset flags
        self.is_job_streaming = False
        self.is_stream_lines_remaining = False
        self.is_job_finished = True

        if not self.m.is_check_mode_enabled:

# >>>>>>> revert-196-vac_fix           
            # move head up and turn vac off
            # self.m.post_cut_sequence() #PROBLEM

            if str(self.job_gcode).count("M3") > str(self.job_gcode).count("M30"):
                self.sm.get_screen('spindle_cooldown').return_screen = 'jobdone'
                self.sm.current = 'spindle_cooldown'
                self.send_stream_time_to_job_done_screen()
            else:
                self.send_stream_time_to_job_done_screen()
                self.sm.current = 'jobdone'

            self._reset_counters()

        else:
            self.m.disable_check_mode()
            self.suppress_error_screens = False
            self._reset_counters()
        
        if self.buffer_monitor_file != None:
            self.buffer_monitor_file.close()
            self.buffer_monitor_file = None 

    def send_stream_time_to_job_done_screen(self):

            # Tell user the job has finished
            log("G-code streaming finished!")
            self.stream_end_time = time.time()
            time_taken_seconds = int(self.stream_end_time - self.stream_start_time) + 10 # to account for cooldown time
            hours = int(time_taken_seconds / (60 * 60))
            seconds_remainder = time_taken_seconds % (60 * 60)
            minutes = int(seconds_remainder / 60)
            seconds = int(seconds_remainder % 60)
            log(" Time elapsed: " + str(time_taken_seconds) + " seconds")

            # send info to the job done screen
            self.sm.get_screen('jobdone').return_to_screen = self.sm.get_screen('go').return_to_screen
            self.sm.get_screen('jobdone').jobdone_text = "The job has finished. It took " + str(hours) + \
             " hours, " + str(minutes) + " minutes, and " + str(seconds) + " seconds."

    def cancel_stream(self):
        self.is_job_streaming = False  # make grbl_scanner() stop stuffing buffer
        self.is_stream_lines_remaining = False
        self._reset_counters()

        if not self.m.is_check_mode_enabled:
            # self.sm.get_screen('go').reset_go_screen_prior_to_job_start()
            
            # Flush
            self.FLUSH_FLAG = True

# >>>>>>> revert-196-vac_fix        
#             # Move head up and turn vac off after a delay
#             Clock.schedule_once(lambda dt: self.m.post_cut_sequence(), 0.5) #PROBLEM
#             
            # Move head up        
            Clock.schedule_once(lambda dt: self.m.self.m.zUp(), 0.5)
            Clock.schedule_once(lambda dt: self.m.self.m.vac_off(), 1)
            # self.sm.get_screen('spindle_cooldown').return_screen = self.sm.get_screen('stop_or_resume_job_decision').return_screen
            # self.sm.current = 'spindle_cooldown'
            

        else:
            self.m.disable_check_mode()
            self.suppress_error_screens = False
            
            # Flush
            self.FLUSH_FLAG = True
        
        
        if self.buffer_monitor_file != None:
            self.buffer_monitor_file.close()
            self.buffer_monitor_file = None

        log("G-code streaming cancelled!")
        


# PUSH MESSAGE HANDLING

    m_state = 'Unknown'

    # Machine co-ordinates
    m_x = '0.0'
    m_y = '0.0'
    m_z = '0.0'

    # Work co-ordinates
    w_x = '0.0'
    w_y = '0.0'
    w_z = '0.0'

    # Work co-ordinate offset
    wco_x = '0.0'
    wco_y = '0.0'
    wco_z = '0.0'

    # G28 position
    g28_x = '0.0'
    g28_y = '0.0'
    g28_z = '0.0'

    # IO Pins for switches etc
    limit_x = False # convention: min is lower_case
    limit_X = False # convention: MAX is UPPER_CASE
    limit_y = False
    limit_Y = False
    limit_z = False
    probe = False
    dust_shoe_cover = False
    spare_door = False

    serial_blocks_available = GRBL_BLOCK_SIZE
    serial_chars_available = RX_BUFFER_SIZE
    print_buffer_status = True


    expecting_probe_result = False
    
    fw_version = ''


    def process_grbl_push(self, message):

        if self.VERBOSE_ALL_PUSH_MESSAGES: print message

        # If it's a status message, e.g. <Idle|MPos:-1218.001,-2438.002,-2.000|Bf:35,255|FS:0,0>
        if message.startswith('<'):
            # 13:09:46.077 < <Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ>
            # 13:09:46.178 < <Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|WCO:-166.126,-213.609,-21.822>
            # 13:09:46.277 < <Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:PxXyYZ|Ov:100,100,100>

            status_parts = message.translate(string.maketrans("", "", ), '<>').split('|') # fastest strip method

            if (status_parts[0] != "Idle" and
                status_parts[0] != "Run" and
                not  (status_parts[0]).startswith("Hold") and
                status_parts[0] != "Jog" and
                status_parts[0] != "Alarm" and
                not (status_parts[0]).startswith("Door") and
                status_parts[0] != "Check" and
                status_parts[0] != "Home" and
                status_parts[0] != "Sleep"):
                log("ERROR status parse: Status invalid: " + message)
                return

            # Get machine's status
            self.m_state = status_parts[0]

            for part in status_parts:

                # Get machine's position (may not be displayed, depending on mask)
                if part.startswith('MPos:'):
                    pos = part[5:].split(',')
                    try:
                        float(pos[0])
                        float(pos[1])
                        float(pos[2])
                    except:
                        log("ERROR status parse: Position invalid: " + message)
                        return

                    self.m_x = pos[0]
                    self.m_y = pos[1]
                    self.m_z = pos[2]

                # Get work's position (may not be displayed, depending on mask)
                elif part.startswith('WPos:'):
                    pos = part[5:].split(',')
                    try:
                        float(pos[0])
                        float(pos[1])
                        float(pos[2])
                    except:
                        log("ERROR status parse: Position invalid: " + message)
                        return
                    self.w_x = pos[0]
                    self.w_y = pos[1]
                    self.w_z = pos[2]

                # Get Work Co-ordinate Offset
                elif part.startswith('WCO:'):
                    pos = part[4:].split(',')
                    try:
                        float(pos[0])
                        float(pos[1])
                        float(pos[2])
                    except:
                        log("ERROR status parse: Position invalid: " + message)
                        return
                    self.wco_x = pos[0]
                    self.wco_y = pos[1]
                    self.wco_z = pos[2]

                # Get grbl's buffer status
                elif part.startswith('Bf:'):
                    buffer_info = part[3:].split(',')

                    try:
                        int(buffer_info[0])
                        int(buffer_info[1])
                    except:
                        log("ERROR status parse: Buffer status invalid: " + message)
                        return

                    # if different from last check
                    if self.serial_chars_available != buffer_info[1]:
                        self.serial_chars_available = buffer_info[1]
#                         self.sm.get_screen('go').grbl_serial_char_capacity.text = "[color=808080]C: " + self.serial_chars_available + "[/color]"
                        self.print_buffer_status = True # flag to print

                    if self.serial_blocks_available != buffer_info[0]:
                        self.serial_blocks_available = buffer_info[0]
#                         self.sm.get_screen('go').grbl_serial_line_capacity.text = "[color=808080]L: " + self.serial_blocks_available + "[/color]"
                        self.print_buffer_status = True # flag to print

                    # print if change flagged
                    if self.print_buffer_status == True:
                        self.print_buffer_status = False

                # Get limit switch states: Pn:PxXyYZ
                elif part.startswith('Pn:'):
                    
                    pins_info = part.split(':')[1]
                    
                    if 'x' in pins_info: self.limit_x = True
                    else: self.limit_x = False
                    
                    if 'X' in pins_info: self.limit_X = True
                    else: self.limit_X = False
                    
                    if 'y' in pins_info: self.limit_y = True
                    else: self.limit_y = False
                    
                    if 'Y' in pins_info: self.limit_Y = True
                    else: self.limit_Y = False
                    
                    if 'Z' in pins_info: self.limit_z = True
                    else: self.limit_z = False

                    if 'P' in pins_info: self.probe = True
                    else: self.probe = False

                    if 'g' in pins_info: self.spare_door = True
                    else: self.spare_door = False
                    
                    if 'G' in pins_info: self.dust_shoe_cover = True
                    else: self.dust_shoe_cover = False
                
                elif part.startswith("Door") and self.m.is_machine_paused == False:
                    if part.startswith("Door:3"):
                        pass
                    else:
                        self.m.set_pause(True) # sets flag is_machine_paused so this stub only gets called once
                        if self.sm.current != 'door':
                            log("Hard " + self.m_state)

                            if self.suppress_door_screens == False:
                                self.sm.get_screen('door').return_to_screen = self.sm.current 
                                self.sm.current = 'door'

                elif part.startswith('Ld:'):
                    overload_raw_mV = int(part.split(':')[1])  # gather spindle overload analogue voltage, and evaluate to general state
                    if overload_raw_mV < 750 : overload_mV_equivalent_state = 0
                    elif overload_raw_mV < 1750 : overload_mV_equivalent_state = 20
                    elif overload_raw_mV < 3000 : overload_mV_equivalent_state = 40
                    elif overload_raw_mV < 3750 : overload_mV_equivalent_state = 60
                    elif overload_raw_mV < 4250 : overload_mV_equivalent_state = 80
                    elif overload_raw_mV < 4750 : overload_mV_equivalent_state = 90
                    elif overload_raw_mV >= 4750 : overload_mV_equivalent_state = 100
                    else: log("Overload value not recognised")
                   

                    self.overload_pin_mV = overload_raw_mV
                    # # update stuff if there's a change
                    # if overload_mV_equivalent_state != self.overload_state:  
                    #     self.overload_state = overload_mV_equivalent_state
                    #     log("Overload state change: " + str(self.overload_state))
                    
                    #     try:
                    #         self.sm.get_screen('go').update_overload_label(self.overload_state)
                    #     except:
                    #         log('Unable to update_overlaod_state on go screen')
                    
                    # # if it's max load, activate a timer to check back in a second. The "checking back" is about ensuring the signal wasn't a noise event.
                    # if self.overload_state == 100 and self.is_ready_to_assess_spindle_for_shutdown:
                    #     self.is_ready_to_assess_spindle_for_shutdown = False  # flag prevents further shutdowns until this one has been cleared
                    #     Clock.schedule_once(self.check_for_sustained_max_overload, 1)

                else:
                    continue

            if self.VERBOSE_STATUS: print (self.m_state, self.m_x, self.m_y, self.m_z,
                                           self.serial_blocks_available, self.serial_chars_available)

 
        elif message.startswith('ALARM:'):
            log('ALARM from GRBL: ' + message)
            if self.suppress_alarm_screens == False:
                if self.sm.current != 'alarmScreen':
                    self.sm.get_screen('alarmScreen').message = message
                    if self.sm.current == 'errorScreen':
                        self.sm.get_screen('alarmScreen').return_to_screen = self.sm.get_screen('errorScreen').return_to_screen
                    else:
                        self.sm.get_screen('alarmScreen').return_to_screen = self.sm.current
                    self.sm.current = 'alarmScreen'

        elif message.startswith('$'):
            log(message)
            setting_and_value = message.split("=")
            setting = setting_and_value[0]
            value = float(setting_and_value[1])

            # Detect setting and update value in software
            # '$$' is called to yield the report from grbl
            # It is called at init, at end of "start_sequential_stream" function - this forces sw to be in sync with grbl settings

            if setting == '$0': self.setting_0 = value; # Step pulse, microseconds
            elif setting == '$1': self.setting_1 = value;  # Step idle delay, milliseconds
            elif setting == '$2': self.setting_2 = value;  # Step port invert, mask
            elif setting == '$3': self.setting_3 = value;  # Direction port invert, mask
            elif setting == '$4': self.setting_4 = value;  # Step enable invert, boolean
            elif setting == '$5': self.setting_5 = value;  # Limit pins invert, boolean
            elif setting == '$6': self.setting_6 = value;  # Probe pin invert, boolean
            elif setting == '$10': self.setting_10 = value;  # Status report, mask
            elif setting == '$11': self.setting_11 = value;  # Junction deviation, mm
            elif setting == '$12': self.setting_12 = value;  # Arc tolerance, mm
            elif setting == '$13': self.setting_13 = value;  # Report inches, boolean
            elif setting == '$20': self.setting_20 = value;  # Soft limits, boolean
            elif setting == '$21': self.setting_21 = value;  # Hard limits, boolean
            elif setting == '$22': self.setting_22 = value;  # Homing cycle, boolean
            elif setting == '$23': self.setting_23 = value;  # Homing dir invert, mask
            elif setting == '$24': self.setting_24 = value;  # Homing feed, mm/min
            elif setting == '$25': self.setting_25 = value;  # Homing seek, mm/min
            elif setting == '$26': self.setting_26 = value;  # Homing debounce, milliseconds
            elif setting == '$27': self.setting_27 = value;  # Homing pull-off, mm
            elif setting == '$30': self.setting_30 = value;  # Max spindle speed, RPM
            elif setting == '$31': self.setting_31 = value;  # Min spindle speed, RPM
            elif setting == '$32': self.setting_32 = value;  # Laser mode, boolean
            elif setting == '$50': self.setting_50 = value; # Serial number and product code
            elif setting == '$100': self.setting_100 = value;  # X steps/mm
            elif setting == '$101': self.setting_101 = value;  # Y steps/mm
            elif setting == '$102': self.setting_102 = value;  # Z steps/mm
            elif setting == '$110': # X Max rate, mm/min
                self.setting_110 = value;
                self.sm.get_screen('home').common_move_widget.fast_x_speed = value
                self.sm.get_screen('home').common_move_widget.set_jog_speeds()
            elif setting == '$111': # Y Max rate, mm/min
                self.setting_111 = value;
                self.sm.get_screen('home').common_move_widget.fast_y_speed = value
                self.sm.get_screen('home').common_move_widget.set_jog_speeds()
            elif setting == '$112': # Z Max rate, mm/min
                self.setting_112 = value;
                self.sm.get_screen('home').common_move_widget.fast_z_speed = value
                self.sm.get_screen('home').common_move_widget.set_jog_speeds()
            elif setting == '$120': self.setting_120 = value;  # X Acceleration, mm/sec^2
            elif setting == '$121': self.setting_121 = value;  # Y Acceleration, mm/sec^2
            elif setting == '$122': self.setting_122 = value;  # Z Acceleration, mm/sec^2
            elif setting == '$130':
                self.setting_130 = value;
                self.m.grbl_x_max_travel = value  # X Max travel, mm
                self.m.set_jog_limits()
            elif setting == '$131':
                self.setting_131 = value;
                self.m.grbl_y_max_travel = value  # Y Max travel, mm
                self.m.set_jog_limits()
            elif setting == '$132':
                self.setting_132 = value;
                self.m.grbl_z_max_travel = value  # Z Max travel, mm
                self.m.set_jog_limits()


        # [G54:], [G55:], [G56:], [G57:], [G58:], [G59:], [G28:], [G30:], [G92:],
        # [TLO:], and [PRB:] messages indicate the parameter data printout from a $# user query.
        elif message.startswith('['):
                      
            stripped_message = message.translate(string.maketrans("", "", ), '[]') # fastest strip method

            if stripped_message.startswith('G28:'):

                pos = stripped_message[4:].split(',')
                self.g28_x = pos[0]
                self.g28_y = pos[1]
                self.g28_z = pos[2]
                
            elif stripped_message.startswith('G54:'):
                
                pos = stripped_message[4:].split(',')
                self.g54_x = pos[0]
                self.g54_y = pos[1]
                self.g54_z = pos[2]

            # Process a successful probing op [PRB:0.000,0.000,0.000:0]
            elif self.expecting_probe_result and stripped_message.startswith('PRB'):

                log(stripped_message)

                successful_probe = stripped_message.split(':')[2]
                
                if successful_probe:

                    z_machine_coord_when_probed = stripped_message.split(':')[1].split(',')[2]
                    log('Probed at machine height: ' + z_machine_coord_when_probed)
                    self.m.probe_z_detection_event(z_machine_coord_when_probed)


                self.expecting_probe_result = False # clear flag
                
            elif stripped_message.startswith('ASM CNC'):
                self.fw_version = stripped_message.split(':')[1]
                log('FW version: ' + str(self.fw_version))


    def check_for_sustained_max_overload(self, dt):
        
        if self.overload_state == 100:  # if still at max overload, begin the spindle pause procedure
            
            self.sm.get_screen('spindle_shutdown').reason_for_pause = "spindle_overload"
            self.sm.get_screen('spindle_shutdown').return_screen = str(self.sm.current)
            self.sm.current = 'spindle_shutdown'

        else: # must have just been a noisy blip
            
            self.is_ready_to_assess_spindle_for_shutdown = True  # allow spindle overload assessment to resume
        


## SEQUENTIAL STREAMING

    # This stream_file method waits for an 'ok' before sending the next setting
    # It does not stuff the grbl buffer
    # It is for:
    ## Anything sending EEPROM settings (which require special attention, due to writing of values)
    ## Matching Error/Alarm messages to exact commands (not possible during buffer stuffing)
    # WARNING: this function is not blocking, as such, the is_sequential_streaming flag should be checked before using.
    
    is_sequential_streaming = False
    _sequential_stream_buffer = []
    _reset_grbl_after_stream = False

    def start_sequential_stream(self, list_to_stream, reset_grbl_after_stream=False):
        log("start_sequential_stream")
        self._sequential_stream_buffer = list_to_stream
        self._reset_grbl_after_stream = reset_grbl_after_stream
        self._send_next_sequential_stream()
        
                
    def _send_next_sequential_stream(self):
        if self._sequential_stream_buffer:
            self.is_sequential_streaming = True
            self.write_direct(self._sequential_stream_buffer[0])
            del self._sequential_stream_buffer[0]
        else:
            self.is_sequential_streaming = False
            log("sequential stream ended")
            if self._reset_grbl_after_stream:
                self.m.reset_after_sequential_stream()
                log("GRBL Reset after sequential stream ended")


    def cancel_sequential_stream(self, reset_grbl_after_cancel = False):
        self.is_sequential_streaming = False
        _sequential_stream_buffer = []
        if reset_grbl_after_cancel:
            self.m.reset_after_sequential_stream()
            print "GRBL Reset after sequential stream cancelled"


## WRITE-----------------------------------------------------------------------------


    def write_direct(self, serialCommand, show_in_sys = True, show_in_console = True, altDisplayText = None, realtime = False):

#         print "Write in console = ", show_in_console
        # Issue to logging outputs first (so the command is logged before any errors/alarms get reported back)
        try:
            # Print to sys (external command interface e.g. console in Eclipse, or at the prompt on the Pi)
            #if show_in_sys and altDisplayText==None: print serialCommand
            if not serialCommand.startswith('?'):
                log('> ' + serialCommand)
            if altDisplayText != None: print altDisplayText

            # Print to console in the UI
            if show_in_console == True and altDisplayText == None:
                self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('snd', serialCommand)
            if altDisplayText != None:
                self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('snd', altDisplayText)

        except:
            print "FAILED to display on CONSOLE: " + serialCommand + " (Alt text: " + str(altDisplayText) + ")"
            # log('Console display error: ' + str(consoleDisplayError))

        # Finally issue the command        
        if self.s:
            try:
                
                if realtime == False:
                    # INLCUDES end of line command (which returns an 'ok' from grbl - used in algorithms)
                    self.s.write(serialCommand + '\n')
                
                elif realtime == True:
                    # OMITS end of line command (which returns an 'ok' from grbl - used in counting/streaming algorithms)
                    self.s.write(serialCommand)

                # SmartBench maintenance monitoring 
#                 self.maintenance_value_logging(serialCommand)
                

            except:
#                  SerialException as serialError:
                print "FAILED to write to SERIAL: " + serialCommand + " (Alt text: " + str(altDisplayText) + ")"
                self.get_serial_screen('Could not write last command to serial buffer.')
    #                 log('Serial Error: ' + str(serialError))
        

    # TODO: Are kwargs getting pulled successully by write_direct from here?
    def write_command(self, serialCommand, **kwargs):
        
        self.write_command_buffer.append([serialCommand, kwargs])        
## OLD --------------------------------------------------------------------------------------------
#         # INLCUDES end of line command (which returns an 'ok' from grbl - used in algorithms)
#         # Issue to logging outputs first (so the command is logged before any errors/alarms get reported back)
#         try:
#             # Print to sys (external command interface e.g. console in Eclipse, or at the prompt on the Pi)
#             #if show_in_sys and altDisplayText==None: print serialCommand
#             log('> ' + serialCommand)
#             if altDisplayText != None: print altDisplayText
# 
#             # Print to console in the UI
#             if show_in_console  and altDisplayText == None:
#                 self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('snd', serialCommand)
#             if altDisplayText != None:
#                 self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('snd', altDisplayText)
# 
#         except:
#             print "FAILED to display on CONSOLE: " + serialCommand + " (Alt text: " + str(altDisplayText) + ")"
#             log('Console display error: ' + str(consoleDisplayError))
# 
#         # Finally issue the command
#         if self.s:
#             try:
#                 self.s.write(serialCommand + '\n')
#                 
#             except SerialException as serialError:
#                 print "FAILED to write to SERIAL: " + serialCommand + " (Alt text: " + str(altDisplayText) + ")"
#                 log('Serial Error: ' + str(serialError))
## -----------------------------------------------------------------------------------------------------

    # Many realtime commands are non-printables, and cause the gcode console to crash. 
    # GCode console with therefore print 'altDisplayText' arg instead
    def write_realtime(self, serialCommand, altDisplayText = None):
        
        self.write_realtime_buffer.append([serialCommand, altDisplayText])

## OLD -------------------------------------------------------------------------------------------------
#         # OMITS end of line command (which returns an 'ok' from grbl - used in counting/streaming algorithms)
# 
#         # Issue to logging outputs first (so the command is logged before any errors/alarms get reported back)
#         try:
#             # Print to sys (external command interface e.g. console in Eclipse, or at the prompt on the Pi)
#             #if show_in_sys and altDisplayText==None: print serialCommand
#             if not serialCommand.startswith('?'):
#                 log('> ' + serialCommand)
#             if altDisplayText != None: print altDisplayText
# 
#             # Print to console in the UI
#             if show_in_console and altDisplayText == None:
#                 self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('snd', serialCommand)
#             if altDisplayText != None:
#                 self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('snd', altDisplayText)
# 
#         except:
#             print "FAILED to display on CONSOLE: " + serialCommand + " (Alt text: " + str(altDisplayText) + ")"
#             log('Console display error: ' + str(consoleDisplayError))
# 
#         # Finally issue the command
#         if self.s:
#             try:
#                 self.s.write(serialCommand)
# 
#             except SerialException as serialError:
#                 print "FAILED to write to SERIAL: " + serialCommand + " (Alt text: " + str(altDisplayText) + ")"
#                 log('Serial Error: ' + str(serialError))
## --------------------------------------------------------------------------------------------------------






##### Warning: WIP. 
# Dangerous conflicts. 
# E.g. cannot handle an 'M56' command, since it acts on it as if it was an M5!!!!!!

# 
#     def maintenance_value_logging(self, serialCommand):
#         
#         # Record spindle up time
#         if serialCommand.find('M30') >= 0: 
#             pass
#         elif serialCommand.find ('M3') >= 0 or serialCommand.find ('M03') >= 0:
#             log("Spindle timer started")
#             self.spindle_start_time = time.time()
#             
#         if serialCommand.find ('M5') >= 0 or serialCommand.find ('M05') >= 0 or serialCommand.find ('M30') >= 0 or serialCommand.find ('M2') >= 0:
#             log("Spindle timer stopped")
#             self.spindle_finish_time = time.time()
#             spindle_session_on_seconds = int(self.spindle_finish_time - self.spindle_start_time)
#             try:
#                 file = open(self.m.spindle_brush_use_file_path, 'r')
#                 existing_value_in_file = file.readline()
#                 total_up_seconds = int(existing_value_in_file) + spindle_session_on_seconds
#                 file = open(self.m.spindle_brush_use_file_path, 'w')
#                 file.write(str(total_up_seconds))
#                 file.close
#             except:
#                 log("Unable to write to " + self.m.spindle_brush_use_file_path)
# 
# 


