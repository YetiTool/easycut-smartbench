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

    header_label: header_label
    show_details_button: show_details_button

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
                id: header_label
                size_hint: (None, None)
                font_size: '30sp'
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
                    id: show_details_button
                    size_hint: (None,None)
                    height: dp(80)
                    width: dp(280)
                    # background_color: hex('#F4433600')
                    # center: self.parent.center
                    # pos: self.parent.pos
                    background_normal: "./asmcnc/skavaUI/img/show_details_blue_blank.png"
                    background_down: "./asmcnc/skavaUI/img/show_details_blue_blank.png"
                    border: [dp(20)]*4
                    on_press: root.show_details()
                    text: '         ' + 'Show Details'
                    markup: True
                    text_size: self.size
                    valign: "middle"
                    halign: "left"

                    # BoxLayout:
                    #     padding: 0
                    #     size: self.parent.size
                    #     pos: self.parent.pos
                    #     Image:
                    #         source: "./asmcnc/skavaUI/img/show_details_blue_blank.png"
                    #         center_x: self.parent.center_x
                    #         y: self.parent.y
                    #         size: self.parent.width, self.parent.height
                    #         allow_stretch: True

        # Button:
        #     id: button_system_info
        #     text: 'System Info'
        #     valign: "bottom"
        #     halign: "center"
        #     markup: True
        #     font_size: root.default_font_size
        #     text_size: self.size
        #     on_press: root.go_to_build_info()
        #     background_normal: "./asmcnc/apps/systemTools_app/img/system_info.png"
        #     background_down: "./asmcnc/apps/systemTools_app/img/system_info.png"
        #     border: [dp(25)]*4
        #     padding_y: 5
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

    # define alarm description to make kivy happy
    alarm_description = StringProperty()
    message = StringProperty()
    return_to_screen = 'home'
    # button_space = '         '
    default_font_size = 30
    
    def __init__(self, **kwargs):
        super(AlarmScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']

        self.header_label.text = self.l.get_bold('Alarm!')
        self.show_details_button.text = self.l.get_str('Show Details')
        self.update_font_size(self.show_details_button)
    
    def on_enter(self):
        self.show_details_button.text = self.l.get_str('Show Details')
        self.update_font_size(self.show_details_button)
        self.alarm_description = self.l.get_str(ALARM_CODES.get(self.message, ""))
        self.m.set_state('Alarm')
        self.m.led_restore()

    def show_details(self):
        self.m.reset_from_alarm()

        def trigger_popup():
            details = ('\n').join(self.sm.get_screen('home').gcode_monitor_widget.status_report_buffer)
            popup_info.PopupInfo(self.sm, self.l, 600, details)

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

    def update_font_size(self, value):

        button_space = 10*" "

        print(str(len(value.text)))

        if len(value.text) < 12:
            value.font_size = self.default_font_size
            button_space = 9*" "
        elif len(value.text) > 11: 
            value.font_size = self.default_font_size - 4
            button_space = 10*" "
        if len(value.text) > 14: 
            value.font_size = self.default_font_size - 8
            button_space = 11*" "
        if len(value.text) > 16: 
            value.font_size = self.default_font_size - 10
            button_space = 12*" "

        value.text = button_space + value.text

            