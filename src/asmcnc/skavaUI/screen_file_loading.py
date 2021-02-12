# -*- coding: utf-8 -*-
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
from kivy.graphics import Color, Rectangle


import sys, os, time
from datetime import datetime
import re

from asmcnc.skavaUI import screen_check_job, widget_gcode_view, popup_info
from asmcnc.geometry import job_envelope

Builder.load_string("""

<LoadingScreen>:

    check_button:check_button
    home_button:home_button
    filename_label:filename_label
    warning_title_label:warning_title_label
    warning_body_label:warning_body_label
    usb_status_label:usb_status_label
    
    canvas:
        Color: 
            rgba: hex('#E5E5E5FF')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'vertical'
        padding: 0
        spacing: 0
        size_hint_x: 1

        Label:
            id: usb_status_label
            canvas.before:
                Color:
                    rgba: hex('#333333FF')
                Rectangle:
                    size: self.size
                    pos: self.pos
            size_hint_y: 0.7
            markup: True
            font_size: '18sp'   
            valign: 'middle'
            halign: 'left'
            text_size: self.size
            padding: [10, 0]

        BoxLayout: 
            spacing: 0
            padding: 20
            orientation: 'vertical'
            size_hint_y: 7.81
             
            Label:
                id: header_label
                size_hint_y: 1
                markup: True
                valign: 'center'
                halign: 'center'
                size: self.texture_size
                text_size: self.size
                color: hex('#333333ff')
                font_size: '40sp'
                text: root.progress_value          

            Label:
                id: filename_label
                font_size: '20sp'
                halign: 'center'
                valign: 'bottom'
                size_hint_y: 0.5
                markup: True
                valign: 'top'
                halign: 'center'
                size: self.texture_size
                text_size: self.size
                color: hex('#333333ff')
                text: 'Filename here'
                
            Label:
                id: warning_title_label
                font_size: '24sp'
                halign: 'center'
                valign: 'bottom'
                size_hint_y: 0.5
                markup: True
                valign: 'center'
                halign: 'center'
                size: self.texture_size
                text_size: self.size
                color: hex('#333333ff')
                text: "[b]WARNING![/b]"
                
            Label:
                id: warning_body_label
                font_size: '20sp'
                halign: 'center'
                valign: 'bottom'
                size_hint_y: 1.4
                markup: True
                valign: 'center'
                halign: 'center'
                size: self.texture_size
                text_size: self.size
                color: hex('#333333ff')

            BoxLayout:
                orientation: 'horizontal'
                padding: [20,0,20,0]
                spacing: 60
                size_hint_y: 2.6
            
                # Button:
                #     size_hint_y:0.9
                #     id: check_button
                #     size: self.texture_size
                #     valign: 'top'
                #     halign: 'center'
                #     disabled: True
                #     background_color: hex('#0d47a1')
                #     on_press: 
                #         root.go_to_check_job()
                        
                #     BoxLayout:
                #         padding: 5
                #         size: self.parent.size
                #         pos: self.parent.pos
                        
                #         Label:
                #             id: check_button_label
                #             #size_hint_y: 1
                #             font_size: '18sp'
                #             text: ''

                Button:
                    id: home_button
                    size_hint_x: 1
                    valign: "middle"
                    halign: "center"
                    markup: True
                    font_size: root.default_font_size
                    text_size: self.size
                    background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    background_disabled_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    border: [dp(30)]*4
                    padding: [40, 40]
                    on_press: root.quit_to_home()

                Button:
                    id: check_button
                    size_hint_x: 1
                    on_press: root.go_to_check_job()
                    valign: "middle"
                    halign: "center"
                    markup: True
                    font_size: root.default_font_size
                    text_size: self.size
                    background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    background_disabled_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    border: [dp(30)]*4
                    padding: [40, 40]

                        
                # Button:
                #     size_hint_y:0.9
                #     id: home_button
                #     size: self.texture_size
                #     valign: 'top'
                #     halign: 'center'
                #     disabled: True
                #     background_color: hex('#0d47a1')
                #     on_press: 
                #         root.quit_to_home()

                #     BoxLayout:
                #         padding: 5
                #         size: self.parent.size
                #         pos: self.parent.pos
                        
                #         Label:
                #             id: quit_button_label
                #             #size_hint_y: 1
                #             font_size: '18sp'
                #             text: ''



                            
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
    maximum_spindle_rpm = 25000

    # Feed rate flag parameters
    minimum_feed_rate = 100
    maximum_feed_rate = 5000

    usb_status = None

    default_font_size = '30sp'
    
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']
        self.job_gcode=kwargs['job']

    def on_enter(self):    

        # display file selected in the filename display label
        if sys.platform == 'win32':
            self.filename_label.text = self.loading_file_name.split("\\")[-1]
        else:
            self.filename_label.text = self.loading_file_name.split("/")[-1]

        self.update_usb_status()
        self.sm.get_screen('home').gcode_has_been_checked_and_its_ok = False
        self.load_value = 0
        self.update_screen('Getting ready')

        # CAD file processing sequence
        self.job_gcode = []
        self.sm.get_screen('home').job_gcode = []
        Clock.schedule_once(partial(self.objectifiled, self.loading_file_name),0.1)

    def update_usb_status(self):
        if self.usb_status == 'connected':
            self.usb_status_label.text = self.l.get_str("USB connected: Please do not remove USB until file is loaded.")
            self.usb_status_label.canvas.before.clear()
            with self.usb_status_label.canvas.before:
                Color(76 / 255., 175 / 255., 80 / 255., 1.)
                Rectangle(pos=self.usb_status_label.pos,size=self.usb_status_label.size)
        elif self.usb_status == 'ejecting':
            self.usb_status_label.text = self.l.get_str("Ejecting USB: please wait") + "..."
            self.usb_status_label.opacity = 1
            self.usb_status_label.canvas.before.clear()
            with self.usb_status_label.canvas.before:
                Color(51 / 255., 51 / 255., 51 / 255. , 1.)
                Rectangle(pos=self.usb_status_label.pos,size=self.usb_status_label.size)
        elif self.usb_status == 'ejected':
            self.usb_status_label.text = self.l.get_str("Safe to remove USB.")
            with self.usb_status_label.canvas.before:
                Color(76 / 255., 175 / 255., 80 / 255., 1.)
                Rectangle(pos=self.usb_status_label.pos,size=self.usb_status_label.size)
        else: 
            self.usb_status_label.opacity = 0

    def quit_to_home(self):
        self.sm.get_screen('home').job_gcode = self.job_gcode
        self.sm.get_screen('home').job_filename = self.loading_file_name
        self.sm.get_screen('home').z_datum_reminder_flag = True
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
            file_empty_warning = (self.l.get_str('File is empty!') + '\n\n' + \
            self.l.get_str('Please load a different file.'))

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
                    and l_block.find('M30') == -1 and l_block.find('M2') == -1 and l_block.find('M02') == -1):    # Drop undesirable lines
                    
                    # enforce minimum spindle speed (e.g. M3 S1000: M3 turns spindle on, S1000 sets rpm to 1000. Note incoming string may be inverted: S1000 M3)
                    if l_block.find ('M3') >= 0 or l_block.find ('M03') >= 0:
                        self.sm.get_screen('check_job').flag_spindle_off = False

                        if l_block.find ('S') >= 0:
                            
                            # find 'S' prefix and strip out the value associated with it
                            rpm = int(l_block[l_block.find("S")+1:].split("M")[0])


                            # If the bench has a 110V spindle, need to convert to "instructed" values into equivalent for 230V spindle, 
                            # in order for the electronics to send the right voltage for the desired RPM
                            if self.m.spindle_voltage == 110:
                                # if not self.m.spindle_digital or not self.m.fw_can_operate_digital_spindle(): # this is only relevant much later on
                                rpm = self.m.convert_from_110_to_230(rpm)
                                l_block = "M3S" + str(rpm)

                            # Ensure all rpms are above the minimum (assuming a 230V spindle)
                            if rpm < self.minimum_spindle_rpm:
                                l_block = "M3S" + str(self.minimum_spindle_rpm)

                            if rpm > self.maximum_spindle_rpm: 
                                l_block = "M3S" + str(self.maximum_spindle_rpm)


                    elif l_block.find('S0'):
                        l_block = l_block.replace('S0','')

    
                    if l_block.find ('F') >= 0:

                        try: 

                            feed_rate = re.match('\d+',l_block[l_block.find("F")+1:]).group()

                            if float(feed_rate) < self.minimum_feed_rate:
                                
                                self.sm.get_screen('check_job').flag_min_feed_rate = True

                                if float(feed_rate) < self.sm.get_screen('check_job').as_low_as:
                                    self.sm.get_screen('check_job').as_low_as = float(feed_rate)


                            if float(feed_rate) > self.maximum_feed_rate:

                                self.sm.get_screen('check_job').flag_max_feed_rate = True

                                if float(feed_rate) > self.sm.get_screen('check_job').as_high_as:
                                    self.sm.get_screen('check_job').as_high_as = float(feed_rate)

                        except: print 'Failed to extract feed rate. Probable G-code error!'


                    self.preloaded_job_gcode.append(l_block)  #append cleaned up gcode to object
            
                self.lines_scrubbed += 1

            # take a breather and update progress report
            self.line_threshold_to_pause_and_update_at += self.interrupt_line_threshold
            percentage_progress = int((self.lines_scrubbed * 1.0 / self.total_lines_in_job_file_pre_scrubbed * 1.0) * 100.0)
            self.update_screen('Preparing', percentage_progress)
            Clock.schedule_once(self._scrub_file_loop, self.interrupt_delay)

        else: 

            log('> Finished scrubbing ' + str(self.lines_scrubbed) + ' lines.')
            self.job_gcode = self.preloaded_job_gcode
            self._get_gcode_preview_and_ranges()


    def _get_gcode_preview_and_ranges(self):

        self.load_value = 2
        self.sm.get_screen('home').job_gcode = self.job_gcode
        
        # This has to be the same widget that the home screen uses, otherwise
        # preview does not work
        self.gcode_preview_widget = self.sm.get_screen('home').gcode_preview_widget
    
        log('> get_non_modal_gcode')
        self.gcode_preview_widget.prep_for_non_modal_gcode(self.job_gcode, False, self.sm, 0)


    def update_screen(self, stage, percentage_progress=0):

        if stage == 'Getting ready':
            self.check_button.disabled = True
            self.home_button.disabled = True
            self.progress_value = self.l.get_str('Getting ready') + '...'
            self.warning_title_label.text = ''
            self.warning_body_label.text = ''
            self.check_button.text = ''
            self.home_button.text = ''

        if stage == 'Preparing':
            self.progress_value = self.l.get_str('Preparing file') + ': ' + str(percentage_progress) + ' %'

        if stage == 'Analysing':
            self.progress_value = self.l.get_str('Analysing file') + ': ' + str(percentage_progress) + ' %'

        if stage == 'Loaded':
            self.progress_value = self.l.get_bold('Job loaded')
            self.warning_title_label.text = self.l.get_bold('WARNING') + '[b]:[/b]'
            self.warning_body_label.text = (
                self.l.get_str('We strongly recommend error-checking your job before it goes to the machine.') + \
                "\n" + \
                self.l.get_str('Would you like SmartBench to check your job now?')
                )
            self.check_button.text = self.l.get_str('Yes, check my job for errors')
            self.home_button.text = self.l.get_str('No, quit to home')
            
            self.check_button.disabled = False
            self.home_button.disabled = False


    def _finish_loading(self, non_modal_gcode_list): # called by gcode preview widget


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
        
        self.update_screen('Loaded')

        log('> END LOAD')
        



