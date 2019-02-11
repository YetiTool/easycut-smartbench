'''
Created on 31 Jan 2018
@author: Ed
Module to manage all serial comms between pi (EasyCut s/w) and realtime arduino chip (GRBL f/w)
'''

from kivy.config import Config

# Set the Kivy "Clock" to tick at its fastest.
# Clock usually used to establish consistent framerate for animations, but we need it to tick much faster (e.g. than 25fps) for serial refreshing
Config.set('graphics', 'maxfps', '30')
Config.write()

import serial, sys, time, string, threading
from datetime import datetime
from os import listdir
from kivy.clock import Clock

from asmcnc.skavaUI import popup_alarm_homing, popup_alarm_general, popup_error,\
    popup_job_done
import re
from functools import partial


BAUD_RATE = 115200
ENABLE_STATUS_REPORTS = True
GRBL_SCANNER_MIN_DELAY = 0.01 # Delay between checking for response from grbl. Needs to be hi-freq for quick streaming, e.g. 0.01 = 100Hz

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

class SerialConnection(object):

    STATUS_INTERVAL = 0.1 # How often to poll general status to update UI (0.04 = 25Hz = smooth animation)

    s = None    # Serial comms object
    sm = None   # Screen manager object

    def __init__(self, machine, screen_manager):

        self.sm = screen_manager

        # This is the object which calls the serial connection so can be referenced to do machine moves from Alarm popup
        # This seems to work fine, but feel wrong - should I be using super()? Maybe? But super() creates module errors...
        self.m = machine

    def __del__(self):
        print 'Destructor'

    def establish_connection(self, win_port):

        # Parameter 'win'port' only used for windows dev e.g. "COM4"
        if sys.platform == "win32":
            try:
                self.s = serial.Serial(win_port, BAUD_RATE)
                return True
            except:
                return False
        else:
            try:
                filesForDevice = listdir('/dev/') # put all device files into list[]
                for line in filesForDevice: # run through all files

                    # EITHER: USB Comms hardware
                     # if (line[:6] == 'ttyUSB' or line[:6] == 'ttyACM'): # look for prefix of known success (covers both Mega and Uno)

                    # OR: UART Comms hardware
                    if (line[:4] == 'ttyS' or line[:6] == 'ttyACM'): # look for... 
                    
                        devicePort = line # take whole line (includes suffix address e.g. ttyACM0
                        self.s = serial.Serial('/dev/' + str(devicePort), BAUD_RATE) # assign
                        return True
            except:
                return False


    # is serial port connected?
    def is_connected(self):

        if self.s: return True
        else: return False


    def initialise_grbl(self):

        if self.is_connected():
            self.write_command("\r\n\r\n", show_in_sys=False, show_in_console=False)    # Wakes grbl
            Clock.schedule_once(self.start_services, 3) # Delay for grbl to initialize


    def start_services(self, dt):

        self.s.flushInput()  # Flush startup text in serial input
        # Clock.schedule_once(self.grbl_scanner, 0)   # Listen for messages from grbl
        t = threading.Thread(target=self.grbl_scanner)
        t.daemon = True
        t.start()

        # Enter any initial settings into this list
        # We are preparing for a sequential stream since some of these setting commands store data to the EEPROM
        # When Grbl stores data to EEPROM, the AVR requires all interrupts to be disabled during this write process, including the serial RX ISR.
        # This means that if a g-code or Grbl $ command writes to EEPROM, the data sent during the write may be lost.
        # Sequential streaming handles this
        grbl_settings = [
#                     '$0=10',    #Step pulse, microseconds
#                     '$1=25',    #Step idle delay, milliseconds
#                     '$2=0',           #Step port invert, mask
#                     '$3=1',           #Direction port invert, mask
#                     '$4=0',           #Step enable invert, boolean
#                     '$5=1',           #Limit pins invert, boolean
#                     '$6=0',           #Probe pin invert, boolean
#                     '$10=3',          #Status report, mask <----------------------
#                     '$11=0.010',      #Junction deviation, mm
#                     '$12=0.002',      #Arc tolerance, mm
#                     '$13=0',          #Report inches, boolean
#                     '$20=0',          #Soft limits, boolean <-------------------
#                     '$21=0',          #Hard limits, boolean <------------------
#                     '$22=0',          #Homing cycle, boolean <------------------------
#                     '$23=3',          #Homing dir invert, mask
#                     '$24=500.0',     #Homing feed, mm/min
#                     '$25=10000.0',    #Homing seek, mm/min
#                     '$26=250',        #Homing debounce, milliseconds
#                     '$27=2.000',      #Homing pull-off, mm
#                     '$30=1000.0',      #Max spindle speed, RPM
#                     '$31=0.0',         #Min spindle speed, RPM
#                     '$32=0',           #Laser mode, boolean
#                     '$100=62.954',   #X steps/mm
#                     '$101=68.075',   #Y steps/mm
#                     '$102=1066.667',   #Z steps/mm
#                     '$110=10000.0',   #X Max rate, mm/min
#                     '$111=10000.0',   #Y Max rate, mm/min
#                     '$112=2000.0',   #Z Max rate, mm/min
#                     '$120=500.0',    #X Acceleration, mm/sec^2
#                     '$121=500.0',    #Y Acceleration, mm/sec^2
#                     '$122=100.0',    #Z Acceleration, mm/sec^2
#                     '$130=1220.0',   #X Max travel, mm TODO: Link to a settings object
#                     '$131=2440.0',   #Y Max travel, mm
#                     '$132=150.0',   #Z Max travel, mm
                    '$$', # Echo grbl settings, which will be read by sw, and internal parameters sync'd
                    '$#' # Echo grbl parameter info, which will be read by sw, and internal parameters sync'd
                    ]

        self.start_sequential_stream(grbl_settings, reset_grbl_after_stream=True)   # Send any grbl specific parameters

        if ENABLE_STATUS_REPORTS:
            Clock.schedule_interval(self.poll_status, self.STATUS_INTERVAL)      # Poll for status


    def poll_status(self, dt):

        self.write_realtime('?', show_in_sys=False, show_in_console=False)



