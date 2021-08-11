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

    dots_label: dots_label

    canvas:
        Color: 
            rgba: hex('#FFFFFF')
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
                text: "Finishing install... please wait"
                color: hex('#000000')
                markup: True
                font_size: '40sp'   
                valign: 'middle'
                halign: 'center'

            Label:
                id: dots_label
                text_size: self.size
                size_hint_y: 0.5
                text: "..."
                color: hex('1976d2ff')
                markup: True
                font_size: '200sp'   
                valign: 'middle'
                halign: 'center'

            Label:
                text_size: self.size
                size_hint_y: 0.5
                text: "DO NOT POWER OFF SMARTBENCH"
                color: hex('#000000')
                markup: True
                font_size: '40sp'   
                valign: 'middle'
                halign: 'center'

""")

class PowerCycleScreen(Screen):
    
    def __init__(self, **kwargs):
        super(PowerCycleScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']

    def on_enter(self):
        self.wait_for_install = Clock.schedule_once(self.finished_installing, 30)
        self.update_dots = Clock.schedule_interval(self.update_label, 0.5)

    def update_label(self, dt):
        self.dots_label.text = self.dots_label.text + '.'
        if len(self.dots_label.text) == 4:
            self.dots_label.text = ''

    def finished_installing(self, *args):
        Clock.unschedule(self.update_dots)
        self.sm.current = 'release_notes'

    def on_touch_down(self, touch):
        if sys.platform == 'win32':
            Clock.unschedule(self.wait_for_install)
            self.finished_installing()
