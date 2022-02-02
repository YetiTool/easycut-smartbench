from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

import datetime

Builder.load_string("""
<ZHeadQC6>:
    ok_button:ok_button

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
                text: 'PUT BELT ON Z MOTOR'
                font_size: dp(50)
            
            Button:
                id: ok_button
                disabled: 'True'
                on_press: root.enter_next_screen()
                text: 'OK'
                font_size: dp(30)
                size_hint_y: 0.2
                size_hint_x: 0.3

""")

class ZHeadQC6(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQC6, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

        Clock.schedule_once(self.enable_button, 2)

    def enable_button(self, dt):
        self.ok_button.disabled = False

    def enter_next_screen(self):
        self.sm.current = 'qc7'

    def enter_prev_screen(self):
        self.sm.current = 'qc2'