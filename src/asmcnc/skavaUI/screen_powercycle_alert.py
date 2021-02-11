# -*- coding: utf-8 -*-
'''
Created March 2020

@author: Letty

Basic screen 
'''
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import sys, os


# Kivy UI builder:
Builder.load_string("""

<PowerCycleScreen>:

    only_label: only_label

    canvas:
        Color: 
            rgba: hex('#000000')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding: 70
        spacing: 70
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 1
                
            Label:
                id: only_label
                text_size: self.size
                size_hint_y: 0.5
                markup: True
                font_size: '40sp'   
                valign: 'middle'
                halign: 'center'

""")

class PowerCycleScreen(Screen):
    
    def __init__(self, **kwargs):
        super(PowerCycleScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.l=kwargs['localization']

    def on_enter(self):
        self.only_label.text = self.l.get_str("Please wait") "..."
        Clock.schedule_once(self.update_label, 25)

    def update_label(self, dt):
        self.only_label.text = self.l.get_str("Please restart SmartBench now")
    