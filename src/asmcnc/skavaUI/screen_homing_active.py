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
                size_hint_x: .5
                text: '[color=333333][b]Homing...[/b][/color]'
                markup: True
                font_size: '30px' 
                valign: 'middle'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                        
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

    
    def windows_cheat_to_procede(self):

        if sys.platform == 'win32':
            self.homing_detected_as_complete()
        else: pass


    def on_enter(self):

        if sys.platform != 'win32':

            self.m.reset_pre_homing()
            Clock.schedule_once(lambda dt: self.start_homing(),0.2)


    def start_homing(self):

        # Issue homing commands
        self.m.set_led_colour('MAGENTA')
        normal_homing_sequence = ['G4 P0.25', # delay, to guarantee LED command to process
                                  '$H']
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
            self.sm.current = self.return_to_screen
            Clock.schedule_once(lambda dt: self.m.set_led_colour("BLUE"),0.2)


    def cancel_homing(self):

        print('Cancelling homing...')
        if self.poll_for_completion_loop != None: self.poll_for_completion_loop.cancel() # necessary so that when sequential stream is cancelled, clock doesn't think it was because of successful completion

        # ... will trigger an alarm screen
        self.m.s.cancel_sequential_stream(reset_grbl_after_cancel = False)
        self.m.reset_on_cancel_homing()
        self.sm.current = self.cancel_to_screen

    
    def on_leave(self):
        
        if self.poll_for_completion_loop != None: self.poll_for_completion_loop.cancel()
        
        