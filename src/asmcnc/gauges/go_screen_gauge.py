from __future__ import division

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock

from asmcnc.gauges.gauge_utils import get_gradient, calculate_width

Builder.load_string("""
<GoScreenGauge>:
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
                size_hint_x: 0.5
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                color: 0, 0, 0, 1

            Label:
                id: value_label
                size_hint_x: 0.5
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
                        hsv: root.hue, root.saturation, root.luminosity
                        a: 1

                    Rectangle:
                        pos: [self.parent.center_x, self.parent.center_y - (0.5 * self.height)]
                        size: self.size

                BoxLayout:
                    size_hint: None, None
                    pos: [self.parent.center_x, self.parent.center_y]
                    
                    canvas:
                        Color: 
                            rgba: 0.5, 0.5, 0.5, 1
                            
                        Line:
                            points: self.parent.parent.center_x, self.parent.parent.center_y - (0.5 * self.parent.height), self.parent.parent.center_x, self.parent.parent.center_y + (0.5 * self.parent.height)
                        
                BoxLayout:
                    id: peak_line
                    size_hint: None, None
                    pos: [self.parent.center_x, self.parent.center_y]
                    
                    canvas:
                        Color:
                            rgba: 0, 0, 0, 1

                        Line:
                            points: self.parent.parent.center_x + root.peak_value, self.parent.parent.center_y - (0.5 * self.parent.height), self.parent.parent.center_x + root.peak_value, self.parent.parent.center_y + (0.5 * self.parent.height)
""")


class GoScreenGauge(Widget):
    hue = NumericProperty(0)
    saturation = NumericProperty(1)
    luminosity = NumericProperty(1)

    sm = ObjectProperty()
    m = ObjectProperty()

    reading_clock = None

    peak_value = NumericProperty(0)
    current_value = NumericProperty(0)

    def __init__(self, title, key, max_value, lower_boundary=15, upper_boundary=15, inverse=False, unit='', factor=1, **kwargs):
        super(GoScreenGauge, self).__init__(**kwargs)

        self.bind(hue=self.redraw_colour)
        self.bind(peak_value=self.redraw_peak)
        self.bind(current_value=self.redraw_value)

        self.title = title
        self.title_label.text = title
        self.key = key
        self.max_value = max_value
        self.lower_boundary = lower_boundary
        self.upper_boundary = upper_boundary
        self.inverse = inverse
        self.unit = unit
        self.factor = factor

    def begin_reading(self):
        self.reading_clock = Clock.schedule_interval(self.update_reading, 0.1)

    def stop_reading(self):
        Clock.unschedule(self.reading_clock)

    def update_reading(self, dt):
        # if self.m.s.m_state == 'Idle':
        #     Clock.unschedule(self.reading_clock)
        #     return

        self.peak_value = self.m.s.get_peak_value_from_gauge_stack(self.key)
        self.current_value = self.m.s.get_value_from_gauge_stack(self.key)

    def set_sizes(self):
        # clean this mess - need to be variable and more accurate
        self.size_hint = None, None
        self.outer_box.width = 150
        self.height = 100 + 25
        self.outer_box.height = 100
        self.wrapper.height = 100 + 25
        self.wrapper.width = 150
        # 0.08 * 100 is probably not accurate for all values of height
        self.inner_box.height = 100 - (0.08 * 100)

    def redraw_colour(self, *args):
        with self.inner_box.canvas:
            Color(self.hue, self.saturation, self.luminosity)

    def redraw_peak(self, *args):
        self.peak_line.canvas.clear()
        with self.peak_line.canvas:
            Color(0, 0, 0, 1)
            Line(points=(
                self.outer_box.center_x + self.peak_value, self.outer_box.center_y - (0.5 * self.inner_box.height),
                self.outer_box.center_x + self.peak_value, self.outer_box.center_y + (0.5 * self.inner_box.height)),
                close=True)

    def redraw_value(self, *args):
        self.value_label.text = str(self.current_value) + ' ' + self.unit

        width = calculate_width(self.current_value, self.max_value, self.factor)

        self.inner_box.width = width

        colour = get_gradient(self.current_value, self.max_value, self.lower_boundary,
                              self.upper_boundary, self.inverse)

        self.hue, self.saturation, self.luminosity = colour

