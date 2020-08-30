'''
Created on 25 Feb 2019

@author: Letty

This screen does three things: 
- Reads a file from filechooser into an object passed throughout easycut.
- Prevents the user from clicking on things while a file is loading or being checked. 
- Asks the user to check their file before sending it to the machine
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.uix.progressbar import ProgressBar
from __builtin__ import file, False
from kivy.clock import Clock
from functools import partial


import sys, os, time
from datetime import datetime
import re

from asmcnc.skavaUI import screen_check_job, widget_gcode_view, popup_info
from asmcnc.geometry import job_envelope

# from asmcnc.comms import usb_storage


# Kivy UI builder:
Builder.load_string("""

<LoadingScreen>:

    check_button:check_button
    home_button:home_button
    filename_label:filename_label
    warning_title_label:warning_title_label
    warning_body_label:warning_body_label
    quit_button_label:quit_button_label
    check_button_label:check_button_label
    
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
                text: root.progress_value
                markup: True             

            Label:
                id: filename_label
                text_size: self.size
                font_size: '20sp'
                halign: 'center'
                valign: 'bottom'
                text: 'Filename here'
                
            Label:
                id: warning_title_label
                text_size: self.size
                font_size: '20sp'
                halign: 'center'
                valign: 'bottom'
                text: ''
                
            Label:
                id: warning_body_label
                text_size: self.size
                font_size: '20sp'
                halign: 'center'
                valign: 'top'
                text: ''
            
            BoxLayout:
                orientation: 'horizontal'
                padding: 10, 0
                spacing: 10
            
                Button:
                    size_hint_y:0.9
                    id: check_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: True
                    background_color: hex('#0d47a1')
                    on_press: 
                        root.go_to_check_job()
                        
                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            id: check_button_label
                            #size_hint_y: 1
                            font_size: '18sp'
                            text: ''
                        
                Button:
                    size_hint_y:0.9
                    id: home_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: True
                    background_color: hex('#0d47a1')
                    on_press: 
                        root.quit_to_home()

                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            id: quit_button_label
                            #size_hint_y: 1
                            font_size: '18sp'
                            text: ''



                            
""")


job_cache_dir = './jobCache/'    # where job files are cached for selection (for last used history/easy access)
job_q_dir = './jobQ/'            # where file is copied if to be used next in job


def log(message):
    
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)


class LoadingScreen(Screen):  
 
    load_value = NumericProperty()
    loading_file_name = StringProperty()
    progress_value = StringProperty()
    objectifile = None

    # scrubbing parameters        
    minimum_spindle_rpm = 3500
    
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.job_gcode=kwargs['job']

        if self.m.spindle_voltage == 110:
            self.minimum_spindle_rpm = 10000
        
    def on_enter(self):    

        # display file selected in the filename display label
        if sys.platform == 'win32':
            self.filename_label.text = self.loading_file_name.split("\\")[-1]
        else:
            self.filename_label.text = self.loading_file_name.split("/")[-1]

        self.sm.get_screen('home').gcode_has_been_checked_and_its_ok = False

        self.load_value = 0

        self.check_button.disabled = True
        self.home_button.disabled = True
        self.progress_value = 'Getting ready...'
        self.warning_title_label.text = ''
        self.warning_body_label.text = ''
        self.check_button_label.text = ''
        self.quit_button_label.text = ''


#         Clock.usleep(1)
        # CAD file processing sequence
        self.job_gcode = []
        self.sm.get_screen('home').job_gcode = []
        Clock.schedule_once(partial(self.objectifiled, self.loading_file_name),0.1)        
    
    def quit_to_home(self):
        self.sm.get_screen('home').job_gcode = self.job_gcode
        self.sm.get_screen('home').job_filename = self.loading_file_name
        self.sm.current = 'home'
        
    def return_to_filechooser(self):
        self.job_gcode = []
        self.sm.current = 'local_filechooser'
        
    def go_to_check_job(self):
               
        self.sm.get_screen('check_job').checking_file_name = self.loading_file_name
        self.sm.get_screen('check_job').job_gcode = self.job_gcode
        self.sm.get_screen('check_job').entry_screen = 'file_loading'
        self.sm.get_screen('home').job_gcode = []
        self.sm.current = 'check_job'
        
    def objectifiled(self, job_file_path, dt):

        log('> LOADING:')

        with open(job_file_path) as f:
            self.job_file_as_list = f.readlines()

        if len(self.job_file_as_list) == 0:
            file_empty_warning = 'File is empty!\n\nPlease load a different file.'
            popup_info.PopupError(self.sm, file_empty_warning)
            self.sm.current = 'local_filechooser'
            return

        self.total_lines_in_job_file_pre_scrubbed = len(self.job_file_as_list)
        
        self.load_value = 1
        log('> Job file loaded as list... ' + str(self.total_lines_in_job_file_pre_scrubbed) + ' lines')
        log('> Scrubbing file...')

        # clear objects
        self.preloaded_job_gcode = []
        self.lines_scrubbed = 0
        self.line_threshold_to_pause_and_update_at = self.interrupt_line_threshold

        Clock.schedule_once(self._scrub_file_loop, 0)


    interrupt_line_threshold = 10000
    interrupt_delay = 0.1

    def _scrub_file_loop(self, dt):

        # clear out undesirable lines

        # a lot of this wrapper code is to force a break in the loops so we can allow Kivy to update
        if self.lines_scrubbed < self.total_lines_in_job_file_pre_scrubbed:
            
            break_threshold = min(self.line_threshold_to_pause_and_update_at, self.total_lines_in_job_file_pre_scrubbed)

            # main scrubbing loop
            while self.lines_scrubbed < break_threshold:
                
                line = self.job_file_as_list[self.lines_scrubbed]
    
                # Strip comments/spaces/new line and capitalize:
                l_block = re.sub('\s|\(.*?\)', '', (line.strip()).upper())  
                
                if (l_block.find('%') == -1 and l_block.find('M6') == -1 and l_block.find('M06') == -1 and l_block.find('G28') == -1
                    and l_block.find('M30') == -1 and l_block.find('M2') == -1):    # Drop undesirable lines
                    
                    # enforce minimum spindle speed (e.g. M3 S1000: M3 turns spindle on, S1000 sets rpm to 1000. Note incoming string may be inverted: S1000 M3)
                    if l_block.find ('M3') >= 0 or l_block.find ('M03') >= 0:
                        if l_block.find ('S') >= 0:
                            
                            # find 'S' prefix and strip out the value associated with it
                            rpm = int(l_block[l_block.find("S")+1:].split("M")[0])
                            if rpm < self.minimum_spindle_rpm:
                                l_block = "M3S" + str(self.minimum_spindle_rpm)


                            # If the bench has a 110V spindle, need to convert to "instructed" values into equivalent for 230V spindle, 
                            # in order for the electronics to send the right voltage for the desired RPM

                            if self.m.spindle_voltage == 110:
                                # if not self.m.spindle_digital or not self.m.fw_can_operate_digital_spindle(): # this is only relevant much later on
                                rpm_red = self.m.convert_from_110_to_230(rpm)
                                l_block = "M3S" + str(rpm_red)


                    elif l_block.find('S0'):
                        l_block = l_block.replace('S0','')

    
                    self.preloaded_job_gcode.append(l_block)  #append cleaned up gcode to object
            
                self.lines_scrubbed += 1

            # take a breather and update progress report
            self.line_threshold_to_pause_and_update_at += self.interrupt_line_threshold
            percentage_progress = int((self.lines_scrubbed * 1.0 / self.total_lines_in_job_file_pre_scrubbed * 1.0) * 100.0)
            self.progress_value = 'Preparing file: ' + str(percentage_progress) + ' %' # update progress label
            Clock.schedule_once(self._scrub_file_loop, self.interrupt_delay)

        else: 

            log('> Finished scrubbing ' + str(self.lines_scrubbed) + ' lines.')
            self._get_gcode_preview_and_ranges()


    def _get_gcode_preview_and_ranges(self):

        self.job_gcode = self.preloaded_job_gcode
        self.load_value = 2
        self.sm.get_screen('home').job_gcode = self.job_gcode
        
        # This has to be the same widget that the home screen uses, otherwise
        # preview does not work
        self.gcode_preview_widget = self.sm.get_screen('home').gcode_preview_widget
    
        log('> get_non_modal_gcode')
        self.gcode_preview_widget.prep_for_non_modal_gcode(self.job_gcode, False, self.sm, 0)


    def _finish_loading(self, non_modal_gcode_list):


        job_box = job_envelope.BoundingBox()

        # Get bounding box
        job_box.range_x[0] = self.gcode_preview_widget.min_x
        job_box.range_x[1] = self.gcode_preview_widget.max_x
        job_box.range_y[0] = self.gcode_preview_widget.min_y
        job_box.range_y[1] = self.gcode_preview_widget.max_y
        job_box.range_z[0] = self.gcode_preview_widget.min_z
        job_box.range_z[1] = self.gcode_preview_widget.max_z
        
        self.sm.get_screen('home').job_box = job_box

        # non_modal_gcode also used for file preview in home screen
        self.sm.get_screen('home').non_modal_gcode_list = non_modal_gcode_list
        
        self.progress_value = '[b]Job loaded[/b]'
        self.warning_title_label.text = 'WARNING:'
        self.warning_body_label.text = 'We strongly recommend error-checking your job before it goes to the machine. Would you like SmartBench to check your job now?'
        self.check_button_label.text = 'Yes please, check my job for errors'
        self.quit_button_label.text = 'No thanks, quit to home'
        
        self.check_button.disabled = False
        self.home_button.disabled = False

        log('> END LOAD')
        



