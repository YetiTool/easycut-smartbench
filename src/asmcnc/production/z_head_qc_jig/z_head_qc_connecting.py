from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from datetime import datetime

Builder.load_string("""
<ZHeadQCConnecting>:


    connecting_label: connecting_label

    canvas:
        Color: 
            rgba: hex('#000000')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding: 70
        spacing: 70
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 1
                
            Label:
                id: connecting_label
                text_size: self.size
                size_hint_y: 0.5
                markup: True
                font_size: '40sp'   
                valign: 'middle'
                halign: 'center'    
    

""")

def log(message):
    timestamp = datetime.now()
    print ('Z Head Connecting Screen: ' + timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class ZHeadQCConnecting(Screen):

    def __init__(self, **kwargs):

        super(ZHeadQCConnecting, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.connecting_label.text = "Connecting to Z Head..."
        self.z_current = 5
        self.x_current = 5

    def on_enter(self):

        log("Set Z current to 25 if it is not set already...")
        log("Set X current to 26 if it is not set already...")
        self.connecting_label.text = "Connecting to Z Head..."
        self.get_and_set_current()

    
    def progress_to_next_screen(self):
        log("Progress to next screen")
        self.sm.current = 'qchome'


    def progress_after_all_registers_read_in(self):

        if self.m.TMC_registers_have_been_read_in():
            log("Registers have been read in")
            self.progress_to_next_screen()
            return

        Clock.schedule_once(lambda dt: self.progress_after_all_registers_read_in(), 0.5)


    def get_and_set_current(self):

        if not self.m.s.fw_version:
            log("Waiting to get FW version")
            Clock.schedule_once(lambda dt: self.get_and_set_current(), 0.5)
            return

        if not self.m.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'setting current'):
            log("FW version too low - not setting current")
            self.progress_to_next_screen()
            return

        if not self.m.TMC_registers_have_been_read_in():
            log("TMC registers have not been read in yet")
            Clock.schedule_once(lambda dt: self.get_and_set_current(), 1)
            return

        if self.m.TMC_motor[TMC_Z].ActiveCurrentScale == self.z_current and \
            self.m.TMC_motor[TMC_X1].ActiveCurrentScale == self.x_current and \
            self.m.TMC_motor[TMC_X2].ActiveCurrentScale == self.x_current:
            log("Z Current already set at 25")
            log("X Current already set at 26")

            if self.m.TMC_motor[TMC_Z].temperatureCoefficient == 10000 and \
              (self.m.TMC_motor[TMC_Y1].temperatureCoefficient == 5000 and self.m.TMC_motor[TMC_Y2].temperatureCoefficient == 5000) and \
              (self.m.TMC_motor[TMC_X1].temperatureCoefficient == 5000 and self.m.TMC_motor[TMC_X2].temperatureCoefficient == 5000):

                log("Thermal coeffs already set")
                self.progress_after_all_registers_read_in()
            
            else:
                self.set_thermal_coefficients()

            return

        self.connecting_label.text = "Setting current..."
        log("Setting Z current to 25...")
        log("Setting X current to 26...")
        if self.m.set_motor_current("Z", self.z_current) and self.m.set_motor_current("X", self.x_current):
            Clock.schedule_once(lambda dt: self.set_thermal_coefficients(), 0.5)
        else: 
            log("Z Head not Idle yet, waiting...")
            Clock.schedule_once(lambda dt: self.get_and_set_current(), 1) # If unsuccessful it's because it's not Idle


    def set_thermal_coefficients(self):

        if self.m.TMC_motor[TMC_Z].temperatureCoefficient == 10000 and \
          (self.m.TMC_motor[TMC_Y1].temperatureCoefficient == 5000 and self.m.TMC_motor[TMC_Y2].temperatureCoefficient == 5000) and \
          (self.m.TMC_motor[TMC_X1].temperatureCoefficient == 5000 and self.m.TMC_motor[TMC_X2].temperatureCoefficient == 5000):

            log("Thermal coeffs already set")
            self.store_params_and_progress()
            return

        self.connecting_label.text = "Setting thermal coeffs..."
        log("Setting thermal coeffs...")

        if self.m.set_thermal_coefficients("X", 5000) and self.m.set_thermal_coefficients("Y", 5000) and self.m.set_thermal_coefficients("Z", 10000):
            Clock.schedule_once(lambda dt: self.store_params_and_progress(), 1)

        else:
            log("Z Head not Idle yet, waiting...")
            Clock.schedule_once(lambda dt: self.set_thermal_coefficients(), 0.5)


    def store_params_and_progress(self):
        log("Storing TMC params...")
        self.m.store_tmc_params_in_eeprom_and_handshake()
        self.progress_after_all_registers_read_in()











