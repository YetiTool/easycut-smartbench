# -*- coding: utf-8 -*-
'''
Created March 2019

@author: Ed

Squaring decision: manual or auto?
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from kivy.clock import Clock

Builder.load_string("""

<HomingScreenActive>:
    
    homing_label: homing_label

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

        BoxLayout:
            orientation: 'horizontal'
            spacing: 20
            size_hint_y: 1.5

            Button:
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.windows_cheat_to_procede()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/home_big.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
            Label:
                id: homing_label
                size_hint_x: 1.1
                markup: True
                font_size: '30px' 
                valign: 'middle'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')
                        
            Button:
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.cancel_homing()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/stop_big.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
        Label:
            size_hint_y: 1                

""")


class HomingScreenActive(Screen):


    return_to_screen = 'lobby'
    cancel_to_screen = 'lobby'    
    poll_for_completion_loop = None

    def __init__(self, **kwargs):

        super(HomingScreenActive, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']
        self.update_strings()

    def on_enter(self):
        if sys.platform == 'win32' or sys.platform == 'darwin': return
        if self.m.homing_interrupted: return
        if not self.m.homing_in_progress: self.m.do_standard_homing_sequence()
        self.poll_for_completion_loop = Clock.schedule_interval(self.poll_for_homing_status_func, 0.2)

    def after_successful_completion_return_to_screen(self):
        self.sm.current = self.return_to_screen
    
    def on_leave(self):
        if self.poll_for_completion_loop: self.poll_for_completion_loop.cancel()
        self.check_next_screen_and_set_homing_flag()

    def check_next_screen_and_set_homing_flag(self):
        if self.sm.current not in [self.return_to_screen, 'squaring_active']: self.m.homing_interrupted = True
        else: self.m.homing_interrupted = False

    def poll_for_homing_status_func(self, dt=0):

        # if homing interrupted then eventually go back to cancel to screen (maybe from on_enter?)
        if not self.m.homing_in_progress: self.after_successful_completion_return_to_screen()
        if self.m.i_am_auto_squaring(): self.go_to_auto_squaring_screen()

    def go_to_auto_squaring_screen(self, dt=0):
        # in case the sequence quickly skips over auto-squaring, delay screen change
        if self.m.homing_task_idx > 3: return
        self.sm.get_screen('squaring_active').cancel_to_screen = self.cancel_to_screen
        self.sm.get_screen('squaring_active').return_to_screen = self.return_to_screen
        self.sm.current = 'squaring_active'

    def cancel_homing(self):
        self.m.cancel_homing_sequence()
        if self.poll_for_completion_loop: self.poll_for_completion_loop.cancel()
        self.sm.current = self.cancel_to_screen

    def update_strings(self):
        self.homing_label.text = self.l.get_str('Homing') + '...'
        
    def windows_cheat_to_procede(self):

        if sys.platform == 'win32' or sys.platform == 'darwin':
            self.homing_detected_as_complete()
        else: pass

    def homing_detected_as_complete(self):
        self.after_successful_completion_return_to_screen()
