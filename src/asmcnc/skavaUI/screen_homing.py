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

# Intent of class is to send homing commands
# Commands are sent via sequential streaming, which is monitored to evaluate whether the op has completed or not

class HomingScreen(Screen):
    
    
    is_squaring_XY_needed_after_homing = True

    
    def __init__(self, **kwargs):
    
        super(HomingScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
    
    
    def on_enter(self):
        
        # Is this first time since power cycling?
        if self.is_squaring_XY_needed_after_homing: 
            self.home_with_squaring()
        else: 
            self.home_normally()

        # Due to polling timings, and the fact grbl doesn't issues status during homing, EC may have missed the 'home' status, so we tell it.
        self.m.set_state('Home') 

        # monitor sequential stream status for completion
        self.poll_for_success = Clock.schedule_interval(self.check_for_successful_completion, 1)           


    def home_normally(self):
        
        normal_homing_sequence = ['$H']
        self.m.s.start_sequential_stream(normal_homing_sequence)


    def home_with_squaring(self):

        # This function is designed to square the machine's X&Y axes
        # It does this by killing the limit switches and driving the X frame into mechanical deadstops at the end of the Y axis.
        # The steppers will stall out, but the X frame will square against the mechanical deadstops.
        # Intended use is first home after power-up only, or the stalling noise will get annoying!

        # Because we're setting grbl configs in this function (i.e.$x=n), we need to adopt the grbl config approach used in the serial module.
        # So no direct writing to serial here, we're waiting for grbl responses before we send each line:

        square_homing_sequence =  [
                                  '$H', # home
                                  '$20=0', # soft limits off
                                  '$21=0', # hard limits off
                                  'G91', # relative coords
                                  'G1 Y-25 F500', # drive lower frame into legs, assumes it's starting from a 3mm pull off
                                  'G1 Y25', # re-enter work area
                                  'G90', # abs coords
                                  
                                  # Coming up we have some $x=n commands, and the machine needs to be idle when sending these
                                  # Since it will be moving due to previous G command, we need to wait until it has stopped
                                  # The simplest way to do this is to send a G4 command (grbl pause)
                                  # This is fairly unique since it gets a "blocking ok" respoinse from grbl
                                  # ie. grbl only issues the 'ok' response AFTER the pause command has been completed
                                  # (most other commands get the 'ok' response as soon as they are loaded into the line buffer, not on completion)
                                  # Therefore we know the machine has stopped moving before the line after the pause is sent
                                  
                                  'G4 P0.5', # delay, which is needed solely for it's "blocking ok" response
                                  '$21=1', # soft limits on
                                  '$20=1', # soft limits off
                                  '$H' # home - which also issues a "blocking ok" response
                                  ]

        self.m.s.start_sequential_stream(square_homing_sequence)

        
    def check_for_successful_completion(self, dt):

        # if alarm state happens to prevent homing from completing, stop the success checking
        if self.m.state == 'Alarm':
            print "Poll for homing success unscheduled"
            Clock.unschedule(self.poll_for_success)

        # if sequential_stream completes
        elif self.m.s.is_sequential_streaming == False:
            # Success!
            print "Homing success!"
            self.is_squaring_XY_needed_after_homing = False # clear flag, so this function doesn't run again

            self.m.is_machine_homed = True # status on powerup
            Clock.unschedule(self.poll_for_success)
            self.sm.current = 'home'

    def cancel_homing(self):

        print('Cancelling homing...')
        Clock.unschedule(self.poll_for_success) # necessary so that when sequential stream is cancelled, clock doesn't think it was because of successful completion
        self.m.s.cancel_sequential_stream(reset_grbl_after_cancel = False)

        self.m.soft_reset()
        # ... will trigger an alarm screen




        