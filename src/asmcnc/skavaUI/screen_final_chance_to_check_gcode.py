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


import sys, os
from datetime import datetime
import re

from asmcnc.skavaUI import screen_check_job

# from asmcnc.comms import usb_storage


# Kivy UI builder:
Builder.load_string("""

<AskToCheckBeforeGo>:

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
                spacing: 10
            
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
                        root.proceed_to_go()

                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            font_size: '18sp'
                            text: 'No thanks, lets go'
                            
""")

job_cache_dir = './jobCache/'    # where job files are cached for selection (for last used history/easy access)
job_q_dir = './jobQ/'            # where file is copied if to be used next in job

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

class AskToCheckBeforeGo(Screen):  
    
    def __init__(self, **kwargs):
        super(AskToCheckBeforeGo, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.job_gcode=kwargs['job']
        
    def on_enter(self):    
        pass    

    def proceed_to_go(self):
        self.sm.current = 'go'
        
    def go_to_check_job(self):
        self.sm.get_screen('check_job').checking_file_name = self.loading_file_name
        self.sm.get_screen('check_job').job_gcode = self.job_gcode
        self.sm.get_screen('check_job').entry_screen = 'file_loading'
        self.sm.get_screen('home').job_gcode = []
        self.sm.current = 'check_job'