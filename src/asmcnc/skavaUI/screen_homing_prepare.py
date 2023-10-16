"""
Created March 2019

@author: Ed

Prepare to home
"""
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from kivy.clock import Clock
Builder.load_string(
    """

<HomingScreenPrepare>:

    instruction_label:instruction_label
    press_to_home_label: press_to_home_label

    canvas:
        Color: 
            rgba: hex('#E5E5E5FF')
        Rectangle: 
            size: self.size
            pos: self.pos         

    BoxLayout: 
        spacing: 0
        padding: [0.025*app.width,0.0833333333333*app.height]
        orientation: 'vertical'

        # Cancel button
        BoxLayout:
            size_hint: (None,None)
            height: dp(0.0416666666667*app.height)
            padding: (0.025*app.width,0,0.025*app.width,0)
            spacing: 0.85*app.width
            orientation: 'horizontal'
            pos: self.parent.pos

            Label:
                text: ""

            Button:
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
            id: instruction_label
            size_hint_y: 2.3
            markup: True
            font_size: root.default_font_size
            valign: 'bottom'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            color: hex('#333333ff')

        Label:
            font_size: str(0.01875 * app.width) + 'sp'
            id: press_to_home_label
            size_hint_y: 2.3
            markup: True
            font_size: root.default_font_size
            valign: 'top'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            color: hex('#333333ff')

        # Label:
        #     size_hint_y: 0.1                

        Button:
            font_size: str(0.01875 * app.width) + 'sp'
            size_hint_y: 4.9
            background_color: hex('#FFFFFF00')
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
    cancel_to_screen = 'lobby'
    return_to_screen = 'lobby'
    default_font_size = 30

    def __init__(self, **kwargs):
        super(HomingScreenPrepare, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.update_strings()

    def on_enter(self):
        self.m.set_led_colour('ORANGE')
        if self.m.is_squaring_XY_needed_after_homing == True:
            self.instruction_label.text = self.l.get_str(
                'Ensure SmartBench is clear and remove extraction hose from Z head.'
                )
        else:
            self.instruction_label.text = self.l.get_str(
                'Ensure SmartBench is clear.')

    def begin_homing(self):
        self.sm.get_screen('homing_active'
            ).cancel_to_screen = self.cancel_to_screen
        self.sm.get_screen('homing_active'
            ).return_to_screen = self.return_to_screen
        self.sm.current = 'homing_active'

    def cancel(self):
        self.sm.current = self.cancel_to_screen

    def update_strings(self):
        self.press_to_home_label.text = self.l.get_str(
            'Then, press button to home.')
        if self.m.is_squaring_XY_needed_after_homing == True:
            self.instruction_label.text = self.l.get_str(
                'Ensure SmartBench is clear and remove extraction hose from Z head.'
                )
        else:
            self.instruction_label.text = self.l.get_str(
                'Ensure SmartBench is clear.')
        self.update_font_size(self.press_to_home_label, self.instruction_label)

    def update_font_size(self, value1, value2):
        if self.l.get_text_length(value1.text) > 100:
            value1.font_size = self.default_font_size
            value2.font_size = self.default_font_size
        else:
            value1.font_size = self.default_font_size - 2
            value2.font_size = self.default_font_size - 2
