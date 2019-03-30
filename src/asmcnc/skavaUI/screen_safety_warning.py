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
        padding: 60
        spacing: 0
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 1
            
            Label:
                size_hint_y: 0.2
                text: '[color=000000][b]Safety Warning[/b][/color]'
                markup: True
                font_size: '40sp' 
            
            BoxLayout:
                orientation: 'vertical'
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
                            text: '[color=000000]What needs to go here?[/color]'
                            markup: True
                           
            Button:
                size_hint_y: 0.2
                size_hint_x: 0.5
                halign: 'right'
                on_release:
                    root.quit_to_lobby()

                      

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