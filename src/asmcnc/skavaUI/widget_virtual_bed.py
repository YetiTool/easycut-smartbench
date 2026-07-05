"""
Created on 1 Feb 2018
@author: Ed
"""
import kivy
from asmcnc.comms.logging_system.logging_system import Logger
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.uix.stencilview import StencilView
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Color, Line, Mesh, Rectangle

from asmcnc.core_UI.utils import color_provider

try:
    from kivy.graphics.tesselator import Tesselator
except ImportError:
    Tesselator = None

Builder.load_string(
    """
#:import color_provider asmcnc.core_UI.utils.color_provider

<VirtualBed>

    xBar:xBar
    carriage:carriage
    g54_zone:g54_zone
    g54_marker:g54_marker
    g28Marker:g28Marker
    virtual_bed_image:virtual_bed_image
    touch_zone:touch_zone
    laser_crosshair:laser_crosshair
    trace_geometry_overlay:trace_geometry_overlay

    StencilBox2:
        size: self.parent.size
        pos: self.parent.pos
        
        Scatter:
            do_rotation: False
            do_translation: True
            do_scale: True        
        
            Image:
                id: virtual_bed_image
                source: './asmcnc/skavaUI/img/virtual_bed.png'
                allow_stretch: True
                keep_ratio: False
                size: self.parent.size

                Image:
                    id: touch_zone
                    source: './asmcnc/skavaUI/img/virtual_bed_touch_zone.png'
                    opacity: 0
                    allow_stretch: True
                    keep_ratio: False
                    size: self.parent.size[0]-root.width_modifier, self.parent.size[1]-(0.125*app.height)
                    pos: self.parent.pos[0]+root.x_pos_modifier,self.parent.pos[1]+(0.0625*app.height)

                Image:
                    id: xBar
                    source: './asmcnc/skavaUI/img/virtual_x_bar.png'
                    allow_stretch: True
                    keep_ratio: True
                    height: self.parent.height
                    pos: self.parent.pos
                Image:
                    id: carriage
                    source: './asmcnc/skavaUI/img/virtual_carriage.png'
                    allow_stretch: True
                    keep_ratio: True
                    pos: self.parent.pos
                    width: (self.parent.width - (0.1*app.width))/6
                Image:
                    id: g54_zone
                    source: './asmcnc/skavaUI/img/virtual_g54_zone.png'
                    allow_stretch: True
                    keep_ratio: False
                    pos: self.parent.pos   
                    opacity: 0.7     
                Image:
                    id: g28Marker
                    source: './asmcnc/skavaUI/img/park.png'
                    allow_stretch: True
                    keep_ratio: True
                    width: self.parent.width/20
                    pos: self.parent.pos    
                Image:
                    id: g54_marker
                    source: './asmcnc/skavaUI/img/jobstart.png'
                    allow_stretch: True
                    keep_ratio: True
                    width: self.parent.width/10
                    pos: self.parent.pos

                # Live laser position, distinct from the carriage/z-head marker
                # above, so the physical offset between them is always visible.
                Widget:
                    id: laser_crosshair
                    size: self.parent.width/20, self.parent.width/20
                    pos: self.parent.pos
                    opacity: 0
                    canvas:
                        Color:
                            rgba: color_provider.get_rgba('red')
                        Line:
                            points: [self.x, self.center_y, self.x + self.width, self.center_y]
                            width: 1.2
                        Line:
                            points: [self.center_x, self.y, self.center_x, self.y + self.height]
                            width: 1.2
                        Line:
                            circle: (self.center_x, self.center_y, self.width / 3)
                            width: 1.2

                # Optional overlay for apps (e.g. trace_app) that want to draw
                # captured geometry on top of the bed preview. Empty/inert unless
                # a screen calls set_trace_geometry().
                Widget:
                    id: trace_geometry_overlay
                    pos: touch_zone.pos
                    size: touch_zone.size

"""
)


