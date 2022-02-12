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


Builder.load_string("""

<TestScreen>:
    
    # canvas:
    #     Color: 
    #         rgba: hex('#E5E5E5FF')
    #     Rectangle: 
    #         size: self.size
    #         pos: self.pos
                
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
    

""")


class TestScreen(Screen):  

    default_font_size = '30sp'

    test_label = 'TEST' 
    
    def __init__(self, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']