from kivy.core.window import Window

"""
Created on 1 February 2021
@author: Letty

Screen to provide user with important safety information prior to every job start.
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

Builder.load_string(
    """

#:import hex kivy.utils.get_color_from_hex
#:import Factory kivy.factory.Factory

<RoundedButton@Button>:
    background_color: color_provider.get_rgba("invisible")
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
        height: dp(1.0*app.height)
        width: dp(1.0*app.width)
        canvas.before:
            Color: 
                rgba: color_provider.get_rgba("light_grey")
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding: 0
            orientation: "vertical"
            spacing:0.0208333333333*app.height

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
                    height: dp(0.125*app.height)
                    width: dp(1.0*app.width)
                    text: "Safety Warning"
                    color: color_provider.get_rgba("near_white")
                    font_size: 0.0375*app.width
                    halign: "center"
                    valign: "bottom"
                    markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.666666666667*app.height)
                padding:[dp(0.025)*app.width, dp(0.0208333333333)*app.height, dp(0.025)*app.width, 0]
                spacing: 0
                orientation: 'vertical'
             
                BoxLayout:
                    orientation: 'horizontal'
                    spacing:0.0125*app.width
                    size_hint_y: 1.22
                    BoxLayout:
                        padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                        size_hint_x: 0.2
                        Image:
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/fire_warning.png"

                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 0.8
                        padding:[0, 0, dp(0.025)*app.width, 0]
                        Label:
                            id: risk_of_fire
                            size_hint_y: 0.2
                            markup: True
                            halign: 'left'
                            font_size: str(0.04*app.width) + 'sp' 
                            markup: True
                            valign: 'top'
                            size:self.texture_size
                            text_size: self.size
                            color: color_provider.get_rgba("dark_grey")

                        Label:
                            id: causes_of_fire
                            size_hint_y: 0.8
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            size: self.texture_size
                            text_size: self.size
                            color: color_provider.get_rgba("dark_grey")
                            markup: True
                            font_size: str(0.025*app.width) + 'sp' 

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_x: 1
                    size_hint_y: 0.78

                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:0.0125*app.width
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
                                font_size: str(0.04*app.width) + 'sp' 
                                markup: True
                                size:self.size
                                valign: 'middle'
                                size:self.texture_size
                                text_size: self.size
                                color: color_provider.get_rgba("dark_grey")

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
                            font_size: str(0.0275*app.width) + 'sp' 
                            markup: True
                            size:self.size
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: color_provider.get_rgba("dark_grey")
  

            BoxLayout:
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.166666666667*app.height)
                padding:[dp(0.3125)*app.width, 0, dp(0.3125)*app.width, dp(0.0208333333333)*app.height]
                orientation: 'horizontal'

                Button:
                    id: confirm_button
                    size_hint: (None,None)
                    on_press: root.continue_to_go_screen()
                    background_normal: "./asmcnc/skavaUI/img/next.png"
                    background_down: "./asmcnc/skavaUI/img/next.png"
                    border: [dp(14.5)]*4
                    width: dp(0.36375*app.width)
                    height: dp(0.164583333333*app.height)
                    font_size: str(0.035*app.width) + 'sp'
                    color: color_provider.get_rgba("near_white")
                    markup: True
                    center: self.parent.center
                    pos: self.parent.pos
                  

"""
)


class RoundedButton(Button):
    pass


class JobstartWarningScreen(Screen):
    def __init__(self, **kwargs):
        super(JobstartWarningScreen, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.l = kwargs["localization"]
        self.update_strings()

    def continue_to_go_screen(self):
        self.m.spindle_health_check_failed = False
        self.m.spindle_health_check_passed = False
        self.m.s.yp.set_adjusting_spindle_speed(False)
        self.sm.current = "go"

    def update_strings(self):
        self.header_label.text = self.l.get_str("Safety Warning")
        self.risk_of_fire.text = self.l.get_str("Risk of fire")
        self.causes_of_fire.text = (
            self.l.get_str("Common causes of fire")
            + ":\n- "
            + self.l.get_str("Processing combustible materials, e.g. woods")
            + "\n- "
            + self.l.get_str("Using dull cutters which produce heat through friction")
            + "\n- "
            + self.l.get_str("Variation in extraction")
            + "\n"
        )
        self.never_unattended.text = self.l.get_bold(
            "Never leave CNC machines unattended"
        )
        self.scan_label.text = self.l.get_bold("SCAN ME")
        self.confirm_button.text = self.l.get_str("I understand")
        self.update_font_size(self.scan_label)

    def update_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length > 11:
            value.font_size = 0.02375 * Window.width
        else:
            value.font_size = 0.0275 * Window.width
