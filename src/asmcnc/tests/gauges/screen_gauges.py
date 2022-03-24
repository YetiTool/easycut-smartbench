from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import  Button
from asmcnc.tests.gauges.widget_gauge import Gauge

Builder.load_string("""
<GaugeScreen>:
    BoxLayout:
        orientation: 'vertical'

        size: self.parent.size
        pos: self.parent.pos    

""")

class GaugeScreen(Screen):
    def __init__(self, **kwargs):
        super(GaugeScreen, self).__init__(**kwargs)

        self.m = kwargs['m']
        self.sm = kwargs['sm']

    def add_gauge(self, gauge):
        self.add_widget(gauge)
        self.start_overnight_test()
    
    def run_load_test(self):
        
        pass