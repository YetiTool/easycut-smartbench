'''
Created on 8 April 2019

Screen to tell user that machine is not Idle (before running a job). 

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

<WarningMState>:

    getout_button:getout_button

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
            spacing: 20
             
            Label:
                size_hint_y: 0.8
                text_size: self.size
                font_size: '29sp'
                text: '[b]WARNING[/b]\\nSmartBench is not in an idle state.'
                markup: True
                halign: 'left'
                vallign: 'top'
 
            Label:
                size_hint_y: 1.2
                text_size: self.size
                font_size: '22sp'
                halign: 'left'
                valign: 'middle'
                text: 'Cannot start job.'
                
            Label:
                size_hint_y: 0.6
                font_size: '22sp'
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                text: root.user_instruction
                
            BoxLayout:
                orientation: 'horizontal'
                padding: 130, 0
            
                Button:
                    size_hint_y:0.9
                    id: getout_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: False
                    background_normal: ''
                    background_down: ''
                    background_color: hex('#e65100')
                    on_press:
                        root.button_press()
                    on_release:
                        root.button_release()
                        
                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            font_size: '20sp'
                            text: 'Return to EasyCut'
                        
  
            
""")

class WarningMState(Screen):

    # define error description to make kivy happy
    button_text = StringProperty()
    user_instruction = StringProperty()
    
    def __init__(self, **kwargs):
        super(WarningMState, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']  

    def on_enter(self):
        
        if self.m.state().startswith('Alarm'):
            self.user_instruction = 'SmartBench is in an Alarm state. Please clear the machine, and then reset and unlock it.'
        
        elif self.m.state().startswith('Check'):
            self.user_instruction = 'SmartBench is in Check state. Please disable by typing \'$C\' into the G-code console.'
            
        elif self.m.state().startswith('Door') or self.m.state().startswith('Hold'):
            self.user_instruction = 'SmartBench is paused. Please resume by typing \'$~\' into the G-code console.'
            
        else:
            self.user_instruction = 'SmartBench is still carrying out a command. Please wait for SmartBench to finish' + \
            ' before attempting to start a job.'
            
    
    def button_press(self):
        self.getout_button.background_color = get_color_from_hex('#c43c00')
              
    
    def button_release(self):
        self.sm.current = 'home' 
                      

        
 