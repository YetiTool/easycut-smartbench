import serial, sys, time, string, threading
from datetime import datetime
from os import listdir
from kivy.clock import Clock

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))


class EncoderConnection(object):

    STATUS_INTERVAL = 0.1 # How often to poll general status to update UI (0.04 = 25Hz = smooth animation)

    e = None    # Serial comms object
    sm = None   # Screen manager object

    grbl_out = ""
    FLUSH_FLAG = False
    
    write_command_buffer = []
    write_realtime_buffer = []
    
    monitor_text_buffer = ""


    def __init__(self, machine, screen_manager):

        self.sm = screen_manager

    def __del__(self):
        print 'Destructor'


    def establish_connection(self):

        try:
            filesForDevice = listdir('/dev/') # put all device files into list[]
            for line in filesForDevice: # run through all files

                # FLAG: This if statement is only relevant in linux environment. 
                # EITHER: USB Comms hardware
                # if (line[:6] == 'ttyUSB' or line[:6] == 'ttyACM'): # look for prefix of known success (covers both Mega and Uno)
                # OR: UART Comms hardware
                if line[:6] == 'ttyACM': # look for...   
                    # When platform is updated, this needs to be moved across to the AMA0 port :)
                    devicePort = line # take whole line (includes suffix address e.g. ttyACM0
                    self.e = serial.Serial('/dev/' + str(devicePort), BAUD_RATE, timeout = 6, writeTimeout = 20) # assign

                # elif (line[:6] == 'ttyAMA'): # in the case that in /boot/config.txt, dtoverlay=pi3-disable-bt
                
                #     devicePort = line # take whole line (includes suffix address e.g. ttyACM0
                #     self.s = serial.Serial('/dev/' + str(devicePort), BAUD_RATE, timeout = 6, writeTimeout = 20) # assign
                #     return True
                    
                elif (line[:12] == 'tty.usbmodem'): # look for...   
                    devicePort = line # take whole line (includes suffix address e.g. ttyACM0
                    self.e = serial.Serial('/dev/' + str(devicePort), BAUD_RATE, timeout = 6, writeTimeout = 20) # assign

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
        self.e.flushInput()  # Flush startup text in serial input
        self.next_poll_time = time.time()
        t = threading.Thread(target=self.encoder_scanner)
        t.daemon = True
        t.start()
        
        # # Clear any hard switch presses that may have happened during boot
        # self.m.bootup_sequence()


    def grbl_scanner(self):
        
        log('Running grbl_scanner thread')

        while True:

                         
            if self.FLUSH_FLAG == True:
                self.e.flushInput()
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

            # If there's a message received, deal with it depending on type:
            if self.e.inWaiting():
                # Read line in from serial buffer
                try:
                    rec_temp = self.e.readline().strip() #Block the executing thread indefinitely until a line arrives
                    self.grbl_out = rec_temp;
                    # print self.grbl_out
                except Exception as exc:
                    log('serial.readline exception:\n' + str(exc))
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
                except Exception as exc:
                    log('Process response exception:\n' + str(exc))
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

        # This is a special condition, used only at startup to set EEPROM settings
        if self.is_sequential_streaming:
            self._send_next_sequential_stream()
            
        elif self.is_job_streaming:
            self.g_count += 1 # Iterate g-code counter
            if self.c_line != []:
                del self.c_line[0] # Delete the block character count corresponding to the last 'ok'

# PUSH MESSAGE HANDLING

    def process_grbl_push(self, message):
    	# this just needs to translate pulses out into actions
    	log(message)

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
        
        else: 

            log("No serial! Command lost!: " + serialCommand + " (Alt text: " + str(altDisplayText) + ")") 

    # TODO: Are kwargs getting pulled successully by write_direct from here?
    def write_command(self, serialCommand, **kwargs):
        
        self.write_command_buffer.append([serialCommand, kwargs])   

    # Many realtime commands are non-printables, and cause the gcode console to crash. 
    # GCode console with therefore print 'altDisplayText' arg instead
    def write_realtime(self, serialCommand, altDisplayText = None):
        
        self.write_realtime_buffer.append([serialCommand, altDisplayText])