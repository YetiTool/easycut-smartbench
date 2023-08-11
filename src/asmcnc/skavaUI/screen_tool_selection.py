"""
Created on 30 June 2021
@author: Dennis

Screen to select router or CNC stylus tool
"""
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string(
    """

<ToolSelectionScreen>:

    question_label : question_label
    router_button : router_button
    stylus_button : stylus_button

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
                id: question_label
                markup: True
                font_size: '28px' 
                valign: 'top'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333')

        # Buttons

        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(44)
            size_hint_y: dp(2.5)
            padding: [dp(0),dp(0),dp(0),dp(20)]

            # Stylus button

            Button:
                id: stylus_button
                # text: '[color=333333]CNC Stylus'
                on_press: root.stylus_button_pressed()
                valign: 'bottom'
                halign: 'center'
                markup: True
                font_size: '23px'
                text_size: self.size
                background_normal: "./asmcnc/skavaUI/img/stylus_option.png"
                padding_y: 30
                color: hex('#333333')

            # Router button

            Button:
                id: router_button
                # text: '[color=333333]Router'
                on_press: root.router_button_pressed()
                valign: 'bottom'
                halign: 'center'
                markup: True
                font_size: '23px'
                text_size: self.size
                background_normal: "./asmcnc/skavaUI/img/router_option.png"
                padding_y: 30
                color: hex('#333333')



"""
)


class ToolSelectionScreen(Screen):
    def __init__(self, **kwargs):
        self.sm = kwargs.pop("screen_manager")
        self.m = kwargs.pop("machine")
        self.l = kwargs.pop("localization")
        super(ToolSelectionScreen, self).__init__(**kwargs)
        self.update_strings()

    def router_button_pressed(self):
        self.m.stylus_router_choice = "router"
        self.exit_stylus_router_selection()

    def stylus_button_pressed(self):
        self.m.stylus_router_choice = "stylus"
        self.exit_stylus_router_selection()

    def exit_stylus_router_selection(self):
        if self.m.fw_can_operate_zUp_on_pause():
            if self.m.stylus_router_choice == "stylus":
                self.sm.get_screen("go").lift_z_on_job_pause = True
                self.sm.current = "jobstart_warning"
            else:
                self.sm.current = "lift_z_on_pause_or_not"
        else:
            self.sm.current = "jobstart_warning"

    def update_strings(self):
        self.question_label.text = self.l.get_str("Which tool are you using?")
        self.router_button.text = self.l.get_str("Router")
        self.stylus_button.text = "CNC Stylus"
