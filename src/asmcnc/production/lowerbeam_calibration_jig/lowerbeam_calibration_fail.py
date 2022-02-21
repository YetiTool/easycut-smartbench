from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

import os, sys

Builder.load_string("""
<LBCalibrationFail>:
    success_label:success_label

    canvas:
        Color:
            rgba: [1,0,0,1]
        Rectangle:
            pos:self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1.00

        Button:
            text: '<<< Back'
            on_press: root.enter_prev_screen()
            text_size: self.size
            markup: 'True'
            halign: 'left'
            valign: 'middle'
            padding: [dp(10),0]
            size_hint_y: 0.2
            size_hint_x: 0.5
            font_size: dp(20)

        GridLayout:
            cols: 1
            rows: 2

            Label:
                id: success_label
                text: 'Database update failed'
                font_size: dp(50)
            
            Button:
                on_press: root.retry_send()
                text: 'RETRY DATA SEND'
                font_size: dp(30)
                size_hint_y: 0.2
                size_hint_x: 0.3

""")

class LBCalibrationFail(Screen):
    def __init__(self, **kwargs):
        super(LBCalibrationFail, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    def enter_prev_screen(self):
        self.sm.current = 'lbc4'

    def retry_send(self):
        self.sm.current = 'lbc4'

    def set_serial_no(self, serial_no):
        self.success_label.text = 'Database update failed: ' + serial_no
