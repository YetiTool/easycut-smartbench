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
            spacing: 20
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
                    size_hint_x: 0.4
                    size_hint_y: 0.8
                    halign: 'center'
                    valign: 'middle'
                    background_normal: ''
                    background_color: hex('#1E88E5')
                    disabled: False
                    on_press: 
                        root.button_press()
                    
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
            Label: 
                size_hint_y: 0.2
                text: root.warning_text
                markup: True
                font_size: '18sp' 
                valign: 'bottom'
                halign: 'center'
                size: self.texture_size
                text_size: root.width, None
                padding_x: 100
                padding_y: 60
""")


class ScreenSaverScreen(Screen):
    
    wakeup_text = StringProperty()
    warning_text = StringProperty()
    
    def __init__(self, **kwargs):
        super(ScreenSaverScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.wakeup_text = '[b]Wake Up Yeti[/b]'
        self.warning_text = ("If the console has been left idle for a while, " 
                             "it can be slow to wake up again. " 
                             "Please be patient, and wait for the screen to respond.")


    def on_enter(self):
        self.yeti_counter = 1
        self.swap_image_event = Clock.schedule_interval(lambda *args: self.swap_image(), 1.2)
        self.go_home = False
        
    def swap_image(self):
        if self.yeti_counter == 0:
            self.yeti_image.source = "./asmcnc/skavaUI/img/Sleeping_Yeti.png"
            self.yeti_counter = 1
        else:
            self.yeti_image.source = "./asmcnc/skavaUI/img/Sleeping_Yeti_Alt.png"
            self.yeti_counter = 0   
            
    def button_press(self):
        if self.go_home:
            self.go_home = False
            self.quit_to_home()
        else:
            self.wake_up_yeti()

    def wake_up_yeti(self):
        self.wakeup_text = '[b]Waking Up...[/b]'
        self.wake_up_button.disabled = True
        Clock.unschedule(self.swap_image_event)
        self.yeti_image.source = "./asmcnc/skavaUI/img/Waking_Yeti.png"
        Clock.schedule_once(lambda *args: self.enable_return(), 1)
        
    def enable_return(self):
        self.wakeup_text = '[b]Return to home[/b]'
        self.yeti_image.source = "./asmcnc/skavaUI/img/Waking_Yeti_Alt.png"   
        self.wake_up_button.disabled = False 
        self.go_home = True
        
    def quit_to_home(self):
        self.sm.current = 'home'
        
    def on_leave(self):
        self.yeti_image.source = "./asmcnc/skavaUI/img/Sleeping_Yeti.png"
        self.go_home = False
        self.wakeup_text = '[b]Wake Up Yeti[/b]'
        self.wake_up_button.disabled = False
        
