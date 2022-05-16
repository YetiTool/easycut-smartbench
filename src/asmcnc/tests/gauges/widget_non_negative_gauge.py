from __future__ import division

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty, ObjectProperty

def get_hsl_by_percentage(percentage):
    return (120 * (1 - percentage)) / 360, 1, 1

def get_gradient(value, max_value, lower_boundary=15, upper_boundary=15, inverse=False):
    if abs(float(value) / float(max_value)) * 100 < lower_boundary:
        return (0, 1, 1) if inverse else (120 / 360, 1, 1)

    if abs(float(value) / float(max_value)) * 100 > 100 - upper_boundary:
        return (120 / 360, 1, 1) if inverse else (0, 1, 1)

    # logic behind gradient?
    percentage = float(value) / float(max_value) 

    return get_hsl_by_percentage(percentage)


Builder.load_string("""
<PositiveLoadGauge>:
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

        BoxLayout:
            cols: 2

            Label:
                id: title_label
                size_hint_x: 0.65
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                color: 0, 0, 0, 1

            Label:
                id: value_label
                size_hint_x: 0.35
                text_size: self.size
                halign: 'right'
                valign: 'middle'
                color: 0, 0, 0, 1
                
        BoxLayout:
            id: outer_box
            orientation: 'vertical'
            size_hint: None, None
            # height: self.parent.height

            canvas:
                Color:
                    rgba: 0, 0, 0, 0.8

                Line:
                    width: 2
                    rectangle: self.x, self.y, self.width, self.height

            BoxLayout:
                id: inner_box
                size_hint: None, None
                height: self.parent.height

                canvas:
                    Color:
                        hsv: root.h, root.s, root.l
                        a: 1

                    Rectangle:
                        pos: [self.pos[0] + 2, self.parent.center_y - (0.5 * self.height)]
                        size: self.size
                        
                BoxLayout:
                    id: peak_line
                    size_hint: None, None
                    pos: [self.parent.center_x, self.parent.center_y]

                    canvas:
                        Color:
                            rgba: 0, 0, 0, 1

                        Line:
                            points: self.parent.parent.pos[0] + root.peak_value, self.parent.parent.center_y - (0.5 * self.parent.height), self.parent.parent.pos[0] + root.peak_value, self.parent.parent.center_y + (0.5 * self.parent.height)
""")


def mean(values):
    return float(sum(values) / max(len(values), 1))


class PositiveLoadGauge(Widget):
    h = NumericProperty(0)
    s = NumericProperty(1)
    l = NumericProperty(1)

    peak_value = NumericProperty(0)

    sm = ObjectProperty()
    m = ObjectProperty()

    def __init__(self, **kwargs):
        super(PositiveLoadGauge, self).__init__(**kwargs)

        self.bind(h=self.redraw)
        self.bind(peak_value=self.redraw_peak)

        self.max_value = 100
        self.inverse_boundaries = False
        self.peak_visibility = True
        self.unit = ''
        self.peak_line_avg = False

        self.lower_bound = 15
        self.upper_bound = 15

        self.value_stack = []

    def set_unit(self, unit):
        self.unit = unit

    def redraw_peak(self, *args):
        peak_value = self.peak_value
        self.peak_line.canvas.clear()
        with self.peak_line.canvas:
            Color(0, 0, 0, 1)
            Line(points=(self.outer_box.pos[0] + peak_value, self.outer_box.center_y - (0.5 * self.inner_box.height),
                         self.outer_box.pos[0] + peak_value, self.outer_box.center_y + (0.5 * self.inner_box.height)),
                 close=True)

    def set_title(self, title):
        self.title_label.text = title

    def set_max_value(self, max_value):
        self.max_value = max_value

    def set_size(self, width, height):
        self.size_hint = None, None

        self.outer_box.width = 150
        self.height = height + 25
        self.outer_box.height = height
        self.wrapper.height = height + 25
        self.wrapper.width = 150
        self.inner_box.height = height - (0.08 * height)

    def set_boundaries(self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def set_value(self, value, dt=None):
        if value == -999 or value < 0:
            value = 0

        width = ((self.outer_box.width / self.max_value) * value)

        if value >= self.max_value:
            width = ((self.outer_box.width / self.max_value) * self.max_value) - 3

        if self.inverse_boundaries:
            width = ((self.outer_box.width / self.max_value) * abs(value - self.max_value)) - 3

        if self.peak_visibility:
            self.add_value_to_stack(width)

        self.value_label.text = str(value) + ' ' + self.unit

        if self.peak_line_avg:
            self.inner_box.width = mean(self.value_stack)
        else:
            self.inner_box.width = width

        colour = get_gradient(value, self.max_value, inverse=self.inverse_boundaries, upper_boundary=self.upper_bound,
                              lower_boundary=self.lower_bound)

        self.h = colour[0]
        self.s = colour[1]
        self.l = colour[2]

    def animate_width(self, el, width):
        self.inner_box.width = width

    def redraw(self, *args):
        with self.inner_box.canvas:
            Color(self.h, self.s, self.l, 1)

    def set_inverse_boundaries(self, value):
        self.inverse_boundaries = value

    def set_peak_visibility(self, value):
        self.peak_visibility = value

    def add_value_to_stack(self, value):
        if len(self.value_stack) == 10:
            self.value_stack.pop(0)
            self.value_stack.append(value)
        else:
            self.value_stack.append(value)

        peak_value = max(self.value_stack, key=abs)
        avg_value = mean(self.value_stack)

        if self.peak_line_avg:
            self.peak_value = avg_value
        else:
            self.peak_value = peak_value

    def set_peak_line_avg(self, peak_line_avg):
        self.peak_line_avg = peak_line_avg

