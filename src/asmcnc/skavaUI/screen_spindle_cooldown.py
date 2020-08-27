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

    BoxLayout: 
        spacing: 0
        padding: 20
        orientation: 'vertical'
        size_hint: (None, None)
        height: 480
        width: 800
        canvas:
            Color: 
                rgba: hex('#E5E5E5FF')
            Rectangle: 
                size: self.size
                pos: self.pos         

        BoxLayout: 
            spacing: 0
            padding: 
            orientation: 'vertical'
            canvas:
                Color: 
                    rgba: [1,1,1,1]
                RoundedRectangle:
                    size: self.size
                    pos: self.pos    
            
            Label:
                size_hint_y: 1
                text: 'Cooling down spindle...'
                color: [0,0,0,1]
                markup: True
                font_size: '30px' 
                valign: 'middle'
                halign: 'center'
                size:self.texture_size
                text_size: self.size

            BoxLayout: 
                spacing: 0
                padding: [100, 0, 100, 130]
                orientation: 'horizontal'          
                size_hint: (None, None)
                height: 251
                width: 800
                pos: self.parent.pos


                BoxLayout: 
                    spacing: 0
                    padding: [8, 0, 57, 0]
                    orientation: 'horizontal'          
                    size_hint: (None, None)
                    height: 121
                    width: 180
                    Image:
                        id: spindle_icon
                        source: "./asmcnc/skavaUI/img/spindle_cooldown_on.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
                        size_hint: (None, None)
                        height: dp(121)
                        width: dp(115) 

                BoxLayout: 
                    spacing: 0
                    padding: [0, 0, 0, 0]
                    orientation: 'horizontal'          
                    size_hint: (None, None)
                    height: 121
                    width: 200
                    Label:
                        id: countdown
                        markup: True
                        font_size: '100px' 
                        valign: 'middle'
                        halign: 'center'
                        size:self.texture_size
                        text_size: self.size  
                        text: '10'
                        color: [0,0,0,1]

                BoxLayout: 
                    spacing: 0
                    padding: [70, 0, 10, 3]
                    orientation: 'horizontal'          
                    size_hint: (None, None)
                    height: 121
                    width: 180
                    Image:
                        id: countdown_icon
                        source: "./asmcnc/skavaUI/img/countdown_big.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
                        size_hint: (None, None)
                        height: dp(118)
                        width: dp(100) 


""")


class SpindleCooldownScreen(Screen):

    return_screen = 'jobdone'
    seconds = self.m.spindle_cooldown_time_seconds

    def __init__(self, **kwargs):
        
        super(SpindleCooldownScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def on_pre_enter(self):
        self.m.cooldown_zUp_and_spindle_on()
        self.seconds = self.m.spindle_cooldown_time_seconds
        self.countdown.text = str(self.seconds)

    def on_enter(self):
        Clock.schedule_once(self.exit_screen, self.seconds)
        self.update_timer_event = Clock.schedule_interval(self.update_timer, 1)
    
    def exit_screen(self, dt):
        self.sm.current = self.return_screen

    def update_timer(self, dt):
        self.seconds = self.seconds - 1
        self.countdown.text = str(self.seconds)

    def on_leave(self):
        self.m.spindle_off()
        self.m.vac_off()
        Clock.unschedule(self.update_timer_event)
        self.seconds = self.m.spindle_cooldown_time_seconds
        self.countdown.text = str(self.seconds)
        