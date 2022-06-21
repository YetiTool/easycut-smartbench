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
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class ZHeadQCConnecting(Screen):

    def __init__(self, **kwargs):

        super(ZHeadQCConnecting, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.connecting_label.text = "Connecting to Z Head..."
        self.current = 22

    def on_enter(self):

        log("Set X current to 22 if it is not set already...")
    	self.get_and_set_current()

    
    def progress_to_next_screen(self):

    	self.sm.current = 'qchome'


    def get_and_set_current(self):

    	if not self.m.s.fw_version:

    		Clock.schedule_once(lambda dt: self.get_and_set_current(), 0.5)
    		return

    	# If current is already set to 22, carry onto QC home
    	if 	self.m.TMC_motor[TMC_X1].ActiveCurrentScale == self.current or \
    		not self.m.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'setting current'):

    		self.progress_to_next_screen()
    		return

    	elif self.m.TMC_motor[TMC_X1].ActiveCurrentScale == 0:

    		Clock.schedule_once(lambda dt: self.get_and_set_current(), 1)
    		return

    	else:
			
			self.connecting_label.text = "Setting current..."
			if self.m.set_motor_current("X", self.current): Clock.schedule_once(lambda dt: self.progress_to_next_screen(), 0.5)
			else: Clock.schedule_once(lambda dt: self.get_and_set_current(), 1) # If unsuccessful it's because it's not Idle


