'''
Created on 31 Jan 2018
@author: Ed
Module to manage all serial comms between pi (EasyCut s/w) and realtime arduino chip (GRBL f/w)
'''

from kivy.config import Config
from __builtin__ import True

import serial, sys, time, string, threading, serial.tools.list_ports
from datetime import datetime, timedelta
from os import listdir
from kivy.clock import Clock

import re
from functools import partial
from serial.serialutil import SerialException

# Import managers for GRBL Notification screens (e.g. alarm, error, etc.)
from asmcnc.core_UI.sequence_alarm import alarm_manager


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

    yp = None # Yetipilot object

    grbl_out = ""
    response_log = []
    suppress_error_screens = False
    FLUSH_FLAG = False
    
    write_command_buffer = []
    write_realtime_buffer = []
    write_protocol_buffer = []

    last_protocol_send_time = 0
    
    monitor_text_buffer = ""
    overload_state = 0
    prev_overload_state = 0
    is_ready_to_assess_spindle_for_shutdown = True

    power_loss_detected = False

    # Flag to kill grbl scanner (used in zhead cycle app)
    # Need to disable grbl scanner before closing serial connection, or else causes problems (at least in windows)
    grbl_scanner_running = False

    def __init__(self, machine, screen_manager, settings_manager, localization, job):

        self.sm = screen_manager
        self.sett =settings_manager     
        self.m = machine
        self.jd = job
        self.l = localization
        # Initialise managers for GRBL Notification screens (e.g. alarm, error, etc.)
        self.alarm = alarm_manager.AlarmSequenceManager(self.sm, self.sett, self.m, self.l, self.jd)
        self.FINAL_TEST = False

    def __del__(self):
        if self.s: self.s.close()
        log('Serial connection destructor')

    def get_serial_screen(self, serial_error):

        try:
            if self.sm.current != 'serialScreen' and self.sm.current != 'rebooting':
                self.sm.get_screen('serialScreen').error_description = self.l.get_str(serial_error)
                self.sm.current = 'serialScreen'

        except:
            log("Serial comms interrupted but no serial screen - are you in diagnostics mode?")
            log("Serial error: " + str(serial_error))


    def is_port_SmartBench(self, available_port):

        try: 
            log("Try to connect to: " + available_port)
            # set up connection
            self.s = serial.Serial(str(available_port), BAUD_RATE, timeout = 6, writeTimeout = 20) # assign

            # reopen port, just in case its been in use somewhere else
            self.s.close()
            self.s.open()
            # serial object needs time to make the connection before we can do anything else
            time.sleep(1)

            try:
                # flush input and soft-reset: this will trigger the GRBL welcome message
                self.s.flushInput()
                self.s.write("\x18")
                # give it a second to reply
                time.sleep(1)
                first_bytes = self.s.inWaiting()
                log("Is port SmartBench? " + str(available_port) + "| First read: " + str(first_bytes))

                if first_bytes:

                    # Read in first input and log it
                    def strip_and_log(input_string):
                        new_string = input_string.strip()
                        log(new_string)
                        return new_string

                    stripped_input = map(strip_and_log, self.s.readlines())

                    # Is this device a SmartBench? 
                    if any('SmartBench' in ele for ele in stripped_input):
                        # Found SmartBench! 
                        SmartBench_port = available_port
                        return SmartBench_port

                    else:
                        self.s.close()
                else:
                    self.s.close()

            except:
                log("Could not communicate with that port at all")

        except: 
            log("Wow definitely not that port")

        return ''

    def quick_connect(self, available_port):
        try: 
            log("Try to connect to: " + available_port)
            # set up connection
            self.s = serial.Serial(str(available_port), BAUD_RATE, timeout = 6, writeTimeout = 20) # assign
            self.s.flushInput()
            self.s.write("\x18")
            return available_port
        
        except:
            log("Could not connect to given port.")
            return ''


    def establish_connection(self, win_port):

        log('Start to establish connection...')
        SmartBench_port = ''

        # Parameter 'win'port' only used for windows dev e.g. "COM4"
        # No idea if this works yet - needs testing on a windows computer!
        if sys.platform == "win32":
            self.suppress_error_screens = True

            # try user-given Comport first
            SmartBench_port = self.quick_connect(win_port)

            # If given port doesn't work, try others:
            if not SmartBench_port:

                port_list = [port.device for port in serial.tools.list_ports.comports() if 'n/a' not in port.description]

                print("Windows port list: ") # for debugging
                print(str(port_list))

                for comport in port_list:

                    print("Windows port to try: ")
                    print comport

                    SmartBench_port = self.is_port_SmartBench(comport)
                    if SmartBench_port: break
                    
                if not SmartBench_port: 
                    log("No arduino connected")

        elif sys.platform == "darwin":
            self.suppress_error_screens = True

            filesForDevice = listdir('/dev/') # put all device files into list[]
            for line in filesForDevice:
                if line.startswith('tty.usbmodem'): # look for... 

                    print("Mac port to try: ") # for debugging
                    print line

                    SmartBench_port = self.is_port_SmartBench('/dev/' + str(line))
                    if SmartBench_port: break

            if not SmartBench_port: 
                log("No arduino connected")

        else:
            try:
                # list of portst that we may want to use, in order of preference
                default_serial_port = 'ttyS'
                ACM_port = 'ttyACM'
                USB_port = 'ttyUSB'
                AMA_port = 'ttyAMA'

                port_list = [default_serial_port, ACM_port, USB_port, AMA_port]

                filesForDevice = listdir('/dev/') # put all device files into list[]

                # this comes out in order of preference too :)
                list_of_available_ports = [port for potential_port in port_list for port in filesForDevice if potential_port in port]

                # set up serial connection with first (most preferred) available port
                for available_port in list_of_available_ports:
                    SmartBench_port = self.is_port_SmartBench('/dev/' + str(available_port))
                    if SmartBench_port: break

                # If all else fails, try to connect to ttyS or ttyAMA port anyway
                if SmartBench_port == '':

                    first_port = list_of_available_ports[0]
                    last_port = list_of_available_ports[-1]
                    try: 
                        if default_serial_port in first_port:
                            first_list_index = 1
                            self.s = serial.Serial('/dev/' + first_port, BAUD_RATE, timeout = 6, writeTimeout = 20) # assign
                            SmartBench_port = ": could not identify if any port was SmartBench, so attempting " + first_port
                    except: 
                        if AMA_port in last_port:
                            last_list_index = -1
                            self.s = serial.Serial('/dev/' + last_port, BAUD_RATE, timeout = 6, writeTimeout = 20) # assign
                            SmartBench_port = ": could not identify if any port was SmartBench, so attempting " + last_port

                    if SmartBench_port == '':
                        Clock.schedule_once(lambda dt: self.get_serial_screen('Could not establish a connection on startup.'), 5)

            except:
                # I doubt this will be triggered with all the other try-excepts, but will leave it in anyway. 
                Clock.schedule_once(lambda dt: self.get_serial_screen('Could not establish a connection on startup.'), 5) # necessary bc otherwise screens not initialised yet      

        log("Serial connection status: " + str(self.is_connected()) + " " + str(SmartBench_port))
        
        try: 
            if self.is_connected():
                log('Initialising grbl...')
                self.write_direct("\r\n\r\n", realtime = False, show_in_sys = False, show_in_console = False)    # Wakes grbl

        except:
            Clock.schedule_once(lambda dt: self.get_serial_screen('Could not establish a connection on startup.'), 5) # necessary bc otherwise screens not initialised yet      

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
        self.grbl_scanner_running = True
        t = threading.Thread(target=self.grbl_scanner)
        t.daemon = True
        t.start()
        
        # Clear any hard switch presses that may have happened during boot
        self.m.bootup_sequence()

        self.m.starting_serial_connection = False

