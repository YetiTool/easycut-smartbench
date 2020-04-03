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

import sys, os
from os.path import expanduser
from shutil import copy
from datetime import datetime
from functools import partial
import re

Builder.load_string("""

<BoundaryWarningScreen>:
    
    quit_button:quit_button

    canvas:
        Color: 
            rgba: hex('#fb8c00')
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
                size_hint_y: 2
                font_size: '40sp'
                text: '[b]Job Outside Machine Limits[/b]'
                markup: True
                valign: 'top'
                halign: 'center'
                text_size: self.size
                
 
                
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
                    background_normal: ''
                    background_down: ''
                    background_color: hex('#e65100')
                    text: 'Return'
                    on_press: 
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
                size_hint: 1, 1
                pos_hint: {'center_x': .5, 'center_y': .5}
                do_scroll_x: True
                do_scroll_y: True
                scroll_type: ['content']
                
                RstDocument:
                    text: root.display_output
                    background_color: hex('#fb8c00')
                             
""")

class BoundaryWarningScreen(Screen):
    
    check_outcome = StringProperty()
    display_output = StringProperty()
    exit_label = StringProperty()

    entry_screen = StringProperty()
    job_box_details = []
    
#     gcode_has_been_checked_and_its_ok = False # actually put this in screen_home, and route everything back there. 
    
    def __init__(self, **kwargs):
        super(BoundaryWarningScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def on_enter(self):
        
        self.check_outcome = '[b]WARNING: Job is not within machine bounds![/b]' + \
        '\n\nPlease set datum appropriately, so that job boundaries are within SmartBench limits.'
        
        self.write_boundary_output()
        
    def write_boundary_output(self):
        self.display_output = '[color=#FFFFFF][b]DETAILS OF BOUNDARY CONFLICT[/b]\n\n' + \
        '\n\n'.join(map(str,self.job_box_details))
        
    def quit_to_home(self): 
        self.sm.current = 'home'
            
    def button_press(self):
        self.quit_button.background_color = get_color_from_hex('#c43c00')
        
    def on_leave(self):
        self.display_output = ''
        self.job_box_details = []

        