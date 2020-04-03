'''
Created March 2019

@author: Letty

Screen to prevent user interaction with GUI while machine is homing
'''
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.clock import Clock
import sys, os


from asmcnc.skavaUI import widget_status_bar

# Kivy UI builder:
Builder.load_string("""

<HomingScreen>:

    homing_label:homing_label
    status_container:status_container
    right_button:right_button
    middle_button:middle_button
    left_button:left_button
    right_button_label:right_button_label
    middle_button_label:middle_button_label
    left_button_label:left_button_label
    
    canvas:
        Color: 
            rgba: hex('#FFFFFF')
        Rectangle: 
            size: self.size
            pos: self.pos         

    BoxLayout: 
        spacing: 0
        padding: 0
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos        
        
        BoxLayout:
            orientation: 'horizontal'
            padding: 40
            spacing: 70
            size_hint_x: 1
    
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 1
                spacing: 10
                
                Image:
                    size_hint_y: 1.2
                    keep_ratio: True
                    allow_stretch: True
                    source: "./asmcnc/skavaUI/img/home_big.png"
                    valign: 'top'
                    
                Label:
                    id: homing_label
                    text_size: self.size
                    size_hint_y: 0.8
                    text: root.homing_text
                    markup: True
                    font_size: '18sp'   
                    valign: 'bottom'
                    halign: 'center'
    
                BoxLayout:
                    orientation: 'horizontal'
                    padding: 0, 0
                    spacing: 20
                    size_hint_y: 0.7
                
                    Button:
                        size_hint_y: 1
                        id: right_button
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: hex('#FFCDD2')
                        on_press: 
                            root.cancel_homing()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: right_button_label
                                font_size: '22sp'
                                text: '[color=455A64]No, cancel[/color]'
                                markup: True
                    Button:
                        id: middle_button
                        size_hint_y: None
                        size_hint_x: None
                        opacity: 0
                        height: '0dp'
                        width: '0dp'
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: hex('#64B5F6')
                        on_press: 
                            root.cancel_homing()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: middle_button_label
                                font_size: '24sp'
                                markup: True
                    
                    Button:
                        size_hint_y: 1
                        id: left_button
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: hex('#BBDEFB')
                        on_press: 
                            root.pre_homing_reset()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: left_button_label
                                font_size: '22sp'
                                text: '[color=455A64]Yes, continue[/color]'
                                markup: True
                

""")

# Intent of class is to send homing commands
# Commands are sent via sequential streaming, which is monitored to evaluate whether the op has completed or not

