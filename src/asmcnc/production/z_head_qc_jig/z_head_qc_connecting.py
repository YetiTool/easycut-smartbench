import sys
from datetime import datetime

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

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
    print('Z Head Connecting Screen: ' + timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class ZHeadQCConnecting(Screen):

    def __init__(self, **kwargs):

        super(ZHeadQCConnecting, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.usb = kwargs['usb']
        self.connecting_label.text = "Connecting to Z Head..."
        self.z_current = 25
        self.x_current = 26

    def on_enter(self):
        self.connecting_label.text = "Connecting to Z Head..."
        self.ensure_hw_version_and_registers_are_loaded_in()
        if sys.platform == 'win32' or sys.platform == 'darwin': self.progress_to_next_screen()
    
    def ensure_hw_version_and_registers_are_loaded_in(self):

        if not self.m.s.fw_version:
            log("Waiting to get FW version")
            self.connecting_label.text = "Waiting to get FW version"
            Clock.schedule_once(lambda dt: self.ensure_hw_version_and_registers_are_loaded_in(), 0.5)
            return

        if not self.m.TMC_registers_have_been_read_in() and self.m.s.fw_version.startswith("2"):
            log("Waiting to get TMC registers")
            self.connecting_label.text = "Waiting to get TMC registers"
            Clock.schedule_once(lambda dt: self.ensure_hw_version_and_registers_are_loaded_in(), 1)
            return

        if not self.usb.is_available():
            log("Getting USB")
            self.connecting_label.text = "Getting USB"
            Clock.schedule_once(lambda dt: self.ensure_hw_version_and_registers_are_loaded_in(), 1)
            return

        self.progress_to_next_screen()

    def progress_to_next_screen(self):
        log("Progress to next screen")
        self.sm.current = 'qcpcbsetup'
