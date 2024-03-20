# -*- coding: utf-8 -*-
from kivy.core.window import Window

"""
Created March 2019

@author: Ed

Squaring decision: manual or auto?
"""
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.skavaUI import popup_info
from kivy.clock import Clock
from asmcnc.core_UI import scaling_utils as utils

Builder.load_string(
    """

<SquaringScreenDecisionManualVsSquare>:

    header_label: header_label
    subtitle_label: subtitle_label
    no_button: no_button
    yes_button: yes_button

    canvas:
        Color: 
            rgba: hex('#E5E5E5FF')
        Rectangle: 
            size: self.size
            pos: self.pos         

    BoxLayout: 
        spacing: 0
        padding:[dp(0.05)*app.width, dp(0.0833333333333)*app.height]
        orientation: 'vertical'

        # Cancel button
        BoxLayout:
            size_hint: (None,None)
            height: dp(0.0416666666667*app.height)
            padding:[dp(0.025)*app.width, 0, dp(0.025)*app.width, 0]
            spacing:0.85*app.width
            orientation: 'horizontal'
            pos: self.parent.pos

            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                text: ""

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint: (None,None)
                height: dp(0.104166666667*app.height)
                width: dp(0.0625*app.width)
                background_color: hex('#FFFFFF00')
                opacity: 1
                on_press: root.cancel()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/cancel_btn_decision_context.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

        Label:
            font_size: str(0.01875 * app.width) + 'sp'
            size_hint_y: 0.1

        BoxLayout:
            orientation: 'vertical'
            spacing:0.0208333333333*app.height
            padding:[0, dp(0.0416666666667)*app.height, 0, dp(0.0416666666667)*app.height]
            size_hint_y: 3
            

            Label:
                id: header_label
                size_hint_y: 2
                markup: True
                font_size: str(0.0375*app.width) + 'px' 
                valign: 'bottom'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')
         
            Label:
                id: subtitle_label
                size_hint_y: 1
                markup: True
                font_size: str(0.0225*app.width) + 'px' 
                valign: 'top'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')
     
        BoxLayout:
            orientation: 'horizontal'
            spacing:0.0375*app.width
            size_hint_y: 3

            Button:
                id: no_button
                size_hint_x: 1
                on_press: root.already_square()
                valign: "middle"
                halign: "center"
                markup: True
                font_size: root.default_font_size
                text_size: self.size
                background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                border: [dp(30)]*4
                padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                        
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_x: 0.3
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
                id: yes_button
                size_hint_x: 1
                on_press: root.needs_auto_squaring()
                # text: "Yes, enable auto-square"
                valign: "middle"
                halign: "center"
                markup: True
                font_size: root.default_font_size
                text_size: self.size
                background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                border: [dp(30)]*4
                padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                        
        Label:
            font_size: str(0.01875 * app.width) + 'sp'
            size_hint_y: .5                

"""
)


class SquaringScreenDecisionManualVsSquare(Screen):
    cancel_to_screen = "lobby"
    return_to_screen = "lobby"
    default_font_size = utils.get_scaled_width(30)

    def __init__(self, **kwargs):
        super(SquaringScreenDecisionManualVsSquare, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def on_pre_enter(self):
        if self.m.is_machine_completed_the_initial_squaring_decision:
            self.no_button.text = self.l.get_str("No, SmartBench is still square")

    def already_square(self):
        self.m.is_squaring_XY_needed_after_homing = False
        self.proceed_to_next_screen()

    def needs_auto_squaring(self):
        self.m.is_squaring_XY_needed_after_homing = True
        self.proceed_to_next_screen()

    def proceed_to_next_screen(self):
        self.sm.get_screen("prepare_to_home").cancel_to_screen = self.cancel_to_screen
        self.sm.get_screen("prepare_to_home").return_to_screen = self.return_to_screen
        self.sm.current = "prepare_to_home"

    def popup_help(self):
        info = (
            self.l.get_bold("Manual squaring")
            + "\n"
            + self.l.get_str(
                "Before power up, the user manually pushes the X beam up against the bench legs at the home end."
            )
            + " "
            + self.l.get_str("The power is then switched on.")
            + " "
            + self.l.get_str(
                "The motor coils lock the lower beam into position with a high degree of reliability."
            )
            + " "
            + self.l.get_str(
                "Thus, mechanical adjustments to square the beam can be repeated."
            )
            + "\n\n"
            + self.l.get_bold("Auto squaring")
            + "\n"
            + self.l.get_str("No special preparation from the user is needed.")
            + " "
            + self.l.get_str(
                "When homing, the lower beam automatically drives into the legs to square the X beam against the bench legs."
            )
            + " "
            + self.l.get_str("The stalling procedure can offer a general squareness.")
            + " "
            + self.l.get_str(
                "But at the end of the movement, the motor coils can bounce into a different step position."
            )
            + " "
            + self.l.get_str(
                "Thus, mechanical adjustments to square the beam can be repeated less reliably than manual squaring."
            )
        )
        popup_info.PopupInfo(self.sm, self.l, 760, info)

    def cancel(self):
        self.sm.current = self.cancel_to_screen

    def update_strings(self):
        self.header_label.text = self.l.get_str(
            "Does SmartBench need to auto-square the XY?"
        ).replace(self.l.get_str("auto-square"), self.l.get_bold("auto-square"))
        self.subtitle_label.text = self.l.get_str(
            "Click on the question mark to learn more about this."
        )
        self.yes_button.text = self.l.get_str("Yes, enable auto-square")
        if self.m.is_machine_completed_the_initial_squaring_decision:
            self.no_button.text = self.l.get_str("No, SmartBench is still square")
        else:
            self.no_button.text = self.l.get_str("No, I manually squared already")
        self.update_font_size(self.no_button)
        self.update_font_size(self.yes_button)

    def update_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length < 35:
            value.font_size = self.default_font_size
        elif text_length > 38:
            value.font_size = self.default_font_size - 0.0025 * Window.width
        if text_length > 42:
            value.font_size = self.default_font_size - 0.005 * Window.width
        if text_length > 44:
            value.font_size = self.default_font_size - 0.00625 * Window.width
        if text_length > 50:
            value.font_size = self.default_font_size - 0.00875 * Window.width
