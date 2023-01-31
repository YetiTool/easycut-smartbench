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
    start_homing_event = None
    go_to_squaring_screen_event = None
   
    
    def __init__(self, **kwargs):

        super(HomingScreenActive, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']
        self.update_strings()

    def on_enter(self):
        if sys.platform == 'win32' or sys.platform == 'darwin': return
        self.m.do_standard_homing_sequence()
        self.poll_for_completion_loop = Clock.schedule_interval(self.poll_for_homing_status_func, 0.2)

    def after_successful_completion_return_to_screen(self):
        self.sm.current = self.return_to_screen
    
    def on_leave(self):
        if self.poll_for_completion_loop: self.poll_for_completion_loop.cancel()

    def poll_for_homing_status_func(self, dt=0):
        if not self.m.homing_in_progress: self.after_successful_completion_return_to_screen()
        if self.m.homing_completed_task_idx == 2: 
            # in case the sequence quickly skips over auto-squaring, delay screen change
            self.go_to_squaring_screen_event = Clock.schedule_once(self.go_to_auto_squaring_screen, 0.15)

    def go_to_auto_squaring_screen(self, dt=0):
        self.sm.get_screen('squaring_active').cancel_to_screen = self.cancel_to_screen
        self.sm.get_screen('squaring_active').return_to_screen = self.return_to_screen
        self.sm.current = 'squaring_active'

    def cancel_homing(self):

        print('Cancelling homing...')
        if self.poll_for_completion_loop: self.poll_for_completion_loop.cancel() # necessary so that when sequential stream is cancelled, clock doesn't think it was because of successful completion
        if self.start_homing_event: self.start_homing_event.cancel()
        # ... will trigger an alarm screen
        self.m.s.cancel_sequential_stream(reset_grbl_after_cancel = False)
        self.m.reset_on_cancel_homing()
        self.sm.current = self.cancel_to_screen


    def update_strings(self):
        self.homing_label.text = self.l.get_str('Homing') + '...'
        
    def windows_cheat_to_procede(self):

        if sys.platform == 'win32' or sys.platform == 'darwin':
            self.homing_detected_as_complete()
        else: pass

    def homing_detected_as_complete(self):
        self.after_successful_completion_return_to_screen()

# OLD ------------------------------------------------

    # self.start_homing_event = Clock.schedule_once(lambda dt: self.start_homing(),0.4)


    # def start_homing(self):

    #     # Issue homing commands
    #     normal_homing_sequence = ['$H']
    #     self.m.s.start_sequential_stream(normal_homing_sequence)

    #     # Due to polling timings, and the fact grbl doesn't issues status during homing, EC may have missed the 'home' status, so we tell it.
    #     self.m.set_state('Home') 

    #     # Check for completion - since it's a sequential stream, need a poll loop
    #     self.poll_for_completion_loop = Clock.schedule_interval(self.check_for_successful_completion, 0.2)
       
     
    # def check_for_successful_completion(self, dt):

    #     # if alarm state is triggered which prevents homing from completing, stop checking for success
    #     if self.m.state().startswith('Alarm'):
    #         print "Poll for homing success unscheduled"
    #         if self.poll_for_completion_loop != None: self.poll_for_completion_loop.cancel()

    #     # if sequential_stream completes successfully
    #     elif self.m.s.is_sequential_streaming == False:
    #         print "Homing detected as success!"
    #         self.homing_detected_as_complete()


    # def homing_detected_as_complete(self):

    #     if self.poll_for_completion_loop != None: self.poll_for_completion_loop.cancel()
    #     self.m.is_machine_homed = True # clear this flag too
        
    #     if self.m.is_squaring_XY_needed_after_homing:
    #         self.sm.get_screen('squaring_active').cancel_to_screen = self.cancel_to_screen
    #         self.sm.get_screen('squaring_active').return_to_screen = self.return_to_screen
    #         self.sm.current = 'squaring_active'
    #     else: 
    #         self.m.is_machine_completed_the_initial_squaring_decision = True

    #         # Chosen to sync with grbl after homing. Ensures that no clash of threads on boot, and that grbl is in definte ready state. So user must home!
    #         # Enter any initial grbl settings into this list
    #         # We are preparing for a sequential stream since some of these setting commands store data to the EEPROM
    #         # When Grbl stores data to EEPROM, the AVR requires all interrupts to be disabled during this write process, including the serial RX ISR.
    #         # This means that if a g-code or Grbl $ command writes to EEPROM, the data sent during the write may be lost.
    #         # Sequential streaming handles this
    #         grbl_settings = [
    #                     '$$', # Echo grbl settings, which will be read by sw, and internal parameters sync'd
    #                     '$#', # Echo grbl modes, which will be read by sw, and internal parameters sync'd
    #                     '$I' # Echo grbl version info, which will be read by sw, and internal parameters sync'd
    #                     ]
    #         self.m.s.start_sequential_stream(grbl_settings)

    #         Clock.schedule_once(lambda dt: self.post_homing_sequence(), 1)


    # def post_homing_sequence(self):

    #     # If laser is enabled, move by offset
    #     if self.m.is_laser_enabled:

    #         tolerance = 5 # mm

    #         print("Jog absolute: " + str(float(self.m.x_min_jog_abs_limit) + tolerance - self.m.laser_offset_x_value))
    #         self.m.jog_absolute_single_axis('X', float(self.m.x_min_jog_abs_limit) + tolerance - self.m.laser_offset_x_value, 3000)

    #     # allow breather for sequential stream to process
    #     Clock.schedule_once(lambda dt: self.after_successful_completion_return_to_screen(),1)
    #     Clock.schedule_once(lambda dt: self.m.set_led_colour("GREEN"),1)
        