# SCANNER: listens for responses from Grbl

    # "Response" is a message from GRBL saying how a line of gcode went (either 'ok', or 'error') when it was loaded from the serial buffer into the line buffer
    # When streaming, monitoring the response from GRBL is essential for EasyCut to know when to send the next line
    # Full docs: https://github.com/gnea/grbl/wiki/Grbl-v1.1-Interface

    # "Push" is for messages from GRBL to provide more general feedback on what Grbl is doing (e.g. status)

    VERBOSE_ALL_PUSH_MESSAGES = False
    VERBOSE_ALL_RESPONSE = False
    VERBOSE_STATUS = False


    def grbl_scanner(self):
        # If there's a message received, deal with it depending on type
        # if self.s.inWaiting():
        while True:
            try:
                rec_temp = self.s.readline().strip() #Block the executing thread indefinitely until a line arrives
            except Exception as e:
                log('serial.readline exception:\n' + str(e))
            #time.sleep(1)
            #print 'RX line length: ', len(rec_temp)
            if len(rec_temp):
                #print 'RX line: ', rec_temp
                #HACK send every line received to console
                #if not rec_temp.startswith('<Alarm|MPos:') and not rec_temp.startswith('<Idle|MPos:'):
                if True:
                    log('< ' + rec_temp)

                # Update the gcode monitor (may not be initialised) and console
                try:
                    self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('rec', rec_temp)
                except:
                    pass
                if self.VERBOSE_ALL_RESPONSE: print rec_temp

                try:
                    # If RESPONSE message (used in streaming, counting processed gcode lines)
                    if rec_temp.startswith(('ok', 'error')):
                        self.process_grbl_response(rec_temp)
                    # If PUSH message
                    else:
                        self.process_grbl_push(rec_temp)
                except Exception as e:
                    log('Process response exception:\n' + str(e))
                    raise # HACK allow error to cause serial comms thread to exit

                # if we're streaming, check to see if the buffer can be filled
                if self.is_job_streaming:
                    if self.is_stream_lines_remaining:
                        self.stuff_buffer()
                    else: self.end_stream()

        # Loop this method
        #Clock.schedule_once(self.grbl_scanner, GRBL_SCANNER_MIN_DELAY)



