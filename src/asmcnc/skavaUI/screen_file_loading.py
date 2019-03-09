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
from __builtin__ import file
from kivy.clock import Clock


import sys, os
from os.path import expanduser
from shutil import copy
from datetime import datetime
import re

from asmcnc.comms import serial_connection
# from asmcnc.comms import usb_storage


# Kivy UI builder:
Builder.load_string("""

<LoadingScreen>:

    load_button:load_button


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
                font_size: '15sp'
                halign: 'center'
                valign: 'center'
                text: root.loading_file_name
                
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
                    id: load_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: False
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
                    id: load_button
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
        self.s = serial_connection.SerialConnection(self, self.sm)

        
    def on_enter(self):    
               
        self.job_loading_loaded = '[b]Loading Job...[/b]'
        self.load_value = 0
        
        # CAD file processing sequence
        self.job_gcode = []
        self.objectifile = self.objectifiled(self.loading_file_name)        # put file contents into a python object (objectifile)        
        self.job_loading_loaded = '[b]Job Loaded[/b]'
        
        # Take this out and moooooveee
        # self.check_grbl_stream(self.objectifile)
        self.load_value = 3
        
        self.job_gcode = self.objectifile    
        self.load_value = 4
     # Instead pass file back to home:
        # self.quit_to_home()

    def quit_to_home(self):
        self.sm.get_screen('home').job_gcode = self.job_gcode
        self.sm.current = 'home'
        
    def go_to_check_job(self):
        self.sm.get_screen('check_job').checking_file_name = self.loading_file_name
        self.sm.get_screen('check_job').job_gcode = self.objectifile
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
        return preloaded_job_gcode        # a.k.a. objectifile
    
# MOVED TO SCREEN_CHECK_JOB--------------------------------------------------------------    
#     def check_grbl_stream(self, objectifile):
# 
#         if self.m.is_connected():
#             error_log = self.m.s.check_job(objectifile)
#             
#             # There is a $C on each end of the objectifile; these two lines just strip of the associated 'ok's        
#             del error_log[0]
#             del error_log[(len(error_log)-1)]
#             
#             # If 'error' is found in the error log, show the error log on screen. 
#             if any('error' in listitem for listitem in error_log):
#                 print('ERROR FOUND IN G-CODE CHECK')
#     
#             # self.m.s.write_command('$C')
#             log('File has been checked!')
#             
#         else:
#             log('Cannot check file: no serial connection. Please ensure your machine is connected, and re-load the file.')

# NO LONGER REQUIRED -------------------------------------------------------------------------------------  
#     def clean_up_objectifile(self, objectifile):
#         
#         # write cleaned up GRBL to a new file
#         new_file = open(job_q_dir+'LoadedGCode.nc','w')
#         clean_objectifile = []
#         
#         for line in objectifile:
#         # stolen from serial -----------------------
# 
#             # Refine GCode
#             l_block = re.sub('\s|\(.*?\)', '', line.upper()) # Strip comments/spaces/new line and capitalize
#             print(line)
# 
#             if l_block.find('%') == -1 and l_block.find('M6') == -1:  # Drop undesirable lines
#                 new_file.write(l_block)
#                 clean_objectifile.append(l_block)
#          # ----------------------------------------
#         new_file.close()
#         return objectifile  
   
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
# 

#-----------------------------------------------------------------------------------
#         # Move over the preview image (??)
# #         if self.preview_image_path:
# #             if os.path.isfile(self.preview_image_path):
#                 
#                 # ... to Q
# #             copy(self.preview_image_path, job_q_dir) # "copy" overwrites same-name file at destination
#         
# #     def preview(self, objectifile):
# #         
# #         # can I pass the preview back to the screen_home preview widget? 
# #         log(' preview')
# #         pass
# 
# 
# # this might be necessary but I don't know what it does yet.
#     def load_gcode_list(self, filename, gcode_mgr_list):
#         
#         log ('> get_non_modal_gcode thread')
#         #time.sleep(2)
#         #for x in range(10000000):
#         #    x = x + 1
#             #if x % 10000 == 0:
#             #    sleep(0.0001)
#         #log ('counted')
# 
#         gcode_list = self.gcode_preview_widget.get_non_modal_gcode(self.job_q_dir + filename)
# 
#         for line in gcode_list:
#             gcode_mgr_list.append(line)
# 
#         log ('< get_non_modal_gcode thread ' + str(len(gcode_list)))
#         return gcode_list
#     
#     
# # OLD ----------------------------------
#     
#     def stream_file(self):
# 
#     #### Scan for files in Q, and update info panels
# 
#         files_in_q = os.listdir(self.job_q_dir)
#         filename = ''
#     
#         if files_in_q:
#     
#             # Search for nc file in Q dir and process
#             for filename in files_in_q:
#     
#                 if filename.split('.')[1].startswith(('nc','NC','gcode','GCODE')):
#     
#                     try:
#                         self.m.stream_file(self.job_q_dir + filename)
#                     except:
#                         print 'Fail: could not stream_file ' + str(self.job_q_dir + filename)
# ----------------------------------
        
# Questions: where does this object need to go? Where do we put it/keep it?
# A: At the moment we don't -> we just move the file and use that explicitly in jobQ I bet.

# Possible: 
#    - Global persistent object that is used instead.
#    - Write to new jobQ file that's all cleaned up and ready to go. << Gonna do this for now.


#--------------------------
                
#             ProgressBar:
#                 id: PB
#                 max: 5
#                 value: root.load_value
                
#             BoxLayout:
#                 orientation: 'horizontal'
#                 padding: 0, 0