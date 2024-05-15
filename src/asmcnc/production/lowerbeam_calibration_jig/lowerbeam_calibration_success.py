import os
import sys

from asmcnc.comms.logging import log_exporter
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from asmcnc.core_UI import console_utils

Builder.load_string("""
<LBCalibrationSuccess>:
    success_label:success_label

    canvas:
        Color:
            rgba: hex('#4CAF50FF')
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
            padding: app.get_scaled_tuple([10.0, 0.0])
            size_hint_y: 0.2
            size_hint_x: 0.5
            font_size: app.get_scaled_width(20.0)

        GridLayout:
            cols: 1
            rows: 2

            Label:
                id: success_label
                text: 'Database updated for '
                font_size: app.get_scaled_width(50.0)
            
            Button:
                on_press: console_utils.shutdown()
                text: 'OK, SHUT DOWN'
                font_size: app.get_scaled_width(30.0)
                size_hint_y: 0.2
                size_hint_x: 0.3

""")


class LBCalibrationSuccess(Screen):
    def __init__(self, **kwargs):
        super(LBCalibrationSuccess, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    def enter_prev_screen(self):
        self.sm.current = 'lbc4'

    def set_serial_no(self, serial_no):
        self.success_label.text = 'Database updated for: ' + serial_no
