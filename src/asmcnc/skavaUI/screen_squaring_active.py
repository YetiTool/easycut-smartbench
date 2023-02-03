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

<SquaringScreenActive>:

    overdrive_label: overdrive_label
    squaring_label: squaring_label

    canvas:
        Color: 
            rgba: hex('#E5E5E5FF')
        Rectangle: 
            size: self.size
            pos: self.pos         

    BoxLayout: 
        spacing: 0
        padding: [20, 20]
        orientation: 'vertical'

        Label:
            size_hint_y: 1

        BoxLayout:
            padding: [20, 0]
            orientation: 'horizontal'
            spacing: 30
            size_hint_y: 1.5

            Button:
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.windows_cheat_to_procede()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/squaring_icon_big.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
            Label:
                id: squaring_label
                size_hint_x: 1.1
                markup: True
                font_size: '30px' 
                valign: 'middle'
                halign: 'center'
                size:self.texture_size
                # text_size: self.size
                color: hex('#333333ff')
                        
            Button:
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.cancel_squaring()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/stop_big.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
            
        Label:
            id: overdrive_label
            size_hint_y: 2
            markup: True
            font_size: '28px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            color: hex('#333333ff')           


""")


class SquaringScreenActive(Screen):
    
    return_to_screen = 'lobby'
    cancel_to_screen = 'lobby'     
    poll_for_completion_loop = None
    
    def __init__(self, **kwargs):
    
        super(SquaringScreenActive, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']
        self.update_strings()

    def on_enter(self):
        if sys.platform == 'win32' or sys.platform == 'darwin': return
        self.poll_for_completion_loop = Clock.schedule_interval(self.poll_for_squaring_status_func, 0.2)

    def on_leave(self):
        if self.poll_for_completion_loop != None: self.poll_for_completion_loop.cancel()

    def poll_for_squaring_status_func(self, dt=0):
        # if homing interrupted then eventually go back to cancel to screen (maybe from on_enter?)

        if not self.m.homing_in_progress: self.sm.current = self.cancel_to_screen
        if not self.m.i_am_auto_squaring(): self.return_to_homing_active_screen()

    def check_next_screen_and_set_homing_flag(self):
        if self.sm.current not in [self.return_to_screen, 'homing_active']: self.m.homing_interrupted = True
        else: self.m.homing_interrupted = False

    def return_to_homing_active_screen(self):        
        self.sm.get_screen('homing_active').cancel_to_screen = self.cancel_to_screen
        self.sm.get_screen('homing_active').return_to_screen = self.return_to_screen
        self.sm.current = 'homing_active'

    def cancel_squaring(self):
        self.m.cancel_homing_sequence()
        if self.poll_for_completion_loop: self.poll_for_completion_loop.cancel()
        self.sm.current = self.cancel_to_screen

    def update_strings(self):

        self.overdrive_label.text = self.l.get_str("This operation will over-drive the X beam into the legs, creating a stalling noise. This is normal.")
        self.squaring_label.text = self.l.get_bold("Squaring") + "..."

    def windows_cheat_to_procede(self):

        if sys.platform == 'win32' or sys.platform == 'darwin':
            self.squaring_detected_as_complete()
        else: pass

    def squaring_detected_as_complete(self):
        self.return_to_homing_active_screen()
