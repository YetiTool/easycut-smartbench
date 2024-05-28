from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
import datetime

Builder.load_string(
    """
<ZHeadQC5>:
    canvas:
        Color:
            rgba: hex('#FF9E40FF')
        Rectangle:
            pos:self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1.00

        GridLayout:
            cols: 1
            rows: 2

            Label:
                text: 'Calibration complete!'
                font_size: dp(50)
            
            Button:
                on_press: root.enter_next_screen()
                text: 'OK'
                font_size: dp(30)
                size_hint_y: 0.2
                size_hint_x: 0.3

"""
)


class ZHeadQC5(Screen):

    def __init__(self, **kwargs):
        self.sm = kwargs.pop("sm")
        self.m = kwargs.pop("m")
        super(ZHeadQC5, self).__init__(**kwargs)

    def enter_next_screen(self):
        self.sm.current = "qcDB1"
