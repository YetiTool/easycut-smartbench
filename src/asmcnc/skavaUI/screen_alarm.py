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

from asmcnc.skavaUI import popup_info

import sys, os

ALARM_CODES = {

    "ALARM:1" : "End-of-axis limit switch triggered during a move. The machine's position was likely lost. Re-homing is highly recommended.",
    "ALARM:2" : "The requested motion target exceeds the machine's travel.",
    "ALARM:3" : "Machine was reset while in motion and cannot guarantee position. Lost steps are likely. Re-homing is recommended.",
    "ALARM:4" : "Probe fail. Probe was not in the expected state before starting probe cycle.",
    "ALARM:5" : "Probe fail. Probe did not contact the workpiece within the programmed travel.",
    "ALARM:6" : "Homing fail. Reset during active homing cycle.",
    "ALARM:7" : "Homing fail. Safety switch was activated during the homing cycle.",
    "ALARM:8" : "Homing fail. Cycle failed to clear limit switch when pulling off.",
    "ALARM:9" : "Homing fail. Could not find limit switch within search distance.",

}

# Kivy UI builder:
Builder.load_string("""

<AlarmScreenClass>:

    alarm_description_label : alarm_description_label
    trigger_description_label : trigger_description_label

    canvas:
        Color: 
            rgba: [1, 1, 1, 1]
        Rectangle: 
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        padding: 0
        spacing: 0
        size_hint: (None, None)
        height: dp(480)
        width: dp(800)

        # Alarm label
        BoxLayout: 
            padding: [15,0,15,0]
            spacing: 0
            size_hint: (None, None)
            height: dp(50)
            width: dp(800)
            orientation: 'horizontal'

            Label:
                size_hint: (None, None)
                font_size: '30sp'
                text: '[b]Alarm![/b]'
                color: [0,0,0,1]
                markup: True
                halign: 'left'
                height: dp(50)
                width: dp(170)
                text_size: self.size

            Label:
                id: trigger_description_label
                size_hint: (None, None)
                font_size: '20sp'
                color: [0,0,0,1]
                markup: True
                halign: 'right'
                height: dp(50)
                width: dp(600)
                text_size: self.size

        BoxLayout: 
            padding: [10,0,10,0]
            spacing: 0
            size_hint: (None, None)
            height: dp(5)
            width: dp(800)
            Image:
                id: red_underline
                source: "./asmcnc/skavaUI/img/red_underline.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True
        
        # Alarm image and text
        BoxLayout: 
            padding: [30,35,30,0]
            spacing: 20
            size_hint: (None, None)
            height: dp(295)
            width: dp(800)
            orientation: 'vertical'
            BoxLayout: 
                padding: [305,0,0,0]
                size_hint: (None, None)
                height: dp(130)
                width: dp(740)       
                Image:
                    id: alarm_icon
                    source: "./asmcnc/skavaUI/img/alarm_icon.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True
                    size_hint: (None, None)
                    height: dp(130)
                    width: dp(130)
            Label:
                id: alarm_description_label
                size_hint: (None, None)
                font_size: '20sp'
                text: root.alarm_description
                color: [0,0,0,1]
                markup: True
                halign: 'center'
                valign: 'middle'
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos
                height: dp(90)
                width: dp(700)

        BoxLayout: 
            padding: [0,0,0,0]
            spacing: 0
            size_hint: (None, None)
            height: dp(130)
            width: dp(800)
            orientation: 'horizontal'
            BoxLayout: 
                padding: [20,0,0,20]
                spacing: 0
                size_hint: (None, None)
                height: dp(130)
                width: dp(400)
                Button:
                    size_hint: (None,None)
                    height: dp(80)
                    width: dp(280)
                    background_color: hex('#F4433600')
                    center: self.parent.center
                    pos: self.parent.pos
                    on_press: root.show_details()
                    BoxLayout:
                        padding: 0
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/skavaUI/img/show_details_blue.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
            BoxLayout: 
                padding: [258,0,30,10]
                spacing: 0
                size_hint: (None, None)
                height: dp(130)
                width: dp(400)
                Button:
                    size_hint: (None,None)
                    height: dp(112)
                    width: dp(112)
                    background_color: hex('#F4433600')
                    center: self.parent.center
                    pos: self.parent.pos
                    on_press: root.quit_to_home()
                    BoxLayout:
                        padding: 0
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/skavaUI/img/quit_to_lobby_btn.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
         
            
""")

