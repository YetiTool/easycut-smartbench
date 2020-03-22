'''
Created on 25 Feb 2019

@author: Letty

This screen checks the users job, and allows them to review any errors 
'''

import kivy
import docutils
import time
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from __builtin__ import file
from kivy.clock import Clock

from asmcnc.geometry import job_envelope
from asmcnc.skavaUI import widget_gcode_view


import sys, os
from os.path import expanduser
from shutil import copy
from datetime import datetime
from functools import partial
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
    load_file_now_button:load_file_now_button
    load_file_now_label:load_file_now_label
    check_gcode_button:check_gcode_button
    check_gcode_label:check_gcode_label

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
                valign: 'top'
 
            Label:
                text_size: self.size
                font_size: '15sp'
                halign: 'center'
                valign: 'center'
                text: root.checking_file_name
                
            Label:
                size_hint_y: 1.7
                text_size: self.size
                font_size: '15sp'
                halign: 'center'
                valign: 'top'
                text: root.check_outcome
                markup: True
                
            BoxLayout:
                orientation: 'horizontal'
                padding: 10, 0
                #spacing: 50
                                    
                Button:
                    id: quit_button
                    size_hint_y:0.8
                    size_hint_x: 0.6
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: False
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
                            text: root.exit_label
        
        BoxLayout:
            orientation: 'vertical'
                            
            ScrollView:
                size_hint: 1.2, 1
                pos_hint: {'center_x': .5, 'center_y': .5}
                do_scroll_x: True
                do_scroll_y: True
                scroll_type: ['content']
                
                RstDocument:
                    text: root.display_output
                    background_color: hex('#0d47a1')

            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: 0.15
                spacing: 20
                
                Button:
                    id: load_file_now_button
                    background_color: hex('#0d47a1')
                    on_release:
                        root.load_file_now()
                   
                    Label:
                        id: load_file_now_label
                        text: ''
                        markup: True
                        #text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                    
                Button:
                    id: check_gcode_button
                    background_color: hex('#0d47a1')
                    on_release:
                        root.check_gcode()
                    
                    Label:
                        id: check_gcode_label
                        text: ''
                        markup: True
                        #text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                             
