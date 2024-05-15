"""
Created Mayh 2019

@author: Letty

Basic screen 
"""
import os
import sys

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from asmcnc.core_UI import console_utils

Builder.load_string(
    """

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
        padding: app.get_scaled_tuple([70.0, 70.0])
        spacing: app.get_scaled_width(70.0)
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 1
                
            Label:
                id: reboot_label
                text_size: self.size
                size_hint_y: 0.5
                markup: True
                font_size: app.get_scaled_sp('40.0sp')
                valign: 'middle'
                halign: 'center'            

"""
)


class RebootingScreen(Screen):
    def __init__(self, **kwargs):
        super(RebootingScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.l = kwargs["localization"]
        self.reboot_label.text = self.l.get_str("Rebooting") + "..."

    def on_pre_enter(self):
        self.reboot_label.text = self.l.get_str("Rebooting") + "..."
        self.reboot_label.font_name = self.l.font_regular

    def on_enter(self):
        Clock.schedule_once(console_utils.reboot, 1)
