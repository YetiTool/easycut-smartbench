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
            AnchorLayout: 
                Button:
                    size_hint_x: 0.25
                    size_hint_y: 0.35
                    halign: 'center'
                    valign: 'middle'
                    background_normal: ''
                    background_color: hex('#1E88E5')
                    on_release: 
                        root.cancel_homing()
                    
                    Label:
                        #size: self.texture_size
                        text: '[b]Cancel Homing[/b]'
                        size: self.parent.size
                        pos: self.parent.pos
                        text_size: self.size
                        valign: 'middle'
                        halign: 'center'
                        font_size: '22sp'
                        markup: True
            Label: 
                size_hint_y: 0.2
                text: 'Squaring the axes will cause the machine to make a stalling noise. This is normal.'
                markup: True
                font_size: '20sp' 
                valign: 'top'
                

""")

class HomingScreen(Screen):
    
    wait_for_homing_finished = None
    poll_machine_status = None

    def __init__(self, **kwargs):
        super(HomingScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
    
    def on_enter(self):
        self.m.s.suppress_error_screens = True
        
        if self.m.is_squaring_XY_needed_after_homing:
            self.poll_machine_status = Clock.schedule_interval(self.check_machine_status, 2)           
            self.m.home_all()
        else:
            self.m.home_all()
            self.wait_for_homing_finished = Clock.schedule_interval(self.exit_sequence, 0.5)
        
    def check_machine_status(self, dt):
        if self.m.homing_stage_counter == 2:
                # Because there's a GRBL pause in the homing sequence, will take an extra 5 seconds for anything
                # else to happen. Hence delay here too. 
                Clock.unschedule(self.poll_machine_status)
                self.wait_for_homing_finished = Clock.schedule_interval(self.exit_sequence, 0.5)

    def exit_sequence(self, dt):
        if not self.m.s.is_sequential_streaming and self.m.state().startswith('Idle'):
            self.m.s.suppress_error_screens = False
            if self.wait_for_homing_finished != None: Clock.unschedule(self.wait_for_homing_finished)
            self.m.homing_stage_counter = 0
            self.sm.current = 'home'
            
    def cancel_homing(self):
        if self.poll_machine_status != None: Clock.unschedule(self.poll_machine_status)
        if self.wait_for_homing_finished != None: Clock.unschedule(self.wait_for_homing_finished)
        self.m.s.is_sequential_streaming = False
        self.m.s.write_direct("\x18", realtime = True, show_in_sys = True, show_in_console = False) # Soft-reset. This forces the need to home when the controller starts up
        print('Homing Cancelled')
        self.m.homing_stage_counter = 0
        self.sm.current = 'home'
        