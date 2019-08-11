'''
Created on 11 Aug 2019

@author: Letty
'''
# config

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.clock import Clock

from time import sleep

import sys, os


Builder.load_string("""

<ScreenSaverScreen>:
    
    wake_up_button:wake_up_button
    yeti_image:yeti_image
    
    canvas:
        Color: 
            rgba: hex('#0D47A1')
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
#             spacing: 20
#             padding: 10
            
            Image:
                id: yeti_image
                size_hint_y: 3
                keep_ratio: True
                allow_stretch: False
                source: "./asmcnc/skavaUI/img/Sleeping_Yeti.png"

            Label:
                text_size: self.size
                size_hint_y: 0.5
                text: "Yeti went to sleep while you were away..."
                markup: True
                font_size: '20sp'   
                valign: 'bottom'
                halign: 'center'
                               
            AnchorLayout: 
                Button:
                    id: wake_up_button
                    size_hint_x: 0.25
                    size_hint_y: 0.45
                    halign: 'center'
                    valign: 'middle'
                    background_normal: ''
                    background_color: hex('#1E88E5')
                    disabled: False
                    on_release: 
                        root.wake_up_yeti()
                    
                    Label:
                        #size: self.texture_size
                        text: root.wakeup_text
                        size: self.parent.size
                        pos: self.parent.pos
                        text_size: self.size
                        valign: 'middle'
                        halign: 'center'
                        font_size: '22sp'
                        markup: True
""")


class ScreenSaverScreen(Screen):
    
    wakeup_text = StringProperty()
    
    def __init__(self, **kwargs):
        super(ScreenSaverScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def on_enter(self):
        self.wakeup_text = '[b]Wake Up Yeti[/b]'
        self.wake_up_button.disabled = False
        self.yeti_counter = 1
        self.swap_image_event = Clock.schedule_interval(lambda *args: self.swap_image(), 1.2)
        
    def swap_image(self):
        if self.yeti_counter == 0:
            self.yeti_image.source = "./asmcnc/skavaUI/img/Sleeping_Yeti.png"
            self.yeti_counter = 1
        else:
            self.yeti_image.source = "./asmcnc/skavaUI/img/Sleeping_Yeti_Alt.png"
            self.yeti_counter = 0           

    def wake_up_yeti(self):
        self.wakeup_text = '[b]Waking Up...[/b]'
        self.wake_up_button.disabled = True
        Clock.unschedule(self.swap_image_event)
        Clock.schedule_once(lambda *args: self.quit_to_home(), 3)
        
    def quit_to_home(self):
        
        self.sm.current = 'home'
  
        