class HomingScreen(Screen):
    
    dev_win_dt = 2
    
    is_squaring_XY_needed_after_homing = True
    homing_label = ObjectProperty()
    homing_text = StringProperty()

    right_button = ObjectProperty()
    middle_button = ObjectProperty()
    left_button = ObjectProperty()
    
    right_button_label = ObjectProperty()
    middle_button_label = ObjectProperty()
    left_button_label = ObjectProperty()   
    
    poll_for_ready = None
    poll_for_success = None
    quit_home = False
    
    return_to_screen = 'home'
    cancel_to_screen = 'home'
    
    def __init__(self, **kwargs):
    
        super(HomingScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        
        # Status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)
        self.status_bar_widget.cheeky_color = '#42A5F5'

    def on_pre_enter(self):

        if self.m.state().startswith('Idle'):
            self.pre_homing_reset()          


        elif self.m.state().startswith('Alarm'):
            self.quit_home = True
            self.layout_in_alarm_state()

        else:
            self.quit_home = True
            self.layout_other_state()                     
    
    def layout_in_alarm_state(self):

        # Text
        self.homing_label.font_size =  '19sp'
        self.homing_text = '[color=546E7A]The Machine is in an alarm state.' \
                        '\n\nHoming will clear the alarm state, and the machine will resume normal operation.' \
                        '\nWould you like to continue?[/color]'
        
        # Status bar colour      
        self.status_bar_widget.cheeky_color = '#E53935'
        
        # Two button layout
        
        ## Right button
        self.right_button.size_hint_y = 1
        self.right_button.size_hint_x = 0.1
        self.right_button.opacity = 1
        self.right_button.disabled = False
        self.right_button_label.text = '[color=455A64]No, cancel[/color]'
        
        ## Left button
        self.left_button.size_hint_y = 1
        self.left_button.size_hint_x = 0.1
        self.left_button.opacity = 1
        self.left_button.disabled = False
        self.left_button_label.text = '[color=455A64]Yes, continue[/color]'

        ## Middle button
        self.middle_button.size_hint_y = None
        self.middle_button.size_hint_x = None
        self.middle_button.height = '0dp'
        self.middle_button.width = '0dp'
        self.middle_button.opacity = 0
        self.middle_button.disabled = True
        self.middle_button_label.text = ''

    def layout_during_homing(self):
        
        # Text
        self.homing_label.font_size =  '20sp'
        self.homing_text = '[color=546E7A]Homing. Please wait...' \
                        '\n\nSquaring the axes will cause the machine to make a stalling noise.' \
                        '\nThis is normal.[/color]'
        
        # Status bar colour
        self.status_bar_widget.cheeky_color = '#42A5F5'
        
        # Single button layout

        ## Right button
        self.right_button.size_hint_y = None
        self.right_button.size_hint_x = None
        self.right_button.height = '0dp'
        self.right_button.width = '220dp'
        self.right_button.opacity = 0
        self.right_button.disabled = True
        self.right_button_label.text = ''
        
        ## Left button
        self.left_button.size_hint_y = None
        self.left_button.size_hint_x = None
        self.left_button.height = '0dp'
        self.left_button.width = '220dp'
        self.left_button.opacity = 0
        self.left_button.disabled = True
        self.left_button_label.text = ''

        ## Middle button
        self.middle_button.size_hint_y = 1
        self.middle_button.size_hint_x = 0.1
        self.middle_button.opacity = 1
        self.middle_button.disabled = False
        self.middle_button_label.text = '[color=FFFFFF]Cancel Homing[/color]'      

    def layout_other_state(self):
        # Text
        self.homing_label.font_size =  '19sp'
        self.homing_text = '[color=546E7A]The Machine is not in an idle state.' \
                        '\n\nHoming will reset and unlock the machine, and it will resume normal operation.' \
                        '\nWould you like to continue?[/color]'
        
        # Status bar colour      
        self.status_bar_widget.cheeky_color = '#FF7043'
        
        # Two button layout
        
        ## Right button
        self.right_button.size_hint_y = 1
        self.right_button.size_hint_x = 0.1
        self.right_button.opacity = 1
        self.right_button.disabled = False
        self.right_button_label.text = '[color=455A64]No, cancel[/color]'
        
        ## Left button
        self.left_button.size_hint_y = 1
        self.left_button.size_hint_x = 0.1
        self.left_button.opacity = 1
        self.left_button.disabled = False
        self.left_button_label.text = '[color=455A64]Yes, continue[/color]'

        ## Middle button
        self.middle_button.size_hint_y = None
        self.middle_button.size_hint_x = None
        self.middle_button.height = '0dp'
        self.middle_button.width = '0dp'
        self.middle_button.opacity = 0
        self.middle_button.disabled = True
        self.middle_button_label.text = ''
        
    def pre_homing_reset(self):
        
        self.layout_during_homing() 
        self.m.reset_pre_homing()
        self.poll_for_ready = Clock.schedule_interval(self.is_machine_idle, 1)
        
    def is_machine_idle(self, dt):  
        if self.m.state().startswith('Idle'):
            Clock.unschedule(self.poll_for_ready)
            
            if sys.platform == "win32":
                Clock.schedule_once(self.developer_windows_esc, self.dev_win_dt) 
            
            else: 
                self.trigger_homing()
    
    def trigger_homing(self):
        
        self.quit_home = False
        
        # Is this first time since power cycling?
        if self.is_squaring_XY_needed_after_homing: 
            self.home_with_squaring()
        else: 
            self.home_normally()

        # Due to polling timings, and the fact grbl doesn't issues status during homing, EC may have missed the 'home' status, so we tell it.
        self.m.set_state('Home') 

        # monitor sequential stream status for completion
        
        def create_poll_for_success():    
            self.poll_for_success = Clock.schedule_interval(self.check_for_successful_completion, 0.2)
   
        Clock.schedule_once(lambda dt: create_poll_for_success(), 1)

    def home_normally(self):
        # home without suaring the axis
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
                                  'G53 G0 X900', # position zHead to put CoG of X beam on the mid plane (mX: -400)
                                  '$20=0', # soft limits off
                                  '$21=0', # hard limits off
                                  'G91', # relative coords
                                  '*L11FF00',
                                  'G1 Y-28 F700', # drive lower frame into legs, assumes it's starting from a 3mm pull off
                                  'G1 Y28', # re-enter work area
                                  '*LFF00FF',
                                  'G90', # abs coords
                                  'G53 G0 X15', # position zHead to put CoG of X beam on the mid plane (mX: -400)

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

        self.m.set_state('Home')
        # if alarm state is triggered which prevents homing from completing, stop checking for success

        if self.m.state().startswith('Alarm'):

            print "Poll for homing success unscheduled"
            Clock.unschedule(self.poll_for_success)
            self.homing_text = '[b]Homing unsuccessful.[/b]'

        # if sequential_stream completes successfully
        elif self.m.s.is_sequential_streaming == False:
            print "Homing success!"
            self.is_squaring_XY_needed_after_homing = False # clear flag, so this function doesn't run again
            self.m.is_machine_homed = True # clear this flag too
            Clock.unschedule(self.poll_for_success)
            self.return_to_app()
            
    def return_to_app(self):
        Clock.schedule_once(lambda dt: self.m.set_led_colour("BLUE"),0.2)
        self.sm.current = self.return_to_screen

    def cancel_homing(self):
        print('Cancelling homing...')
        if self.poll_for_success != None: Clock.unschedule(self.poll_for_success) # necessary so that when sequential stream is cancelled, clock doesn't think it was because of successful completion

        if self.quit_home == True:
            self.sm.current = self.cancel_to_screen
            
        else:
            # ... will trigger an alarm screen
            self.m.s.cancel_sequential_stream(reset_grbl_after_cancel = False)
            self.m.reset_on_cancel_homing()
            self.sm.current = self.cancel_to_screen
    
    def on_leave(self):
        if self.poll_for_success != None: Clock.unschedule(self.poll_for_success)
        if self.poll_for_ready != None: Clock.unschedule(self.poll_for_ready)
        self.quit_home = False
        
        
    def developer_windows_esc(self, dt):
        print "pretend Homing success!"
        self.is_squaring_XY_needed_after_homing = False # clear flag, so this function doesn't run again
        self.m.is_machine_homed = True # clear this flag too
        self.m.set_state('Idle')
        self.return_to_app()

        
