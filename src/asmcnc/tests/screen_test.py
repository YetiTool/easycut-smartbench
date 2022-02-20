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

from asmcnc.comms.yeti_grbl_protocol.c_defines import *


import sys, os, time
from datetime import datetime
import re


Builder.load_string("""

<TestScreen>:

    BoxLayout:
        orientation: 'vertical'
                    
        Label:
            id: warning_body_label
            font_size: '60sp'
            halign: 'center'
            valign: 'bottom'
            size_hint_y: 1
            markup: True
            valign: 'center'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            text: root.test_label

        BoxLayout: 
            orientation: 'horizontal'

            Button:
                text: "Tune X and Z"
                on_press: root.tune_X_Z()
                size_hint_y: 1

            Button:
                text: "Cal X and Z"
                on_press: root.cal_X_Z()
                size_hint_y: 1
        
        BoxLayout: 
            orientation: 'horizontal'

            Button:
                text: "Tune Y"
                on_press: root.tune_Y()
                size_hint_y: 1

            Button:
                text: "Cal Y"
                on_press: root.cal_Y()
                size_hint_y: 1
        


""")


class TestScreen(Screen):  

    default_font_size = '30sp'

    test_label = 'TEST' 
    
    def __init__(self, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']


    def tune_X_Z(self):
        self.m.tune_X_and_Z_for_calibration()

    def cal_X_Z(self):
        self.m.calibrate_X_and_Z()

    def tune_Y(self):
        self.m.tune_Y_for_calibration()

    def cal_Y(self):
        self.m.calibrate_Y()



        