# SCANNER: listens for responses from Grbl

    # "Response" is a message from GRBL saying how a line of gcode went (either 'ok', or 'error') when it was loaded from the serial buffer into the line buffer
    # When streaming, monitoring the response from GRBL is essential for EasyCut to know when to send the next line
    # Full docs: https://github.com/gnea/grbl/wiki/Grbl-v1.1-Interface

    # "Push" is for messages from GRBL to provide more general feedback on what Grbl is doing (e.g. status)

    VERBOSE_ALL_PUSH_MESSAGES = False
    VERBOSE_ALL_RESPONSE = False
    VERBOSE_STATUS = False


    def grbl_scanner(self, run_grbl_scanner_once = False):
        
        log('Running grbl_scanner thread')

        while self.grbl_scanner_running or run_grbl_scanner_once:

                         
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
                
            del self.write_command_buffer[0:(command_counter)]

            realtime_counter = 0
            for realtime_command in self.write_realtime_buffer:
                self.write_direct(realtime_command[0], altDisplayText = realtime_command[1], realtime = True)
                realtime_counter += 1

            del self.write_realtime_buffer[0:(realtime_counter)]

            if self.write_protocol_buffer and self.last_protocol_send_time + 0.05 < time.time():
                protocol_command = self.write_protocol_buffer[0]
                self.write_direct(protocol_command[0], altDisplayText = protocol_command[1], protocol = True)
                del self.write_protocol_buffer[0]



            # If there's a message received, deal with it depending on type:
            if self.s.inWaiting():
                # Read line in from serial buffer
                try:
                    rec_temp = self.s.readline().strip() #Block the executing thread indefinitely until a line arrives

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
                        # - this bit grinds to a halt
    
                # Job streaming: stuff buffer
                if (self.is_job_streaming and not self.m.is_machine_paused and not "Alarm" in self.m.state()):
                    if self.yp.use_yp: self.yp.add_to_stack()
                    if self.is_stream_lines_remaining:
                        self.stuff_buffer()
                    else: 
                        if self.g_count == self.l_count:
                            self.end_stream()

                # Sets off sequential streaming from this grbl scanner thread:
                if self._ready_to_send_first_sequential_stream and self.is_buffer_clear():
                    self._send_next_sequential_stream()

            run_grbl_scanner_once = False
                    
        # Loop this method
        #Clock.schedule_once(self.grbl_scanner, GRBL_SCANNER_MIN_DELAY)

        # These lines should only be executed when grbl scanner is intentionally killed
        log('Killed grbl_scanner')
        self.m_state = 'Off'



