from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_string("""
<ZHeadQC4>:
    
    canvas:
        Color:
            rgba: hex('#1976d2ff')

        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'

        Label:
            text: 'Calibrating...'
            font_size: dp(50)

    
""")

class ZHeadQC4(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQC4, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    #temporary hack to fake calibration

    def on_enter(self):
        self.run_calibration()

    def run_calibration(self):
        Clock.schedule_once(self.enter_next_screen, 5)

    def enter_next_screen(self, dt):
        self.sm.current = 'qc5'