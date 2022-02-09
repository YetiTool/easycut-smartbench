from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_string("""
<LBCalibration2>:
    
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

class LBCalibration2(Screen):
    def __init__(self, **kwargs):
        super(LBCalibration2, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    #temporary hack to fake calibration

    def on_enter(self):
        self.run_calibration()

    def run_calibration(self):
        Clock.schedule_once(self.enter_next_screen, 5)

    def enter_next_screen(self, dt):
        self.sm.current = 'lbc3'