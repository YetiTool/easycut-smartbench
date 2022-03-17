from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.skavaUI import popup_info

import datetime
import os, sys

Builder.load_string("""
<ZHeadQC7>:
    shutdown_button : shutdown_button

    BoxLayout:
        orientation: 'vertical'
        spacing: dp(15)

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

            Label:
                text: ''

        Button:
            id: shutdown_button
            text: 'FINISHED! - SHUT DOWN NOW'
            font_size: dp(30)
            size_hint_y: 0.55
            disabled: True
            on_press: root.shutdown_console()

""")

class ZHeadQC7(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQC7, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.l = kwargs['l']

    def on_enter(self):
        Clock.schedule_once(self.enable_button, 1)

    def enable_button(self, dt):
        self.shutdown_button.disabled = False

    def shutdown_console(self):
        if sys.platform != 'win32' and sys.platform != 'darwin': 
            os.system('sudo shutdown -h now')

    def enter_prev_screen(self):
        self.sm.current = 'qc6'