""")

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

class CheckingScreen(Screen):
    
    checking_file_name = StringProperty()
    job_checking_checked = StringProperty()
    check_outcome = StringProperty()
    display_output = StringProperty()
    exit_label = StringProperty()
    entry_screen = StringProperty()
    
    job_ok = False
    error_log = []
    error_out_event = None
    
    job_box = job_envelope.BoundingBox()
    
#     gcode_has_been_checked_and_its_ok = False # actually put this in screen_home, and route everything back there. 
    
    def __init__(self, **kwargs):
        super(CheckingScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.job_gcode=kwargs['job']
        
        self.gcode_preview_widget = widget_gcode_view.GCodeView()
        
    def on_enter(self):
 
        self.job_checking_checked = '[b]Checking Job...[/b]'  
        self.exit_label = 'Cancel'
        
        if self.entry_screen == 'file_loading':        
            try: self.boundary_check()
            except:
                self.toggle_boundary_buttons(True)
                self.job_checking_checked = '[b]Cannot Check Job[/b]' 
                self.check_outcome = 'Cannot check job: unable to run boundary check on file. Please make sure file is in recognisable format.'
                self.job_gcode = []
        
        else:
            self.try_gcode_check()
    
    def try_gcode_check(self):
        try: self.check_gcode()
        except:
            self.toggle_boundary_buttons(True)
            self.job_checking_checked = '[b]Cannot Check Job[/b]' 
            self.check_outcome = 'Cannot check job: unable to run g-code check on file. Please make sure file is in recognisable format.'
            self.job_gcode = []        

              
    def boundary_check(self):            
        
        # check limits
        bounds_output = self.is_job_within_bounds()
        
        if bounds_output == True:
            # update screen
            self.check_outcome = 'Job is within bounds.'
            Clock.schedule_once(lambda dt: self.try_gcode_check(), 0.4)
            # auto check g-code? Yeah, why not.

        else:
            self.toggle_boundary_buttons(False)
            self.check_outcome = 'WARNING: Job is not within machine bounds!' + \
            '\n\nWARNING: Checking the job\'s G-code when it is outside of the machine bounds may trigger an alarm state.'
            self.write_boundary_output(bounds_output)


## BOUNDARY CHECK:

    def is_job_within_bounds(self):

        errorfound = 0
        error_message = ''
        job_box = self.sm.get_screen('home').job_box
        
        # Mins
        
        if -(self.m.x_wco()+job_box.range_x[0]) >= (self.m.grbl_x_max_travel - self.m.limit_switch_safety_distance):
            error_message = error_message + "\n\n\t[color=#FFFFFF]The job target is too close to the X home position. The job will crash into the home position."
            errorfound += 1 
        if -(self.m.y_wco()+job_box.range_y[0]) >= (self.m.grbl_y_max_travel - self.m.limit_switch_safety_distance):
            error_message = error_message + "\n\n\t[color=#FFFFFF]The job target is too close to the Y home position. The job will crash into the home position."
            errorfound += 1 
        if -(self.m.z_wco()+job_box.range_z[0]) >= (self.m.grbl_z_max_travel - self.m.limit_switch_safety_distance):
            error_message = error_message + "\n\n\t[color=#FFFFFF]The job target is too far from the Z home position. The router will not reach that far."
            errorfound += 1 
            
        # Maxs

        if self.m.x_wco()+job_box.range_x[1] >= -self.m.limit_switch_safety_distance:
            error_message = error_message + "\n\n\t[color=#FFFFFF]The job target is too far from the X home position. The router will not reach that far."
            errorfound += 1 
        if self.m.y_wco()+job_box.range_y[1] >= -self.m.limit_switch_safety_distance:
            error_message = error_message + "\n\n\t[color=#FFFFFF]The job target is too far from the Y home position. The router will not reach that far."
            errorfound += 1 
        if self.m.z_wco()+job_box.range_z[1] >= -self.m.limit_switch_safety_distance:
            error_message = error_message + "\n\n\t[color=#FFFFFF]The job target is too close to the Z home position. The job will crash into the home position."
            errorfound += 1 

        if errorfound > 0: return error_message
        else: return True  
  
    def write_boundary_output(self, bounds_output):
        
        self.display_output = '[color=#FFFFFF][b]BOUNDARY CONFLICT[/b]\n\n' + \
        '\n\n[color=#FFFFFF]It looks like your job is outside the bounds of the machine:' + \
        '[color=#FFFFFF]' + bounds_output + '\n\n' + \
        '[color=#FFFFFF]\n\n[color=#FFFFFF]To fix this, load the job now and set the datum to an appropriate location.\n\n' + \
        '[color=#FFFFFF]You will still be prompted to check your G-code before running your job.\n\n' + \
        '[color=#FFFFFF]If you have already tried to set the datum, or if the graphics on the virtual' + \
        '[color=#FFFFFF] machine don\'t look right, your G-code may be corrupt.\n\n' + \
        '[color=#FFFFFF]If this is the case, please check your G-code now. \n\n'

    def toggle_boundary_buttons(self, hide_boundary_buttons):
        
        if hide_boundary_buttons:
            self.check_gcode_label.text = ''
            self.check_gcode_button.disabled = True
            self.check_gcode_button.opacity = 0
            self.check_gcode_button.size_hint_y = None
            self.check_gcode_button.size_hint_x = None 
            self.check_gcode_button.height = '0dp'
            self.check_gcode_button.width = '0dp'
    
            
            self.load_file_now_label.text = ''
            self.load_file_now_button.disabled = True
            self.load_file_now_button.opacity = 0
            self.load_file_now_button.size_hint_y = None 
            self.load_file_now_button.size_hint_x = None       
            self.load_file_now_button.height = '0dp' 
            self.load_file_now_button.width = '0dp'
            
        else:
            self.check_gcode_label.text = 'Check G-code'
            self.check_gcode_button.disabled = False
            self.check_gcode_button.opacity = 1
            self.check_gcode_button.size_hint_y = 1
            self.check_gcode_button.size_hint_x = 1
            self.check_gcode_button.height = '0dp'
            self.check_gcode_button.width = '0dp'
    
            
            self.load_file_now_label.text = 'Load job now'
            self.load_file_now_button.disabled = False
            self.load_file_now_button.opacity = 1
            self.load_file_now_button.size_hint_y = 1 
            self.load_file_now_button.size_hint_x = 1       
            self.load_file_now_button.height = '0dp' 
            self.load_file_now_button.width = '0dp'            


## GRBL CHECK:     

    def check_gcode(self):
        
        self.toggle_boundary_buttons(True)
        
        if self.m.is_connected():
            
            self.display_output = ''
            
            if self.m.state() == "Idle":
                self.job_checking_checked = '[b]Checking Job...[/b]'
                self.check_outcome = ' Looking for errors. Please wait, this can take a while.'
                
                # This clock gives kivy time to sort out the screen before the pi has to do any serious legwork
                Clock.schedule_once(partial(self.check_grbl_stream, self.job_gcode), 0.1)

            else: 
                self.job_checking_checked = '[b]Cannot Check G-Code[/b]' 
                self.check_outcome = 'Cannot check job: machine is not idle. Please ensure machine is in idle state before attempting to re-load the file.'
                self.job_gcode = []
                # self.quit_button.disabled = False

            
        else:
            self.job_checking_checked = '[b]Cannot Check G-Code[/b]'
            self.check_outcome = 'Cannot check job: no serial connection. Please ensure your machine is connected, and re-load the file.'
            self.job_gcode = []
            # self.quit_button.disabled = False
 
     
    def check_grbl_stream(self, objectifile, dt):

        #utilise check_job from serial_conn
        self.m.s.check_job(objectifile)
        
        # display the error log when it's filled - setting up the event makes it easy to unschedule
        self.error_out_event = Clock.schedule_interval(partial(self.get_error_log),0.1)
    
    def get_error_log(self, dt):  
    
        if self.error_log != []:
            Clock.unschedule(self.error_out_event)

            # There is a $C on each end of the job object; these two lines just strip of the associated 'ok's        
#             del self.error_log[0]
#             del self.error_log[(len(self.error_log)-1)]
            
            # If 'error' is found in the error log, tell the user
            if any('error' in listitem for listitem in self.error_log):
                
                if self.entry_screen == 'file_loading':
                    self.check_outcome = 'Errors found in G-code. Please review your job before attempting to re-load it.'
                elif self.entry_screen == 'home':
                    self.check_outcome = 'Errors found in G-code. Please review and re-load your job before attempting to run it.'
                self.job_ok = False
            else:
                self.check_outcome =  'No errors found. You\'re good to go!'
                self.job_ok = True
                
                # add job checked already flag here
                self.sm.get_screen('home').gcode_has_been_checked_and_its_ok = True
    
            self.job_checking_checked = '[b]Job Checked[/b]'
            self.write_error_output(self.error_log)
            
            if self.job_ok == False:
                self.job_gcode = []
    
            log('File has been checked!')
            self.exit_label = 'Finish'
            # self.quit_button.disabled = False


    def write_error_output(self, error_log):
        
        error_summary = []
        
        # Zip error log and GRBL commands together, and remove any lines with no gcode
        no_empties = list(filter(lambda x: x != ('ok', ''), zip(error_log, self.job_gcode)))

        # Read out which error codes flagged up, and put into an "error summary" with descriptions
        for idx, f in enumerate(no_empties):
            if f[0].find('error') != -1:
                error_description = ERROR_CODES.get(f[0], "")
                error_summary.append('[color=#FFFFFF][b]Line ' + str(idx) + ':[/b][/color]')
                error_summary.append('[color=#FFFFFF]' + (f[0].replace(':',' ')).capitalize() + ': ' + error_description + '[/color]' +'\n\n')
                error_summary.append('[color=#FFFFFF]G-code: "' + f[1] + '"[/color]\n\n')
        
        if error_summary == []:
            error_summary.append('[color=#FFFFFF]There\'s nothing here. Excellent.[/color]')
        
        # Put everything into a giant string for the ReStructed Text object        
        self.display_output = '[color=#FFFFFF][b]ERROR SUMMARY[/b][/color]\n\n' + \
        '\n\n'.join(map(str,error_summary))
        
#        # If want to print all the lines of the file and oks:
#         + \
#         '\n\n[color=#FFFFFF]---------------------------------------------------\n\n[color=#FFFFFF]' \
#         '[b]GRBL RESPONSE LOG[/b][/color]\n\n' + \
#         ('\n\n'.join('[color=#FFFFFF]' + str(idx).rjust(3,'\t') + \
#         '\t\t [b]%s[/b]..........%s[/color]' % t for idx, t in enumerate(no_empties)))


## EXITING SCREEN

    def quit_to_home(self): 
        
        if self.entry_screen == 'file_loading':
        
            if self.job_ok:
                self.sm.get_screen('home').job_gcode = self.job_gcode
                self.sm.get_screen('home').job_filename = self.checking_file_name
                self.sm.current = 'home'
                
            else:         
                if self.m.s.is_job_streaming:
                    self.m.s.cancel_stream()
                                        
                self.sm.current = 'home'
                
        elif self.entry_screen == 'home':
            
            if self.job_ok:
                self.sm.current = 'go'
                
            else:
                self.sm.current = 'home'
            
    def load_file_now(self):
        self.sm.get_screen('home').job_gcode = self.job_gcode
        self.sm.get_screen('home').job_filename = self.checking_file_name
        self.sm.current = 'home'       
    
    def on_leave(self, *args):
        # self.quit_button.disabled = True
        if self.error_out_event != None: 
            Clock.unschedule(self.error_out_event)
        self.job_gcode = []
        self.checking_file_name = ''
        self.job_checking_checked = ''
        self.check_outcome = ''
        self.display_output = ''
        self.job_ok = False
        self.error_log = []
        if self.m.s.is_job_streaming:
            self.m.s.cancel_stream()
