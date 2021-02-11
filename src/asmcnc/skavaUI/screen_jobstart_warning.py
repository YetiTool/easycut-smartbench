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

    header_label : header_label
    risk_of_fire : risk_of_fire
    causes_of_fire : causes_of_fire
    never_unattended : never_unattended
    scan_label : scan_label
    confirm_button : confirm_button

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
                    id: header_label
                    size_hint: (None,None)
                    height: dp(60)
                    width: dp(800)
                    text: "Safety Warning"
                    color: hex('#f9f9f9ff')
                    font_size: 30
                    halign: "center"
                    valign: "bottom"
                    markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(310)
                padding: [10,10,10,0]
                spacing: 0
                orientation: 'vertical'
             
                BoxLayout:
                    orientation: 'horizontal'
                    spacing:10
                    size_hint_y: 1.22
                    BoxLayout:
                        padding: 20
                        size_hint_x: 0.2
                        Image:
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/fire_warning.png"

                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 0.8
                        Label:
                            id: risk_of_fire
                            size_hint_y: 0.2
                            markup: True
                            halign: 'left'
                            font_size: '32sp' 
                            markup: True
                            size:self.size
                            valign: 'top'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333FF')

                        Label:
                            id: causes_of_fire
                            size_hint_y: 0.8
                            halign: 'left'
                            markup: True
                            size:self.size
                            valign: 'bottom'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333FF')
                            markup: True
                            font_size: '20sp' 

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_x: 1
                    size_hint_y: 0.78

                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:10
                        size_hint_x: 0.75

                        BoxLayout:
                            padding: 0
                            size_hint_x: 0.27
                            Image:
                                keep_ratio: True
                                allow_stretch: True                           
                                source: "./asmcnc/skavaUI/img/never_unattended.png"

                        BoxLayout:
                            size_hint_x: 0.73
                            Label:
                                id: never_unattended
                                markup: True
                                halign: 'left'
                                font_size: '32sp' 
                                markup: True
                                size:self.size
                                valign: 'middle'
                                size:self.texture_size
                                text_size: self.size
                                color: hex('#333333FF')

                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 0.25

                        Image:
                            source: "./asmcnc/skavaUI/img/qr_safety.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
                        Label:
                            id: scan_label
                            size_hint_y: 0.18
                            markup: True
                            halign: 'center'
                            font_size: '22sp' 
                            markup: True
                            size:self.size
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333FF')
  

            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(80)
                padding: [dp(250),dp(0), dp(250), dp(20)]
                orientation: 'horizontal'

                RoundedButton:
                    id: confirm_button
                    size_hint: (None,None)
                    height: dp(60)
                    width: dp(300)
                    center: self.parent.center
                    pos: self.parent.pos
                    on_press: root.continue_to_go_screen()
                    color: hex('#f9f9f9ff')
                    markup: True
                    font_size: '28sp'
                  

""")

class RoundedButton(Button):
    pass

class JobstartWarningScreen(Screen):

    def __init__(self, **kwargs):

        super(JobstartWarningScreen, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.l=kwargs['localization']

        self.update_strings()

    def on_enter(self):
        self.update_strings()

    def continue_to_go_screen(self):
        self.sm.current = 'go'

    def update_strings(self):

        self.header_label.text = self.l.get_str("Safety Warning")
        self.risk_of_fire.text = self.l.get_str("Risk of fire")
        self.causes_of_fire.text = (
                self.l.get_str("Common causes of fire") + ":\n"
                "- " + self.l.get_str("Processing combustible materials, e.g. woods") + "\n"
                "- " + self.l.get_str("Using dull cutters which produce heat through friction") + "\n"
                "- " + self.l.get_str("Variation in extraction") + "\n"
            )
        self.never_unattended.text = self.l.get_bold("Never leave CNC machines unattended")
        self.scan_label.text = self.l.get_bold("SCAN ME")
        self.confirm_button.text = self.l.get_str("I understand")