# STREAMING: sending gcode, using character counting protocol described here:
# https://github.com/gnea/grbl/wiki/Grbl-v1.1-Interface


    # streaming variables
    GRBL_BLOCK_SIZE = 35    # max number of gcode lines which GRBL can put in its 'BLOCK' or look ahead buffer
    RX_BUFFER_SIZE = 255    # serial buffer which gets filled by EasyCut. GRBL grabs from this when there is block space

    is_job_streaming = False
    is_stream_lines_remaining = False

    g_count = 0 # gcodes processed (ok/error'd) by grbl (gcodes may not get processed immediately after being sent)
    l_count = 0 # lines sent to grbl
    c_line = [] # char count of blocks/lines in grbl's serial buffer
    
    stream_start_time = 0
    stream_end_time = 0

    stream_pause_start_time = 0
    stream_paused_accumulated_time = 0

    check_streaming_started = False

    NOT_SKELETON_STUFF = True # do buffer stuffing in "skeleton mode" - no go/job screens/spindle moves etc. 
    
    def check_job(self, job_object):
        
        log('Checking job...')

        self.m.enable_check_mode()
        self.yp.use_yp = False

        def check_job_inner_function():
            # Check that check mode has been enabled before running:
            if self.m_state == "Check":

                # check has now started:
                self.check_streaming_started = True

                # Set up error logging
                self.suppress_error_screens = True
                self.response_log = []
                
                # run job as per normal
                self.run_job(job_object)

                # get error log back to the checking screen when it's ready
                Clock.schedule_interval(partial(self.return_check_outcome, job_object), 0.1)

            else:
                Clock.schedule_once(lambda dt: check_job_inner_function(), 0.9)

        # Sleep to ensure check mode ok isn't included in log, AND to ensure it's enabled before job run
        Clock.schedule_once(lambda dt: check_job_inner_function(), 0.9)

    def return_check_outcome(self, job_object, dt):
        if len(self.response_log) >= len(job_object):
            self.suppress_error_screens = False
            self.sm.get_screen('check_job').error_log = self.response_log
            return False
        
    def run_job(self, job_object):

        self.jd.job_gcode_running = job_object

        log('Job starting...')
        # SET UP FOR BUFFER STUFFING ONLY: 
        ### (if not initialised - come back to this one later w/ pausing functionality)    

        if self.initialise_job() and self.jd.job_gcode_running:
            Clock.schedule_once(lambda dt: self.set_streaming_flags_to_true(), 2)
                                       
        elif not self.jd.job_gcode_running:
            log('Could not start job: File empty')
            self.sm.get_screen('go').reset_go_screen_prior_to_job_start()

    def initialise_job(self):
            
        if self.m_state != "Check":
            self.m.set_led_colour('GREEN')
            self.m.zUp()
  
        self.FLUSH_FLAG = True
        self.NOT_SKELETON_STUFF = True
        time.sleep(0.1)
        self._reset_counters()
        return True

    # USED FOR RUNNING THINGS THAT ARE NOT CUSTOMER FACING
    def run_skeleton_buffer_stuffer(self, gcode_obj):
        self.jd.job_gcode_running = gcode_obj

        log('Skeleton buffer stuffing starting...')
        # SET UP FOR BUFFER STUFFING ONLY: 
        ### (if not initialised - come back to this one later w/ pausing functionality)    

        self.FLUSH_FLAG = True
        self.NOT_SKELETON_STUFF = False
        time.sleep(0.1)
        self._reset_counters()

        if self.jd.job_gcode_running:
            Clock.schedule_once(lambda dt: self.set_streaming_flags_to_true(), 2)

    def _reset_counters(self):
        
        # Reset counters & flags
        self.l_count = 0
        self.g_count = 0
        self.c_line = []
        self.stream_pause_start_time = 0
        self.stream_paused_accumulated_time = 0
        self.stream_start_time = time.time()

    def set_streaming_flags_to_true(self):
        # self.m.set_pause(False) # moved to go screen for timing reasons
        self.is_stream_lines_remaining = True
        self.is_job_streaming = True    # allow grbl_scanner() to start stuffing buffer
        log('Job running')
    
    def stuff_buffer(self): # attempt to fill GRBLS's serial buffer, if there's room      

        while self.l_count < len(self.jd.job_gcode_running):
            
            line_to_go = self.add_line_number_to_gcode_line(self.jd.job_gcode_running[self.l_count], self.l_count)
            serial_space = self.RX_BUFFER_SIZE - sum(self.c_line)
    
            # if there's room in the serial buffer, send the line
            if len(line_to_go) + 1 <= serial_space:
                self.c_line.append(len(line_to_go) + 1) # Track number of characters in grbl serial read buffer
                self.write_direct(line_to_go, show_in_sys = True, show_in_console = False) # Send g-code block to grbl
                self.l_count += 1 # lines sent to grbl           
            else:
                return
 
        self.is_stream_lines_remaining = False

    # line counting for buffer stuffing
    def add_line_number_to_gcode_line(self, line, i):
        return line if self.gcode_line_is_excluded(line) else 'N' + str(i) + line

    def gcode_line_is_excluded(self, line):
        return '(' in line or ')' in line or '$' in line or 'AE' in line or 'AF' in line

    # PROCESSING GRBL RESPONSES

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
        if self._process_oks_from_sequential_streaming:
            self._send_next_sequential_stream()
            
        elif self.is_job_streaming:
            self.g_count += 1 # Iterate g-code counter
            if self.c_line != []:
                del self.c_line[0] # Delete the block character count corresponding to the last 'ok'

    # After streaming is completed
    def end_stream(self):

        log("Ending stream...")

        # Reset flags
        self.is_job_streaming = False
        self.is_stream_lines_remaining = False
        self.m.set_pause(False)
        self.yp.use_yp = False

        if self.NOT_SKELETON_STUFF:

            if self.m_state != "Check":

                if (str(self.jd.job_gcode_running).count("M3") > str(self.jd.job_gcode_running).count("M30")) and self.m.stylus_router_choice != 'stylus':
                    Clock.schedule_once(lambda dt: self.update_machine_runtime(), 0.4)
                    self.sm.get_screen('spindle_cooldown').return_screen = 'job_feedback'
                    self.sm.current = 'spindle_cooldown'
                else:
                    self.m.spindle_off()
                    time.sleep(0.4)
                    self.update_machine_runtime()
                    self.sm.current = 'job_feedback'

            else:
                self.check_streaming_started = False
                self.m.disable_check_mode()
                self.suppress_error_screens = False
                self._reset_counters()

        else:
            self._reset_counters()
            self.NOT_SKELETON_STUFF = True

        self.jd.job_gcode_running = []
        self.jd.percent_thru_job = 100

    def cancel_stream(self):

        self.is_job_streaming = False  # make grbl_scanner() stop stuffing buffer
        self.is_stream_lines_remaining = False
        self.m.set_pause(False)
        self.jd.job_gcode_running = []
        self.yp.use_yp = False

        if self.m_state != "Check":
            
            # Flush
            self.FLUSH_FLAG = True
     
            # Move head up        
            Clock.schedule_once(lambda dt: self.m.zUp(), 0.5)
            Clock.schedule_once(lambda dt: self.m.vac_off(), 1)

            # Update time for maintenance reminders
            time.sleep(0.4)
            self.update_machine_runtime()
            

        else:
            self.check_streaming_started = False
            self.m.disable_check_mode()
            self.suppress_error_screens = False
            
            # Flush
            self.FLUSH_FLAG = True
            self._reset_counters()

        self.NOT_SKELETON_STUFF = True

        log("G-code streaming cancelled!")


    def update_machine_runtime(self):

        log("G-code streaming finished!")
        self.stream_end_time = time.time()
        time_taken_seconds = int(self.stream_end_time - self.stream_start_time) + 10 # to account for cooldown time
        only_running_time_seconds = time_taken_seconds - self.stream_paused_accumulated_time

        self.jd.pause_duration = str(timedelta(seconds=self.stream_paused_accumulated_time)).split(".")[0]
        self.jd.total_time = str(timedelta(seconds=time_taken_seconds)).split(".")[0]
        self.jd.actual_runtime = str(timedelta(seconds=only_running_time_seconds)).split(".")[0]

        log("Time elapsed: " + self.jd.total_time)
        log("Time paused: " + self.jd.pause_duration)
        log("Actual running time: " + self.jd.actual_runtime)

        ## UPDATE MAINTENANCE TRACKING

        # Add time taken in seconds to brush use: 
        if self.m.stylus_router_choice == 'router': # and not self.m.get_dollar_setting(51):
            self.m.spindle_brush_use_seconds += only_running_time_seconds
            self.m.write_spindle_brush_values(self.m.spindle_brush_use_seconds, self.m.spindle_brush_lifetime_seconds)

        # Add time taken in seconds to calibration tracking
        self.m.time_since_calibration_seconds += only_running_time_seconds
        self.m.write_calibration_settings(self.m.time_since_calibration_seconds, self.m.time_to_remind_user_to_calibrate_seconds)

        # Add time taken in seconds since Z head last lubricated
        self.m.time_since_z_head_lubricated_seconds += only_running_time_seconds
        self.m.write_z_head_maintenance_settings(self.m.time_since_z_head_lubricated_seconds)

        self._reset_counters()
        

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

    # Line number
    grbl_ln = None

    # Feeds and speeds
    spindle_speed = 0
    feed_rate = 0

    # Feed override feedback
    feed_override_percentage = 100
    speed_override_percentage = 100

    # Analogue spindle feedback
    spindle_load_voltage = None

    # Digital spindle feedback
    digital_spindle_ld_qdA = None
    digital_spindle_temperature = None
    digital_spindle_kill_time = None
    digital_spindle_mains_voltage = None

    # Spindle data "inrush" counter
    digital_load_pattern = re.compile(r"Ld:\d+,\d+,\d+,\d+")
    inrush_counter = 0

    # IO Pins for switches etc
    limit_x = False # convention: min is lower_case
    limit_X = False # convention: MAX is UPPER_CASE
    limit_y = False
    limit_Y = False
    limit_z = False
    probe = False
    dust_shoe_cover = False
    spare_door = False
    limit_Y_axis = False
    stall_X = False
    stall_Z = False
    stall_Y = False

    # Is GRBL locked due to an alarm? 
    grbl_waiting_for_reset = False

    serial_blocks_available = GRBL_BLOCK_SIZE
    serial_chars_available = RX_BUFFER_SIZE
    print_buffer_status = True

    expecting_probe_result = False
    
    # VERSIONS
    fw_version = ''
    hw_version = ''

    # TEMPERATURES
    motor_driver_temp = None
    pcb_temp = None
    transistor_heatsink_temp = None

    # VOLTAGES
    microcontroller_mV = None
    LED_mV = None
    PSU_mV = None
    spindle_speed_monitor_mV = None

    # STALL GUARD
    sg_z_motor_axis = None
    sg_x_motor_axis = None
    sg_y_axis = None
    sg_y1_motor = None
    sg_y2_motor = None
    sg_x1_motor = None
    sg_x2_motor = None

    # STALL GUARD WARNING
    last_stall_tmc_index = None
    last_stall_motor_step_size = None
    last_stall_load = None
    last_stall_threshold = None
    last_stall_travel_distance = None
    last_stall_temperature = None
    last_stall_x_coord = None
    last_stall_y_coord = None
    last_stall_z_coord = None
    last_stall_status = None

    # FOR CALIBRATION TUNING
    record_sg_values_flag = False

    # SPINDLE STATISTICS
    spindle_serial_number = None
    spindle_production_year = None
    spindle_production_week = None
    spindle_firmware_version = None
    spindle_total_run_time_seconds = None
    spindle_brush_run_time_seconds = None
    spindle_mains_frequency_hertz = None

    # DETECT SOFT RESET
    grbl_initialisation_message = "^Grbl .+ \['\$' for help\]$"

    # IF NEED TO MEASURE RUNNING DATA
    measure_running_data = False
    running_data = []
    measurement_stage = 0

    # TMC REGISTERS ARE ALL HANDLED BY TMC_MOTOR CLASSES IN ROUTER MACHINE

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

            # If there is no Pn part in the status, set all limits to defaults.
            # (except power loss 'r' pin, which is a special condition)
            if not "|Pn:" in message:
                self.limit_x = False
                self.limit_X = False
                self.limit_y = False
                self.limit_Y = False
                self.limit_z = False
                self.probe = False
                self.dust_shoe_cover = False
                self.spare_door = False
                self.limit_Y_axis = False
                self.stall_X = False
                self.stall_Z = False
                self.stall_Y = False

            # If "Ld:x,x,x,x" is in the status, the spindle is communicating
            # If spindle is not sending data, reset the "inrush" counter, which discards any weird loads from the spindle starting
            if not re.search(self.digital_load_pattern, message):
                self.inrush_counter = 0

            elif self.inrush_counter <= 5:
                self.inrush_counter += 1

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

                # Get line number first so that all other data is in relation to this
                elif part.startswith('Ln:'):
                    value = part[3:]

                    try: 
                        int(value)

                    except: 
                        log("ERROR status parse: Line number invalid: " + message)
                        return

                    self.grbl_ln = int(value)

                # Get limit switch states: Pn:PxXyYZ
                elif part.startswith('Pn:'):
                    
                    pins_info = part.split(':')[1]
                    
                    self.limit_x = 'x' in pins_info
                    self.limit_X = 'X' in pins_info
                    self.limit_z = 'Z' in pins_info

                    if 'P' in pins_info: self.probe = True
                    else: self.probe = False

                    if 'g' in pins_info: self.spare_door = True
                    else: self.spare_door = False
                    
                    if 'G' in pins_info: self.dust_shoe_cover = True
                    else: self.dust_shoe_cover = False

                    if 'Y' or 'y' in pins_info:

                        # Depending on the firmware version (and the alarm type), 
                        # Y pin means either Y max limit OR Y stall
                        # and little y could be y home OR y limit
                        if self.fw_version and int(self.fw_version.split('.')[0]) < 2:

                            self.limit_y = 'y' in pins_info
                            self.limit_Y = 'Y' in pins_info

                        else:

                            self.limit_Y_axis = 'y' in pins_info
                            self.stall_Y = 'Y' in pins_info

                    else:
                        self.limit_y = False
                        self.limit_Y = False
                        self.limit_Y_axis = False
                        self.stall_Y = False

                    self.stall_X = 'S' in pins_info
                    self.stall_Z = 'z' in pins_info

                    if self.stall_X or self.stall_Y or self.stall_Z:
                        self.alarm.sg_alarm = True

                    if 'r' in pins_info and not self.power_loss_detected and sys.platform not in ['win32', 'darwin']:
                            # trigger power loss procedure!!
                            self.m._grbl_door()
                            self.sm.get_screen('door').db.send_event(2, 'Power loss', 'Connection loss: Check power and WiFi', 0)
                            self.m.set_pause(True)
                            log("Power loss or DC power supply")
                            self.power_loss_detected = True
                            Clock.schedule_once(lambda dt: self.m.resume_from_a_soft_door(), 1)
                
                elif part.startswith("Door") and self.m.is_machine_paused == False:
                    if part.startswith("Door:3"):
                        pass
                    else:
                        self.m.set_pause(True) # sets flag is_machine_paused so this stub only gets called once
                        if self.sm.current != 'door':
                            log("Hard " + self.m_state)
                            self.sm.get_screen('door').return_to_screen = self.sm.current 
                            self.sm.current = 'door'

                elif part.startswith('Ld:'):

                    spindle_feedback = part.split(':')[1]

                    if ',' in spindle_feedback:

                        digital_spindle_feedback = spindle_feedback.split(',')

                        try: 
                            int(digital_spindle_feedback[0])
                            int(digital_spindle_feedback[1])
                            int(digital_spindle_feedback[2])
                            int(digital_spindle_feedback[3])

                        except:
                            log("ERROR status parse: Digital spindle feedback invalid: " + message)
                            return

                        self.digital_spindle_ld_qdA = int(digital_spindle_feedback[0])
                        self.digital_spindle_temperature = int(digital_spindle_feedback[1])
                        self.digital_spindle_kill_time = int(digital_spindle_feedback[2])
                        self.digital_spindle_mains_voltage = int(digital_spindle_feedback[3])

                        # Check overload state
                        if self.digital_spindle_kill_time >= 160 : overload_mV_equivalent_state = 0
                        elif self.digital_spindle_kill_time >= 80 : overload_mV_equivalent_state = 20
                        elif self.digital_spindle_kill_time >= 40 : overload_mV_equivalent_state = 40
                        elif self.digital_spindle_kill_time >= 20 : overload_mV_equivalent_state = 60
                        elif self.digital_spindle_kill_time >= 10 : overload_mV_equivalent_state = 80
                        elif self.digital_spindle_kill_time < 10 : overload_mV_equivalent_state = 100
                        else: log("Killtime value not recognised")

                    else: 

                        try:
                            int(spindle_feedback)

                        except:
                            log("ERROR status parse: Analogue spindle feedback invalid: " + message)
                            return

                        self.spindle_load_voltage = int(spindle_feedback)

                        # gather spindle overload analogue voltage, and evaluate to general state

                        if self.spindle_load_voltage < 400 : overload_mV_equivalent_state = 0
                        elif self.spindle_load_voltage < 1000 : overload_mV_equivalent_state = 20
                        elif self.spindle_load_voltage < 1500 : overload_mV_equivalent_state = 40
                        elif self.spindle_load_voltage < 2000 : overload_mV_equivalent_state = 60
                        elif self.spindle_load_voltage < 2500 : overload_mV_equivalent_state = 80
                        elif self.spindle_load_voltage >= 2500 : overload_mV_equivalent_state = 100
                        else: log("Overload value not recognised")

                    # update stuff if there's a change
                    if overload_mV_equivalent_state != self.overload_state:  
                        self.overload_state = overload_mV_equivalent_state
                        log("Overload state change: " + str(self.overload_state))
                        log("Load voltage: " + str(self.spindle_load_voltage))
                    
                        try:
                            self.sm.get_screen('go').update_overload_label(self.overload_state)

                            # Only report as a peak if state stays elevated for longer than 1 second
                            if 20 <= self.overload_state < 100 and self.is_ready_to_assess_spindle_for_shutdown:
                                self.prev_overload_state = self.overload_state
                                Clock.schedule_once(self.check_for_sustained_peak, 1)

                        except:
                            log('Unable to update overload state on go screen')
                    
                    # if it's max load, activate a timer to check back in a second. The "checking back" is about ensuring the signal wasn't a noise event.
                    if self.overload_state == 100 and self.is_ready_to_assess_spindle_for_shutdown:
                        self.is_ready_to_assess_spindle_for_shutdown = False  # flag prevents further shutdowns until this one has been cleared
                        Clock.schedule_once(self.check_for_sustained_max_overload, 0.5)

                elif part.startswith('FS:'):
                    feed_speed = part[3:].split(',')
                    self.feed_rate = feed_speed[0]
                    self.spindle_speed = feed_speed[1]

                elif part.startswith('Ov:'):
                    values = part[3:].split(',')

                    try:
                        int(values[0])
                        int(values[1])
                        int(values[2])

                    except:
                        log("ERROR status parse: Ov values invalid: " + message)
                        return

                    self.feed_override_percentage = int(values[0])
                    self.speed_override_percentage = int(values[2])

                # TEMPERATURES
                elif part.startswith('TC:'):
                    temps = part[3:].split(',')

                    try: 
                        float(temps[0])
                        float(temps[1])
                    except:
                        log("ERROR status parse: Temperature invalid: " + message)
                        return

                    self.motor_driver_temp = float(temps[0])
                    self.pcb_temp = float(temps[1])

                    try:
                        float(temps[2])
                        self.transistor_heatsink_temp = float(temps[2])

                    except IndexError:
                        pass

                    except:
                        log("ERROR status parse: Temperature invalid: " + message)
                        return

                # VOLTAGES
                elif part.startswith('V:'):
                    voltages = part[2:].split(',')
                    try: 
                        float(voltages[0])
                        float(voltages[1])
                        float(voltages[2])
                        float(voltages[3])

                    except:
                        log("ERROR status parse: Voltage invalid: " + message)
                        return

                    self.microcontroller_mV = float(voltages[0])
                    self.LED_mV = float(voltages[1])
                    self.PSU_mV = float(voltages[2])
                    self.spindle_speed_monitor_mV = float(voltages[3])


                # SG VALUES
                elif part.startswith('SG:'):
                    sg_values = part[3:].split(',')

                    try:
                        int(sg_values[0])
                        int(sg_values[1])
                        int(sg_values[2])
                        int(sg_values[3])
                        int(sg_values[4])

                    except:
                        log("ERROR status parse: SG values invalid: " + message)
                        return

                    self.sg_z_motor_axis = int(sg_values[0])
                    self.sg_x_motor_axis = int(sg_values[1])
                    self.sg_y_axis = int(sg_values[2])
                    self.sg_y1_motor = int(sg_values[3])
                    self.sg_y2_motor = int(sg_values[4])

                    try:
                        int(sg_values[5])
                        int(sg_values[6])

                    except IndexError:
                        pass

                    except:
                        log("ERROR status parse: SG values invalid: " + message)
                        return

                    else:
                        self.sg_x1_motor = int(sg_values[5])
                        self.sg_x2_motor = int(sg_values[6]) 

                    if self.record_sg_values_flag:

                        self.m.temp_sg_array.append([
                                                    self.sg_z_motor_axis,
                                                    self.sg_x_motor_axis,
                                                    self.sg_y_axis,
                                                    self.sg_y1_motor,
                                                    self.sg_y2_motor,
                                                    self.sg_x1_motor,
                                                    self.sg_x2_motor
                                                ])

                    if self.FINAL_TEST:
                        if self.sm.has_screen('calibration_testing'):
                            self.sm.get_screen('calibration_testing').measure()

                        if self.sm.has_screen('overnight_testing'):
                            self.sm.get_screen('overnight_testing').measure()

                        if self.sm.has_screen('current_adjustment'):
                            self.sm.get_screen('current_adjustment').measure()

                # SG ALARM
                elif part.startswith('SGALARM:'):

                    sg_alarm_parts = part[8:].split(',')

                    try:
                        int(sg_alarm_parts[0])
                        int(sg_alarm_parts[1])
                        int(sg_alarm_parts[2])
                        int(sg_alarm_parts[3])
                        int(sg_alarm_parts[4])
                        float(sg_alarm_parts[5])
                        float(sg_alarm_parts[6])
                        float(sg_alarm_parts[7])

                    except:
                        log("ERROR status parse: SGALARM pins_info invalid: " + message)
                        return

                    self.last_stall_tmc_index = int(sg_alarm_parts[0])
                    self.last_stall_motor_step_size = int(sg_alarm_parts[1])
                    self.last_stall_load = int(sg_alarm_parts[2])
                    self.last_stall_threshold = int(sg_alarm_parts[3])
                    self.last_stall_travel_distance = int(sg_alarm_parts[4])
                    self.last_stall_temperature = int(sg_alarm_parts[5])
                    self.last_stall_x_coord = float(sg_alarm_parts[6])
                    self.last_stall_y_coord = float(sg_alarm_parts[7])
                    self.last_stall_z_coord = float(sg_alarm_parts[8])
                    self.last_stall_status = message

                elif part.startswith('Sp:'):

                    spindle_statistics = part[3:].split(',')

                    try: 
                        int(spindle_statistics[0])
                        int(spindle_statistics[1])
                        int(spindle_statistics[2])
                        int(spindle_statistics[3])
                        int(spindle_statistics[4])
                        int(spindle_statistics[5])
                        int(spindle_statistics[6])

                    except:
                        log("ERROR status parse: Sp values invalid: " + message)
                        return

                    self.spindle_serial_number = int(spindle_statistics[0])
                    self.spindle_production_year = int(spindle_statistics[1])
                    self.spindle_production_week = int(spindle_statistics[2])
                    self.spindle_firmware_version = int(spindle_statistics[3])
                    self.spindle_total_run_time_seconds = int(spindle_statistics[4])
                    self.spindle_brush_run_time_seconds = int(spindle_statistics[5])
                    self.spindle_mains_frequency_hertz = int(spindle_statistics[6])

                elif part.startswith('TREG:'):

                    tmc_registers = part[5:].split(',')

                    try: 
                        int(tmc_registers[0])
                        int(tmc_registers[1])
                        int(tmc_registers[2])
                        int(tmc_registers[3])
                        int(tmc_registers[4])
                        int(tmc_registers[5])
                        int(tmc_registers[6])
                        int(tmc_registers[7])
                        int(tmc_registers[8])
                        int(tmc_registers[9])
                        int(tmc_registers[10])

                    except:
                        log("ERROR status parse: TMC registers invalid: " + message)
                        return

                    self.m.TMC_motor[int(tmc_registers[0])].shadowRegisters[0] = int(tmc_registers[1])
                    self.m.TMC_motor[int(tmc_registers[0])].shadowRegisters[1] = int(tmc_registers[2])
                    self.m.TMC_motor[int(tmc_registers[0])].shadowRegisters[2] = int(tmc_registers[3])
                    self.m.TMC_motor[int(tmc_registers[0])].shadowRegisters[3] = int(tmc_registers[4])
                    self.m.TMC_motor[int(tmc_registers[0])].shadowRegisters[4] = int(tmc_registers[5])
                    self.m.TMC_motor[int(tmc_registers[0])].ActiveCurrentScale = int(tmc_registers[6])
                    self.m.TMC_motor[int(tmc_registers[0])].standStillCurrentScale = int(tmc_registers[7])
                    self.m.TMC_motor[int(tmc_registers[0])].stallGuardAlarmThreshold = int(tmc_registers[8])
                    self.m.TMC_motor[int(tmc_registers[0])].max_step_period_us_SG = int(tmc_registers[9])
                    self.m.TMC_motor[int(tmc_registers[0])].temperatureCoefficient = int(tmc_registers[10])
                    self.m.TMC_motor[int(tmc_registers[0])].got_registers = True

                    try:
                        self.m.print_tmc_registers(int(tmc_registers[0]))

                    except:
                        log("Could not print TMC registers")

                elif part.startswith('TCAL:M'):

                    [motor_index, all_cal_data] = part[6:].split(':')
                    all_cal_data_list = all_cal_data.strip(',').split(',')

                    try: 
                        map(int, all_cal_data_list)

                    except: 
                        log("ERROR status parse: TCAL registers invalid: " + message)
                        return

                    self.m.TMC_motor[int(motor_index)].calibration_dataset_SG_values = [int(i) for i in all_cal_data_list[0:128]]
                    self.m.TMC_motor[int(motor_index)].calibrated_at_current_setting = int(all_cal_data_list[128])
                    self.m.TMC_motor[int(motor_index)].calibrated_at_sgt_setting = int(all_cal_data_list[129])
                    self.m.TMC_motor[int(motor_index)].calibrated_at_toff_setting = int(all_cal_data_list[130])
                    self.m.TMC_motor[int(motor_index)].calibrated_at_temperature = int(all_cal_data_list[131])
                    self.m.TMC_motor[int(motor_index)].got_calibration_coefficients = True

                    try: 

                        calibration_report_string = (
                        "-------------------------------------" + "\n" + \
                        "MOTOR ID: " + str(int(motor_index)) + "\n" + \
                        "Calibration coefficients: " + str(all_cal_data_list[0:128]) + "\n" + \
                        "Current setting: " + str(self.m.TMC_motor[int(motor_index)].calibrated_at_current_setting) + "\n" + \
                        "SGT setting: " + str(self.m.TMC_motor[int(motor_index)].calibrated_at_sgt_setting) + "\n" + \
                        "TOFF setting: " + str(self.m.TMC_motor[int(motor_index)].calibrated_at_toff_setting) + "\n" + \
                        "Calibration temperature: " + str(self.m.TMC_motor[int(motor_index)].calibrated_at_temperature) + "\n" + \
                        "-------------------------------------"
                        )

                        map(log, calibration_report_string.split("\n"))

                    except:
                        log("Could not print calibration output")


            if self.VERBOSE_STATUS: print (self.m_state, self.m_x, self.m_y, self.m_z,
                                           self.serial_blocks_available, self.serial_chars_available)

            if self.measure_running_data:

                try:

                    self.running_data.append([
                        int(self.measurement_stage),
                        float(self.m_x),
                        float(self.m_y),
                        float(self.m_z),
                        int(self.sg_x_motor_axis),
                        int(self.sg_y_axis),
                        int(self.sg_y1_motor),
                        int(self.sg_y2_motor),
                        int(self.sg_z_motor_axis),
                        int(self.motor_driver_temp),
                        int(self.pcb_temp),
                        int(self.transistor_heatsink_temp),
                        datetime.now(),
                        int(self.feed_rate),
                        self.sg_x1_motor,
                        self.sg_x2_motor,
                    ])

                except: 
                    pass
 
        elif message.startswith('ALARM:'):
            self.grbl_waiting_for_reset = True
            log('ALARM from GRBL: ' + message)
            self.alarm.alert_user(message)

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
            elif setting == '$51': self.setting_51 = value; # Enable digital feedback spindle, boolean
            elif setting == '$53': self.setting_53 = value; # Enable stall guard alarm operation, boolean
            elif setting == '$54': self.setting_54 = value; # Motor load (SG) values reporting type, boolean
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
                fw_hw_versions = stripped_message.split(';')
                try: 
                    self.fw_version = (fw_hw_versions[1]).split(':')[1]
                    log('FW version: ' + str(self.fw_version))
                except: 
                    log("Could not retrieve FW version")

                try: 
                    self.hw_version = (fw_hw_versions[2]).split(':')[1]
                    log('HW version: ' + str(self.hw_version))
                except: 
                    log("Could not retrieve HW version")

        elif re.match(self.grbl_initialisation_message, message):
            # Let sw know that grbl is unlocked now that statuses are being received
            self.grbl_waiting_for_reset = False


    def check_for_sustained_max_overload(self, dt):

        try:

            if self.overload_state == 100 and sys.platform != 'win32':  # if still at max overload, begin the spindle pause procedure
                
                self.m.stop_for_a_stream_pause("spindle_overload")
                self.sm.get_screen('spindle_shutdown').reason_for_pause = "spindle_overload"
                self.sm.get_screen('spindle_shutdown').return_screen = str(self.sm.current)
                self.sm.current = 'spindle_shutdown'

                try:
                    self.sm.get_screen('go').update_overload_peak(self.overload_state)

                except:
                    log('Unable to update overload peak on go screen')

            else: # must have just been a noisy blip
                
                self.is_ready_to_assess_spindle_for_shutdown = True  # allow spindle overload assessment to resume

        except:

            log("Could not display spindle overload - are you on diagnostics mode?")

        
    def check_for_sustained_peak(self, dt):

        if self.overload_state >= self.prev_overload_state and self.overload_state != 100:

            try:
                self.sm.get_screen('go').update_overload_peak(self.prev_overload_state)

            except:
                log('Unable to update overload peak on go screen')



