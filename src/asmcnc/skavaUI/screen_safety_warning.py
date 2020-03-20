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
            spacing: 20
            # size_hint_x: 2
            size: self.parent.size
            pos: self.parent.pos
        
            Label:
                size_hint_y: 0.2
                text: '[color=000000]Safety Warning![/color]'
                markup: True
                font_size: '29sp' 
                valign: 'top'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                
            Label:
                size_hint_y: 0.1
                text: '[color=616161]\\nRead the user manual prior to use.\\nImproper use of SmartBench can cause serious injury.\\n\\n[/color]'
                markup: True
                font_size: '19sp' 
                valign: 'bottom'
                halign: 'center'
            
            BoxLayout:
                orientation: 'vertical'
                BoxLayout:
                    orientation: 'horizontal'    
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            orientation: 'right'
                            size_hint_x: 0.2
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            halign: 'left'
                            text: '[color=000000]RISK OF INJURY FROM ROTATING \\nTOOLS[/color]'
                            markup: True
                            size:self.size
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            orientation: 'right'
                            size_hint_x: 0.2
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            text: '[color=000000]ALWAYS WEAR EAR DEFENDERS[/color]'
                            markup: True    
                            halign: 'left' 
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size    
        
                BoxLayout:
                    orientation: 'horizontal'
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            size_hint_x: 0.2
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            text: '[color=000000]RISK OF INJURY BY AXIS MOTION[/color]'
                            markup: True
                            halign: 'left'
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            size_hint_x: 0.2
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            text: '[color=000000]ALWAYS WEAR EYE PROTECTION[/color]'
                            markup: True
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            halign: 'left'
                              
        
                BoxLayout:
                    orientation: 'horizontal'
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            size_hint_x: 0.2
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            text: '[color=000000]NEVER PUT HANDS INTO MOVING MACHINERY[/color]'
                            markup: True
                            halign: 'left'
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            size_hint_x: 0.2
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            text: '[color=000000]ALWAYS WEAR A DUST MASK[/color]'
                            markup: True
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            halign: 'left'
                            
                BoxLayout:
                    orientation: 'horizontal'
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            size_hint_x: 0.2
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                            halign: 'left'
                            size:self.texture_size
                        Label:
                            text: '[color=000000]  DANGER TO LIFE BY MAGNETIC FIELDS.\\n  DO NOT USE IF YOU HAVE A PACEMAKER.[/color]'
                            markup: True
                            halign: 'left'
                            valign: 'middle'
                            size:self.texture_size
                            #text_size: self.size
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            size_hint_x: 0.2
                            keep_ratio: True
                            allow_stretch: True                           
                            #source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            #text: '[color=000000]ALWAYS WEAR A DUST MASK[/color]'
                            markup: True
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            halign: 'left'
            
            BoxLayout:
                orientation: 'horizontal'
                pos: self.pos
                size_hint_y: 0.2
                AnchorLayout:               
                    Button:
                        size_hint_x: 0.75
                        pos: self.pos
                        halign: 'right'
                        background_normal: ''
                        background_color: hex('#0d47a1')
                        on_release:
                            root.quit_to_lobby()
                        Label:
                            text: '[color=FFFFFF]I have read the manual and understand the safety warnings[/color]'
                            font_size: '19sp'
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
        self.button_press = False
        
    def quit_to_lobby(self):
        self.button_press = True
        self.sm.current = 'lobby'
        
    def on_leave(self):
        if self.button_press == True: self.sm.remove_widget(self.sm.get_screen('safety'))