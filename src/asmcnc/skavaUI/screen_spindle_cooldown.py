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
                font_size: '24px' 
                valign: 'middle'
                halign: 'center'
                size:self.texture_size
                text_size: self.size

            BoxLayout: 
                spacing: 100
                padding: 0
                orientation: 'vertical'                 

                Image:
                    id: spindle_icon
                    # source: "./asmcnc/skavaUI/img/alarm_icon.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True
                    # size_hint: (None, None)
                    # height: dp(130)
                    # width: dp(130)

                Label:
                    id: countdown
                    markup: True
                    font_size: '80px' 
                    valign: 'middle'
                    halign: 'center'
                    size:self.texture_size
                    text_size: self.size  
                    text: '10'
                    color: [0,0,0,1]

                Image:
                    id: countdown_icon
                    # source: "./asmcnc/skavaUI/img/alarm_icon.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True
                    # size_hint: (None, None)
                    # height: dp(130)
                    # width: dp(130) 


""")


class SpindleCooldownScreen(Screen):

    return_screen = 'jobdone'
    seconds = 10

    def __init__(self, **kwargs):
        
        super(SpindleCooldownScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
    #     self.m=kwargs['machine']

    # def on_pre_enter(self):
    #     self.m.zUp_and_spindle_on()

    def on_enter(self):
        Clock.schedule_once(self.exit_screen, 10)
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
        self.seconds = 10
        self.countdown.text = '10'
        