## SEQUENTIAL STREAMING

    # This stream_file method waits for an 'ok' before sending the next setting
    # It does not stuff the grbl buffer
    # It is for:
    ## Anything sending EEPROM settings (which require special attention, due to writing of values)
    # WARNING: this function is not blocking, as such, the is_sequential_streaming flag should be checked before using.
    
    is_sequential_streaming = False
    _sequential_stream_buffer = []
    _reset_grbl_after_stream = False
    _ready_to_send_first_sequential_stream = False
    _process_oks_from_sequential_streaming = False
    _dwell_time = 0.5 # time for grbl to wait after sending dollar settings commands
    _dwell_command = "G4 P" + str(_dwell_time)
    _micro_dwell_command = "G4 P" + str(0.01)

    def start_sequential_stream(self, list_to_stream, reset_grbl_after_stream=False, end_dwell=False):
        self.is_sequential_streaming = True
        log("Start_sequential_stream")
        if reset_grbl_after_stream: list_to_stream.append(self._dwell_command)
        elif end_dwell: list_to_stream.append(self._micro_dwell_command)
        self._sequential_stream_buffer = list_to_stream
        self._reset_grbl_after_stream = reset_grbl_after_stream
        self._ready_to_send_first_sequential_stream = True
                
    def _send_next_sequential_stream(self):

        if self._ready_to_send_first_sequential_stream:
            self._ready_to_send_first_sequential_stream = False
            self._process_oks_from_sequential_streaming = True

        if self._sequential_stream_buffer:
            try: 
                self.write_direct(self._sequential_stream_buffer[0])
                if self._after_grbl_settings_insert_dwell(): self._sequential_stream_buffer[0] = self._dwell_command
                else: del self._sequential_stream_buffer[0]

            except IndexError: 
                log("Sequential streaming buffer empty")
                return

        else:
            self._process_oks_from_sequential_streaming = False
            log("Sequential stream ended")
            if self._reset_grbl_after_stream:
                self._reset_grbl_after_stream = False
                self.m._grbl_soft_reset()
                log("GRBL Reset after sequential stream ended")
            self.is_sequential_streaming = False

    def _after_grbl_settings_insert_dwell(self):

        if self._sequential_stream_buffer[0].startswith('$'):
            try: 
                if not self._sequential_stream_buffer[1].startswith('$') \
                and not self._sequential_stream_buffer[1] == self._dwell_command:
                    return True
            except: 
                return True

        return False


    def cancel_sequential_stream(self, reset_grbl_after_cancel = False):
        
        self._sequential_stream_buffer = []
        self._process_oks_from_sequential_streaming = False
        self._ready_to_send_first_sequential_stream = False
        if reset_grbl_after_cancel or self._reset_grbl_after_stream:
            self._reset_grbl_after_stream = False
            self.m._grbl_soft_reset()
            print "GRBL Reset after sequential stream cancelled"
        self.is_sequential_streaming = False

    def is_buffer_clear(self):

        if int(self.serial_chars_available) == self.RX_BUFFER_SIZE \
        and int(self.serial_blocks_available) == self.GRBL_BLOCK_SIZE:
            return True

        return False


