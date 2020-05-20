'''
Created March 2019

@author: Ed

Prepare to home
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os


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


class SpindeShutdownScreen(Screen):


    cancel_to_screen = 'lobby'   
    return_to_screen = 'lobby'   
    
    
    def __init__(self, **kwargs):
        
        super(SpindeShutdownScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
    
    def on_enter(self):
        self.m.set_led_colour('ORANGE')
     
        
        