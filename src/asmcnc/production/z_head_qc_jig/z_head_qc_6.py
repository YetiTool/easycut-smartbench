from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
import datetime
Builder.load_string(
    """
<ZHeadQC6>:
    ok_button:ok_button

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1.00

        GridLayout:
            cols: 1
            rows: 3

            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                text: '28. Set wheels and leadscrew(s)'
                font_size: dp(0.0625*app.width)

            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                text: '29. Install top plate'
                font_size: dp(0.0625*app.width)
            
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                id: ok_button
                disabled: 'True'
                on_press: root.enter_next_screen()
                text: 'OK'
                font_size: dp(0.0375*app.width)
                size_hint_y: 0.4
                size_hint_x: 0.3

"""
    )


class ZHeadQC6(Screen):

    def __init__(self, **kwargs):
        super(ZHeadQC6, self).__init__(**kwargs)
        self.sm = kwargs['sm']
        self.m = kwargs['m']

    def on_enter(self):
        Clock.schedule_once(self.enable_button, 2)

    def enable_button(self, dt):
        self.ok_button.disabled = False

    def on_leave(self):
        self.ok_button.disabled = True

    def enter_next_screen(self):
        self.sm.current = 'qc7'
