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

<SquaringScreenDecisionManualVsSquare>:

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
            size_hint_y: 1

        Label:
            size_hint_y: 2
            text: '[color=333333]X beam squaring:[/color]'
            markup: True
            font_size: '30px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
     
        BoxLayout:
            orientation: 'horizontal'
            spacing: 30
            size_hint_y: 2.5

            Button:
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.already_square()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/squaring_btn_already_square.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
            Button:
                size_hint_x: 0.2
                background_color: hex('#FFFFFF00')
                on_press: root.popup_help()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/help_btn_orange_round.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
            Button:
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.needs_auto_squaring()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/squaring_btn_decide_auto_square.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
        Label:
            size_hint_y: 1                

""")


class SquaringScreenDecisionManualVsSquare(Screen):
    
    
    def __init__(self, **kwargs):
        super(SquaringScreenDecisionManualVsSquare, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
    
    def already_square(self):
        self.m.is_squaring_XY_needed_after_homing = False
        self.sm.current = 'prepare_to_home'
    
    def popup_help(self):
        pass

    def needs_auto_squaring(self):
        self.m.is_squaring_XY_needed_after_homing = True
        self.sm.current = 'prepare_to_home'
    
    