## WRITE-----------------------------------------------------------------------------
    def write_direct(self, serialCommand, show_in_sys = True, show_in_console = True, altDisplayText = None, realtime = False, protocol = False):


        # sometimes shapecutter likes to generate empty unicode characters, which serial cannae handle. 
        if not serialCommand and not isinstance(serialCommand, str):
            serialCommand = str(serialCommand)

        # Issue to logging outputs first (so the command is logged before any errors/alarms get reported back)
        try:

            if not serialCommand.startswith('?') and not protocol:
                log('> ' + serialCommand)

            if altDisplayText != None: log('> ' + str(altDisplayText))

            # Print to console in the UI
            if show_in_console == True and altDisplayText == None:
                self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('snd', serialCommand)

            if altDisplayText != None:
                self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('snd', altDisplayText)

        except:
            log("FAILED to display on CONSOLE: " + str(serialCommand) + " (Alt text: " + str(altDisplayText) + ")")

        # Finally issue the command        
        if self.s:
            try:

                if realtime == True:
                    # OMITS end of line command (which returns an 'ok' from grbl - used in counting/streaming algorithms)
                    self.s.write(serialCommand)

                elif realtime == False and protocol == False:
                    # INLCUDES end of line command (which returns an 'ok' from grbl - used in algorithms)
                    self.s.write(serialCommand + '\n')

                elif protocol == True:
                        self.s.write(serialCommand)
                        self.last_protocol_send_time = time.time()

            except:

                try:

                    if not protocol:
                        log("FAILED to write to SERIAL: " + str(serialCommand) + " (Alt text: " + str(altDisplayText) + ")")
                        self.get_serial_screen('Could not write last command to serial buffer.')

                    else:
                        log("FAILED to write to SERIAL: " + hex(serialCommand) + " (Alt text: " + str(altDisplayText) + ")")
                        self.get_serial_screen('Could not write last command to serial buffer.')

                except:
                    log("FAILED to write to SERIAL: " + "unprintable command!" + " (Alt text: " + str(altDisplayText) + ")")
                    self.get_serial_screen('Could not write last command to serial buffer.')


        else:

            try:
                if not protocol:
                    log("No serial! Command lost!: " + str(serialCommand) + " (Alt text: " + str(altDisplayText) + ")")
                    self.get_serial_screen('Could not write last command to serial buffer.')

                else:
                    log("No serial! Command lost!: " + hex(serialCommand) + " (Alt text: " + str(altDisplayText) + ")")
                    self.get_serial_screen('Could not write last command to serial buffer.')
            except:

                log("No serial! Command lost!: " + "unprintable command!" + " (Alt text: " + str(altDisplayText) + ")")
                self.get_serial_screen('Could not write last command to serial buffer.')

    def write_command(self, serialCommand, **kwargs):
        
        self.write_command_buffer.append([serialCommand, kwargs])        

    # Many realtime commands are non-printables, and cause the gcode console to crash. 
    # GCode console with therefore print 'altDisplayText' arg instead
    def write_realtime(self, serialCommand, altDisplayText = None):
        
        self.write_realtime_buffer.append([serialCommand, altDisplayText])

    def write_protocol(self, serialCommand, altDisplayText):
        
        self.write_protocol_buffer.append([serialCommand, altDisplayText])
        return serialCommand
