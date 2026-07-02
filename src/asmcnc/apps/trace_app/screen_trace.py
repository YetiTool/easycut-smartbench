"""
Created on 18 Aug 2024
Trace app: lets an operator jog the laser crosshair around a physical object and
capture points to build up a 2D outline, which can be replayed or exported as an SVG.

@author: Benji
"""
import os
import time

from kivy.clock import Clock
from kivy.properties import StringProperty

from asmcnc.apps.trace_app import widget_xy_move_trace, widget_geometry_preview
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.skavaUI import widget_virtual_bed
from asmcnc.skavaUI import popup_info

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

Builder.load_string("""
#:import color_provider asmcnc.core_UI.utils.color_provider

<TraceScreenClass>:
    xy_move_container: xy_move_container
    virtual_bed_container: virtual_bed_container
    geometry_preview_container: geometry_preview_container
    geometry_status_label: geometry_status_label

    canvas.before:
        Color:
            rgba: color_provider.get_rgba('shapes_white')
        Rectangle:
            pos: self.pos
            size: self.size

    GridLayout:
        cols: 2
        row_default_height: dp(0.5 * app.height)
        row_force_default: True

        ### Top ###

        # Buttons
        BoxLayout:
            padding: [10, 10]
            spacing: 10
            size_hint_x: None
            size_hint_y: None
            height: dp(0.5 * app.height)
            width: self.height
            orientation: 'vertical'

            GridLayout:
                cols: 2

                Button:
                    background_color: hex('#F4433600')
                    on_release: self.background_color = hex('#F4433600')
                    on_press:
                        root.home()
                        self.background_color = hex('#F44336FF')
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        padding: dp(8)
                        Image:
                            source: "./asmcnc/apps/trace_app/img/home_button.png"
                            allow_stretch: True

                Button:
                    background_color: hex('#F4433600')
                    on_release: self.background_color = hex('#F4433600')
                    on_press:
                        root.add_segment()
                        self.background_color = hex('#F44336FF')
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        padding: dp(8)
                        Image:
                            source: "./asmcnc/apps/trace_app/img/capture_point_button.png"
                            allow_stretch: True

                Button:
                    text: 'Clear geometry'
                    size_hint_x: 1
                    font_size: sp(20)
                    on_press: root.clear()

                Button:
                    text: 'Close contour'
                    size_hint_x: 1
                    font_size: sp(20)
                    on_press: root.close_contour()

                Button:
                    text: 'Exit app'
                    size_hint_x: 1
                    font_size: sp(20)
                    on_press: root.exit()

                Button:
                    text: 'Export SVG'
                    size_hint_x: 1
                    font_size: sp(20)
                    on_press: root.export_svg()

            Button:
                text: 'Stop'
                size_hint_x: 1
                size_hint_y: 0.5

                font_size: sp(38)
                on_press: root.stop()

            # Point display
            BoxLayout:
                orientation: 'vertical'

                Label:
                    text: 'Recent points'
                    font_size: sp(20)
                    color: color_provider.get_rgba('black')
                    size_hint_y: None
                    height: dp(0.08 * app.height)

                BoxLayout:
                    id: recent_points_container
                    orientation: 'horizontal'
                    size_hint_x: 1
                    size_hint_y: None
                    height: dp(0.08 * app.height)

        # Geometry preview
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 1
            canvas.before:
                Color:
                    rgba: color_provider.get_rgba('shapes_white')
                Rectangle:
                    size: self.size
                    pos: self.pos

            Label:
                id: geometry_status_label
                text: root.status_text
                font_size: sp(24)
                color: color_provider.get_rgba('black')
                size_hint_y: None
                height: dp(0.06 * app.height)

            BoxLayout:
                id: geometry_preview_container
                size_hint_y: 1

        ### Bottom ###

        # XY move widget
        BoxLayout:
            id: xy_move_container
            orientation: 'vertical'
            size_hint: (None, None)
            padding: [10, 10]
            height: dp(0.5 * app.height)
            width: self.height

        # Virtual bed widget
        BoxLayout:
            orientation: 'vertical'
            canvas:
                Color:
                    rgba: color_provider.get_rgba('shapes_white')
                Rectangle:
                    size: self.size
                    pos: self.pos

            BoxLayout:
                id: virtual_bed_container
                size_hint_y: 1
                padding: [dp(0.0125) * app.width, dp(0.0208333333333) * app.height]
                canvas:
                    Color:
                        rgba: color_provider.get_rgba('shapes_white')
                    Rectangle:
                        size: self.size
                        pos: self.pos
""")


class Point(object):
    def __init__(self, x, y):
        self.x = round(x, 1)
        self.y = round(y, 1)

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)


