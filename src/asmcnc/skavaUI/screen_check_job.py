'''
Created on 25 Feb 2019

@author: Letty

This screen checks the users job, and allows them to review any errors 
'''

import kivy
import docutils
import pandas as pd
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from __builtin__ import file
from kivy.clock import Clock


import sys, os
from os.path import expanduser
from shutil import copy
from datetime import datetime
import re

from asmcnc.comms import serial_connection

Builder.load_string("""

<CheckingScreen>:

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
                text: root.job_checking_checked
                markup: True
 
            Label:
                text_size: self.size
                font_size: '15sp'
                halign: 'center'
                valign: 'center'
                text: root.checking_file_name
                
            ProgressBar:
                id: PB
                max: 5
                value: 5 
                # root.check_value
                
            Label:
                text_size: self.size
                font_size: '17sp'
                halign: 'center'
                valign: 'top'
                text: root.check_outcome
                
            BoxLayout:
                orientation: 'horizontal'
                padding: 10, 0
                spacing: 50
            
#                 Button:
#                     size_hint_y:0.9
#                     id: load_button
#                     size: self.texture_size
#                     valign: 'top'
#                     halign: 'center'
#                     disabled: False
#                     background_color: hex('#0d47a1')
# #                    on_release: 
#                         #root.load_file()
#                         
#                     BoxLayout:
#                         padding: 5
#                         size: self.parent.size
#                         pos: self.parent.pos
#                         
#                         Label:
#                             #size_hint_y: 1
#                             font_size: '18sp'
#                             text: 'Dummy button, ignore me for now :)'
                        
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
                            text: 'Finish'
                            
        ScrollView:
            size_hint: 0.8, 1
#            size: 500, 320
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
        self.s = serial_connection.SerialConnection(self, self.sm)
        
        # Scrollable widget showing line : ok/error status
        # self.error_log_container.addWidget()
        
    def on_enter(self):
        self.job_checking_checked = '[b]Checking Job...[/b]'
        self.check_outcome = ' Looking for errors'
        error_log = self.check_grbl_stream(self.job_gcode)
        self.write_output(error_log)
        if self.job_ok == False:
            self.job_gcode = []
        self.job_checking_checked = '[b]Job Checked[/b]'
    
    def quit_to_home(self): 
        self.sm.get_screen('home').job_gcode = self.job_gcode
        self.sm.current = 'home'
    
        
    def check_grbl_stream(self, objectifile):
        if self.m.is_connected():
            error_log = self.m.s.check_job(objectifile)
            
            # There is a $C on each end of the objectifile; these two lines just strip of the associated 'ok's        
            del error_log[0]
            del error_log[(len(error_log)-1)]
            
            # If 'error' is found in the error log, show the error log on screen. 
            if any('error' in listitem for listitem in error_log):
                self.check_outcome = 'Errors found in G-code. Please review your job before attempting to re-load it.'
                job_ok = False
            else:
                self.check_outcome = 'No errors found. You\'re good to go!'
                self.job_ok = True
    
            # self.m.s.write_command('$C')
            log('File has been checked!')
            
            return error_log
            
        else:
            self.check_outcome = 'Cannot check file: no serial connection. Please ensure your machine is connected, and re-load the file.'

 
    def write_output(self, error_log):   
        self.display_output = '\n\n'.join('[color=#FFFFFF][b]%s[/b]..........\t%s[/color]' % t for t in zip(error_log, self.job_gcode))
        
#         tablist = ['\n']*len(error_log)
#     
#         maxlen = len(max(self.job_gcode, key=len))
#         padded_gcode = [line.ljust(maxlen,'.') for line in self.job_gcode]
#         
# #         if  maxlen < 22:
# #             padded_gcode = [line.ljust(maxlen,'.') for line in self.job_gcode]
# #             
# #         else: 
# #             maxlen = 20
# #             padded_gcode = [line.ljust(maxlen,'\t') for line in self.job_gcode]
#         
#         # df = (pd.DataFrame(zip(self.job_gcode, error_log, tablist), columns = ['','','']))
#         # self.display_output = str(df.to_string())
        
