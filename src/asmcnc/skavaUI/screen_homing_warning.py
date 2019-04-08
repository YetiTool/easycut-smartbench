'''
Created on 8 April 2019

Screen to tell user that machine has not been homed(before running a job). 

@author: Letty
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget

import sys, os
from kivy.utils import get_color_from_hex


# Kivy UI builder:
Builder.load_string("""

<WarningHoming>:

    getout_button:getout_button
    homing_button:homing_button

    canvas:
        Color: 
            rgba: hex('#fb8c00')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding: 60
        spacing: 30
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 1
            spacing: 30
             
            Label:
                size_hint_y: 0.8
                text_size: self.size
                font_size: '29sp'
                text: '[b]WARNING[/b]\\nSmartBench has not been homed yet.'
                markup: True
                halign: 'left'
                vallign: 'top'
 
            Label:
                size_hint_y: 0.6
                font_size: '22sp'
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                text: '\\nCannot start Job.'
                                
            Label:
                size_hint_y: 0.6
                font_size: '22sp'
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                text: root.user_instruction
                
            BoxLayout:
                orientation: 'horizontal'
                padding: 70, 0
                spacing: 70
 
                Button:
                    size_hint_y:0.5
                    size_hint_x: 3
                    id: homing_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: False
                    background_normal: ''
                    background_down: ''
                    background_color: hex('#e65100')
                    on_press:
                        root.home_SmartBench_press()
                    on_release:
                        root.home_SmartBench_release()
                        
                    BoxLayout:
                        padding: 20
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            font_size: '20sp'
                            text: 'Home SmartBench'
                            size: self.parent.size
                            pos: self.parent.pos
            
                Button:
                    size_hint_y: 0.5
                    size_hint_x: 3
                    id: getout_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: False
                    background_normal: ''
                    background_down: ''
                    background_color: hex('#e65100')
                    on_press:
                        root.return_press()
                    on_release:
                        root.return_release()
                        
                    BoxLayout:
                        padding: 20
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            font_size: '20sp'
                            text: 'Return to EasyCut'
                            size: self.parent.size
                            pos: self.parent.pos
                        
  
            
""")

class WarningHoming(Screen):

    # define error description to make kivy happy
    button_text = StringProperty()
    user_instruction = StringProperty()
    
    def __init__(self, **kwargs):
        super(WarningHoming, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']  

    def on_enter(self):
        self.user_instruction = 'Please home SmartBench before attempting to start a job.'
    
    def return_press(self):
        self.getout_button.background_color = get_color_from_hex('#c43c00')
        
    def home_SmartBench_press(self):
        self.homing_button.background_color = get_color_from_hex('#c43c00')
              
    def home_SmartBench_release(self):
        self.sm.current = 'homing'
    
    def return_release(self):
        self.sm.current = 'home' 
                      
