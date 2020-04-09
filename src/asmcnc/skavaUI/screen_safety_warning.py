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

from asmcnc.skavaUI import widget_status_bar # @UnresolvedImport



# Kivy UI builder:
Builder.load_string("""

<SafetyScreen>:

    status_container:status_container


    canvas:
        Color:
            rgba: hex('#E5E5E5FF')
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
    
        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos  
                
        BoxLayout:
            size_hint_y: 0.9
            orientation: 'vertical'
            padding: 40
            size: self.parent.size
            pos: self.parent.pos
    
      
            
            BoxLayout:
                size_hint_y: .5
    
                orientation: 'vertical'
#                 padding: 10
                size: self.parent.size
                pos: self.parent.pos
            
                Label:
                    text: '[color=333333]Safety Warning[/color]'
                    markup: True
                    font_size: '29sp' 
                    valign: 'middle'
                    halign: 'center'
                    size:self.texture_size
                    text_size: self.size
                    
#             Label:
#                 size_hint_y: 0.25
                
            BoxLayout:
                size_hint_y: 4
    
                padding: 40
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
                            text: '[color=333333]Improper use of SmartBench can cause serious injury[/color]'
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
                            text: '[color=333333]Always wear ear defenders, eye protection and a dust mask[/color]'
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
                            text: '[color=333333]Risk of injury from rotating tools and axis motion[/color]'
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
                            text: '[color=333333]Never put hands into moving machinery[/color]'
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
                            text: '[color=333333]Danger to life by magnetic fields - do not use near a pacemaker[/color]'
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
                            text: '[color=333333]Ensure the machine is powered from an earth supply[/color]'
                            markup: True
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            halign: 'left'

#             Label:
#                 size_hint_y: 0.25
                
            BoxLayout:
                size_hint_y: 1
                padding: 
                orientation: 'horizontal'
                pos: self.pos
                AnchorLayout:               
                    Button:
                        pos: self.pos
                        halign: 'right'
                        background_normal: ''
                        background_color: hex('#1e88e5')
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
        self.m=kwargs['machine']
        
        # Status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)
        self.status_bar_widget.cheeky_color = '#1e88e5'
            
    def quit_to_lobby(self):
        self.sm.current = 'lobby'
        
    def on_leave(self):
        if self.sm.current != 'alarmScreen' and self.sm.current != 'errorScreen' and self.sm.current != 'door': 
            self.sm.remove_widget(self.sm.get_screen('safety'))