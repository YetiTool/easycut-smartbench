from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.properties import NumericProperty
from kivy.graphics import Color
from kivy.animation import Animation

Builder.load_string("""
<CircleGauge>:
    BoxLayout:
        orientation: 'vertical'
        size_hint: None, None
        center: self.parent.center

        canvas:
            Color:
                rgba: 1, 1, 1, 1
            Ellipse:
                size: 200, 200
                angle_start: 0
                angle_end: 360

        BoxLayout:
            size_hint: None, None
            canvas:
                Color:
                    rgba: 0, 0, 0, 1
                Ellipse:
                    size: 190, 190
                    angle_start: 0
                    angle_end: 360
""")

class CircleGauge(Widget):
    def __init__(self, **kwargs):
        super(CircleGauge, self).__init__(**kwargs)

    