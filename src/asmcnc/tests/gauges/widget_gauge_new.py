from __future__ import division

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Color
from kivy.properties import NumericProperty, ObjectProperty


Builder.load_string("""
<LoadGauge>:
    wrapper:wrapper
    outer_box:outer_box
    inner_box:inner_box
    title_label:title_label
    value_label:value_label
    peak_line:peak_line

    GridLayout:
        id: wrapper
        size_hint: None, None
        pos: self.parent.pos
        rows: 2

        GridLayout:
            size: self.parent.size
            cols: 2

            Label:
                id: title_label
                color: 0, 0, 0, 1

            Label:
                id: value_label
                color: 0, 0, 0, 1

        BoxLayout:
            id: outer_box
            orientation: 'vertical'
            size_hint: None, None
            # height: self.parent.height

            canvas:
                Color:
                    rgba: 0, 0, 0, 1

                Line:
                    width: 2
                    rectangle: self.x, self.y, self.width, self.height
            
            BoxLayout:
                id: inner_box
                size_hint: None, None
                height: self.parent.height

                canvas:
                    Color:
                        rgba: root.r, root.g, root.b, 1

                    Rectangle:
                        pos: [self.parent.center_x, self.parent.center_y - (0.5 * self.height)]
                        size: self.size

                BoxLayout:
                    id: peak_line
                    size_hint: None, None
                    pos: [self.parent.center_x, self.parent.center_y]
                    
                    canvas:
                        Color:
                            rgba: 0, 0, 0, 1

                        Line:
                            points: self.parent.parent.center_x + root.peak_value, self.center_y - (0.5 * self.height), self.parent.parent.center_x + root.peak_value, self.center_y + (0.5 * self.height)
""")

class LoadGauge(Widget):
    r = NumericProperty(0)
    g = NumericProperty(0)
    b = NumericProperty(0)

    peak_value = 0

    sm = ObjectProperty()
    m = ObjectProperty()

    def __init__(self, **kwargs):
        super(LoadGauge, self).__init__(**kwargs)

        self.bind(r=self.redraw)

        # max of 10 values
        self.value_stack = []

    def set_title(self, title):
        self.title_label.text = title

    def set_max_value(self, max_value):
        self.max_value = max_value

    def set_size(self, width, height):
        self.size_hint = None, None

        self.outer_box.width = 150

        self.height = height
        self.outer_box.height = height
        self.wrapper.height = height
        self.inner_box.height = height - (0.05 * height)

    def set_boundaries(self, warning_percentage, error_percentage):
        self.warning_percentage = warning_percentage
        self.error_percentage = error_percentage

    def set_value(self, value):
        if value == -999:
            value = 0

        width = ((self.outer_box.width / self.max_value) * value) / 2
        
        self.add_value_to_stack(width)

        self.value_label.text = str(value)

        self.inner_box.width = width

        if abs(float(value) / float(self.max_value)) > self.error_percentage:
            self.r = 1
            self.g = 0
            self.b = 0
        elif abs(float(value) / float(self.max_value)) > self.warning_percentage:
            self.r = 1
            self.g = 1
            self.b = 0
        else:
            self.r = 0
            self.g = 1
            self.b = 0

    def animate_width(self, el, width):
        self.inner_box.width = width

    def redraw(self, *args):
        with self.inner_box.canvas:
            Color(self.r, self.g, self.b, 1)
    
    def add_value_to_stack(self, value):
        if len(self.value_stack) == 10:
            self.value_stack.pop(0)
            self.value_stack.append(value)
        else:
            self.value_stack.append(value)
        
        peak_value = max(self.value_stack, key=abs)

        self.peak_value = peak_value