"""
Live preview of captured trace geometry, drawn directly on a Kivy canvas.

@author: Benji
"""
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle, Mesh
from kivy.properties import ListProperty, NumericProperty

from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.core_UI.utils import color_provider

try:
    from kivy.graphics.tesselator import Tesselator
except ImportError:
    Tesselator = None

# Cycled through by shape index so each closed shape gets a distinct fill.
SHAPE_FILL_COLOURS = [
    (0.96, 0.87, 0.20, 0.55),  # yellow
    (0.30, 0.69, 0.99, 0.55),  # light blue
    (0.99, 0.60, 0.20, 0.55),  # orange
    (0.61, 0.35, 0.71, 0.55),  # purple
    (0.40, 0.73, 0.42, 0.55),  # green
    (0.94, 0.38, 0.57, 0.55),  # pink
    (0.25, 0.80, 0.80, 0.55),  # teal
    (0.65, 0.55, 0.35, 0.55),  # brown
]


class GeometryPreview(Widget):
    """
    Draws a scaled outline of the machine bed plus the captured shapes.
    Coordinates are expected in bed-mm space: positive, origin at the machine home corner.

    `shapes` is a list of (points, is_closed) pairs, where points is a list of
    (x, y) tuples. Closed shapes are filled with a colour unique to their
    position in the list; the in-progress (not yet closed) shape is left as an
    outline only.
    """

    shapes = ListProperty([])
    bed_width = NumericProperty(2500.0)
    bed_height = NumericProperty(1300.0)

    def __init__(self, **kwargs):
        super(GeometryPreview, self).__init__(**kwargs)
        self.bind(pos=self.redraw, size=self.redraw, shapes=self.redraw,
                  bed_width=self.redraw, bed_height=self.redraw)

    def set_geometry(self, shapes, bed_width, bed_height):
        if bed_width:
            self.bed_width = bed_width
        if bed_height:
            self.bed_height = bed_height
        self.shapes = [(list(points), bool(is_closed)) for points, is_closed in shapes]

    def _bed_to_pixels(self, x, y, scale, origin_x, origin_y):
        # Screen-horizontal follows the bed's Y axis and screen-vertical follows
        # the bed's X axis, to match the orientation used by the VirtualBed widget.
        px = origin_x + y * scale
        py = origin_y + (self.bed_width - x) * scale
        return px, py

    def _draw_fill(self, pixel_points):
        # Best-effort polygon fill via Kivy's tesselator. If it's unavailable, or
        # fails for any reason (degenerate/self-intersecting shape, etc.), just
        # skip the fill - the outline/points are still drawn, so the shape stays
        # visible either way.
        if Tesselator is None:
            return
        try:
            tess = Tesselator()
            tess.add_contour(pixel_points)
            if tess.tesselate():
                for vertices, indices in tess.meshes:
                    Mesh(vertices=vertices, indices=indices, mode='triangle_fan')
        except Exception:
            Logger.warning("Trace app: failed to fill shape preview")

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

            for shape_index, (shape_points, is_closed) in enumerate(self.shapes):
                pixel_points = []
                for x, y in shape_points:
                    pixel_points.extend(self._bed_to_pixels(x, y, scale, origin_x, origin_y))

                if is_closed and len(shape_points) >= 3:
                    Color(*SHAPE_FILL_COLOURS[shape_index % len(SHAPE_FILL_COLOURS)])
                    self._draw_fill(pixel_points)

                if len(shape_points) >= 2:
                    Color(*color_provider.get_rgba('primary'))
                    Line(points=pixel_points, width=2)

                Color(*color_provider.get_rgba('secondary'))
                point_radius = 4
                for x, y in shape_points:
                    px, py = self._bed_to_pixels(x, y, scale, origin_x, origin_y)
                    Rectangle(pos=(px - point_radius, py - point_radius),
                              size=(point_radius * 2, point_radius * 2))
