import serial, sys, time, string, threading
from datetime import datetime
from os import listdir
from kivy.clock import Clock


BAUD_RATE = 9600

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

    H_side = 0
    F_side = 0

    prev_message = ''

    raw_message = ''

    def __init__(self, screen_manager, port):

        self.sm = screen_manager
        PORT = port # e.g. 'ttyACM0' or 'ttyACM1'

    def __del__(self):
        print 'Destructor'


    def establish_connection(self):

        self.e = serial.Serial('/dev/' + str(PORT), BAUD_RATE, timeout = 6, writeTimeout = 20)

        # try:

            # self.e = serial.Serial('/dev/' + str(PORT), BAUD_RATE, timeout = 6, writeTimeout = 20)

            # filesForDevice = listdir('/dev/') # put all device files into list[]
            # for line in filesForDevice: # run through all files


            #     print(line)

            #     # if sys.platform == 'darwin':

            #     #     if (line[:12] == 'tty.usbmodem'): # look for...   
            #     #         devicePort = line # take whole line (includes suffix address e.g. ttyACM0
            #     #         self.e = serial.Serial('/dev/' + str(devicePort), BAUD_RATE, timeout = 6, writeTimeout = 20) # assign

            #     # FLAG: This if statement is only relevant in linux environment. 
            #     # EITHER: USB Comms hardware
            #     # if (line[:6] == 'ttyUSB' or line[:6] == 'ttyACM'): # look for prefix of known success (covers both Mega and Uno)
            #     # OR: UART Comms hardware
            #     if line[:7] == PORT: # looks specifically for USB port that encoder is plugged into
            #         devicePort = line # take whole line (includes suffix address e.g. ttyACM0
            #         self.e = serial.Serial('/dev/' + str(devicePort), BAUD_RATE, timeout = 6, writeTimeout = 20) # assign

            #     # if (line[:12] == 'tty.usbmodem'): # look for...   
            #     #     devicePort = line # take whole line (includes suffix address e.g. ttyACM0
            #     #     self.e = serial.Serial('/dev/' + str(devicePort), BAUD_RATE, timeout = 6, writeTimeout = 20) # assign

        # except: 
        #     log('No arduino connected')

        if self.is_connected():
            log('Connected to ' + str(devicePort))
            log('Initialising encoder...')
            if sys.platform == 'darwin':
                self.start_services(1)
            else: 
                Clock.schedule_once(self.start_services, 1)
            

    # is serial port connected?
    def is_connected(self):

        if self.e != None:
            return True
        else: 
            return False


    # called by first kivy screen when safe to assume kivy processing is completed, to ensure correct clock scheduling
    def start_services(self, dt):

        log('Starting services')
        self.e.flushInput()  # Flush startup text in serial input
        t = threading.Thread(target=self.encoder_scanner)
        t.daemon = True
        t.start()

    def encoder_scanner(self):
        
        log('Running encoder_scanner thread')

        while True:

            if self.FLUSH_FLAG == True:
                self.e.flushInput()
                self.FLUSH_FLAG = False

            # If there's a message received, deal with it depending on type:
            if self.e.inWaiting():
                # Read line in from serial buffer
                try:
                    rec_temp = self.e.readline().strip() #Block the executing thread indefinitely until a line arrives
                    # log('New serial output')
                    log(rec_temp)
                except Exception as exc:
                    log('serial.readline exception:\n' + str(exc))
                    rec_temp = ''
            else: 
                rec_temp = ''

            # If something received from serial buffer, process it. 
            if len(rec_temp):
    
                # Process the GRBL response:
                # NB: Sequential streaming is controlled through process_grbl_response
                try:
                    self.process_grbl_push(rec_temp)

                except Exception as exc:
                    log('Process response exception:\n' + str(exc))
                    raise # HACK allow error to cause serial comms thread to exit

# PUSH MESSAGE HANDLING

    def process_grbl_push(self, message):

        # self.raw_message = message

        if message.startswith('H:'):
                self.H_side = float(message.split(':')[1])
        elif message.startswith('F:'):
                self.F_side = float(message.split(':')[1])
                
        # if self.prev_message != message: 
        #     log(message)
        #     # self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('rec', "Pulse out " + PORT + ": "+ message)
        #     self.prev_message = message