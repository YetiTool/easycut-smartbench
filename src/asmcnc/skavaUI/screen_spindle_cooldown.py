'''
Created July 2020

@author: Letty

Spindle cooldown screen
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from kivy.clock import Clock
from datetime import datetime


Builder.load_string("""

<SpindleCooldownScreen>:

    countdown: countdown

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
            text: '[color=333333]SmartBench is cooling down the spindle after the job.[/color]'
            markup: True
            font_size: '30px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size

        Label:
            size_hint_y: 1
            text: '[color=333333]Please wait.[/color]'
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
                # Image:
                #     source: "./asmcnc/skavaUI/img/spindle_shutdown_wait.png"
                #     size: self.parent.width, self.parent.height
                #     allow_stretch: True 
                Label:
                    id: countdown
                    markup: True
                    font_size: '80px' 
                    valign: 'middle'
                    halign: 'center'
                    size:self.texture_size
                    text_size: self.size  
                    text: '0'
                    color: [0,0,0,1]       

        Label:
            size_hint_y: 1

""")


class SpindleCooldownScreen(Screen):

    return_screen = 'jobdone'

    def __init__(self, **kwargs):
        
        super(SpindleCooldownScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def on_pre_enter(self):
        self.m.zUp_and_spindle_on()
        self.seconds = 0

    def on_enter(self):
        Clock.schedule_once(self.exit_screen, 10)
        Clock.schedule_interval(self.update_timer, 1)
    
    def exit_screen(self, dt):
        self.sm.current = self.return_screen

    def update_timer(self, dt):
        self.seconds = self.seconds + 1
        self.countdown.text = str(self.seconds)

    def on_leave(self):
        self.m.spindle_off()
        self.m.vac_off()
        self.seconds = 0
        
        