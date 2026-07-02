"""
Live preview of captured trace geometry, drawn directly on a Kivy canvas.

@author: Benji
"""
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import ListProperty, NumericProperty

from asmcnc.core_UI.utils import color_provider


class GeometryPreview(Widget):
    """
    Draws a scaled outline of the machine bed plus the captured points/segments.
    Coordinates are expected in bed-mm space: positive, origin at the machine home corner.
    """

    points = ListProperty([])
    bed_width = NumericProperty(2500.0)
    bed_height = NumericProperty(1300.0)

    def __init__(self, **kwargs):
        super(GeometryPreview, self).__init__(**kwargs)
        self.bind(pos=self.redraw, size=self.redraw, points=self.redraw,
                  bed_width=self.redraw, bed_height=self.redraw)

    def set_geometry(self, points, bed_width, bed_height):
        if bed_width:
            self.bed_width = bed_width
        if bed_height:
            self.bed_height = bed_height
        self.points = list(points)

    def _bed_to_pixels(self, x, y, scale, origin_x, origin_y):
        # Screen-horizontal follows the bed's Y axis and screen-vertical follows
        # the bed's X axis, to match the orientation used by the VirtualBed widget.
        px = origin_x + y * scale
        py = origin_y + (self.bed_width - x) * scale
        return px, py

    def redraw(self, *args):
        self.canvas.clear()

        if self.width <= 0 or self.height <= 0 or self.bed_width <= 0 or self.bed_height <= 0:
            return

        scale = min(self.width / self.bed_height, self.height / self.bed_width)
        draw_width = self.bed_height * scale
        draw_height = self.bed_width * scale
        origin_x = self.x + (self.width - draw_width) / 2.0
        origin_y = self.y + (self.height - draw_height) / 2.0

        with self.canvas:
            Color(*color_provider.get_rgba('grey'))
            Line(rectangle=(origin_x, origin_y, draw_width, draw_height), width=1)

            if not self.points:
                return

            if len(self.points) >= 2:
                Color(*color_provider.get_rgba('primary'))
                line_points = []
                for x, y in self.points:
                    line_points.extend(self._bed_to_pixels(x, y, scale, origin_x, origin_y))
                Line(points=line_points, width=2)

            Color(*color_provider.get_rgba('secondary'))
            point_radius = 4
            for x, y in self.points:
                px, py = self._bed_to_pixels(x, y, scale, origin_x, origin_y)
                Rectangle(pos=(px - point_radius, py - point_radius),
                          size=(point_radius * 2, point_radius * 2))
