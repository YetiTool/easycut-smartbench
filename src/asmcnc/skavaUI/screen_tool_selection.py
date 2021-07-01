'''
Created on 30 June 2021
@author: Dennis
Screen to select router or CNC stylus tool
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""

<ToolSelectionScreen>:

    canvas.before:
        Color: 
            rgba: hex('#e5e5e5ff')
        Rectangle: 
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        padding: dp(50)

        # Top text

        BoxLayout:
            orientation: 'vertical'
            padding: [dp(0),dp(36),dp(0),dp(0)]
            

            Label:
                text: '[color=333333]Which tool are you using?'
                markup: True
                font_size: '28px' 
                valign: 'top'
                halign: 'center'
                size:self.texture_size
                text_size: self.size

        # Buttons

        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(44)
            size_hint_y: dp(2.5)
            padding: [dp(0),dp(0),dp(0),dp(20)]

            # Stylus button

            Button:
                text: '[color=333333]CNC Stylus'
                on_press: root.stylus_button_pressed()
                valign: 'bottom'
                halign: 'center'
                markup: True
                font_size: '23px'
                text_size: self.size
                background_normal: "./asmcnc/skavaUI/img/stylus_option.png"
                padding_y: 30

            # Router button

            Button:
                text: '[color=333333]Router'
                on_press: root.router_button_pressed()
                valign: 'bottom'
                halign: 'center'
                markup: True
                font_size: '23px'
                text_size: self.size
                background_normal: "./asmcnc/skavaUI/img/router_option.png"
                padding_y: 30



""")

class ToolSelectionScreen(Screen):


    def __init__(self, **kwargs):
        
        super(ToolSelectionScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']


    def router_button_pressed(self):
        self.sm.current = 'home'

    def stylus_button_pressed(self):
        self.sm.current = 'home'