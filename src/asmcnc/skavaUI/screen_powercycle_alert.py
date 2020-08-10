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
                text_size: self.size
                size_hint_y: 0.5
                text: "Please restart SmartBench now"
                markup: True
                font_size: '40sp'   
                valign: 'middle'
                halign: 'center'            

""")

class PowerCycleScreen(Screen):
    
    def __init__(self, **kwargs):
        super(PowerCycleScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
    