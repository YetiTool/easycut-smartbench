'''
Created on 19 Feb 2019

Screen to show user GRBL errors. Called in serial_connection.

Pauses streaming until user returns (and if they are in Go stream until they resume Job). 

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

ERROR_CODES = {

    "error:1"  : "G-code words consist of a letter and a value. Letter was not found.",
    "error:2"  : "Numeric value format is not valid or is missing an expected value.",
    "error:3"  : "Grbl '$' system command was not recognized or supported.",
    "error:4"  : "Negative value received for an expected positive value.",
    "error:5"  : "Homing cycle is not enabled via settings.",
    "error:6"  : "Minimum step pulse time must be greater than 3usec",
    "error:7"  : "EEPROM read failed. Reset and restored to default values.",
    "error:8"  : "Grbl '$' command cannot be used unless Grbl is IDLE. This ensures smooth operation during a job.",
    "error:9"  : "G-code locked out during alarm or jog grbl_state",
    "error:10" : "Soft limits cannot be enabled without homing also enabled.",
    "error:11" : "Max characters per line exceeded. Line was not processed and executed.",
    "error:12" : "(Compile Option Grbl '$' setting value exceeds the maximum step rate supported.",
    "error:13" : "Stop bar detected as pressed. Check all four contacts at the stop bar ends are not pressed. Pressing each switch a few times may clear the contact.",
    "error:14" : "(Grbl-Mega Only Build info or startup line exceeded EEPROM line length limit.",
    "error:15" : "Have you homed the machine yet? If not, please do so now.\nJog target exceeds machine travel. Command ignored.",
    "error:16" : "Jog command with no '=' or contains prohibited g-code.",
    "error:17" : "Laser mode requires PWM output.",
    "error:20" : "Unsupported or invalid g-code command found in block.",
    "error:21" : "More than one g-code command from same modal group found in block.",
    "error:22" : "Feed rate has not yet been set or is undefined.",
    "error:23" : "G-code command in block requires an integer value.",
    "error:24" : "Two G-code commands that both require the use of the XYZ axis words were detected in the block.",
    "error:25" : "A G-code word was repeated in the block.",
    "error:26" : "A G-code command implicitly or explicitly requires XYZ axis words in the block, but none were detected.",
    "error:27" : "N line number value is not within the valid range of 1 - 9,999,999.",
    "error:28" : "A G-code command was sent, but is missing some required P or L value words in the line.",
    "error:29" : "Grbl supports six work coordinate systems G54-G59. G59.1, G59.2, and G59.3 are not supported.",
    "error:30" : "The G53 G-code command requires either a G0 seek or G1 feed motion mode to be active. A different motion was active.",
    "error:31" : "There are unused axis words in the block and G80 motion mode cancel is active.",
    "error:32" : "A G2 or G3 arc was commanded but there are no XYZ axis words in the selected plane to trace the arc.",
    "error:33" : "The motion command has an invalid target. G2, G3, and G38.2 generates this error, if the arc is impossible to generate or if the probe target is the current position.",
    "error:34" : "A G2 or G3 arc, traced with the radius definition, had a mathematical error when computing the arc geometry. Try either breaking up the arc into semi-circles or quadrants, or redefine them with the arc offset definition.",
    "error:35" : "A G2 or G3 arc, traced with the offset definition, is missing the IJK offset word in the selected plane to trace the arc.",
    "error:36" : "There are unused, leftover G-code words that aren't used by any command in the block.",
    "error:37" : "The G43.1 dynamic tool length offset command cannot apply an offset to an axis other than its configured axis. The Grbl default axis is the Z-axis.",

}

# Kivy UI builder:
Builder.load_string("""

<ErrorScreenClass>:

    getout_button:getout_button

    canvas:
        Color: 
            rgba: hex('#ebbc00FF')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding: 60
        spacing: 30
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 1
            spacing: 20
             
            Label:
                size_hint_y: 0.8
                text_size: self.size
                font_size: '24sp'
                text: '[b]ERROR[/b]\\nSmartBench could not process a command:'
                markup: True
                halign: 'left'
                vallign: 'top'
 
            Label:
                size_hint_y: 1.2
                text_size: self.size
                font_size: '22sp'
                halign: 'left'
                valign: 'middle'
                text: root.error_description 
                
            Label:
                size_hint_y: 0.6
                font_size: '22sp'
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                text: 'The job will now be cancelled. Check the gcode file before re-running it.'
                
            BoxLayout:
                orientation: 'horizontal'
                padding: 130, 0
            
                Button:
                    size_hint_y:0.9
                    id: getout_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: True
                    background_color: hex('#e6c300FF')
                    on_press:
                        root.button_press()
                        
                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            font_size: '20sp'
                            text: 'Return'
                        
  
            
""")

class ErrorScreenClass(Screen):

    # define error description to make kivy happy
    error_description = StringProperty()
    message = StringProperty()
    button_text = StringProperty()
    getout_button = ObjectProperty()
    user_instruction = StringProperty()
    button_function = StringProperty()
    
    return_to_screen = 'home'
    
    def __init__(self, **kwargs):
        super(ErrorScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']  

    def on_enter(self):

        self.getout_button.disabled = True
        
        # use the message to get the error description        
        self.error_description = ERROR_CODES.get(self.message, "")
        self.m.stop_from_gcode_error()

        self.button_function = self.return_to_screen
        Clock.schedule_once(lambda dt: self.enable_getout_button(), 1.6)

    
    def enable_getout_button(self):
        self.getout_button.disabled = False
    
    def button_press(self):       
        
        self.m.resume_from_gcode_error()

        if self.sm.has_screen(self.return_to_screen):
            self.sm.current = self.return_to_screen  
        else: 
            self.sm.current = 'lobby'
        
         
  
