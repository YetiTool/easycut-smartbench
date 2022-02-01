from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

import datetime

Builder.load_string("""
<ZHeadQC7>:
    BoxLayout:
        orientation: 'vertical'

        GridLayout:
            cols: 2
            rows: 1
            size_hint_y: 0.15
            valign: 'top'

            Button:
                text: '<<< Back'
                on_press: root.enter_prev_screen()
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]
                font_size: dp(20)

            Button:
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]
                text: 'STOP'
                background_color: [1,0,0,1]

        Button:
            text: 'CYCLE Z HEAD'
            font_size: dp(30)
            size_hint_y: 0.3
            size_hint_z: 0.3

""")

class ZHeadQC7(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQC7, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    def enter_prev_screen(self):
        self.sm.current = 'qc2'