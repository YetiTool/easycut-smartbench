'''
Created March 2019

@author: Ed

Prepare to home
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from kivy.clock import Clock
from datetime import datetime


Builder.load_string("""

<SpindeShutdownScreen>:

    canvas:
        Color: 
            rgba: hex('#E5E5E5FF')
        Rectangle: 
            size: self.size
            pos: self.pos         

    BoxLayout: 
        spacing: 0
        padding: 40
        orientation: 'vertical'

        Label:
            size_hint_y: 1 
            
        Label:
            size_hint_y: 1
            text: '[color=333333]SmartBench is pausing the spindle motor.[/color]'
            markup: True
            font_size: '30px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size

        Label:
            size_hint_y: 1
            text: '[color=333333]Please wait...[/color]'
            markup: True
            font_size: '30px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size

        Label:
            size_hint_y: 1                        

        Button:
            size_hint_y: 4
            background_color: hex('#FFFFFF00')
            on_press: root.begin_homing()
            BoxLayout:
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/skavaUI/img/spindle_shutdown_wait.png"
                    size: self.parent.width, self.parent.height
                    allow_stretch: True 
                        
        Label:
            size_hint_y: 1                

""")

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))


class SpindeShutdownScreen(Screen):


    cancel_to_screen = 'lobby'   
    return_to_screen = 'lobby'   
    reason_for_shutdown = None
    time_to_allow_spindle_to_rest = 3
    poll_interval_between_checking_z_rest = 0.5
    last_z_pos = 0
    
    def __init__(self, **kwargs):
        
        super(SpindeShutdownScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
    
    
    def on_enter(self):
        
        self.m.stop_for_a_stream_pause()
        self.m.set_led_colour('ORANGE')
        
        # Allow spindle to rest before checking that the machine has stopped any auto-Z-up move
        Clock.schedule_once(self.start_polling_for_z_rest, self.time_to_allow_spindle_to_rest)
        
        
    def start_polling_for_z_rest(self, dt):
        
        self.poll_for_z_rest = Clock.schedule_interval(self.poll_for_z_rest, self.poll_interval_between_checking_z_rest)
    
    
    def poll_for_z_rest(self, dt):
        
        # see if z_pos has changed since last check
        current_z_pos = self.m.z_pos_str()
        
        if current_z_pos == self.last_z_pos:
            # machine has stopped
            self.poll_for_z_rest.cancel()  # stop polling
            log('Safely paused')
            
        else:
            self.last_z_pos = current_z_pos

    
    
     
        
        