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

    "ALARM:1" : "An end-of-axis limit switch was triggered during a move. The machine's position was likely lost. Re-homing is highly recommended.",
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
            padding: [15,0,0,0]
            spacing: 0
            size_hint: (None, None)
            height: dp(50)
            width: dp(800)
            Label:
                size_hint: (None, None)
                font_size: '30sp'
                text: '[b]Alarm![/b]'
                color: [0,0,0,1]
                markup: True
                halign: 'left'
                height: dp(50)
                width: dp(790)
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos

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
                size_hint: (None, None)
                font_size: '20sp'
                text: root.alarm_description
                color: [0,0,0,1]
                markup: True
                halign: 'left'
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
                            source: "./asmcnc/skavaUI/img/show_details.png"
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
                            source: "./asmcnc/skavaUI/img/red_exit.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
         
            
""")

class AlarmScreenClass(Screen):

    # define alarm description to make kivy happy
    alarm_description = "An end-of-axis limit switch was triggered during a move. The machine's position was likely lost. Re-homing is highly recommended." #StringProperty()
    message = StringProperty()
    return_to_screen = 'home'
    
    def __init__(self, **kwargs):
        super(AlarmScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
    
    def on_enter(self):
        
        self.alarm_description = ALARM_CODES.get(self.message, "")
        self.m.set_state('Alarm')
        self.m.led_restore()

    def show_details(self):
        self.m.reset_from_alarm()
        self.details = self.m.s.grbl_out

        def update_description():
            self.details = self.details + '\n' + self.m.s.grbl_out
            print self.details

        def trigger_popup():
            popup_info.PopupInfo(self.sm, 600, self.details)

        update_details_event = Clock.schedule_interval(lambda dt: update_description(), 0.1)
        Clock.schedule_once(lambda dt: trigger_popup(), 0.3)
        Clock.unschedule(update_details_event)

    def quit_to_home(self):
        
        self.m.resume_from_alarm()
        
        if self.sm.has_screen(self.return_to_screen):
            self.sm.current = self.return_to_screen     
        else: 
            self.sm.current = 'lobby'

            