class Segment(object):
    """
    A line (or, in future, an arc) between two already-captured points.
    Points are stored in bed-mm space: positive values, origin at the machine home corner.
    """

    def __init__(self, start, end, radius_x=None, radius_y=None):
        self.start = start
        self.end = end
        self.radius_x = radius_x
        # If only one radius is given, assume the arc is circular rather than elliptical
        self.radius_y = radius_y if radius_y else radius_x

    @property
    def is_arc(self):
        return bool(self.radius_x)

    def to_svg_path_command(self):
        if self.is_arc:
            return "A {} {} 0 0 1 {} {}".format(self.radius_x, self.radius_y, self.end.x, self.end.y)
        return "L {} {}".format(self.end.x, self.end.y)


class TraceScreenClass(Screen):
    JOB_CACHE_DIR = './jobCache/'

    # Joystick axis IDs (SDL2 mapping: axis 0 = left stick Y, axis 1 = left stick X)
    JOYSTICK_AXIS_X = 1
    JOYSTICK_AXIS_Y = 0

    # SDL2 reports raw int16 axis values (range +/-32768)
    JOYSTICK_AXIS_MAX = 32768.0
    JOYSTICK_RAW_DEADZONE = 1000

    JOG_COMMAND_INTERVAL = 0.08

    status_text = StringProperty('Awaiting geometry...')

    current_pulse_opacity = 1
    pulse_poll = None

    def __init__(self, **kwargs):
        super(TraceScreenClass, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.l = kwargs["localization"]
        self.cs = self.m.cs

        self.points = []
        self.geometry_segments = []

        # Joystick state
        self.joystick_axis_x_raw = 0
        self.joystick_axis_y_raw = 0
        self.joystick_max_feed = 8000
        self.joystick_current_max_feed = self.joystick_max_feed
        self.joystick_movement_vector_max = 5
        self.joystick_movement_vector_current_max = self.joystick_movement_vector_max
        self.joystick_slow_factor = 4
        self.joystick_slow_mode = False

        # Widgets
        self.xy_move_widget = widget_xy_move_trace.XYMoveTrace(
            machine=self.m, localization=self.l, screen_manager=self.sm
        )
        self.xy_move_container.add_widget(self.xy_move_widget)
        self.virtual_bed_container.add_widget(
            widget_virtual_bed.VirtualBed(machine=self.m, screen_manager=self.sm)
        )

        self.geometry_preview = widget_geometry_preview.GeometryPreview()
        self.geometry_preview_container.add_widget(self.geometry_preview)

        Window.bind(on_joy_axis=self.on_joy_axis)
        Window.bind(on_joy_button_down=self.on_joy_button_down)
        Clock.schedule_interval(self.send_joystick_jog_command, self.JOG_COMMAND_INTERVAL)

        self.clear()

    def on_enter(self):
        self.m.laser_on()
        self.pulse_poll = Clock.schedule_interval(self.update_pulse_opacity, 0.04)

    def on_leave(self, *args):
        self.m.laser_off()
        if self.pulse_poll:
            Clock.unschedule(self.pulse_poll)

    def update_pulse_opacity(self, dt):
        # Pulse overlay by smoothly alternating between 0 and 1 opacity
        # Hacky way to track pulsing on or off without a variable by storing that information in the opacity value
        if self.current_pulse_opacity <= 0:
            self.current_pulse_opacity = 0.01
        elif self.current_pulse_opacity >= 1:
            self.current_pulse_opacity = 0.98
        elif int(("%.2f" % self.current_pulse_opacity)[-1]) % 2 == 1:
            self.current_pulse_opacity += 0.1
        else:
            self.current_pulse_opacity -= 0.1

        self.xy_move_widget.check_zh_at_datum(self.current_pulse_opacity)

    # --- Joystick handling -------------------------------------------------

    def on_joy_axis(self, window, stick_id, axis_id, value):
        if axis_id == self.JOYSTICK_AXIS_X:
            self.joystick_axis_x_raw = value
        elif axis_id == self.JOYSTICK_AXIS_Y:
            self.joystick_axis_y_raw = value

    def on_joy_button_down(self, window, stick_id, button_id):
        if button_id == 0:  # A button
            self.add_segment()
        elif button_id == 1:  # B button - toggle slow jog mode
            self.joystick_slow_mode = not self.joystick_slow_mode
            if self.joystick_slow_mode:
                self.joystick_current_max_feed = self.joystick_max_feed / self.joystick_slow_factor
                self.joystick_movement_vector_current_max = self.joystick_movement_vector_max / self.joystick_slow_factor
            else:
                self.joystick_current_max_feed = self.joystick_max_feed
                self.joystick_movement_vector_current_max = self.joystick_movement_vector_max
        elif button_id == 2:  # X button
            self.close_contour()
        elif button_id == 3:  # Y button
            self.run_through_points()

    def _apply_deadzone(self, raw_value):
        if abs(raw_value) <= self.JOYSTICK_RAW_DEADZONE:
            return 0.0
        return float(raw_value) / self.JOYSTICK_AXIS_MAX

    def send_joystick_jog_command(self, *args):
        if self.sm.current != self.name:
            return

        joystick_x = self._apply_deadzone(self.joystick_axis_x_raw)
        joystick_y = self._apply_deadzone(self.joystick_axis_y_raw)

        if joystick_x == 0 and joystick_y == 0:
            if self.m.s.m_state.lower() != 'idle':
                self.m.quit_jog()
            return

        jog_x_dist = -joystick_x * self.joystick_movement_vector_current_max
        jog_y_dist = -joystick_y * self.joystick_movement_vector_current_max

        feedrate = int((abs(joystick_x) + abs(joystick_y)) * self.joystick_current_max_feed)
        feedrate = max(min(feedrate, self.joystick_current_max_feed), 0)

        jog_command = "$J=G91 X{:.2f} Y{:.2f} F{}".format(jog_x_dist, jog_y_dist, feedrate)
        self.m.s.write_command(jog_command)

    # --- Machine actions -----------------------------------------------------

    def exit(self):
        self.m.laser_off()
        self.sm.current = 'lobby'
        self.clear()

    def clear(self):
        self.points = []
        self.geometry_segments = []
        self.refresh_geometry_display()
        self.refresh_recent_points_display()

    def home(self):
        self.m.request_homing_procedure('trace', 'trace')

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)

    def capture_point(self):
        # Make sure the machine has stopped moving before trusting the reported position
        if self.m.s.m_state.lower() != 'idle':
            return None
        current_x, current_y = self.cs.laser_position.get_x(), self.cs.laser_position.get_y()
        return Point(abs(current_x), abs(current_y))

    def add_segment(self):
        new_point = self.capture_point()
        if new_point is None:
            return
        if self.points and self.points[-1] == new_point:
            return

        if self.points:
            self.geometry_segments.append(Segment(self.points[-1], new_point))
        self.points.append(new_point)

        self.refresh_geometry_display()
        self.refresh_recent_points_display()

    def close_contour(self):
        if len(self.points) < 2 or self.points[-1] == self.points[0]:
            return

        self.geometry_segments.append(Segment(self.points[-1], self.points[0]))
        self.points.append(self.points[0])

        self.refresh_geometry_display()
        self.refresh_recent_points_display()

    def run_through_points(self):
        for point in self.points:
            self.m.s.write_command('G0 G53 X{} Y{} F8000'.format(-point.x, -point.y))

    def get_move_func(self, point):
        def move(*args):
            self.m.s.write_command('G0 G53 X{} Y{} F8000'.format(-point.x, -point.y))
        return move

    # --- Display ---------------------------------------------------------

    def refresh_recent_points_display(self):
        self.ids.recent_points_container.clear_widgets()

        if not self.points:
            self.ids.recent_points_container.add_widget(
                Label(text='Awaiting geometry...', font_size=20, color=(0, 0, 0, 1)))
            return

        for point in self.points[-3:]:
            display_x = self.m.grbl_x_max_travel - point.x
            display_y = self.m.grbl_y_max_travel - point.y
            button_text = "{:.0f}, {:.0f}".format(display_x, display_y)
            button = Button(text=button_text, font_size=20, on_press=self.get_move_func(point))
            self.ids.recent_points_container.add_widget(button)

    def refresh_geometry_display(self):
        if not self.points:
            self.status_text = 'Awaiting geometry...'
        elif self.points[0] == self.points[-1] and len(self.points) > 1:
            self.status_text = '{} points captured - contour closed'.format(len(self.points))
        else:
            self.status_text = '{} points captured'.format(len(self.points))

        self.geometry_preview.set_geometry(
            [(point.x, point.y) for point in self.points],
            self.m.grbl_x_max_travel,
            self.m.grbl_y_max_travel,
        )

    # --- SVG export --------------------------------------------------------

    def build_svg_string(self):
        if not self.points:
            return None

        path_data = ["M {} {}".format(self.points[0].x, self.points[0].y)]
        for segment in self.geometry_segments:
            path_data.append(segment.to_svg_path_command())
        path_string = " ".join(path_data)

        width = self.m.grbl_x_max_travel
        height = self.m.grbl_y_max_travel

        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="{width}mm" height="{height}mm" '
            'viewBox="0 0 {width} {height}">'
            '<path d="{path}" fill="yellow" stroke="blue" stroke-width="5"/>'
            '</svg>'
        ).format(width=width, height=height, path=path_string)

    def export_svg(self):
        svg_string = self.build_svg_string()
        if not svg_string:
            popup_info.PopupError(self.sm, self.l, self.l.get_str('No geometry has been captured yet.'))
            return

        filename = 'trace_{}.svg'.format(time.strftime('%Y%m%d_%H%M%S'))
        filepath = os.path.join(self.JOB_CACHE_DIR, filename)

        with open(filepath, 'w') as f:
            f.write(svg_string)

        Logger.info("Trace app: exported SVG to {}".format(filepath))
        popup_info.PopupMiniInfo(self.sm, self.l, self.l.get_str('Saved to') + '\njobCache/' + filename)
