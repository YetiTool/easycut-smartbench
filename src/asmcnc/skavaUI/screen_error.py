# -*- coding: utf-8 -*-
"""
Created on 19 Feb 2019

Screen to show user GRBL errors. Called in serial_connection.

Pauses streaming until user returns (and if they are in Go stream until they resume Job). 

@author: Letty
"""
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import (
    ObjectProperty,
    StringProperty,
)
from kivy.uix.screenmanager import Screen

ERROR_CODES = {
    "error:1": "G-code words consist of a letter and a value. Letter was not found.",
    "error:2": "Numeric value format is not valid or missing an expected value.",
    "error:3": "Grbl '$' system command was not recognized or supported.",
    "error:4": "Negative value received for an expected positive value.",
    "error:5": "Homing cycle is not enabled via settings.",
    "error:6": "Minimum step pulse time must be greater than 3 microseconds.",
    "error:7": "EEPROM read failed. Reset and restored to default values.",
    "error:8": "Grbl '$' command cannot be used unless Grbl is IDLE. Ensures smooth operation during a job.",
    "error:9": "G-code locked out during alarm or jog state.",
    "error:10": "Soft limits cannot be enabled without homing also enabled. Check $22 setting.",
    "error:11": "Max characters per line exceeded. Line was not processed and executed.",
    "error:12": "Compile Option Grbl '$' setting value exceeds the maximum step rate supported.",
    "error:13": "Interrupt bar detected as pressed. Check all four contacts at the interrupt bar ends are not pressed. Pressing each switch a few times may clear the contact.",
    "error:14": "Grbl-Mega Only Build info or startup line exceeded EEPROM line length limit.",
    "error:15": "Jog target exceeds machine travel. Command ignored. Have you homed the machine yet? If not, please do so now.",
    "error:16": "Jog command with no '=' or contains prohibited g-code.",
    "error:17": "Laser mode requires PWM output.",
    "error:20": "Unsupported or invalid g-code command found in block.",
    "error:21": "More than one g-code command from same modal group found in block.",
    "error:22": "Feed rate has not yet been set or is undefined.",
    "error:23": "G-code command in block requires an integer value.",
    "error:24": "Two G-code commands that both require the use of the XYZ axis words were detected in the block.",
    "error:25": "A G-code word was repeated in the block.",
    "error:26": "A G-code command implicitly or explicitly requires XYZ axis words in the block, but none were detected.",
    "error:27": "N line number value is not within the valid range of 1 - 9,999,999.",
    "error:28": "A G-code command was sent, but is missing some required P or L value words in the line.",
    "error:29": "Grbl supports six work coordinate systems G54-G59. G59.1, G59.2, and G59.3 are not supported.",
    "error:30": "The G53 G-code command requires either a G0 seek or G1 feed motion mode to be active. A different motion was active.",
    "error:31": "There are unused axis words in the block and G80 motion mode cancel is active.",
    "error:32": "A G2 or G3 arc was commanded but there are no XYZ axis words in the selected plane to trace the arc.",
    "error:33": "The motion command has an invalid target. G2, G3, and G38.2 generates this error, if the arc is impossible to generate or if the probe target is the current position.",
    "error:34": "A G2 or G3 arc, traced with the radius definition, had a mathematical error when computing the arc geometry. Try either breaking up the arc into semi-circles or quadrants, or redefine them with the arc offset definition.",
    "error:35": "A G2 or G3 arc, traced with the offset definition, is missing the IJK offset word in the selected plane to trace the arc.",
    "error:36": "There are unused, leftover G-code words that aren't used by any command in the block.",
    "error:37": "The G43.1 dynamic tool length offset command cannot apply an offset to an axis other than its configured axis. The Grbl default axis is the Z-axis.",
    "error:38": "Tool number greater than max supported value.",
    "error:39": "ASMCNC custom error: this firmware version has not recognized this command.",
    "error:40": "TMC command received for wrong motor (>5).",
    "error:41": "Realtime command crc8 error.",
    "error:42": "Non hex code character received.",
    "error:43": "Command supplied to the function is outside wanted range.",
    "error:44": "Parameter supplied to the function is outside wanted range.",
    "error:45": "Realtime command buffer parser did not find the expected packet start modifier.",
    "error:46": "Realtime command buffer parser found length that is higher than maximum.",
    "error:47": "Sequence number does not match the expected one.",
    "error:48": "Realtime command buffer overflow: slow down sending RTL commands or increase buffer size.",
}
Builder.load_string(
    """

<ErrorScreenClass>:

    getout_button: getout_button
    error_header: error_header
    user_instruction: user_instruction
    return_label: return_label

    canvas:
        Color: 
            rgba: hex('#ebbc00FF')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding: app.get_scaled_tuple([40.0, 40.0])
        spacing: app.get_scaled_width(30.0)
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 1
            spacing: app.get_scaled_width(20.0)
             
            Label:
                id: error_header
                size_hint_y: 0.6
                text_size: self.size
                font_size: app.get_scaled_sp('24.0sp')
                markup: True
                halign: 'left'
                vallign: 'top'
 
            Label:
                size_hint_y: 1.2
                text_size: self.size
                font_size: app.get_scaled_sp('22.0sp')
                halign: 'left'
                valign: 'middle'
                text: root.error_description 
                
            Label:
                id: user_instruction
                size_hint_y: 0.6
                font_size: app.get_scaled_sp('22.0sp')
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                
            BoxLayout:
                orientation: 'horizontal'
                padding: app.get_scaled_tuple([130.0, 0])
                size_hint_y: 0.8
            
                Button:
                    font_size: app.get_scaled_sp('15.0sp')
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
                        padding: app.get_scaled_tuple([5.0, 5.0])
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            id: return_label
                            font_size: app.get_scaled_sp('20.0sp')
                            text: 'Return'
                        
  
            
"""
)


class ErrorScreenClass(Screen):
    error_description = StringProperty()
    message = StringProperty()
    button_text = StringProperty()
    getout_button = ObjectProperty()
    return_to_screen = "home"

    def __init__(self, **kwargs):
        super(ErrorScreenClass, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.jd = kwargs["job"]
        self.db = kwargs["database"]
        self.l = kwargs["localization"]
        self.update_strings()

    def on_enter(self):
        self.getout_button.disabled = True
        if self.m.s.is_job_streaming:
            self.return_to_screen = "job_incomplete"
        self.error_description = self.l.get_str(ERROR_CODES.get(self.message, ""))
        self.m.stop_from_gcode_error()
        if self.return_to_screen == "job_incomplete":
            self.sm.get_screen("job_incomplete").prep_this_screen(
                "Error", event_number=self.message
            )
        Clock.schedule_once(lambda dt: self.enable_getout_button(), 1.6)

    def enable_getout_button(self):
        self.getout_button.disabled = False

    def button_press(self):
        self.m.resume_from_gcode_error()
        if self.sm.has_screen(self.return_to_screen):
            self.sm.current = self.return_to_screen
        else:
            self.sm.current = "lobby"

    def update_strings(self):
        self.error_header.text = (
            self.l.get_bold("ERROR")
            + "\n"
            + self.l.get_str("SmartBench could not process a command")
            + ":"
        )
        self.user_instruction.text = (
            self.l.get_str("The job will now be cancelled.")
            + " "
            + self.l.get_str("Check the gcode file before re-running it.")
        )
        self.return_label.text = self.l.get_str("Return")
