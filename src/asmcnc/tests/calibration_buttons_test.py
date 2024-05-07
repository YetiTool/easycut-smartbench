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
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty 
from kivy.uix.widget import Widget
from kivy.uix.progressbar import ProgressBar

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
            font_size: app.get_scaled_sp('60sp')
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
        
        Button:
            text: "UPLOAD Z CALS"
            on_press: root.FAKE_UPLOAD_TEST()
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

    def FAKE_UPLOAD_TEST(self):

        # need to pull in data from somewhere

        ## FAKE DATA TO TEST WITH:
        coeffs = [509, 509, 509, 509, 509, 509, 509, 509, 509, 509, 509, 509, 509, 509, 509, 509, 509, 509, 509, 508, 508, 508, 508, 508, 508, 508, 508, 507, 505, 506, 504, 506, 504, 504, 504, 505, 504, 505, 504, 503, 502, 501, 501, 502, 502, 501, 501, 500, 499, 498, 500, 499, 496, 497, 496, 496, 494, 494, 492, 492, 491, 489, 489, 490, 490, 485, 487, 484, 484, 484, 487, 487, 485, 486, 484, 484, 483, 481, 480, 479, 481, 478, 476, 477, 475, 474, 473, 470, 471, 469, 465, 465, 461, 453, 439, 440, 450, 464, 460, 459, 457, 458, 456, 452, 452, 450, 448, 448, 444, 444, 443, 440, 438, 436, 435, 432, 431, 431, 428, 428, 426, 427, 422, 421, 421, 418, 418, 416]
        params = [31, 8, 6, 5200]

        self.m.TMC_motor[4].calibration_dataset_SG_values = coeffs
        self.m.TMC_motor[4].calibrated_at_current_setting = params[0]
        self.m.TMC_motor[4].calibrated_at_sgt_setting = params[1]
        self.m.TMC_motor[4].calibrated_at_toff_setting = params[2]
        self.m.TMC_motor[4].calibrated_at_temperature = params[3]

        time.sleep(0.5)

        self.m.upload_Z_calibration_settings_from_motor_class()



        