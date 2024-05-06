# -*- coding: utf-8 -*-
"""
Created March 2019

@author: Ed

Prepare to home
"""
from kivy.core.window import Window
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from kivy.clock import Clock
from asmcnc.core_UI import scaling_utils as utils

Builder.load_string(
    """

<HomingScreenPrepare>:

    instruction_label:instruction_label
    press_to_home_label: press_to_home_label

    canvas:
        Color: 
            rgba: color_provider.get_rgba("light_grey")
        Rectangle: 
            size: self.size
            pos: self.pos         

    BoxLayout: 
        spacing: 0
        padding:[dp(0.025)*app.width, dp(0.0833333333333)*app.height]
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
                background_color: color_provider.get_rgba("invisible")
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
            id: instruction_label
            size_hint_y: 2.3
            markup: True
            font_size: root.default_font_size
            valign: 'bottom'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            color: color_provider.get_rgba("dark_grey")

        Label:
            id: press_to_home_label
            size_hint_y: 2.3
            markup: True
            font_size: root.default_font_size
            valign: 'top'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            color: color_provider.get_rgba("dark_grey")

        # Label:
        #     size_hint_y: 0.1                

        Button:
            font_size: str(0.01875 * app.width) + 'sp'
            size_hint_y: 4.9
            background_color: color_provider.get_rgba("invisible")
            on_press: root.begin_homing()
            BoxLayout:
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/skavaUI/img/home_big.png"
                    size: self.parent.width, self.parent.height
                    allow_stretch: True 
                        
        Label:
            font_size: str(0.01875 * app.width) + 'sp'
            size_hint_y: 1                

"""
)


class HomingScreenPrepare(Screen):
    cancel_to_screen = "lobby"
    return_to_screen = "lobby"
    default_font_size = utils.get_scaled_width(30)

    def __init__(self, **kwargs):
        super(HomingScreenPrepare, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def on_enter(self):
        self.m.set_led_colour("ORANGE")
        if self.m.is_squaring_XY_needed_after_homing == True:
            self.instruction_label.text = self.l.get_str(
                "Ensure SmartBench is clear and remove extraction hose from Z head."
            )
        else:
            self.instruction_label.text = self.l.get_str("Ensure SmartBench is clear.")

    def begin_homing(self):
        self.sm.get_screen("homing_active").cancel_to_screen = self.cancel_to_screen
        self.sm.get_screen("homing_active").return_to_screen = self.return_to_screen
        self.sm.current = "homing_active"

    def cancel(self):
        self.sm.current = self.cancel_to_screen

    def update_strings(self):
        self.press_to_home_label.text = self.l.get_str("Then, press button to home.")
        if self.m.is_squaring_XY_needed_after_homing == True:
            self.instruction_label.text = self.l.get_str(
                "Ensure SmartBench is clear and remove extraction hose from Z head."
            )
        else:
            self.instruction_label.text = self.l.get_str("Ensure SmartBench is clear.")
        self.update_font_size(self.press_to_home_label, self.instruction_label)

    # Update both labels together because they should have the same font size
    def update_font_size(self, value1, value2):
        if self.l.get_text_length(value1.text) > 100:
            value1.font_size = self.default_font_size
            value2.font_size = self.default_font_size
        else:
            value1.font_size = self.default_font_size - 0.0025 * Window.width
            value2.font_size = self.default_font_size - 0.0025 * Window.width
