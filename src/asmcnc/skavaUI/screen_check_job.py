'''
Created on 25 Feb 2019

@author: Letty

This screen checks the users job, and allows them to review any errors 
'''

import kivy
import docutils
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from __builtin__ import file
from kivy.clock import Clock
from functools import partial


import sys, os
from os.path import expanduser
from shutil import copy
from datetime import datetime
import re

ERROR_CODES = {

    "error:1"  : "G-code words consist of a letter and a value. Letter was not found.",
    "error:2"  : "Numeric value format is not valid or missing an expected value.",
    "error:3"  : "Grbl '$' system command was not recognized or supported.",
    "error:4"  : "Negative value received for an expected positive value.",
    "error:5"  : "Homing cycle is not enabled via settings.",
    "error:6"  : "Minimum step pulse time must be greater than 3usec",
    "error:7"  : "EEPROM read failed. Reset and restored to default values.",
    "error:8"  : "Grbl '$' command cannot be used unless Grbl is IDLE. Ensures smooth operation during a job.",
    "error:9"  : "G-code locked out during alarm or jog grbl_state",
    "error:10" : "Soft limits cannot be enabled without homing also enabled.",
    "error:11" : "Max characters per line exceeded. Line was not processed and executed.",
    "error:12" : "(Compile Option Grbl '$' setting value exceeds the maximum step rate supported.",
    "error:13" : "Safety door detected as opened and door grbl_state initiated.",
    "error:14" : "(Grbl-Mega Only Build info or startup line exceeded EEPROM line length limit.",
    "error:15" : "Jog target exceeds machine travel. Command ignored.",
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


Builder.load_string("""

<CheckingScreen>:
    
    quit_button:quit_button

    canvas:
        Color: 
            rgba: hex('#0d47a1')
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
            spacing: 10
             
            Label:
                size_hint_y: 1
                font_size: '40sp'
                text: root.job_checking_checked
                markup: True
 
            Label:
                text_size: self.size
                font_size: '15sp'
                halign: 'center'
                valign: 'center'
                text: root.checking_file_name
                
            Label:
                text_size: self.size
                font_size: '15sp'
                halign: 'center'
                valign: 'top'
                text: root.check_outcome
                
            BoxLayout:
                orientation: 'horizontal'
                padding: 10, 0
                spacing: 50
                                    
                Button:
                    id: quit_button
                    size_hint_y:0.9
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: True
                    background_color: hex('#0d47a1')
                    on_release: 
                        root.quit_to_home()

                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            font_size: '18sp'
                            text: 'Finish'
                            
        ScrollView:
            size_hint: 1.2, 1
            pos_hint: {'center_x': .5, 'center_y': .5}
            do_scroll_x: True
            do_scroll_y: True
            
            RstDocument:
                size_hint: 2, 5
                text: root.display_output
                background_color: hex('#0d47a1')

        
                            
""")

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

class CheckingScreen(Screen):
    
    check_value = NumericProperty()
    checking_file_name = StringProperty()
    job_checking_checked = StringProperty()
    check_outcome = StringProperty()
    display_output = StringProperty()
    job_ok = False
    
    def __init__(self, **kwargs):
        super(CheckingScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.job_gcode=kwargs['job']
        
    def on_enter(self):

        if self.m.is_connected():
            
            self.display_output = ''
            
            if self.m.state() == "Idle":
                self.job_checking_checked = '[b]Checking Job...[/b]'
                self.check_outcome = ' Looking for errors. Please wait, this can take a while.'
                
                # This clock gives kivy time to build the screen before the pi has to do any serious legwork
                Clock.schedule_once(self.get_error_log, 1.5)

            else: 
                self.job_checking_checked = '[b]Cannot Check Job[/b]' 
                self.check_outcome = 'Cannot check job: machine is not idle. Please ensure machine is in idle state before attempting to re-load the file.'
                self.job_gcode = []

            
        else:
            self.job_checking_checked = '[b]Cannot Check Job[/b]'
            self.check_outcome = 'Cannot check job: no serial connection. Please ensure your machine is connected, and re-load the file.'
            self.job_gcode = []
        
        self.quit_button.disabled = False
    
    def get_error_log(self, dt):
        error_log = self.check_grbl_stream(self.job_gcode)
        
        self.job_checking_checked = '[b]Job Checked[/b]'
        Clock.usleep(1)
        self.display_output = self.write_output(error_log)
        Clock.usleep(1)
        if self.job_ok == False:
            self.job_gcode = []


    def quit_to_home(self): 
        self.sm.get_screen('home').job_gcode = self.job_gcode
        self.sm.get_screen('home').job_filename = self.checking_file_name
        self.sm.current = 'home'
    
        
    def check_grbl_stream(self, objectifile):

        #utilise check_job from serial_conn
        error_log = self.m.s.check_job(objectifile)
        
        # There is a $C on each end of the objectifile; these two lines just strip of the associated 'ok's        
        del error_log[0]
        del error_log[(len(error_log)-1)]
        
        # If 'error' is found in the error log, tell the user
        if any('error' in listitem for listitem in error_log):
            self.check_outcome = 'Errors found in G-code. Please review your job before attempting to re-load it.'
            self.job_ok = False
        else:
            self.check_outcome = 'No errors found. You\'re good to go!'
            self.job_ok = True

        log('File has been checked!')
        return error_log
            

 
    def write_output(self, error_log):
        
        error_summary = []
        
        # Zip error log and GRBL commands together, and remove any lines with no gcode
        no_empties = list(filter(lambda x: x != ('ok', ''), zip(error_log, self.job_gcode)))

        # Read out which error codes flagged up, and put into an "error summary2 with descriptions
        for idx, f in enumerate(no_empties):
            if f[0].find('error') != -1:
                error_description = ERROR_CODES.get(f[0], "")
                error_summary.append('[color=#FFFFFF][b]Line ' + str(idx) + ':[/b][/color]')
                error_summary.append('[color=#FFFFFF]' + (f[0].replace(':',' ')).capitalize() + ': ' + error_description + '[/color]' +'\n\n')
                error_summary.append('[color=#FFFFFF]G-code: "' + f[1] + '"[/color]\n\n')
        
        # Put everything into a giant string for the ReStructed Text object        
        output = '[color=#FFFFFF][b]ERROR SUMMARY[/b][/color]\n\n' + \
        '\n\n'.join(map(str,error_summary)) + \
        '\n\n[color=#FFFFFF]---------------------------------------------------\n\n[color=#FFFFFF]' \
        '[b]GRBL RESPONSE LOG[/b][/color]\n\n' + \
        ('\n\n'.join('[color=#FFFFFF]' + str(idx).rjust(3,'\t') + \
        '\t\t [b]%s[/b]..........%s[/color]' % t for idx, t in enumerate(no_empties)))
        
        return output       
