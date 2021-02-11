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

<LoadingScreenTest>:
    
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
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')
                font_size: '40sp'
                # text: root.progress_value
                text: 'Job loaded'

            Label:
                id: filename_label
                font_size: '20sp'
                halign: 'center'
                valign: 'bottom'
                text: 'Filename here'
                size_hint_y: 0.5
                markup: True
                valign: 'top'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')

            Label:
                id: warning_title_label
                font_size: '24sp'
                halign: 'center'
                valign: 'bottom'
                size_hint_y: 0.5
                markup: True
                valign: 'center'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')
                text: "[b]WARNING![/b]"
                
            Label:
                id: warning_body_label
                font_size: '20sp'
                halign: 'center'
                valign: 'bottom'
                size_hint_y: 1
                markup: True
                valign: 'center'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')
                text: root.test_label
            
            BoxLayout:
                orientation: 'horizontal'
                padding: [20,0,20,0]
                spacing: 40
                size_hint_y: 3

                # Button:
                #     size_hint_y:0.9
                #     id: check_button
                #     size: self.texture_size
                #     valign: 'top'
                #     halign: 'center'
                #     disabled: True
                #     background_color: hex('#0d47a1')
                #     on_press: 
                        
                        
                #     BoxLayout:
                #         padding: 5
                #         size: self.parent.size
                #         pos: self.parent.pos
                        
                #         Label:
                #             id: check_button_label
                #             #size_hint_y: 1
                #             font_size: '18sp'
                #             text: ''
                        
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

                        
                Button:
                    id: home_button
                    size_hint_x: 1
                    # on_press: root.quit_to_home()()
                    valign: "middle"
                    halign: "center"
                    markup: True
                    font_size: root.default_font_size
                    text_size: self.size
                    background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    border: [dp(30)]*4
                    padding: [40, 40]
                    text: 'Nein, aufhören zu Hause'

                # BoxLayout:
                #     size_hint_x: 0.3
                            
                # Button:
                #     size_hint_x: 0.3
                #     background_color: hex('#FFFFFF00')
                #     on_press: root.popup_help()
                #     BoxLayout:
                #         size: self.parent.size
                #         pos: self.parent.pos
                #         Image:
                #             source: "./asmcnc/skavaUI/img/help_btn_orange_round.png"
                #             size: self.parent.width, self.parent.height
                #             allow_stretch: True 

                Button:
                    id: check_button
                    size_hint_x: 1
                    # on_press: root.go_to_check_job()
                    valign: "middle"
                    halign: "center"
                    markup: True
                    font_size: root.default_font_size
                    text_size: self.size
                    background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                    border: [dp(30)]*4
                    padding: [40, 40]
                    text: 'Ja, überprüfen Sie meine Arbeit für Fehler'
""")



        # Label:
        #     id: header_label
        #     size_hint_y: 3
        #     markup: True
        #     font_size: '30px' 
        #     valign: 'center'
        #     halign: 'center'
        #     size:self.texture_size
        #     text_size: self.size
        #     color: hex('#333333ff')
    
        # BoxLayout:
        #     orientation: 'horizontal'
        #     padding: [20,0,20,0]
        #     spacing: 40
        #     size_hint_y: 3

        #     Button:
        #         id: no_button
        #         size_hint_x: 1
        #         on_press: root.decision_no()
        #         valign: "middle"
        #         halign: "center"
        #         markup: True
        #         font_size: root.default_font_size
        #         text_size: self.size
        #         background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
        #         background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
        #         border: [dp(30)]*4
        #         padding: [20, 20]
                        
        #     Button:
        #         size_hint_x: 0.3
        #         background_color: hex('#FFFFFF00')
        #         on_press: root.popup_help()
        #         BoxLayout:
        #             size: self.parent.size
        #             pos: self.parent.pos
        #             Image:
        #                 source: "./asmcnc/skavaUI/img/help_btn_orange_round.png"
        #                 size: self.parent.width, self.parent.height
        #                 allow_stretch: True 
                        
        #     Button:
        #         id: yes_button
        #         size_hint_x: 1
        #         on_press: root.decision_yes()
        #         valign: "middle"
        #         halign: "center"
        #         markup: True
        #         font_size: root.default_font_size
        #         text_size: self.size
        #         background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
        #         background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
        #         border: [dp(30)]*4
        #         padding: [20, 20]
                        
        # Label:
        #     size_hint_y: .5    

class LoadingScreenTest(Screen):  

    default_font_size = '30sp'

    test_label = 'We strongly recommend error-checking your job before it goes to the machine.' + "\n" + 'Would you like SmartBench to check your job now?' 
    
    def __init__(self, **kwargs):
        super(LoadingScreenTest, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']