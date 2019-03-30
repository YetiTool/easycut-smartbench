'''
Created on 30 March 2019

Screen to give a safety warning to the user when they switch on SmartBench.

@author: Letty
'''
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.clock import Clock

import sys, os


# Kivy UI builder:
Builder.load_string("""

<SafetyScreen>:

    canvas:
        Color: 
            rgba: hex('#FFFFFF')
        Rectangle: 
            size: self.size
            pos: self.pos
            
    BoxLayout:
        orientation: 'horizontal'
        padding: 50
        size_hint_x: 1
        size: self.parent.size
        pos: self.parent.pos
        
        BoxLayout:
            orientation: 'vertical'
            spacing: 5
            # size_hint_x: 2
            size: self.parent.size
            pos: self.parent.pos
        
            Label:
                size_hint_y: 0.2
                text: '[color=000000]Safety Warning![/color]'
                markup: True
                font_size: '40sp' 
                valign: 'top'
                
            Label:
                size_hint_y: 0.1
                text: '[color=616161]\\nUsing SmartBench is a risky business. Heed these warnings.[/color]'
                markup: True
                font_size: '16sp' 
                valign: 'bottom'
            
            BoxLayout:
                orientation: 'vertical'
                BoxLayout:
                    orientation: 'horizontal'    
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:0
                        Image:
                            orientation: 'right'
                            size_hint_x: 0.15
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            text: '[color=000000]What needs to go here?[/color]'
                            markup: True
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:0
                        Image:
                            orientation: 'right'
                            size_hint_x: 0.15
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            text: '[color=000000]What needs to go here?[/color]'
                            markup: True    
                            halign: 'left'     
        
                BoxLayout:
                    orientation: 'horizontal'
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:0
                        Image:
                            size_hint_x: 0.15
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            text: '[color=000000]What needs to go here?[/color]'
                            markup: True
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:0
                        Image:
                            size_hint_x: 0.15
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            text: '[color=000000]What needs to go here?[/color]'
                            markup: True      
        
                BoxLayout:
                    orientation: 'horizontal'
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:0
                        Image:
                            size_hint_x: 0.15
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            text: '[color=000000]What needs to go here?[/color]'
                            markup: True
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:0
                        Image:
                            size_hint_x: 0.15
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            text: '[color=000000]Mac, help![/color]'
                            markup: True
            
            BoxLayout:
                orientation: 'horizontal'
                pos: self.pos
                size_hint_y: 0.2
                AnchorLayout:               
                    Button:
                        size_hint_x: 0.7
                        pos: self.pos
                        halign: 'right'
                        background_normal: ''
                        background_color: hex('#0d47a1')
                        on_release:
                            root.quit_to_lobby()
                        Label:
                            text: '[color=FFFFFF][b]I have read and understand the safety warnings (??)[/b][/color]'
                            font_size: '20sp'
                            markup: True
                            size: self.parent.size
                            pos: self.parent.pos

              

""")

class SafetyScreen(Screen):

    def __init__(self, **kwargs):
        super(SafetyScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        #self.m=kwargs['machine']
    
    def on_enter(self):
        pass
        
    def quit_to_lobby(self):
        self.sm.current = 'lobby'