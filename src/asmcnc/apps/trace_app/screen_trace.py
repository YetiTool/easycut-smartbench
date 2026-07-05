"""
Created on 18 Aug 2024
Trace app: lets an operator jog the laser crosshair around a physical object and
capture points to build up a 2D outline, which can be replayed or exported as an SVG.

@author: Benji
"""
import os
import sys
import time

from kivy.clock import Clock
from kivy.properties import StringProperty

from asmcnc.apps.trace_app import widget_xy_move_trace, widget_geometry_preview, popup_export_svg
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.skavaUI import widget_virtual_bed, widget_status_bar
from asmcnc.skavaUI import popup_info

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

Builder.load_string("""
#:import color_provider asmcnc.core_UI.utils.color_provider

<TraceIconButton@Button>:
    background_color: hex('#F4433600')
    background_normal: ''
    background_down: ''
    on_release: self.background_color = hex('#F4433600')
    on_press: self.background_color = hex('#F44336FF')

<TraceScreenClass>:
    xy_move_container: xy_move_container
    virtual_bed_container: virtual_bed_container
    geometry_preview_container: geometry_preview_container
    geometry_status_label: geometry_status_label
    status_bar_container: status_bar_container

    canvas.before:
        Color:
            rgba: color_provider.get_rgba('shapes_white')
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'

        # Main content row
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.9

            GridLayout:
                cols: 2
                size_hint_x: 0.9
                row_default_height: dp(0.46 * app.height)
                row_force_default: True

                ### Top ###

                # Buttons
                BoxLayout:
                    padding: [10, 10]
                    spacing: 10
                    size_hint_x: None
                    size_hint_y: None
                    height: dp(0.46 * app.height)
                    width: self.height
                    orientation: 'vertical'

                    GridLayout:
                        cols: 2

                        TraceIconButton:
                            text: 'Capture Point'
                            font_size: sp(18)
                            halign: 'center'
                            color: color_provider.get_rgba('black')
                            on_press: root.add_segment()

                        TraceIconButton:
                            text: 'Export SVG'
                            font_size: sp(18)
                            halign: 'center'
                            color: color_provider.get_rgba('black')
                            on_press: root.export_svg()

                        TraceIconButton:
                            text: 'Clear\\nGeometry'
                            font_size: sp(18)
                            halign: 'center'
                            color: color_provider.get_rgba('black')
                            on_press: root.clear()

                        TraceIconButton:
                            text: 'Close\\nContour'
                            font_size: sp(18)
                            halign: 'center'
                            color: color_provider.get_rgba('black')
                            on_press: root.close_contour()

                        TraceIconButton:
                            text: 'Trace Arc\\n(soon)'
                            font_size: sp(16)
                            halign: 'center'
                            color: color_provider.get_rgba('dark_grey')
                            on_press: root.stub_curve_tracing('arc')

                        TraceIconButton:
                            text: 'Trace Curve\\n(soon)'
                            font_size: sp(16)
                            halign: 'center'
                            color: color_provider.get_rgba('dark_grey')
                            on_press: root.stub_curve_tracing('bezier')

                    # Point display
                    BoxLayout:
                        orientation: 'vertical'

                        Label:
                            text: 'Recent points (capture order)'
                            font_size: sp(18)
                            color: color_provider.get_rgba('black')
                            size_hint_y: None
                            height: dp(0.08 * app.height)

                        BoxLayout:
                            id: recent_points_container
                            orientation: 'horizontal'
                            size_hint_x: 1
                            size_hint_y: None
                            height: dp(0.1 * app.height)

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
                    height: dp(0.46 * app.height)
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

            # RHS button tray - global actions, consistent with the Home/Go screens
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.1
                padding: [4, 4]
                spacing: dp(0.02 * app.height)
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 1
                    Rectangle:
                        size: self.size
                        pos: self.pos

                TraceIconButton:
                    on_press: root.home()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        padding: dp(8)
                        Image:
                            source: "./asmcnc/skavaUI/img/home.png"
                            allow_stretch: True

                TraceIconButton:
                    on_press: root.stop()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        padding: dp(8)
                        Image:
                            source: "./asmcnc/skavaUI/img/stop.png"
                            allow_stretch: True

                TraceIconButton:
                    on_press: root.exit()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        padding: dp(8)
                        Image:
                            source: "./asmcnc/skavaUI/img/quit_to_lobby_btn.png"
                            allow_stretch: True

        # Status bar
        BoxLayout:
            id: status_bar_container
            size_hint_y: 0.08
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


class Shape(object):
    """
    One contour being (or having been) traced: an ordered list of points and the
    segments joining them. A trace capture is a list of these, so an operator can
    close one shape and immediately carry on tracing the next one.
    """

    def __init__(self):
        self.points = []
        self.segments = []

    @property
    def is_closed(self):
        return len(self.points) > 1 and self.points[0] == self.points[-1]

    def add_point(self, point):
        if self.points:
            self.segments.append(Segment(self.points[-1], point))
        self.points.append(point)

    def close(self):
        if len(self.points) < 2 or self.is_closed:
            return False
        self.add_point(self.points[0])
        return True

    def to_svg_path_command(self):
        if not self.points:
            return None
        path_data = ["M {} {}".format(self.points[0].x, self.points[0].y)]
        path_data.extend(segment.to_svg_path_command() for segment in self.segments)
        return " ".join(path_data)


class TraceScreenClass(Screen):
    JOB_CACHE_DIR = './jobCache/'
    TRACE_CAPTURES_DIR = os.path.join(JOB_CACHE_DIR, 'trace_captures')

    # Cycled through by shape index so each closed shape gets a distinct SVG fill.
    # Kept in sync with SHAPE_FILL_COLOURS in widget_geometry_preview.py.
    SHAPE_FILL_COLOURS = ['F5DE33', '4CB0FC', 'FC9933', '9C59B5', '66BA6B', 'F0619A', '40CCCC', 'A68C59']

    if sys.platform.startswith("linux"):
        JOYSTICK_AXIS_X = 1
        JOYSTICK_AXIS_Y = 0
    else:
        JOYSTICK_AXIS_X = 4
        JOYSTICK_AXIS_Y = 3

    # SDL2 reports raw int16 axis values (range +/-32768)
    JOYSTICK_AXIS_MAX = 32768.0
    JOYSTICK_RAW_DEADZONE = 1000

    # Nominal execution time (seconds) per jog command. Each jog's distance is
    # derived from the current feed so it takes roughly this long to run - short
    # enough that a stale command can't linger, matching GRBL's own guidance for
    # continuous jogging (see https://github.com/gnea/grbl/wiki/Grbl-v1.1-Jogging
    # and https://www.billiam.org/2022/05/30/grbl-smooth-jogging).
    #
    # Tuned against this machine's GRBL settings: $120/$121 (accel) = 500mm/s^2,
    # $110/$111 (max rate) = 8000/6000mm/min (jog feed is now capped to the
    # tighter of the two - see _max_joystick_feed). At max jog feed (100mm/s),
    # time to reach full speed from a standstill is 100/500 = 0.2s.
    #
    # This needs to be comfortably longer than that, not just equal to it: each
    # segment also has to survive normal jitter in serial/ack round-trip time
    # without running out and decelerating to zero before the next command
    # arrives - that "ran dry, decelerated, had to re-accelerate" is the hiccup
    # you'd see after an occasional slow ack, even though most segments chain
    # together fine.
    JOYSTICK_JOG_DT = 0.3

    # Safety net: if GRBL never acks a jog (e.g. a dropped byte), don't get stuck
    # waiting forever - allow sending again after this long regardless. Kept
    # comfortably above the ~0.4s a segment can now legitimately take to
    # execute (accel + cruise at JOYSTICK_JOG_DT), so it stays a true fallback
    # rather than firing under normal operation.
    JOYSTICK_JOG_ACK_TIMEOUT = 0.9

    JOG_COMMAND_INTERVAL = 0.08

    status_text = StringProperty('Awaiting geometry...')

    current_pulse_opacity = 1
    pulse_poll = None

    def __init__(self, **kwargs):
        super(TraceScreenClass, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.l = kwargs["localization"]
        self.kb = kwargs["keyboard"]
        self.cs = self.m.cs

        self.points = []
        self.shapes = [Shape()]

        # Joystick state
        self.joystick_axis_x_raw = 0
        self.joystick_axis_y_raw = 0
        self.joystick_active = False
        self.joystick_max_feed = 8000
        self.joystick_slow_factor = 4
        self._jog_command_pending = False
        self._jog_command_sent_at = 0

        # Widgets
        self.xy_move_widget = widget_xy_move_trace.XYMoveTrace(
            machine=self.m, localization=self.l, screen_manager=self.sm
        )
        self.xy_move_container.add_widget(self.xy_move_widget)
        self.virtual_bed_widget = widget_virtual_bed.VirtualBed(machine=self.m, screen_manager=self.sm)
        self.virtual_bed_container.add_widget(self.virtual_bed_widget)

        self.geometry_preview = widget_geometry_preview.GeometryPreview()
        self.geometry_preview_container.add_widget(self.geometry_preview)

        self.status_bar_container.add_widget(
            widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        )

        Window.bind(on_joy_axis=self.on_joy_axis)
        Window.bind(on_joy_button_down=self.on_joy_button_down)
        self.m.s.bind(jog_ack_count=self.on_jog_ack)
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
        elif button_id == 1:  # B button - toggle slow jog mode, shared with the on-screen jog widget
            self.xy_move_widget.set_slow_mode(not self.xy_move_widget.is_slow_mode())
        elif button_id == 2:  # X button
            self.close_contour()
        elif button_id == 3:  # Y button
            self.run_through_points()

    def _apply_deadzone(self, raw_value):
        if abs(raw_value) <= self.JOYSTICK_RAW_DEADZONE:
            return 0.0
        return float(raw_value) / self.JOYSTICK_AXIS_MAX

    def _max_joystick_feed(self):
        # Cap to whichever is tightest: our own desired ceiling, or either
        # axis's real $110/$111 max rate. Without this, a direction with a real
        # Y-component gets silently slowed down by GRBL to respect $111 (which
        # on this machine is 6000mm/min, 25% below $110's 8000) - the app keeps
        # commanding/timing for the faster rate while GRBL actually executes
        # slower, which is what made Y-heavy jogging feel worse than X.
        max_feed = self.joystick_max_feed
        x_max_rate = self.m.s.setting_110
        y_max_rate = self.m.s.setting_111
        if x_max_rate > 0:
            max_feed = min(max_feed, x_max_rate)
        if y_max_rate > 0:
            max_feed = min(max_feed, y_max_rate)
        return max_feed

    def on_jog_ack(self, instance, value):
        # GRBL has responded (ok or error) to whatever we last sent it, so we're
        # clear to send the next jog command reflecting the current stick position.
        self._jog_command_pending = False

    def send_joystick_jog_command(self, *args):
        if self.sm.current != self.name:
            return

        joystick_x = self._apply_deadzone(self.joystick_axis_x_raw)
        joystick_y = self._apply_deadzone(self.joystick_axis_y_raw)

        if joystick_x == 0 and joystick_y == 0:
            # Only cancel a jog that the joystick itself started - otherwise this
            # would also cancel jogs started by holding a direction button.
            if self.joystick_active:
                self.joystick_active = False
                if self.m.s.m_state.lower() != 'idle':
                    self.m.quit_jog()
            return

        # Never have more than one jog command outstanding. GRBL processes
        # commands strictly in order, so sending on a fixed timer regardless of
        # whether GRBL has finished the last one builds up a backlog: a
        # direction change then has to wait for that whole backlog to drain,
        # and the feed that finally executes lags well behind the current stick
        # position. Waiting for the previous command's ack (see on_jog_ack)
        # keeps at most one command in flight, so this always reflects "now".
        if self._jog_command_pending:
            if time.time() - self._jog_command_sent_at < self.JOYSTICK_JOG_ACK_TIMEOUT:
                return
            # Safety net: GRBL never acked (e.g. a dropped byte) - don't get stuck.
            self._jog_command_pending = False

        self.joystick_active = True

        base_max_feed = self._max_joystick_feed()
        max_feed = base_max_feed / self.joystick_slow_factor \
            if self.xy_move_widget.is_slow_mode() else base_max_feed

        feedrate = int((abs(joystick_x) + abs(joystick_y)) * max_feed)
        feedrate = max(min(feedrate, max_feed), 1)

        # Distance = speed * time, so each jog command takes about
        # JOYSTICK_JOG_DT to run - short enough that motion stays responsive to
        # both direction and speed changes as soon as the next ack comes back.
        distance = (feedrate / 60.0) * self.JOYSTICK_JOG_DT
        jog_x_dist = -joystick_x * distance
        jog_y_dist = -joystick_y * distance

        self._jog_command_pending = True
        self._jog_command_sent_at = time.time()

        jog_command = "$J=G91 X{:.2f} Y{:.2f} F{}".format(jog_x_dist, jog_y_dist, feedrate)
        self.m.s.write_command(jog_command)

    # --- Machine actions -----------------------------------------------------

    def exit(self):
        self.m.laser_off()
        self.sm.current = 'lobby'
        self.clear()

    def clear(self):
        self.points = []
        self.shapes = [Shape()]
        self.refresh_geometry_display()
        self.refresh_recent_points_display()

    def home(self):
        self.m.request_homing_procedure('trace', 'trace')

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)

    def capture_point(self):
        # Machine coordinates are only meaningful relative to the physical bed once
        # homed - before that, MPos is relative to an arbitrary power-on reference,
        # which is what causes captured geometry to land outside the real bed (or
        # look flipped/scrambled) if a point is captured before homing.
        if not self.m.is_machine_homed and sys.platform != 'win32':
            popup_info.PopupHomingWarning(self.sm, self.m, self.l, 'trace', 'trace')
            return None

        # Make sure the machine has stopped moving before trusting the reported position
        if self.m.s.m_state.lower() != 'idle':
            return None

        current_x, current_y = self.cs.laser_position.get_x(), self.cs.laser_position.get_y()
        return Point(abs(current_x), abs(current_y))

    def add_segment(self):
        new_point = self.capture_point()
        if new_point is None:
            return

        current_shape = self.shapes[-1]
        if current_shape.points and current_shape.points[-1] == new_point:
            return

        current_shape.add_point(new_point)
        self.points.append(new_point)

        self.refresh_geometry_display()
        self.refresh_recent_points_display()

    def close_contour(self):
        current_shape = self.shapes[-1]
        if not current_shape.close():
            return

        self.points.append(current_shape.points[-1])

        # Start a fresh shape so the next captured point begins a new contour
        # rather than continuing this now-closed one.
        self.shapes.append(Shape())

        self.refresh_geometry_display()
        self.refresh_recent_points_display()

    def stub_curve_tracing(self, curve_type):
        # UI-only placeholder: arc/Bezier capture isn't implemented yet, but the
        # Segment/build_svg_string machinery already supports arcs (radius_x/
        # radius_y), so this just needs wiring up to real capture logic later.
        Logger.info("Trace app: '{}' curve tracing requested (not yet implemented)".format(curve_type))
        popup_info.PopupMiniInfo(self.sm, self.l, self.l.get_str('This feature is coming soon.'))

    def _spindle_target_for_point(self, point):
        # point.x/y store the LASER's position (see capture_point), so to send the
        # spindle back to its own original position - which is what puts the
        # LASER, not the spindle, back on the traced point - the laser offset has
        # to be un-applied here, the same way go_xy_datum_with_laser() does.
        return -point.x - self.m.laser_offset_x_value, -point.y - self.m.laser_offset_y_value

    def run_through_points(self):
        for point in self.points:
            target_x, target_y = self._spindle_target_for_point(point)
            self.m.s.write_command('G0 G53 X{} Y{} F8000'.format(target_x, target_y))

    def get_move_func(self, point):
        def move(*args):
            target_x, target_y = self._spindle_target_for_point(point)
            self.m.s.write_command('G0 G53 X{} Y{} F8000'.format(target_x, target_y))
        return move

    # --- Display ---------------------------------------------------------

    def refresh_recent_points_display(self):
        self.ids.recent_points_container.clear_widgets()

        if not self.points:
            self.ids.recent_points_container.add_widget(
                Label(text='Awaiting geometry...', font_size=20, color=(0, 0, 0, 1)))
            return

        recent_points = self.points[-3:]
        first_point_number = len(self.points) - len(recent_points) + 1

        for offset, point in enumerate(recent_points):
            point_number = first_point_number + offset
            display_x = self.m.grbl_x_max_travel - point.x
            display_y = self.m.grbl_y_max_travel - point.y
            is_latest = point_number == len(self.points)
            order_label = 'Latest (#{})'.format(point_number) if is_latest else '#{}'.format(point_number)
            button_text = "{}\n{:.0f}, {:.0f}".format(order_label, display_x, display_y)
            button = Button(text=button_text, font_size=16, halign='center',
                            on_press=self.get_move_func(point))
            self.ids.recent_points_container.add_widget(button)

    def refresh_geometry_display(self):
        closed_shape_count = sum(1 for shape in self.shapes if shape.is_closed)

        if not self.points:
            self.status_text = 'Awaiting geometry...'
        elif not closed_shape_count:
            self.status_text = '{} points captured'.format(len(self.points))
        else:
            self.status_text = '{} points captured - {} shape{} closed'.format(
                len(self.points), closed_shape_count, '' if closed_shape_count == 1 else 's')

        shapes_data = [([(point.x, point.y) for point in shape.points], shape.is_closed)
                       for shape in self.shapes if shape.points]

        self.geometry_preview.set_geometry(shapes_data, self.m.grbl_x_max_travel, self.m.grbl_y_max_travel)
        self.virtual_bed_widget.set_trace_geometry(shapes_data)

    # --- SVG export --------------------------------------------------------

    def build_svg_string(self):
        shapes_with_points = [shape for shape in self.shapes if shape.points]
        if not shapes_with_points:
            return None

        width = self.m.grbl_x_max_travel
        height = self.m.grbl_y_max_travel

        path_elements = []
        for shape_index, shape in enumerate(shapes_with_points):
            if shape.is_closed:
                fill = '#{}'.format(self.SHAPE_FILL_COLOURS[shape_index % len(self.SHAPE_FILL_COLOURS)])
            else:
                fill = 'none'
            path_elements.append('<path d="{}" fill="{}" stroke="blue" stroke-width="5"/>'.format(
                shape.to_svg_path_command(), fill))

        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="{width}mm" height="{height}mm" '
            'viewBox="0 0 {width} {height}">{paths}</svg>'
        ).format(width=width, height=height, paths="".join(path_elements))

    @staticmethod
    def _sanitize_filename(name):
        name = name.strip()
        for char in '/\\:*?"<>|':
            name = name.replace(char, '_')
        return name

    def _save_svg(self, svg_string, name):
        if not os.path.exists(self.TRACE_CAPTURES_DIR):
            os.makedirs(self.TRACE_CAPTURES_DIR)

        name = self._sanitize_filename(name) or time.strftime('%Y-%m-%d %H-%M')
        filename = name + '.svg'
        filepath = os.path.join(self.TRACE_CAPTURES_DIR, filename)

        with open(filepath, 'w') as f:
            f.write(svg_string)

        Logger.info("Trace app: exported SVG to {}".format(filepath))
        popup_info.PopupMiniInfo(self.sm, self.l, self.l.get_str('Saved to') + '\ntrace_captures/' + filename)

    def export_svg(self):
        svg_string = self.build_svg_string()
        if not svg_string:
            popup_info.PopupError(self.sm, self.l, self.l.get_str('No geometry has been captured yet.'))
            return

        default_name = time.strftime('%Y-%m-%d %H-%M')
        popup_export_svg.PopupExportSvg(
            self.sm, self.l, self.kb, default_name,
            on_confirm=lambda name: self._save_svg(svg_string, name)
        )
