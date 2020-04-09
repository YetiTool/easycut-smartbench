'''
Created March 2019

@author: Ed

Squaring decision: manual or auto?
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os

Builder.load_string("""

<SquaringScreenActive>:

    canvas:
        Color: 
            rgba: hex('#E5E5E5FF')
        Rectangle: 
            size: self.size
            pos: self.pos         

    BoxLayout: 
        spacing: 0
        padding: 40
        orientation: 'vertical'


        Label:
            size_hint_y: .5

        BoxLayout:
            orientation: 'horizontal'
            spacing: 30
            size_hint_y: 2

            Button:
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.windows_hack_to_procede()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/squaring_icon_big.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
            Label:
                size_hint_x: .6
                text: '[color=333333]Squaring...[/color]'
                markup: True
                font_size: '30px' 
                valign: 'middle'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                        
            Button:
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.stop_squaring()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/stop_big.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
        Label:
            size_hint_y: .5
            
        Label:
            size_hint_y: 1
            text: '[color=333333]This operation will over-drive the X beam into the legs. This is normal.[/color]'
            markup: True
            font_size: '30px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size             

        Label:
            size_hint_y: .5

""")


class SquaringScreenActive(Screen):
    
    
    def __init__(self, **kwargs):
        super(SquaringScreenActive, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
    
    def windows_hack_to_procede(self):
        self.sm.current = 'lobby'
    
    def stop_squaring(self):
        pass