class StencilBox2(StencilView, BoxLayout):
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(StencilBox2, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(StencilBox2, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(StencilBox2, self).on_touch_up(touch)


class VirtualBed(Widget):
    # G54: workpiece co-ordinates
    # G28: set reference point
    width_modifier = NumericProperty()
    x_pos_modifier = NumericProperty()

    # Cycled through by shape index for any overlaid trace geometry (see
    # set_trace_geometry). Kept in visual sync with trace_app's own palette.
    TRACE_SHAPE_COLOURS = [
        (0.96, 0.87, 0.20, 0.55),  # yellow
        (0.30, 0.69, 0.99, 0.55),  # light blue
        (0.99, 0.60, 0.20, 0.55),  # orange
        (0.61, 0.35, 0.71, 0.55),  # purple
        (0.40, 0.73, 0.42, 0.55),  # green
        (0.94, 0.38, 0.57, 0.55),  # pink
        (0.25, 0.80, 0.80, 0.55),  # teal
        (0.65, 0.55, 0.35, 0.55),  # brown
    ]

    def __init__(self, **kwargs):
        super(VirtualBed, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self._trace_shapes = []
        self.trace_geometry_overlay.bind(pos=self._redraw_trace_geometry, size=self._redraw_trace_geometry)
        self.set_up_virtual_bed()

    def set_up_virtual_bed(self, dt=0):
        if self.m.grbl_y_max_travel == 3000.0:
            Clock.schedule_once(self.set_up_virtual_bed, 1)
            return
        if self.m.bench_is_standard():
            self.virtual_bed_image.source = "./asmcnc/skavaUI/img/virtual_bed.png"
            self.width_modifier = 0.1 * Window.width
            self.x_pos_modifier = 0.05 * Window.width
        if self.m.bench_is_short():
            self.virtual_bed_image.source = "./asmcnc/skavaUI/img/virtual_bed_mini.png"
            self.width_modifier = 0.4075 * Window.width
            self.x_pos_modifier = 0.20375 * Window.width
        Clock.schedule_interval(self.refresh_widget, self.m.s.STATUS_INTERVAL)

    def refresh_widget(self, dt):
        self.setG54PosByMachineCoords(self.m.x_wco(), self.m.y_wco())
        self.setG54SizePx()
        self.setG28PosByMachineCoords(self.m.g28_x(), self.m.g28_y())
        # Carriage marker always tracks the true physical z-head/spindle position,
        # same as every other screen using this widget. Trace app's captured
        # points (drawn via set_trace_geometry, below) are the ones that show the
        # laser-offset position - kept separate so the two are visually distinct.
        self.setCarriagePosByMachineCoords(self.m.mpos_x(), self.m.mpos_y())
        self.setLaserCrosshairPosByMachineCoords(
            self.m.mpos_x() + self.m.laser_offset_x_value,
            self.m.mpos_y() + self.m.laser_offset_y_value,
        )

    g54box_x0 = 0.0
    g54box_y0 = 0.0
    g54box_x1 = 0.0
    g54box_y1 = 0.0
    bedWidgetJogFeedrate = 30000

    def on_touch_down(self, touch):
        pass

    def setCarriagePosByTouch_andGo(self, touch):
        machineX = int(
            (touch.y - self.touch_zone.y)
            / self.touch_zone.height
            * self.m.grbl_x_max_travel
            - self.m.grbl_x_max_travel
        )
        machineY = int(
            (self.touch_zone.x + self.touch_zone.width - touch.x)
            / self.touch_zone.width
            * self.m.grbl_y_max_travel
            - self.m.grbl_y_max_travel
        )
        Logger.debug("Y: ", str(touch.y), str(self.touch_zone.y), str(self.touch_zone.pos[1]))
        self.m.quit_jog()
        self.m.jog_absolute_xy(machineX, machineY, self.bedWidgetJogFeedrate)

    def setG54SizePx(self):
        job_box = self.sm.get_screen("home").job_box
        self.g54box_x0 = (
            job_box.range_x[0] / self.m.grbl_x_max_travel * self.touch_zone.height
        )
        self.g54box_y0 = (
            job_box.range_y[0] / self.m.grbl_y_max_travel * self.touch_zone.width
        )
        self.g54box_x1 = (
            job_box.range_x[1] / self.m.grbl_x_max_travel * self.touch_zone.height
        )
        self.g54box_y1 = (
            job_box.range_y[1] / self.m.grbl_y_max_travel * self.touch_zone.width
        )
        self.g54_zone.width = self.g54box_y1 - self.g54box_y0
        self.g54_zone.height = self.g54box_x1 - self.g54box_x0

    def setG28PosByMachineCoords(self, x_mc_coords, y_mc_coords):
        pixel_datum = self.touch_zone.pos
        pixel_canvas = self.touch_zone.size
        pos_pixels_x = (
            pixel_datum[0]
            + pixel_canvas[0]
            - (y_mc_coords + self.m.grbl_y_max_travel)
            / self.m.grbl_y_max_travel
            * pixel_canvas[0]
        )
        pos_pixels_y = (
            pixel_datum[1]
            + (x_mc_coords + self.m.grbl_x_max_travel)
            / self.m.grbl_x_max_travel
            * pixel_canvas[1]
        )
        self.g28Marker.y = pos_pixels_y - self.g28Marker.height / 2
        self.g28Marker.x = pos_pixels_x - self.g28Marker.width / 2

    def setG54PosByMachineCoords(self, x_mc_coords, y_mc_coords):
        pixel_datum = self.touch_zone.pos
        pixel_canvas = self.touch_zone.size
        pos_pixels_x = (
            pixel_datum[0]
            + pixel_canvas[0]
            - (y_mc_coords + self.m.grbl_y_max_travel)
            / self.m.grbl_y_max_travel
            * pixel_canvas[0]
            - self.g54box_y1
        )
        pos_pixels_y = (
            pixel_datum[1]
            + (x_mc_coords + self.m.grbl_x_max_travel)
            / self.m.grbl_x_max_travel
            * pixel_canvas[1]
            + self.g54box_x0
        )
        self.g54_zone.y = pos_pixels_y
        self.g54_zone.x = pos_pixels_x
        pos_pixels_x = (
            pixel_datum[0]
            + pixel_canvas[0]
            - (y_mc_coords + self.m.grbl_y_max_travel)
            / self.m.grbl_y_max_travel
            * pixel_canvas[0]
        )
        pos_pixels_y = (
            pixel_datum[1]
            + (x_mc_coords + self.m.grbl_x_max_travel)
            / self.m.grbl_x_max_travel
            * pixel_canvas[1]
        )
        self.g54_marker.y = pos_pixels_y - self.g54_marker.height / 2
        self.g54_marker.x = pos_pixels_x - self.g54_marker.width / 2

    def setCarriagePosByMachineCoords(self, grbl_x, grbl_y):
        pixel_datum = self.touch_zone.pos
        pixel_canvas = self.touch_zone.size
        pixels_x = (
            pixel_datum[0]
            + pixel_canvas[0]
            - (grbl_y + self.m.grbl_y_max_travel)
            / self.m.grbl_y_max_travel
            * pixel_canvas[0]
        )
        pixels_y = (
            pixel_datum[1]
            + (grbl_x + self.m.grbl_x_max_travel)
            / self.m.grbl_x_max_travel
            * pixel_canvas[1]
        )
        self.carriage.x = pixels_x - self.carriage.width / 2
        self.carriage.y = pixels_y - self.carriage.height / 2
        self.xBar.x = pixels_x - self.xBar.width / 2

    def setLaserCrosshairPosByMachineCoords(self, grbl_x, grbl_y):
        if not self.m.is_laser_enabled:
            self.laser_crosshair.opacity = 0
            return
        self.laser_crosshair.opacity = 1

        pixel_datum = self.touch_zone.pos
        pixel_canvas = self.touch_zone.size
        pixels_x = (
            pixel_datum[0]
            + pixel_canvas[0]
            - (grbl_y + self.m.grbl_y_max_travel)
            / self.m.grbl_y_max_travel
            * pixel_canvas[0]
        )
        pixels_y = (
            pixel_datum[1]
            + (grbl_x + self.m.grbl_x_max_travel)
            / self.m.grbl_x_max_travel
            * pixel_canvas[1]
        )
        self.laser_crosshair.x = pixels_x - self.laser_crosshair.width / 2
        self.laser_crosshair.y = pixels_y - self.laser_crosshair.height / 2

    # --- Optional trace geometry overlay ------------------------------------
    # Lets a screen (e.g. trace_app) draw captured shapes directly on the bed
    # preview, using the same grbl-coords-to-pixel mapping as the carriage/G54
    # markers above. Points are given in "distance from machine home" space
    # (i.e. positive, same convention as trace_app's Point class) rather than
    # raw (negative) machine coordinates.

    def set_trace_geometry(self, shapes):
        """shapes: list of (points, is_closed) where points is a list of (x, y)
        tuples in positive distance-from-home space."""
        self._trace_shapes = [(list(points), bool(is_closed)) for points, is_closed in shapes]
        self._redraw_trace_geometry()

    def _point_to_pixel(self, point_x, point_y):
        pixel_datum = self.touch_zone.pos
        pixel_canvas = self.touch_zone.size
        px = (
            pixel_datum[0]
            + pixel_canvas[0]
            - (self.m.grbl_y_max_travel - point_y)
            / self.m.grbl_y_max_travel
            * pixel_canvas[0]
        )
        py = (
            pixel_datum[1]
            + (self.m.grbl_x_max_travel - point_x)
            / self.m.grbl_x_max_travel
            * pixel_canvas[1]
        )
        return px, py

    def _draw_trace_fill(self, pixel_points):
        # Best-effort polygon fill - if the tesselator is unavailable or fails,
        # just skip the fill; the outline is still drawn either way.
        if Tesselator is None:
            return
        try:
            tess = Tesselator()
            tess.add_contour(pixel_points)
            if tess.tesselate():
                for vertices, indices in tess.meshes:
                    Mesh(vertices=vertices, indices=indices, mode='triangle_fan')
        except Exception:
            Logger.warning("VirtualBed: failed to fill trace geometry overlay")

    def _redraw_trace_geometry(self, *args):
        self.trace_geometry_overlay.canvas.clear()

        if not self._trace_shapes or not self.m.grbl_x_max_travel or not self.m.grbl_y_max_travel:
            return

        with self.trace_geometry_overlay.canvas:
            for shape_index, (shape_points, is_closed) in enumerate(self._trace_shapes):
                if not shape_points:
                    continue

                pixel_points = []
                for x, y in shape_points:
                    pixel_points.extend(self._point_to_pixel(x, y))

                if is_closed and len(shape_points) >= 3:
                    Color(*self.TRACE_SHAPE_COLOURS[shape_index % len(self.TRACE_SHAPE_COLOURS)])
                    self._draw_trace_fill(pixel_points)

                if len(shape_points) >= 2:
                    Color(*color_provider.get_rgba('primary'))
                    Line(points=pixel_points, width=2)

                Color(*color_provider.get_rgba('secondary'))
                point_radius = 4
                for i in range(0, len(pixel_points), 2):
                    px, py = pixel_points[i], pixel_points[i + 1]
                    Rectangle(pos=(px - point_radius, py - point_radius),
                              size=(point_radius * 2, point_radius * 2))
