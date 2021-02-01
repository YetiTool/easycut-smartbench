'''
Created on 1 February 2021
@author: Letty

Screen to provide user with important safety information prior to every job start.
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex
#:import Factory kivy.factory.Factory

<RoundedButton@Button>:
    background_color: 0,0,0,0
    canvas.before:
        Color:
            rgba: hex('#1976d2ff')
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(15), dp(15)]

<JobstartWarningScreen>:

    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas.before:
            Color: 
                rgba: hex('#E5E5E5FF')
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding: 0
            orientation: "vertical"
            spacing: 10

            BoxLayout:
                padding: 0
                spacing: 0
                canvas:
                    Color:
                        rgba: hex('#1976d2ff')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    size_hint: (None,None)
                    height: dp(60)
                    width: dp(800)
                    text: "Safety Warning"
                    color: hex('#f9f9f9ff')
                    # color: hex('#333333ff') #grey
                    font_size: 30
                    halign: "center"
                    valign: "bottom"
                    markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(320)
                padding: [40,20,40,20]
                spacing: 20
                orientation: 'vertical'
             
                BoxLayout:
                    orientation: 'horizontal'
                    spacing:20
                    size_hint_y: 1.1

                    Image:
                        size_hint_x: 0.25
                        keep_ratio: True
                        allow_stretch: True                           
                        source: "./asmcnc/skavaUI/img/fire_warning.png"

                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 0.75
                        Label:
                            size_hint_y: 0.2
                            text: '[color=333333][b]Significant risk of fire[/b][/color]'
                            markup: True
                            halign: 'left'
                            font_size: '26sp' 
                            markup: True
                            size:self.size
                            valign: 'top'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333FF')

                        Label:
                            size_hint_y: 0.8
                            halign: 'left'
                            text: root.causes_of_fire
                            markup: True
                            size:self.size
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333FF')
                            markup: True
                            font_size: '22sp' 

                BoxLayout:
                    orientation: 'horizontal'
                    spacing:20
                    size_hint_x: 1
                    size_hint_y: 0.9

                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        size_hint_x: 0.75
                        Image:
                            size_hint_x: 0.33
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/never_unattended.png"

                        BoxLayout:
                            size_hint_x: 0.67
                            Label:
                                text: '[color=333333][b]Never leave CNC machines unattended[/b][/color]'
                                markup: True
                                halign: 'left'
                                font_size: '26sp' 
                                markup: True
                                size:self.size
                                valign: 'middle'
                                size:self.texture_size
                                text_size: self.size
                                color: hex('#333333FF')

                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 0.25

                        Label:
                            # size_hint_x: None
                            # width: dp(150)
                            size_hint_y: 0.2
                            text: '[color=333333][b]Learn More[/b][/color]'
                            markup: True
                            halign: 'center'
                            font_size: '22sp' 
                            markup: True
                            size:self.size
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333FF')

                        Image:
                            source: "./asmcnc/skavaUI/img/qr_safety.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

  

            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(80)
                padding: [dp(250),dp(0), dp(250), dp(20)]
                orientation: 'horizontal'

                RoundedButton:
                    size_hint: (None,None)
                    height: dp(60)
                    width: dp(300)
                    center: self.parent.center
                    pos: self.parent.pos
                    on_press: root.continue_to_go_screen()
                    text: 'I understand'
                    color: hex('#f9f9f9ff')
                    markup: True
                    font_size: '22sp'
                  

""")

class RoundedButton(Button):
    pass

class JobstartWarningScreen(Screen):

    causes_of_fire = (
        "Common causes of fire:\n"
        "- Processing combustible materials E.g. woods\n"
        "- Using dull cutters can produce heat through friction\n"
        "- Variation in extraction\n"
        )


    def __init__(self, **kwargs):

        super(JobstartWarningScreen, self).__init__(**kwargs)
        self.sm=kwargs['machine']
        self.sm=kwargs['screen_manager']


    def continue_to_go_screen(self):
        self.sm.current = 'go'

