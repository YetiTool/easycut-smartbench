from kivy.uix.screenmanager import Screen
from asmcnc.gauges.go_screen_gauge import GoScreenGauge
from kivy.lang import Builder

Builder.load_string("""
<GaugeTestScreen>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
""")

class GaugeTestScreen(Screen):
    def __init__(self, **kwargs):
        super(GaugeTestScreen, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

        self.gauge = GoScreenGauge(
            title='Gauge Test',
            key='TEST',
            max_value=100,
            lower_boundary=15,
            upper_boundary=15,
            inverse=False,
            unit='',
            factor=1,
            sm=self.sm,
            m=self.m
        )

        self.add_widget(self.gauge)
