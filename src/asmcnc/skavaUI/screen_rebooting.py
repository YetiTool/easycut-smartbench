# -*- coding: utf-8 -*-
'''
Created Mayh 2019

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

<RebootingScreen>:

    reboot_label: reboot_label

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
                id: reboot_label
                text_size: self.size
                size_hint_y: 0.5
                markup: True
                font_size: '40sp'   
                valign: 'middle'
                halign: 'center'            

""")

class RebootingScreen(Screen):
    
    def __init__(self, **kwargs):
        super(RebootingScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.l=kwargs['localization']
        self.reboot_label.text = self.l.get_str('Rebooting') + '...'
    
    def on_enter(self): 
        self.reboot_label.text = self.l.get_str('Rebooting') + '...'
        Clock.schedule_once(self.reboot, 1)
        
    def reboot(self, dt):
        if sys.platform != "win32" and sys.platform != "darwin":
            os.system('sudo reboot')
        