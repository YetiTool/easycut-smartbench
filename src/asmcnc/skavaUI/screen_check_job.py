# -*- coding: utf-8 -*-
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
    "error:6"  : "Minimum step pulse time must be greater than 3 microseconds.",
    "error:7"  : "EEPROM read failed. Reset and restored to default values.",
    "error:8"  : "Grbl '$' command cannot be used unless Grbl is IDLE. Ensures smooth operation during a job.",
    "error:9"  : "G-code locked out during alarm or jog state.",
    "error:10" : "Soft limits cannot be enabled without homing also enabled.",
    "error:11" : "Max characters per line exceeded. Line was not processed and executed.",
    "error:12" : "Compile Option Grbl '$' setting value exceeds the maximum step rate supported.",
    "error:13" : "Stop bar detected as pressed. Check all four contacts at the stop bar ends are not pressed. Pressing each switch a few times may clear the contact.",
    "error:14" : "Grbl-Mega Only Build info or startup line exceeded EEPROM line length limit.",
    "error:15" : "Have you homed the machine yet? If not, please do so now. Jog target exceeds machine travel. Command ignored.",
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
    filename_label:filename_label

    canvas:
        Color: 
            rgba: hex('#0d47a1')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding: 50
        spacing: 40

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
                id: filename_label
                size_hint_y: 1
                text_size: self.size
                font_size: '20sp'
                halign: 'center'
                valign: 'center'
                text: root.checking_file_name
                
            Label:
                size_hint_y: 3
                text_size: self.size
                font_size: '20sp'
                halign: 'center'
                valign: 'middle'
                text: root.check_outcome
                markup: True
                
            BoxLayout:
                orientation: 'horizontal'
                padding: 10, 0
                size_hint_y: 1
                                    
                Button:
                    id: quit_button
                    size_hint_y:0.8
                    size_hint_x: 0.6
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: False
                    background_color: hex('#0d47a1')
                    on_press: 
                        root.quit_to_home()

                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            font_size: '20sp'
                            text: root.exit_label
        
        BoxLayout:
            size_hint_x: 1
            orientation: 'vertical'
            spacing: 10
                            
            ScrollView:
                size_hint: 1, 1
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
                    on_press:
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
                    on_press:
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
    

    flag_min_feed_rate = False
    as_low_as = 100
    flag_max_feed_rate = False
    as_high_as = 5000

    flag_spindle_off = True

    serial_function_called = False
    
    def __init__(self, **kwargs):
        super(CheckingScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']
        self.job_gcode=kwargs['job']
        
        self.gcode_preview_widget = widget_gcode_view.GCodeView()
        
    def on_enter(self):
 
        self.job_checking_checked = self.l.get_str('Getting ready') + '...'  
        # display file selected in the filename display label
        if sys.platform == 'win32':
            self.filename_label.text = self.checking_file_name.split("\\")[-1]
        else:
            self.filename_label.text = self.checking_file_name.split("/")[-1]
        
        
        self.exit_label = self.l.get_str('Unload job')
        
        if self.entry_screen == 'file_loading':        
            try: self.boundary_check()
            except:
                self.toggle_boundary_buttons(True)
                self.job_checking_checked = self.l.get_str('Cannot Check Job')
                self.check_outcome = (
                    self.l.get_str('Cannot check job') + ': ' + \
                    self.l.get_str('Unable to run boundary check on file.') + ' ' + \
                    self.l.get_str('Please make sure file is in recognisable format.')
                    )
                self.job_gcode = []
        
        else:
            self.try_gcode_check()
    
    def try_gcode_check(self):
        try: self.check_gcode()
        except:
            self.toggle_boundary_buttons(True)
            self.job_checking_checked = self.l.get_str('Cannot Check Job')
            self.check_outcome = (
                self.l.get_str('Cannot check job') + ': ' + \
                self.l.get_str('Unable to run g-code check on file.') + ' ' + \
                self.l.get_str('Please make sure file is in recognisable format.')
                )
            self.job_gcode = []        

              
    def boundary_check(self):            
        
        # check limits
        bounds_output = self.is_job_within_bounds()
      
        if bounds_output == 'job is within bounds':
            log("In bounds...")
            # update screen
            self.check_outcome = self.l.get_str('Job is within bounds.')
            Clock.schedule_once(lambda dt: self.try_gcode_check(), 0.4)

        else:
            log("Out of bounds...")
            self.job_checking_checked = self.l.get_str('Boundary issue!')
            self.toggle_boundary_buttons(False)
            self.check_outcome = (
                self.l.get_bold('The job would exceed the working volume of the machine in one or more axes.') + \
                self.l.get_bold('See help notes (right).')
                )
            self.write_boundary_output(bounds_output)


## BOUNDARY CHECK:

    def is_job_within_bounds(self):

        errorfound = 0
        error_message = ''
        job_box = self.sm.get_screen('home').job_box
        
        # Mins
        
        if -(self.m.x_wco()+job_box.range_x[0]) >= (self.m.grbl_x_max_travel - self.m.limit_switch_safety_distance):
            # error_message = error_message + "\n\n\t[color=#FFCC00]The job extent over-reaches the X axis at the home end. Try positioning the machine's [b]X datum further away from home[/b].[/color]"
            error_message = error_message + ( "\n\n\t[color=#FFCC00]" + \
                self.l.get_str("The job extent over-reaches the N axis at the home end.").replace('N', 'X') + " " + \
                self.l.get_bold("Try positioning the machine's N datum further away from home.").replace('N', 'X') + \
                '[/color]'
                )
            errorfound += 1

        if -(self.m.y_wco()+job_box.range_y[0]) >= (self.m.grbl_y_max_travel - self.m.limit_switch_safety_distance):
            # error_message = error_message + "\n\n\t[color=#FFCC00]The job extent over-reaches the Y axis at the home end. Try positioning the machine's [b]Y datum further away from home[/b].[/color]"
            error_message = error_message + ( "\n\n\t[color=#FFCC00]" + \
                self.l.get_str("The job extent over-reaches the N axis at the home end.").replace('N', 'Y') + " " + \
                self.l.get_bold("Try positioning the machine's N datum further away from home.").replace('N', 'Y') + \
                '[/color]'
                )
            errorfound += 1 

        if -(self.m.z_wco()+job_box.range_z[0]) >= (self.m.grbl_z_max_travel - self.m.limit_switch_safety_distance):
            # error_message = error_message + "\n\n\t[color=#FFCC00]The job extent over-reaches the Z axis at the lower end. Try positioning the machine's [b]Z datum higher up[/b].[/color]"
            error_message = error_message + ( "\n\n\t[color=#FFCC00]" + \
                self.l.get_str("The job extent over-reaches the Z axis at the lower end.") + " " + \
                self.l.get_bold("Try positioning the machine's Z datum higher up.") + \
                '[/color]'
                )
            errorfound += 1 
            
        # Maxs

        if self.m.x_wco()+job_box.range_x[1] >= -self.m.limit_switch_safety_distance:
            # error_message = error_message + "\n\n\t[color=#FFCC00]The job extent over-reaches the X axis at the far end. Try positioning the machine's [b]X datum closer to home[/b].[/color]"
            error_message = error_message + ( "\n\n\t[color=#FFCC00]" + \
                self.l.get_str("The job extent over-reaches the N axis at the far end.").replace('N', 'X') + " " + \
                self.l.get_bold("Try positioning the machine's N datum closer to home.").replace('N', 'X') + \
                '[/color]'
                )
            errorfound += 1 
        if self.m.y_wco()+job_box.range_y[1] >= -self.m.limit_switch_safety_distance:
            # error_message = error_message + "\n\n\t[color=#FFCC00]The job extent over-reaches the Y axis at the far end. Try positioning the machine's [b]Y datum closer to home[/b].[/color]"
            error_message = error_message + ( "\n\n\t[color=#FFCC00]" + \
                self.l.get_str("The job extent over-reaches the N axis at the far end.").replace('N', 'Y') + " " + \
                self.l.get_bold("Try positioning the machine's N datum closer to home.").replace('N', 'Y') + \
                '[/color]'
                )
            errorfound += 1 
        if self.m.z_wco()+job_box.range_z[1] >= -self.m.limit_switch_safety_distance:
            # error_message = error_message + "\n\n\t[color=#FFCC00]The job extent over-reaches the Z axis at the upper end. Try positioning the machine's [b]Z datum lower down[/b].[/color]"
            error_message = error_message + ( "\n\n\t[color=#FFCC00]" + \
                self.l.get_str("The job extent over-reaches the Z axis at the upper end.") + " " + \
                self.l.get_bold("Try positioning the machine's Z datum lower down.") + \
                '[/color]'
                )
            errorfound += 1 

        if errorfound > 0: return error_message
        else: return 'job is within bounds'  
  
    def write_boundary_output(self, bounds_output):
        
        self.display_output = (
            '[color=#FFFFFF]' + self.l.get_bold('BOUNDARY CONFLICT HELP') + '\n\n[/color]' + \
            '[color=#FFFFFF]' + self.l.get_str('It looks like your job exceeds the bounds of the machine') + ':\n\n[/color]' + \
            '[color=#FFCC00]' + bounds_output + '\n\n[/color]' + \
            '[color=#FFFFFF]' + \
            self.l.get_str("The job datum is set in the wrong place.") + " " + \
            self.l.get_str("Press Adjust datums and then reposition the X, Y or Z datums as suggested above so that the job box is within the machine's boundaries.").replace(self.l.get_str('Adjust datums'), self.l.get_bold('Adjust datums')) + " " + \
            self.l.get_str('Use the manual move controls and set datum buttons to achieve this.').replace(self.l.get_str('set datum'), self.l.get_bold('set datum')) + " " + \
            self.l.get_str('You should then reload the job and re-run this check.') + \
            '\n\n[/color]' + '[color=#FFFFFF]' + \
            self.l.get_str('If you have already tried to reposition the datum, but cannot get the job to fit within the machine bounds, your job may simply be set up incorrectly in your CAD/CAM software.') + " " + \
            self.l.get_str('Common causes include setting the CAD/CAM job datum far away from the actual design, or exporting the job from the CAM software in the wrong units.') + " " + \
            self.l.get_str('Check your design and export settings.') + " " + \
            self.l.get_str('You should then reload the job and re-run the check.') + '\n\n[/color]' + \
            '[color=#FFFFFF]' + \
            self.l.get_str('Finally, if you have already tried to reposition the datum, or if the graphics on the job previews do not look normal, your G-code may be corrupt.') + " " + \
            self.l.get_str('If this is the case, you many want to press Check G-code.').replace(self.l.get_str('Check G-code'), self.l.get_bold('Check G-code')) + " " + \
            self.l.get_bold("WARNING") + "[b]:[/b] " + self.l.get_bold("Checking the job's G-code when it is outside of the machine bounds may trigger an alarm screen.") + '\n\n[/color]'
            )

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
            self.check_gcode_label.text = self.l.get_str('Check G-code')
            self.check_gcode_button.disabled = False
            self.check_gcode_button.opacity = 1
            self.check_gcode_button.size_hint_y = 1
            self.check_gcode_button.size_hint_x = 1
            self.check_gcode_button.height = '0dp'
            self.check_gcode_button.width = '0dp'
    
            
            self.load_file_now_label.text = self.l.get_str('Adjust datums')
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
                self.job_checking_checked = self.l.get_str('Starting Check') + '...'
                self.check_outcome = self.l.get_str('Looking for gcode errors') + '...'
                
                # This clock gives kivy time to sort out the screen before the pi has to do any serious legwork
                Clock.schedule_once(partial(self.check_grbl_stream, self.job_gcode), 0.1)

            else: 
                self.job_checking_checked = self.l.get_str('Cannot check job')
                self.check_outcome = self.l.get_str('Cannot check job') + ': ' + self.l.get_str('machine is not idle.') + ' ' + self.l.get_str('Please ensure machine is in idle state before attempting to reload the file.')
                self.job_gcode = []
            
        else:
            self.job_checking_checked = self.l.get_str('Cannot check job')
            self.check_outcome = self.l.get_str('Cannot check job') + ': ' + self.l.get_str('no serial connection.') + ' ' + self.l.get_str('Please ensure your machine is connected, and reload the file.')
            self.job_gcode = []

    loop_for_job_progress = None
     
    def check_grbl_stream(self, objectifile, dt):

        # because this is called by a clock function,
        # so put this check in just in case the user exits the screen prior to this
        if self.sm.current == 'check_job':

            self.serial_function_called = True

            # utilise check_job from serial_conn
            self.m.s.check_job(objectifile)

            # self.poll_for_gcode_check_progress(0)
            self.loop_for_job_progress = Clock.schedule_interval(self.poll_for_gcode_check_progress, 0.6)
            
            # display the error log when it's filled - setting up the event makes it easy to unschedule
            self.error_out_event = Clock.schedule_interval(partial(self.get_error_log),0.1)


    def poll_for_gcode_check_progress(self, dt):

        percent_thru_job = int(round((self.m.s.g_count * 1.0 / (len(self.job_gcode) + 4) * 1.0)*100.0))
        if percent_thru_job > 100: percent_thru_job = 100
        self.job_checking_checked = self.l.get_str("Checking job") +  ": " + str(percent_thru_job) + "  %"

    
    def get_error_log(self, dt):  
    
        if self.error_log != []:
            Clock.unschedule(self.error_out_event)
            if self.loop_for_job_progress != None: self.loop_for_job_progress.cancel()
            
            # If 'error' is found in the error log, tell the user
            if any('error' in listitem for listitem in self.error_log):

                self.job_checking_checked = self.l.get_str('Errors found!')
                if self.entry_screen == 'file_loading':
                    self.check_outcome = self.l.get_str('Errors found in G-code.') + '\n\n' + self.l.get_str('Please review your job before attempting to reload it.')
                elif self.entry_screen == 'home':
                    self.check_outcome = self.l.get_str('Errors found in G-code.') + '\n\n' + self.l.get_str('Please review and reload your job before attempting to run it.')
                self.job_ok = False

            elif self.flag_min_feed_rate or self.flag_max_feed_rate or self.flag_spindle_off:
                self.job_checking_checked = self.l.get_str('Advisories')
                self.check_outcome = self.l.get_str('This file will run, but it might not run in the way you expect.') + '\n\n' + \
                                    self.l.get_str('Please review your job before running it.')
                self.job_ok = True
                
                # add job checked already flag here
                self.sm.get_screen('home').gcode_has_been_checked_and_its_ok = True

            else:
                self.job_checking_checked = self.l.get_str('File is OK!')
                self.check_outcome =  self.l.get_str("No errors found. You're good to go!")
                self.job_ok = True
                
                # add job checked already flag here
                self.sm.get_screen('home').gcode_has_been_checked_and_its_ok = True
    
            self.write_error_output(self.error_log)
            
            if self.job_ok == False:
                self.job_gcode = []
    
            log('File has been checked!')
            self.exit_label = self.l.get_str('Finish')


    def write_error_output(self, error_log):

        self.display_output = ''

        ## SPINDLE WARNING:

        if self.flag_spindle_off:
            self.display_output = self.display_output + '[color=#FFFFFF]' + self.l.get_bold('SPINDLE WARNING') + '[/color]\n\n'
            self.display_output = self.display_output + '[color=#FFFFFF]' + self.l.get_str('This file has no command to turn the spindle on.') + '[/color]\n\n' + \
                                '[color=#FFFFFF]' + \
                                self.l.get_str('This may be intended behaviour, but if you are trying to do a cut you should review your file before trying to run it!') + \
                                '[/color]\n\n'


        ## FEED/SPEED MIN/MAXES HERE: 

        if self.flag_max_feed_rate or self.flag_min_feed_rate:
            self.display_output = self.display_output + '[color=#FFFFFF]' + self.l.get_bold('FEED RATE WARNING') + '[/color]\n\n'

            if self.flag_min_feed_rate: 
                self.display_output = self.display_output + (
                    '[color=#FFFFFF]' + \
                    self.l.get_str('This file contains feed rate commands as low as N00 mm/min.').replace('N00', str(self.as_low_as)) + \
                    '[/color]\n\n' + \
                    '[color=#FFFFFF]' + \
                    self.l.get_str('The recommended minimum feed rate is 100 mm/min.') + \
                    '[/color]\n\n'
                )

            if self.flag_max_feed_rate:
                self.display_output = self.display_output + (
                    '[color=#FFFFFF]' + \
                    self.l.get_str('This file contains feed rate commands as high as N00 mm/min.').replace('N00', str(self.as_high_as)) + \
                    '[/color]\n\n' + \
                    '[color=#FFFFFF]' + \
                    self.l.get_str('The recommended maximum feed rate is 5000 mm/min.') + \
                    '[/color]\n\n'
                )
        
        error_summary = []
        
        # Zip error log and GRBL commands together, and remove any lines with no gcode
        no_empties = list(filter(lambda x: x != ('ok', ''), zip(error_log, self.job_gcode)))

        # Read out which error codes flagged up, and put into an "error summary" with descriptions
        for idx, f in enumerate(no_empties):
            if f[0].find('error') != -1:
                error_description = self.l.get_str(ERROR_CODES.get(f[0], ""))
                error_summary.append('[color=#FFFFFF]' + self.l.get_bold('Line') + '[b] ' + str(idx) + ':[/b][/color]')
                error_summary.append(
                    '[color=#FFFFFF]' + \
                    ((f[0].replace(':',' ')).replace('error', self.l.get_str('error'))).capitalize() + \
                    ': ' + error_description + '[/color]' +'\n\n'
                    )
                error_summary.append('[color=#FFFFFF]G-code: "' + f[1] + '"[/color]\n\n')
        
        if error_summary == []:
            self.display_output = self.display_output + ''
        else:
            # Put everything into a giant string for the ReStructed Text object        
            self.display_output = self.display_output + '[color=#FFFFFF]' + self.l.get_bold('ERROR SUMMARY') + '[/color]\n\n' + \
            '\n\n'.join(map(str,error_summary))
        
#        # If want to print all the lines of the file and oks:
#         + \
#         '\n\n[color=#FFFFFF]---------------------------------------------------\n\n[color=#FFFFFF]' \
#         '[b]GRBL RESPONSE LOG[/b][/color]\n\n' + \
#         ('\n\n'.join('[color=#FFFFFF]' + str(idx).rjust(3,'\t') + \
#         '\t\t [b]%s[/b]..........%s[/color]' % t for idx, t in enumerate(no_empties)))


## EXITING SCREEN

    def stop_check_in_serial(self, pass_no):

        check_again = False
        pass_no += 1

        if self.m.s.check_streaming_started:
            if self.m.s.is_job_streaming: self.m.s.cancel_stream()
            else: check_again = True

        elif (pass_no > 2) and (self.m.state() == "Check") and (not check_again): self.m.disable_check_mode()

        if check_again or (pass_no < 3): Clock.schedule_once(lambda dt: self.stop_check_in_serial(pass_no), 1)

    def quit_to_home(self): 
        
        if self.job_ok:
            self.sm.get_screen('home').job_gcode = self.job_gcode
            self.sm.get_screen('home').job_filename = self.checking_file_name
            self.sm.get_screen('home').z_datum_reminder_flag = True
            self.sm.current = 'home'

        else:            
            self.sm.current = 'home'

            
    def load_file_now(self):
        self.sm.get_screen('home').job_gcode = self.job_gcode
        self.sm.get_screen('home').job_filename = self.checking_file_name
        self.sm.get_screen('home').z_datum_reminder_flag = True
        self.sm.current = 'home'       
    
    def on_leave(self, *args):
        if self.serial_function_called: 
            self.stop_check_in_serial(0)
            self.serial_function_called = False
        if self.error_out_event != None: Clock.unschedule(self.error_out_event)
        self.job_gcode = []
        self.checking_file_name = ''
        self.job_checking_checked = ''
        self.check_outcome = ''
        self.display_output = ''
        self.job_ok = False
        self.flag_min_feed_rate = False
        self.as_low_as = 100
        self.flag_max_feed_rate = False
        self.as_high_as = 5000
        self.flag_spindle_off = True
        self.error_log = []
        if self.loop_for_job_progress != None: self.loop_for_job_progress.cancel()


