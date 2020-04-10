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
            size_hint_y: .5

        BoxLayout:
            orientation: 'horizontal'
            spacing: 30
            size_hint_y: 2

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
                size_hint_x: .6
                text: '[color=333333][b]Squaring...[/b][/color]'
                markup: True
                font_size: '30px' 
                valign: 'middle'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                        
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
            size_hint_y: .5
            
        Label:
            size_hint_y: 1
            text: '[color=333333]This operation will over-drive the X beam into the legs, creating a stalling noise. This is normal.[/color]'
            markup: True
            font_size: '30px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size             

        Label:
            size_hint_y: .5

""")


class SquaringScreenActive(Screen):
    
    return_to_screen = 'lobby'
    cancel_to_screen = 'lobby'     
    poll_for_completion_loop = None
    
    
    def __init__(self, **kwargs):
    
        super(SquaringScreenActive, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
    
    
    def windows_cheat_to_procede(self):

        if sys.platform == 'win32':
            self.squaring_detected_as_complete()
        else: pass
        

    def on_enter(self):

        if sys.platform != 'win32':
            self.start_auto_squaring()
            self.poll_for_completion_loop = Clock.schedule_interval(self.check_for_successful_completion, 0.2)
            print "Polling for completion"

    def start_auto_squaring(self):

        # This function is designed to square the machine's X&Y axes
        # It does this by killing the limit switches and driving the X frame into mechanical deadstops at the end of the Y axis.
        # The steppers will stall out, but the X frame will square against the mechanical deadstops.
        # Intended use is first home after power-up only, or the stalling noise will get annoying!

        # Because we're setting grbl configs in this function (i.e.$x=n), we need to adopt the grbl config approach used in the serial module.
        # So no direct writing to serial here, we're waiting for grbl responses before we send each line:
        
        square_homing_sequence =  [
                                  '$20=0', # soft limits off
                                  '$21=0', # hard limits off
                                  'G4 P0.5', # delay, which is needed solely for it's "blocking ok" response
                                  'G53 G0 X-400', # position zHead to put CoG of X beam on the mid plane (mX: -400)
                                  'G91', # relative coords
                                  'G1 Y-28 F700', # drive lower frame into legs, assumes it's starting from a 3mm pull off
                                  'G1 Y28', # re-enter work area
                                  'G90', # abs coords
                                  'G53 G0 X-1285', # position zHead to put CoG of X beam on the mid plane (mX: -400)

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
        print "Auto squaring..."


    def check_for_successful_completion(self, dt):

        # if alarm state is triggered which prevents homing from completing, stop checking for success
        if self.m.state().startswith('Alarm'):
            print "Poll for homing success unscheduled"
            if self.poll_for_completion_loop != None: self.poll_for_completion_loop.cancel()

        # if sequential_stream completes successfully
        elif self.m.s.is_sequential_streaming == False:
            print "Auto squaring detected as success!"
            self.squaring_detected_as_complete()


    def squaring_detected_as_complete(self):

        if self.poll_for_completion_loop != None: self.poll_for_completion_loop.cancel()
        self.m.is_squaring_XY_needed_after_homing = False
        Clock.schedule_once(lambda dt: self.return_to_homing_active_screen(), 0.5)


    def return_to_homing_active_screen(self):
        
        self.sm.get_screen('homing_active').cancel_to_screen = self.cancel_to_screen
        self.sm.get_screen('homing_active').return_to_screen = self.return_to_screen
        self.sm.current = 'homing_active'


    def cancel_squaring(self):

        print('Cancelling squaring...')
        if self.poll_for_completion_loop != None: self.poll_for_completion_loop.cancel() # necessary so that when sequential stream is cancelled, clock doesn't think it was because of successful completion

        # ... will trigger an alarm screen
        self.m.s.cancel_sequential_stream(reset_grbl_after_cancel = False)
        self.m.reset_on_cancel_homing()
        Clock.schedule_once(lambda dt: self.return_to_screen('squaring_decision'), 0.5)

    
    def on_leave(self):
        
        if self.poll_for_completion_loop != None: self.poll_for_completion_loop.cancel()