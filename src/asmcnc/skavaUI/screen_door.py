'''
Created March 2020

@author: Letty

Screen to handle door command, and allow user to resume.
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

<DoorScreen>:

    door_label:door_label
    status_container:status_container
    right_button:right_button
    left_button:left_button
    right_button_label:right_button_label
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
            padding: [70,40,70,10]
            spacing: 5
            size_hint_x: 1
    
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 1
                spacing: 5
                
                Image:
                    size_hint_y: 2
                    keep_ratio: True
                    allow_stretch: True
                    source: "./asmcnc/skavaUI/img/door_alarm_graphic.png"
                    valign: 'top'

                Label:
                    id: door_label
                    text_size: self.size
                    size_hint_y: 0.5
                    text: '[b]Stop bar has been depressed![/b]'
                    markup: True
                    font_size: '24sp'
                    color: [0,0,0,1]
                    valign: 'middle'
                    halign: 'center'
                    
                Label:
                    id: door_label
                    text_size: self.size
                    size_hint_y: 0.5
                    text: root.door_text
                    markup: True
                    font_size: '20sp'   
                    valign: 'top'
                    halign: 'center'
    
                BoxLayout:
                    orientation: 'horizontal'
                    padding: [0, 10, 0, 0]
                    spacing: 30
                    size_hint_y: 1
                
                    Button:
                        size_hint_y: 1
                        size_hint_x: 0.1
                        id: right_button
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: [230 / 255., 74 / 255., 25 / 255., 1.]
                        on_press: 
                            root.cancel_stream()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: right_button_label
                                font_size: '22sp'
                                text: '[color=FFFFFF]Cancel[/color]'
                                markup: True

                    Button:
                        size_hint_y: 1
                        size_hint_x: 0.1
                        id: left_button
                        size: self.texture_size
                        valign: 'top'
                        halign: 'center'
                        disabled: False
                        background_normal: ''
                        background_color: [76 / 255., 175 / 255., 80 / 255., 1.]
                        on_press: 
                            root.resume_stream()
                            
                        BoxLayout:
                            padding: 5
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                id: left_button_label
                                font_size: '22sp'
                                text: '[color=FFFFFF]Resume[/color]'
                                markup: True
                

""")

# This screen only gets activated when the PHYSICAL door pin is activated. Firmware automatically flicks to door state.

class DoorScreen(Screen):
    
    dev_win_dt = 2
    
    is_squaring_XY_needed_after_homing = True
    door_label = ObjectProperty()
    door_text = StringProperty()

    right_button = ObjectProperty()
    left_button = ObjectProperty()
    
    right_button_label = ObjectProperty()
    left_button_label = ObjectProperty()   
    
    poll_for_success = None
    quit_home = False
    
    return_to_screen = 'home'
    cancel_to_screen = 'home'
    
    def __init__(self, **kwargs):
    
        super(DoorScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        
        # Status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)
        self.status_bar_widget.cheeky_color = '#E64A19'

        # Text
        self.door_label.font_size =  '19sp'
        self.door_text = '[color=000000]Pressing [b]Resume[/b] will cause the machine to continue it\'s normal operation. ' \
                        +'Pressing [b]Cancel[/b] will cancel the current operation completely. [/color]'

    def on_enter(self):
        if self.m.s.is_job_streaming == True and self.sm.get_screen('go').paused == False:
            self.sm.get_screen('go').pause_job()
            
    def resume_stream(self):
        
        print self.sm.get_screen('go').job_in_progress
        print self.return_to_screen
        
        if self.return_to_screen == 'go' and self.sm.get_screen('go').job_in_progress == 'True':
            print "resume scheduled"
            Clock.schedule_once(lambda dt: self.sm.get_screen('go').resume_job(),0.5)
            self.return_to_app()

        else:
            self.m.resume_after_a_hard_door()    
            self.return_to_app()
        
        
    def cancel_stream(self):
        if self.return_to_screen == 'go':
            self.m.s.is_job_streaming = True
        else:
            self.m.s.cancel_sequential_stream(reset_grbl_after_cancel = False)
        self.m.cancel_after_a_hard_door()
        self.return_to_app()
            
    def return_to_app(self):
        self.sm.current = self.return_to_screen
        