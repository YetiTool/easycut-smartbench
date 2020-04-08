'''
Created on 19 March 2020
Software updater screen

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import sys, os

Builder.load_string("""

<SWUpdateScreen>:

    BoxLayout:
        size_hint: (None, None)
        height: dp(480)
        width: dp(800)
        orientation: 'vertical'
        spacing: 0
        canvas:
            Color:
                rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
            Rectangle:
                pos: self.pos
                size: self.size
        
        # Header box    
        BoxLayout:
            size_hint: (None, None)
            height: dp(160)
            width: dp(800)
            padding: [30, 30, 30, 18]
            spacing: 30
            orientation: 'horizontal'

            # Version labels box
            BoxLayout: 
                size_hint: (None, None)
                height: dp(112)
                width: dp(598)
                padding: [0,0,0,12]
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(100)
                    width: dp(598)
                    canvas:
                        Color:
                            rgba: [1,1,1,1]
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                    # Version labels:
                                
            # Exit button
            BoxLayout: 
                size_hint: (None, None)
                height: dp(112)
                width: dp(112)
                Button:
                    size_hint: (None,None)
                    height: dp(112)
                    width: dp(112)
                    background_color: hex('#F4433600')
                    center: self.parent.center
                    pos: self.parent.pos
                    on_press: root.quit_to_lobby()
                    BoxLayout:
                        padding: 0
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/wifi_app/img/quit.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

        # Body box
        BoxLayout:
            size_hint: (None, None)
            height: dp(320)
            width: dp(800)
            padding: [30, 0, 30, 30]
            spacing: 30
            orientation: 'horizontal'
            
            BoxLayout: 
                size_hint: (None, None)
                height: dp(290)
                width: dp(355)    
                orientation: "vertical"  
                padding: [30, 30, 30, 30]
                spacing: 0
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(30)
                    width: dp(295)
                    padding: [0,5,0,0]
                    Label: 
                        color: 0,0,0,1
                        font_size: 18
                        markup: True
                        halign: "left"
                        valign: "top"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                        text: "[b]Update using WiFi[/b]"                    
                    
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(90)
                    width: dp(295)
                    padding: [0,5,0,0]
                    Label: 
                        color: 0,0,0,1
                        font_size: 16
                        markup: True
                        halign: "left"
                        valign: "top"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                        text: root.wifi_instructions

                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(110)
                    width: dp(295)                    
                
                        
            BoxLayout: 
                size_hint: (None, None)
                height: dp(290)
                width: dp(355)
                orientation: "vertical"  
                padding: [30, 30, 30, 30]
                spacing: 0  
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size

                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(30)
                    width: dp(295)
                    Label: 
                        color: 0,0,0,1
                        font_size: 18
                        markup: True
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                        text: "[b]Update using USB[/b]"                    
                    
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(90)
                    width: dp(295)
                    Label: 
                        color: 0,0,0,1
                        font_size: 16
                        markup: True
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                        text: root.usb_instructions

                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(110)
                    width: dp(295) 

               
""")

class SWUpdateScreen(Screen):

    wifi_instructions = 'Ensure connection is stable before attempting to update.'
    usb_instructions = 'Insert a USB stick containing the latest software.\n' + \
    'Go to www.yetitool.com/support for help on how to do this.'
      
    def __init__(self, **kwargs):
        super(SWUpdateScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']