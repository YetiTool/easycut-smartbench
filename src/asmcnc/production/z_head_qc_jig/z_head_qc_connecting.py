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
        self.current = 25

    def on_enter(self):

        log("Set Z current to 25 if it is not set already...")
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

        if self.m.TMC_motor[TMC_Z].ActiveCurrentScale == self.current:
            log("Current already set at 25")
            self.progress_to_next_screen()
            return

        self.connecting_label.text = "Setting current..."
        log("Setting current to 25...")
        if self.m.set_motor_current("Z", self.current): 
            Clock.schedule_once(lambda dt: self.progress_after_all_registers_read_in(), 0.5)
        else: 
            log("Z Head not Idle yet, waiting...")
            Clock.schedule_once(lambda dt: self.get_and_set_current(), 1) # If unsuccessful it's because it's not Idle