class AlarmScreenClass(Screen):

    # these variables are set externally where the alarm screen is called
    message = StringProperty()
    return_to_screen = 'home'

    # this is the screen's description
    alarm_description = StringProperty()

    
    def __init__(self, **kwargs):
        super(AlarmScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
    
    def on_enter(self):

        Clock.schedule_once(lambda dt: self.m.reset_from_alarm(), 0.5)        
        self.alarm_description = ALARM_CODES.get(self.message, "")
        self.m.set_state('Alarm')
        self.m.led_restore()
        if (self.message).endswith('1'):
            Clock.schedule_once(lambda dt: self.get_suspected_trigger(), 0.6)

    def on_leave(self):
        self.alarm_description = ''
        self.trigger_description_label.text = ''

    def show_details(self):

        def trigger_popup():
            details = ('\n').join(self.sm.get_screen('home').gcode_monitor_widget.status_report_buffer)
            popup_info.PopupInfo(self.sm, 600, details)

        Clock.schedule_once(lambda dt: trigger_popup(), 0.45)


    def quit_to_home(self):
        
        self.m.resume_from_alarm()

        if self.return_to_screen == 'go':
            self.sm.get_screen('go').is_job_started_already = False
            self.sm.get_screen('go').temp_suppress_prompts = True
        
        if self.sm.has_screen(self.return_to_screen):
            self.sm.current = self.return_to_screen

        else: 
            self.sm.current = 'lobby'


    def get_suspected_trigger(self):

        # End-of-axis limit switch triggered during a move. The machine's position was likely lost. Re-homing is highly recommended. 
        # Limit code: xXyYz 

        print(self.message)

        limit_code = "Alarm trigger: "

        if self.m.s.limit_x: 
            self.trigger_description_label.text = (
                "[b]Home X limit triggered at " + \
                'X: ' + self.m.x_pos_str() + ', Y: ' + self.m.y_pos_str() + ', Z: ' + self.m.z_pos_str() + '[/b]'
                )
            limit_code  = limit_code  + "x"

        if self.m.s.limit_X: 
            self.trigger_description_label.text = (
                "[b]Far X limit triggered at " + \
                'X: ' + self.m.x_pos_str() + ', Y: ' + self.m.y_pos_str() + ', Z: ' + self.m.z_pos_str() + '[/b]'
                )
            limit_code  = limit_code  + "X"

        if self.m.s.limit_y: 
            self.trigger_description_label.text = (
                "[b]Home Y limit triggered at " + \
                'X: ' + self.m.x_pos_str() + ', Y: ' + self.m.y_pos_str() + ', Z: ' + self.m.z_pos_str() + '[/b]'
                )
            limit_code  = limit_code  + "y"

        if self.m.s.limit_Y: 
            self.trigger_description_label.text = (
                "[b]Far Y limit triggered at " + \
                'X: ' + self.m.x_pos_str() + ', Y: ' + self.m.y_pos_str() + ', Z: ' + self.m.z_pos_str() + '[/b]'
                )
            limit_code  = limit_code  + "Y"

        if self.m.s.limit_z: 
            self.trigger_description_label.text = (
                "[b]Z limit triggered at " + \
                'X: ' + self.m.x_pos_str() + ', Y: ' + self.m.y_pos_str() + ', Z: ' + self.m.z_pos_str() + '[/b]'
                )
            limit_code  = limit_code  + "z"

        if limit_code == "Alarm trigger: ":
            limit_code = limit_code + "Unknown"

        self.alarm_description_label.text = limit_code + '.\n' + self.alarm_description



            