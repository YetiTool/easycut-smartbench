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

import sys, os

ALARM_CODES = {

    "ALARM:1" : "Hard limit triggered. Machine position is likely lost due to sudden and immediate halt. Re-homing is highly recommended.",
    "ALARM:2" : "G-code motion target exceeds machine travel. Machine position safely retained. Alarm may be unlocked.",
    "ALARM:3" : "Reset while in motion. Grbl cannot guarantee position. Lost steps are likely. Re-homing is highly recommended.",
    "ALARM:4" : "Probe fail. The probe is not in the expected initial grbl_state before starting probe cycle, where G38.2 and G38.3 is not triggered and G38.4 and G38.5 is triggered.",
    "ALARM:5" : "Probe fail. Probe did not contact the workpiece within the programmed travel for G38.2 and G38.4.",
    "ALARM:6" : "Homing fail. Reset during active homing cycle.",
    "ALARM:7" : "Homing fail. Safety door was opened during active homing cycle.",
    "ALARM:8" : "Homing fail. Cycle failed to clear limit switch when pulling off. Try increasing pull-off setting or check wiring.",
    "ALARM:9" : "Homing fail. Could not find limit switch within search distance. Defined as 1.5 * max_travel on search and 5 * pull-off on locate phases.",

}

# Kivy UI builder:
Builder.load_string("""

<AlarmScreenClass>:

    canvas:
        Color: 
            #rgba: hex('#0d47a1FF')
            rgba: hex('#d60000FF')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding: 50
        spacing: 70
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 1
            spacing: 20
             
            Label:
                size_hint_y: 1
                font_size: '35sp'
                text: '[b]STOP! ALARM![/b]'
                markup: True
 
            Label:
                size_hint_y: 1.6
                text_size: self.size
                font_size: '20sp'
                halign: 'left'
                valign: 'top'
                text: root.alarm_description 

#             Label:
#                 text_size: self.size
#                 font_size: '18sp'
#                 halign: 'center'
#                 valign: 'top'
#                 text: 'To clear the alarm state:'
              
            Label:
                text_size: self.size
                font_size: '18sp'
                halign: 'left'
                valign: 'middle'
                text: 'If the axes are near limit switches, de-power the machine and move the axes off the switches.'

            Label:
                text_size: self.size
                font_size: '18sp'
                halign: 'left'
                valign: 'middle'
                text: 'If the axes are away from the limit switches, RESET and UNLOCK the machine.'
                
            BoxLayout:
                orientation: 'horizontal'
                padding: 150, 0
            
                Button:
                    size_hint_y:0.9
                    id: getout_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: False
                    background_color: hex('#a80000FF')
                    on_release: 
                        root.quit_to_home()
                        
                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            font_size: '20sp'
                            text: 'Return'
                        
# This is code from when the alarm screen contained an image. It's broken, but might want to come back to it:                     
#                     Image: 
#                         id: image_alarming
#                         #source: root.alarm_image
#                         #source: "./asmcnc/skavaUI/img/popup_alarm_visual2.png"
#                         source: "./asmcnc/skavaUI/img/lobby_pro.png"
#                         center_x: self.parent.center_x
#                         center_y: self.parent.center_y
#                         #size: self.parent.width, self.parent.height
#                         allow_stretch: False
#                         keep_ratio: True
#                         opacity: 1

    
            
""")

class AlarmScreenClass(Screen):

    # define alarm description to make kivy happy
    alarm_description = StringProperty()
    message = StringProperty()
    return_to_screen = 'home'
    # alarm_image = StringProperty('./asmcnc/skavaUI/img/popup_alarm_visual.png')

    
    def __init__(self, **kwargs):
        super(AlarmScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
    
    def on_enter(self):
        # use the message to get the alarm description
        self.alarm_description = ALARM_CODES.get(self.message, "")
#        self.alarm_description = ALARM_CODES.get("ALARM:4", "") (just for testing)  
        self.m.set_state('Alarm')

    def quit_to_home(self):
        self.sm.current = str(self.return_to_screen)
 
      
