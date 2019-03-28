'''
Created on 12 Feb 2019

@author: Letty
'''
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.clock import Clock

import sys, os


# Kivy UI builder:
Builder.load_string("""

<HomingScreen>:

    canvas:
        Color: 
            rgba: hex('#0D47A1')
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
#             spacing: 20
#             padding: 10
            
            Image:
                size_hint_y: 1.2
                keep_ratio: True
                allow_stretch: True
                source: "./asmcnc/skavaUI/img/home_big.png"
                
            Label: 
                size_hint_y: 0.5
                text: '[b]Homing. Please wait...[/b]'
                markup: True
                font_size: '40sp'   
                valign: 'bottom'     
            Label: 
                size_hint_y: 0.2
                text: 'Squaring the axes will cause the machine to make a stalling noise. This is normal.'
                markup: True
                font_size: '20sp' 
                valign: 'top'
""")

class HomingScreen(Screen):

    def __init__(self, **kwargs):
        super(HomingScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
    
    def on_enter(self):
        # self.m.s.suppress_error_screens = True
        self.poll_machine_status = Clock.schedule_interval(self.check_machine_status, 1)
        
    def check_machine_status(self, dt):
        if self.m.s.grbl_out.startswith('<Idle'):
            Clock.unschedule(self.poll_machine_status)
            Clock.schedule_once(self.suppress_errors_false, 0.2)          

    def suppress_errors_false(self, dt):
        # self.m.s.suppress_error_screens = False
        self.quit_to_home()
 
    def quit_to_home(self):
        self.sm.current = 'home'