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
        orientation: 'vertical'
        padding: 20
        size: self.parent.size
        pos: self.parent.pos
        
        BoxLayout:
            size_hint_y: 2

            orientation: 'vertical'
            spacing: 10
            size: self.parent.size
            pos: self.parent.pos
        
            Label:
                text: '[color=000000]Safety Warning![/color]'
                markup: True
                font_size: '29sp' 
                valign: 'top'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                
            Label:
                text: '[color=616161]\\nRead the user manual prior to use.\\nImproper use of SmartBench can cause serious injury.\\n\\n[/color]'
                markup: True
                font_size: '19sp' 
                valign: 'bottom'
                halign: 'center'
            
        BoxLayout:
            size_hint_y: 4

            padding: 20
            orientation: 'vertical'
            BoxLayout:
                orientation: 'horizontal'    
                BoxLayout:
                    orientation: 'horizontal'
                    spacing:20
                    Image:
                        size_hint_x: 1
                        keep_ratio: True
                        allow_stretch: True                           
                        source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                    Label:
                        size_hint_x: 6
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
                        size_hint_x: 1
                        keep_ratio: True
                        allow_stretch: True                           
                        source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                    Label:
                        size_hint_x: 6
                        text: '[color=000000]ALWAYS WEAR EAR DEFENDERS, EYE PROTECTION AND DUST MASK[/color]'
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
                        size_hint_x: 1
                        keep_ratio: True
                        allow_stretch: True                           
                        source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                    Label:
                        size_hint_x: 6
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
                        size_hint_x: 1
                        keep_ratio: True
                        allow_stretch: True                           
                        source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                    Label:
                        size_hint_x: 6
                        text: '[color=000000]NEVER PUT HANDS INTO MOVING MACHINERY[/color]'
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
                        size_hint_x: 1
                        keep_ratio: True
                        allow_stretch: True                           
                        source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                    Label:
                        size_hint_x: 6
                        text: '[color=000000]DANGER TO LIFE BY MAGNETIC FIELDS.\\nDO NOT USE NEAR A PACEMAKER.[/color]'
                        markup: True
                        halign: 'left'
                        valign: 'middle'
                        size:self.texture_size
                        text_size: self.size
                BoxLayout:
                    orientation: 'horizontal'
                    spacing:20
                    Image:
                        size_hint_x: 1
                        keep_ratio: True
                        allow_stretch: True                           
                        source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                    Label:
                        size_hint_x: 6
                        text: '[color=000000]ENSURE THE MACHINE IS POWERED FROM AN EARTHED SUPPLY[/color]'
                        markup: True
                        valign: 'middle'
                        size:self.texture_size
                        text_size: self.size
                        halign: 'left'
            
        BoxLayout:
            size_hint_y: 2.5
            padding: 20
            orientation: 'horizontal'
            pos: self.pos
            AnchorLayout:               
                Button:
                    pos: self.pos
                    halign: 'right'
                    background_normal: ''
                    background_color: hex('#0d47a1')
                    on_press:
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
            
    def quit_to_lobby(self):
        self.sm.current = 'lobby'
        
    def on_leave(self):
        if self.sm.current != 'alarmScreen' and self.sm.current != 'errorScreen' and self.sm.current != 'door': 
            self.sm.remove_widget(self.sm.get_screen('safety'))