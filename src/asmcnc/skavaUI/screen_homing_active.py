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
                size_hint_x: .7
                text: '[color=333333][b]Homing...[/b][/color]'
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

    
    def windows_cheat_to_procede(self):

        if sys.platform == 'win32':
            self.homing_detected_as_complete()
        else: pass


    def on_enter(self):

        self.update_strings()

        if sys.platform != 'win32' and sys.platform != 'darwin':

            self.m.reset_pre_homing()
            Clock.schedule_once(lambda dt: self.start_homing(),0.4)


    def start_homing(self):

        # Issue homing commands
        normal_homing_sequence = ['$H']
        self.m.s.start_sequential_stream(normal_homing_sequence)

        # Due to polling timings, and the fact grbl doesn't issues status during homing, EC may have missed the 'home' status, so we tell it.
        self.m.set_state('Home') 

        # Check for completion - since it's a sequential stream, need a poll loop
        self.poll_for_completion_loop = Clock.schedule_interval(self.check_for_successful_completion, 0.2)
       
     
    def check_for_successful_completion(self, dt):

        # if alarm state is triggered which prevents homing from completing, stop checking for success
        if self.m.state().startswith('Alarm'):
            print "Poll for homing success unscheduled"
            if self.poll_for_completion_loop != None: self.poll_for_completion_loop.cancel()

        # if sequential_stream completes successfully
        elif self.m.s.is_sequential_streaming == False:
            print "Homing detected as success!"
            self.homing_detected_as_complete()


    def homing_detected_as_complete(self):

        if self.poll_for_completion_loop != None: self.poll_for_completion_loop.cancel()
        self.m.is_machine_homed = True # clear this flag too
        
        if self.m.is_squaring_XY_needed_after_homing:
            self.sm.get_screen('squaring_active').cancel_to_screen = self.cancel_to_screen
            self.sm.get_screen('squaring_active').return_to_screen = self.return_to_screen
            self.sm.current = 'squaring_active'
        else: 
            self.m.is_machine_completed_the_initial_squaring_decision = True

            # Chosen to sync with grbl after homing. Ensures that no clash of threads on boot, and that grbl is in definte ready state. So user must home!
            # Enter any initial grbl settings into this list
            # We are preparing for a sequential stream since some of these setting commands store data to the EEPROM
            # When Grbl stores data to EEPROM, the AVR requires all interrupts to be disabled during this write process, including the serial RX ISR.
            # This means that if a g-code or Grbl $ command writes to EEPROM, the data sent during the write may be lost.
            # Sequential streaming handles this
            grbl_settings = [
                        '$$', # Echo grbl settings, which will be read by sw, and internal parameters sync'd
                        '$#', # Echo grbl modes, which will be read by sw, and internal parameters sync'd
                        '$I' # Echo grbl version info, which will be read by sw, and internal parameters sync'd
                        ]
            self.m.s.start_sequential_stream(grbl_settings)
            
            # allow breather for sequential scream to process
            Clock.schedule_once(lambda dt: self.after_successful_completion_return_to_screen(),1)
            Clock.schedule_once(lambda dt: self.m.set_led_colour("GREEN"),1)


    def after_successful_completion_return_to_screen(self):
        self.sm.current = self.return_to_screen


    def cancel_homing(self):

        print('Cancelling homing...')
        if self.poll_for_completion_loop != None: self.poll_for_completion_loop.cancel() # necessary so that when sequential stream is cancelled, clock doesn't think it was because of successful completion

        # ... will trigger an alarm screen
        self.m.s.cancel_sequential_stream(reset_grbl_after_cancel = False)
        self.m.reset_on_cancel_homing()
        self.sm.current = self.cancel_to_screen

    
    def on_leave(self):
        
        if self.poll_for_completion_loop != None: self.poll_for_completion_loop.cancel()

    def update_strings(self):
        self.homing_label.text = self.l.get_str('Homing') + '...'
        
        