# STREAMING: sending gcode, using character counting protocol described here:
# https://github.com/gnea/grbl/wiki/Grbl-v1.1-Interface


    # streaming variables
    GRBL_BLOCK_SIZE = 35    # max number of gcode lines which GRBL can put in its 'BLOCK' or look ahead buffer
    RX_BUFFER_SIZE = 256    # serial buffer which gets filled by EasyCut. GRBL grabs from this when there is block space

    is_job_streaming = False
    is_stream_lines_remaining = False

    g_count = 0 # gcodes processed (ok/error'd) by grbl (gcodes may not get processed immediately after being sent)
    l_count = 0 # lines sent to grbl
    c_line = [] # char count of blocks/lines in grbl's serial buffer

    stream_start_time = 0
    stream_end_time = 0
    buffer_monitor_file = None


    def stream_file(self, job_file_path):

        if self.sm.get_screen('home').developer_widget.buffer_log_mode == "down":
            self.buffer_monitor_file = open("buffer_log.txt", "w")

        # Move head out of the way before moving to the job datum in XY.
        self.m.zUp()

        # Delay to make sure that the grbl-response ('ok') from z-move has been received before beginning to counting for grbl responses.
        Clock.schedule_once(self._load_stream_file, 1)


    def _load_stream_file(self, dt):

        # for the buffer stuffing style streaming

        self.is_stream_lines_remaining = True
        self.s.flushInput()

        # Reset counters & flags
        self.l_count = 0
        self.g_count = 0
        self.c_line = []
        self.stream_start_time = time.time();

        # allow grbl_scanner() to start stuffing buffer
        self.is_job_streaming = True


    # attempt to fill GRBLS's serial buffer, if there's room
    def stuff_buffer(self):

        line_to_go = self.get_next_line(self.m.job_file_gcode)

        serial_space = self.RX_BUFFER_SIZE - sum(self.c_line)

        # if there's room in the serial buffer, send the line
        while len(line_to_go) + 1 <= serial_space:
            self.c_line.append(len(line_to_go) + 1) # Track number of characters in grbl serial read buffer
            self.l_count += 1 # lines sent to grbl
            self.write_command(line_to_go, show_in_sys=True, show_in_console=False) # Send g-code block to grbl

            line_to_go = self.get_next_line(self.m.job_file_gcode)
            if line_to_go == None:
                self.is_stream_lines_remaining = False
                break

            serial_space = self.RX_BUFFER_SIZE - sum(self.c_line)


    def get_next_line(self, job_file_gcode):

        line = None
        while True:
            if self.l_count >= len(job_file_gcode):
                break
            # Refine GCode
            l_block = re.sub('\s|\(.*?\)', '', job_file_gcode[self.l_count]).upper() # Strip comments/spaces/new line and capitalize
            # Drop undesirable lines
            if l_block.find('%') == -1 and l_block.find('M6') == -1:
                line = l_block
                break;
            # Throw current line away, loop again
            self.l_count += 1

        return line


    # if 'ok' or 'error' rec'd from GRBL
    def process_grbl_response(self, message):

        # This is a special condition, used only at startup to set EEPROM settings
        if self.is_sequential_streaming:
            self._send_next_sequential_stream()

        elif self.is_job_streaming:
            self.g_count += 1 # Iterate g-code counter
            del self.c_line[0] # Delete the block character count corresponding to the last 'ok'

        if message.startswith('error'):
            log('ERROR from GRBL: ' + message)
            popup_error.PopupError(self.m, self.sm, message)


    # After streaming is completed
    def end_stream(self):

        self.is_job_streaming = False
        self.is_stream_lines_remaining = False

        log("G-code streaming finished!")
        self.stream_end_time = time.time()
        time_taken_seconds = int(self.stream_end_time - self.stream_start_time)
        hours = int(time_taken_seconds / (60 * 60))
        seconds_remainder = time_taken_seconds % (60 * 60)
        minutes = int(seconds_remainder / 60)
        seconds = int(seconds_remainder % 60)
        #time_take_minutes = int(time_taken_seconds/60)
        log(" Time elapsed: " + str(time_taken_seconds) + " seconds")
        self.sm.get_screen('go').reset_go_screen_after_job_finished()
        #popup_job_done.PopupJobDone(self.m, self.sm, "The job has finished. It took " + str(time_take_minutes) + " minutes.")
        popup_job_done.PopupJobDone(self.m, self.sm, "The job has finished. It took " + str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s")
        if self.buffer_monitor_file != None:
            self.buffer_monitor_file.close()
            self.buffer_monitor_file = None


    def cancel_stream(self):
        self.is_job_streaming = False  # allow grbl_scanner() to start stuffing buffer
        self.is_stream_lines_remaining = False
        self.sm.get_screen('go').reset_go_screen_after_job_finished()
        if self.buffer_monitor_file != None:
            self.buffer_monitor_file.close()
            self.buffer_monitor_file = None

        log("G-code streaming cancelled!")

        # Flush
        self.s.flushInput()



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


    serial_blocks_available = GRBL_BLOCK_SIZE
    serial_chars_available = RX_BUFFER_SIZE
    print_buffer_status = True


    expecting_probe_result = False


    def process_grbl_push(self, message):

        if self.VERBOSE_ALL_PUSH_MESSAGES: print message

        # If it's a status message, e.g. <Idle|MPos:-1218.001,-2438.002,-2.000|Bf:35,255|FS:0,0>
        if message.startswith('<'):
            # 13:09:46.077 < <Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:pxXyYZ>
            # 13:09:46.178 < <Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:pxXyYZ|WCO:-166.126,-213.609,-21.822>
            # 13:09:46.277 < <Idle|MPos:0.000,0.000,0.000|Bf:35,255|FS:0,0|Pn:pxXyYZ|Ov:100,100,100>

#            self.validate_status_message(message)

            validMessage = True

# Error checking from Skippy, but DANGEROUS bc it gets rid of other (more user-useful) errors. 
#             commasCnt = message.count(",")
#             if (commasCnt != 4 and commasCnt != 6):
#                 validMessage = False
#                 log("ERROR status parse: comma count fail: " + message)
#                 return

            status_parts = message.translate(string.maketrans("", "", ), '<>').split('|') # fastest strip method

            if (status_parts[0] != "Idle" and
                status_parts[0] != "Run" and
                status_parts[0] != "Hold" and
                status_parts[0] != "Jog" and
                status_parts[0] != "Alarm" and
                status_parts[0] != "Door" and
                status_parts[0] != "Check" and
                status_parts[0] != "Home" and
                status_parts[0] != "Sleep"):
                validMessage = False
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
                        self.sm.get_screen('go').grbl_serial_char_capacity.text = "C: " + self.serial_chars_available
                        self.print_buffer_status = True # flag to print

                    if self.serial_blocks_available != buffer_info[0]:
                        self.serial_blocks_available = buffer_info[0]
                        self.sm.get_screen('go').grbl_serial_line_capacity.text = "L: " + self.serial_blocks_available
                        self.print_buffer_status = True # flag to print

                    # print if change flagged
                    if self.print_buffer_status == True:
                        self.print_buffer_status = False
                        if self.sm.get_screen('home').developer_widget.buffer_log_mode == "down":
                            print self.serial_blocks_available + " " + self.serial_chars_available
                            if self.buffer_monitor_file: self.buffer_monitor_file.write(self.serial_blocks_available + " " + self.serial_chars_available + "\n")

                else:
                    continue

            if self.VERBOSE_STATUS: print (self.m_state, self.m_x, self.m_y, self.m_z,
                                           self.serial_blocks_available, self.serial_chars_available)


        elif message.startswith('ALARM:'):
            log('ALARM from GRBL: ' + message)
            popup_alarm_general.PopupAlarm(self.m, self.sm, message)


        elif message.startswith('$'):
            setting_and_value = message.split("=")
            setting = setting_and_value[0]
            value = float(setting_and_value[1])

            # Detect setting and update value in software
            # '$$' is called to yield the report from grbl
            # It is called at init, at end of "start_sequential_stream" function - this forces sw to be in sync with grbl settings

            if setting == '$0': pass  # Step pulse, microseconds
            elif setting == '$1': pass  # Step idle delay, milliseconds
            elif setting == '$2': pass  # Step port invert, mask
            elif setting == '$3': pass  # Direction port invert, mask
            elif setting == '$4': pass  # Step enable invert, boolean
            elif setting == '$5': pass  # Limit pins invert, boolean
            elif setting == '$6': pass  # Probe pin invert, boolean
            elif setting == '$10': pass  # Status report, mask
            elif setting == '$11': pass  # Junction deviation, mm
            elif setting == '$12': pass  # Arc tolerance, mm
            elif setting == '$13': pass  # Report inches, boolean
            elif setting == '$20': pass  # Soft limits, boolean
            elif setting == '$21': pass  # Hard limits, boolean
            elif setting == '$22': pass  # Homing cycle, boolean
            elif setting == '$23': pass  # Homing dir invert, mask
            elif setting == '$24': pass  # Homing feed, mm/min
            elif setting == '$25': pass  # Homing seek, mm/min
            elif setting == '$26': pass  # Homing debounce, milliseconds
            elif setting == '$27': pass  # Homing pull-off, mm
            elif setting == '$30': pass  # Max spindle speed, RPM
            elif setting == '$31': pass  # Min spindle speed, RPM
            elif setting == '$32': pass  # Laser mode, boolean
            elif setting == '$100': pass  # X steps/mm
            elif setting == '$101': pass  # Y steps/mm
            elif setting == '$102': pass  # Z steps/mm
            elif setting == '$110': # X Max rate, mm/min
                self.sm.get_screen('home').common_move_widget.fast_x_speed = value
                self.sm.get_screen('home').common_move_widget.set_jog_speeds()
            elif setting == '$111': # Y Max rate, mm/min
                self.sm.get_screen('home').common_move_widget.fast_y_speed = value
                self.sm.get_screen('home').common_move_widget.set_jog_speeds()
            elif setting == '$112': # Z Max rate, mm/min
                self.sm.get_screen('home').common_move_widget.fast_z_speed = value
                self.sm.get_screen('home').common_move_widget.set_jog_speeds()
            elif setting == '$120': pass  # X Acceleration, mm/sec^2
            elif setting == '$121': pass  # Y Acceleration, mm/sec^2
            elif setting == '$122': pass  # Z Acceleration, mm/sec^2
            elif setting == '$130':
                self.m.grbl_x_max_travel = value  # X Max travel, mm
                self.m.set_jog_limits()
            elif setting == '$131':
                self.m.grbl_y_max_travel = value  # Y Max travel, mm
                self.m.set_jog_limits()
            elif setting == '$132':
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

            # Process a successful probing op [PRB:0.000,0.000,0.000:0]
            elif self.expecting_probe_result and stripped_message.startswith('PRB'):

                successful_probe = stripped_message.split(':')[2]
                if successful_probe:
                    self.m.probe_z_detection_event()
                    Clock.schedule_once(self.m.probe_z_post_operation, 0.3) # Delay to dodge EEPROM write blocking

                self.expecting_probe_result = False # clear flag



# WRITE

    def write_command(self, serialCommand, show_in_sys=True, show_in_console=True, altDisplayText=None):

        # INLCUDES end of line command (which returns an 'ok' from grbl - used in algorithms)

        # Issue to logging outputs first (so the command is logged before any errors/alarms get reported back)
        try:
            # Print to sys (external command interface e.g. console in Eclipse, or at the prompt on the Pi)
            #if show_in_sys and altDisplayText==None: print serialCommand
            log('> ' + serialCommand)
            if altDisplayText != None: print altDisplayText

            # Print to console in the UI
            if show_in_console  and altDisplayText == None:
                self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('snd', serialCommand)
            if altDisplayText != None:
                self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('snd', altDisplayText)

        except:
            print "FAILED to display on CONSOLE: " + serialCommand + " (Alt text: " + str(altDisplayText) + ")"

        # Finally issue the command
        if self.s:
            try:
                self.s.write(serialCommand + '\n')
            except:
                print "FAILED to write to SERIAL: " + serialCommand + " (Alt text: " + str(altDisplayText) + ")"



    def write_realtime(self, serialCommand, show_in_sys=True, show_in_console=True, altDisplayText=None):

        # OMITS end of line command (which returns an 'ok' from grbl - used in counting/streaming algorithms)

        # Issue to logging outputs first (so the command is logged before any errors/alarms get reported back)
        try:
            # Print to sys (external command interface e.g. console in Eclipse, or at the prompt on the Pi)
            #if show_in_sys and altDisplayText==None: print serialCommand
            if not serialCommand.startswith('?'):
                log('> ' + serialCommand)
            if altDisplayText != None: print altDisplayText

            # Print to console in the UI
            if show_in_console  and altDisplayText == None:
                self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('snd', serialCommand)
            if altDisplayText != None:
                self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('snd', altDisplayText)

        except:
            print "FAILED to display on CONSOLE: " + serialCommand + " (Alt text: " + str(altDisplayText) + ")"

        # Finally issue the command
        if self.s:
            try:
                self.s.write(serialCommand)
            except:
                print "FAILED to write to SERIAL: " + serialCommand + " (Alt text: " + str(altDisplayText) + ")"

    monitor_text_buffer = ""



# SEQUENTIAL STREAMING

    _sequential_stream_buffer = []
    _reset_grbl_after_stream = False

    def start_sequential_stream(self, list_to_stream, reset_grbl_after_stream=False):

        # This stream_file method waits for an 'ok' before sending the next setting
        # It does not stuff the grbl buffer
        # It is for:
          # EEPROM settings require special attention, due to writing of values
          # Matching Error/Alarm messages to exact commands (not possible during buffer stuffing)
        # WARNING: this function is not blocking, and as of yet there is no way to indicate it has finished

        log("start_sequential_stream")
        self._sequential_stream_buffer = list_to_stream
        self._reset_grbl_after_stream = reset_grbl_after_stream


        if self._sequential_stream_buffer:
            self.is_sequential_streaming = True
            self.write_command(self._sequential_stream_buffer[0])
            del self._sequential_stream_buffer[0]
        else:
            self.is_sequential_streaming = False
            if self._reset_grbl_after_stream:
                self.write_realtime("\x18", show_in_sys=True, show_in_console=False) # Soft-reset. This forces the need to home when the controller starts up

    def _send_next_sequential_stream(self):
        log("_send_next_sequential_stream")
        if self._sequential_stream_buffer:
            self.is_sequential_streaming = True
            self.write_command(self._sequential_stream_buffer[0])
            del self._sequential_stream_buffer[0]
        else:
            self.is_sequential_streaming = False
            if self._reset_grbl_after_stream:
                self.write_realtime("\x18", show_in_sys=True, show_in_console=False) # Soft-reset. This forces the need to home when the controller starts up




