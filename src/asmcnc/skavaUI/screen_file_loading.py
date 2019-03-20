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


import sys, os
from os.path import expanduser
from shutil import copy
from datetime import datetime
import re

from asmcnc.skavaUI import screen_check_job

# from asmcnc.comms import usb_storage


# Kivy UI builder:
Builder.load_string("""

<LoadingScreen>:

    check_button:check_button
    home_button:home_button


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
                text: root.job_loading_loaded
                markup: True
 
            Label:
                text_size: self.size
                font_size: '16sp'
                halign: 'center'
                valign: 'bottom'
                text: root.loading_file_name
                
            Label:
                text_size: self.size
                font_size: '22sp'
                halign: 'center'
                valign: 'bottom'
                text: 'WARNING:'
                
            Label:
                text_size: self.size
                font_size: '20sp'
                halign: 'center'
                valign: 'top'
                text: 'We recommend error-checking your job before it goes to the machine.\\nWould you like us to check your job now?'
            
            BoxLayout:
                orientation: 'horizontal'
                padding: 10, 0
                spacing: 50
            
                Button:
                    size_hint_y:0.9
                    id: check_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: True
                    background_color: hex('#0d47a1')
                    on_release: 
                        root.go_to_check_job()
                        
                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            font_size: '18sp'
                            text: 'Yes please, check my job for errors'
                        
                Button:
                    size_hint_y:0.9
                    id: home_button
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
                            text: 'No thanks, quit to home'
                            
""")

job_cache_dir = './jobCache/'    # where job files are cached for selection (for last used history/easy access)
job_q_dir = './jobQ/'            # where file is copied if to be used next in job

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

class LoadingScreen(Screen):  
 
    load_value = NumericProperty()
    loading_file_name = StringProperty()
    job_loading_loaded = StringProperty()
    objectifile = None
    
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.job_gcode=kwargs['job']
        
    def on_enter(self):    
               
        self.job_loading_loaded = '[b]Loading Job...[/b]'
        self.load_value = 0
        
        # CAD file processing sequence
        self.job_gcode = []
        self.job_gcode = self.objectifiled(self.loading_file_name)        # put file contents into a python object (objectifile)        
        self.job_loading_loaded = '[b]Job Loaded[/b]'
        self.home_button.disabled = False
        self.check_button.disabled = False
    
    def quit_to_home(self):
        self.sm.get_screen('home').job_gcode = self.job_gcode
        self.sm.get_screen('home').job_filename = self.loading_file_name
        self.sm.current = 'home'
        
    def go_to_check_job(self):
               
        self.sm.get_screen('check_job').checking_file_name = self.loading_file_name
        self.sm.get_screen('check_job').job_gcode = self.job_gcode
        self.sm.get_screen('home').job_gcode = []
        self.sm.current = 'check_job'
        
    def objectifiled(self, job_file_path):

        log('> load_job_file')
        
        preloaded_job_gcode = []

        job_file = open(job_file_path, 'r')     # open file and copy each line into the object
        self.load_value = 1
        # clean up code as it's copied into the object
        for line in job_file:
            # Strip comments/spaces/new line and capitalize:
            l_block = re.sub('\s|\(.*?\)', '', (line.strip()).upper())  
            
            if l_block.find('%') == -1 and l_block.find('M6') == -1:    # Drop undesirable lines
                preloaded_job_gcode.append(l_block)  #append cleaned up gcode to object
                
        job_file.close()
        self.load_value = 2

        log('< load_job_file')
        return preloaded_job_gcode
   
# THIS MIGHT STILL BE USEFUL FOR WRITING UP ERROR LOG: 
#     def write_file_to_JobQ(self, objectifile):
#         
#         files_in_q = os.listdir(job_q_dir) # clean Q
#         if files_in_q:
#             for file in files_in_q:
#                 os.remove(job_q_dir+file)
# 
#         # write cleaned up g-code to new file
#         new_file = open(job_q_dir+'LoadedGCode.nc','w')
#         for line in objectifile:
#             new_file.write(line)
#             new_file.write('\n')
#         new_file.close()

