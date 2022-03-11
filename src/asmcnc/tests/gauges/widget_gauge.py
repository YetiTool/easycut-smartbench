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
from functools import partial

Builder.load_string("""
<Gauge>:
    outer_box:outer_box
    inner_box:inner_box
    wrapper:wrapper
    value_label:value_label

    GridLayout:
        id: wrapper
        size_hint: None, None
        center: self.parent.center
        rows: 2

        BoxLayout:
            id: inner_box
            size_hint: None, None

            canvas:
                Color:
                    rgba: root.r,root.g,root.b,1

                Rectangle:
                    pos: self.pos
                    size: self.size
            
            BoxLayout:
                id: outer_box
                orientation: 'vertical'
                size_hint: None, None

                canvas:
                    Color:
                        rgba: 1, 1, 1, 1

                    Line:
                        width: 2
                        rectangle: self.x, self.y, self.width, self.height
    
        Label:
            id: value_label
            text: 'val here'
            halign: 'right'
            valign: 'top'
            size_hint: None, None
            text_size: self.size
            font_size: 28

""")

class Gauge(Widget):
    r = NumericProperty(0)
    g = NumericProperty(0)
    b = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

        self.bind(r=self.redraw)

    def set_title(self, title):
        self.title = title

    def set_max_value(self, max_value):
        self.max_value = max_value

    def set_boundaries(self, warning, error):
        self.warning_bound = warning
        self.error_bound = error

    def set_size(self, width, height):
        self.outer_box.width = width
        self.outer_box.height = height
        self.wrapper.height = height + 30
        self.wrapper.width = width + 20

    def set_value(self, value):
        required_width = (self.outer_box.width / self.max_value) * value

        anim = Animation(width=required_width, duration=0.05, t='in_quad')

        anim.start(self.inner_box)

        if required_width < 24 * len(str(value)):
            required_width = 24 * len(str(value))

        anim = Animation(width=required_width, duration=0.05, t='in_quad')

        anim.start(self.value_label)

        Clock.schedule_once(partial(self.set_text, value), 0.05)

        if float(value) / float(self.max_value) > self.error_bound:
            self.r = 1
            self.g = 0
            self.b = 0
        elif float(value) / float(self.max_value) > self.warning_bound:
            self.r = 1
            self.g = 1
            self.b = 0
        else:
            self.r = 0
            self.g = 1
            self.b = 0 

    def set_text(self, text, *largs):
        self.value_label.text = str(text)

    def redraw(self, *args):
        with self.inner_box.canvas:
            Color(self.r, self.g, self.b, 1)