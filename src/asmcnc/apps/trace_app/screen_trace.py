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
from asmcnc.bluetooth_controller import input_map, popup_pairing, sdl_joystick_hotplug
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.skavaUI import widget_virtual_bed, widget_status_bar
from asmcnc.skavaUI import popup_info

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

from asmcnc.core_UI.utils import color_provider

Builder.load_string("""
#:import hex kivy.utils.get_color_from_hex
#:import color_provider asmcnc.core_UI.utils.color_provider

# Flat image button used in the right-hand tray - red flash on press to match
# the equivalent tray on the Home/Go screens.
<TraceIconButton@Button>:
    background_color: hex('#F4433600')
    background_normal: ''
    background_down: ''
    on_release: self.background_color = hex('#F4433600')
    on_press: self.background_color = hex('#F44336FF')

# Rounded, colour-filled text button - the trace app's standard action button.
# Recolour via bg_rgba; the pressed shade is derived from it automatically.
# Sizes throughout this screen are tuned for Console XL (1280x768 usable) -
# the trace app is only ever run on that console.
<TraceActionButton@Button>:
    bg_rgba: color_provider.get_rgba('primary')
    background_color: 0, 0, 0, 0
    background_normal: ''
    background_down: ''
    color: color_provider.get_rgba('white')
    font_size: sp(22)
    halign: 'center'
    valign: 'middle'
    text_size: self.size
    canvas.before:
        Color:
            # bg_rgba can briefly be None while the rule is first applied
            rgba: (0, 0, 0, 0) if not self.bg_rgba else ((self.bg_rgba[0] * 0.72, self.bg_rgba[1] * 0.72, self.bg_rgba[2] * 0.72, self.bg_rgba[3]) if self.state == 'down' else self.bg_rgba)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(8)]

# White rounded panel used to group each functional area on the grey screen.
<TraceCard@BoxLayout>:
    canvas.before:
        Color:
            rgba: color_provider.get_rgba('shapes_white')
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(8)]

<TraceScreenClass>:
    xy_move_container: xy_move_container
    virtual_bed_container: virtual_bed_container
    geometry_preview_container: geometry_preview_container
    geometry_status_label: geometry_status_label
    status_bar_container: status_bar_container

    canvas.before:
        Color:
            rgba: color_provider.get_rgba('grey')
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'

        # Main content row
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.92

            # Padded content area: actions/jog on the left, previews on the right
            BoxLayout:
                orientation: 'horizontal'
                padding: [dp(8), dp(8)]
                spacing: dp(8)

                # Left column - fixed width so the jog pad below stays square
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: None
                    width: dp(0.46 * app.height)
                    spacing: dp(8)

                    # Action buttons
                    TraceCard:
                        orientation: 'vertical'
                        padding: [dp(8), dp(8)]

                        GridLayout:
                            cols: 2
                            spacing: dp(8)

                            TraceActionButton:
                                text: 'Capture Point'
                                bg_rgba: color_provider.get_rgba('green')
                                on_press: root.add_segment()

                            TraceActionButton:
                                text: 'Close Contour'
                                bg_rgba: color_provider.get_rgba('primary')
                                on_press: root.close_contour()

                            TraceActionButton:
                                text: 'Run Points'
                                bg_rgba: color_provider.get_rgba('secondary')
                                on_press: root.run_through_points()

                            TraceActionButton:
                                text: 'Clear Geometry'
                                bg_rgba: color_provider.get_rgba('red')
                                on_press: root.clear()

                            TraceActionButton:
                                text: 'Export SVG'
                                bg_rgba: color_provider.get_rgba('blue')
                                on_press: root.export_svg()

                            TraceActionButton:
                                text: 'Setup Controller'
                                bg_rgba: color_provider.get_rgba('dark_grey')
                                on_press: root.open_controller_pairing()

                            TraceActionButton:
                                text: 'Trace Arc (soon)'
                                bg_rgba: color_provider.get_rgba('grey')
                                color: color_provider.get_rgba('dark_grey')
                                on_press: root.stub_curve_tracing('arc')

                            TraceActionButton:
                                text: 'Trace Curve (soon)'
                                bg_rgba: color_provider.get_rgba('grey')
                                color: color_provider.get_rgba('dark_grey')
                                on_press: root.stub_curve_tracing('bezier')

                    # XY jog pad
                    TraceCard:
                        id: xy_move_container
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(0.46 * app.height)
                        padding: [dp(10), dp(10)]

                # Right column - geometry preview above the live bed view
                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(8)

                    # Geometry preview card, with status header and recent points footer
                    TraceCard:
                        orientation: 'vertical'
                        padding: [dp(12), dp(8)]
                        spacing: dp(6)

                        Label:
                            id: geometry_status_label
                            text: root.status_text
                            font_size: sp(26)
                            color: color_provider.get_rgba('dark_grey')
                            size_hint_y: None
                            height: dp(34)
                            text_size: self.size
                            halign: 'left'
                            valign: 'middle'

                        BoxLayout:
                            id: geometry_preview_container

                        BoxLayout:
                            orientation: 'horizontal'
                            size_hint_y: None
                            height: dp(52)
                            spacing: dp(8)

                            Label:
                                text: 'Recent points\\n(tap to revisit)'
                                font_size: sp(15)
                                color: color_provider.get_rgba('dark_grey')
                                size_hint_x: None
                                width: dp(120)
                                halign: 'left'
                                valign: 'middle'
                                text_size: self.size

                            BoxLayout:
                                id: recent_points_container
                                orientation: 'horizontal'
                                spacing: dp(8)

                    # Virtual bed widget
                    TraceCard:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(0.46 * app.height)

                        BoxLayout:
                            id: virtual_bed_container
                            padding: [dp(0.0125) * app.width, dp(0.0208333333333) * app.height]

            # RHS button tray - global actions, consistent with the Home/Go screens
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: None
                width: dp(0.1 * app.width)
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

    # SDL2 reports raw int16 axis values (range +/-32768)
    JOYSTICK_AXIS_MAX = 32768.0
    JOYSTICK_RAW_DEADZONE = 1000

    # Set True to log every jog command sent and every ack received, with
    # timing, to asmcnc's logger - handy for tuning JOYSTICK_JOG_DT/timeout
    # against real round-trip behaviour. Fairly verbose; turn off once done.
    JOYSTICK_DEBUG_LOGGING = True

    # Nominal execution time (seconds) per jog command if it were run in
    # isolation. Each jog's distance is derived from the current feed so it
    # takes roughly this long to run - matching GRBL's own guidance for
    # continuous jogging (see https://github.com/gnea/grbl/wiki/Grbl-v1.1-Jogging
    # and https://www.billiam.org/2022/05/30/grbl-smooth-jogging).
    JOYSTICK_JOG_DT = 0.15

    # How many jog commands we allow to be queued (sent but not yet acked) at
    # once. This is the key lever for hiccups vs responsiveness:
    #   - 1 (strict wait-for-ack) means GRBL has zero lookahead - the instant
    #     an ack takes even slightly longer than the segment's execution time,
    #     the queue runs dry, the machine decelerates to a full stop, and the
    #     next command has to start from a standstill. That's the "goes fine
    #     for a while then hiccups a lot" pattern - the log showed ack times
    #     jump from ~0.01s to a *sustained* ~0.25-0.28s for several seconds
    #     with the exact same command being resent, i.e. GRBL had nothing
    #     queued ahead and was pacing acks to its own execution time.
    #   - A small window (2) keeps one segment always queued ahead, so GRBL
    #     never runs out of motion to blend into, without flooding it with an
    #     unbounded backlog (which is what made direction changes laggy
    #     before). A direction change still flushes the whole window
    #     immediately via quit_jog() rather than waiting it out.
    JOYSTICK_MAX_COMMANDS_IN_FLIGHT = 2

    # Safety net: if GRBL stops acking entirely (e.g. a dropped byte), don't
    # get stuck waiting forever - allow sending again after this long
    # regardless, measured from the last time we managed to send anything.
    JOYSTICK_JOG_ACK_TIMEOUT = 0.9

    JOG_COMMAND_INTERVAL = 0.08

    # How often (seconds) to check for newly connected joysticks while on this
    # screen - cheap (a couple of ctypes calls when nothing changed).
    JOYSTICK_HOTPLUG_POLL_INTERVAL = 5

    status_text = StringProperty('Awaiting geometry...')

    current_pulse_opacity = 1
    pulse_poll = None
    joystick_hotplug_poll = None

    def __init__(self, **kwargs):
        super(TraceScreenClass, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.l = kwargs["localization"]
        self.kb = kwargs["keyboard"]
        self.cs = self.m.cs

        self.points = []
        self.shapes = [Shape()]

        # Joystick state - entirely separate from the on-screen move widget's
        # own jog state (widget_xy_move_trace.py). They use different jog
        # mechanisms (continuous $J=G91 streaming here vs discrete
        # jog_absolute_single_axis/jog_relative there) and are tuned/debugged
        # independently, so neither should reach into the other.
        self.joystick_active = False
        self.joystick_max_feed = 8000
        self.joystick_slow_jog_factor = 4
        self.joystick_slow_jog_active = False
        self._jog_commands_in_flight = 0
        self._jog_command_last_sent_at = 0
        self._jog_command_sent_times = []  # FIFO of send timestamps, for per-ack latency logging

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

        # User-reassignable controller bindings (see the pairing popup's
        # "Configure controls"). Defaults reproduce the previous hardcoded
        # mapping: face buttons A/B/X/Y and the platform-specific stick axes.
        self.input_map = input_map.ControllerInputMap(
            app_id='trace',
            actions=[
                ('capture_point', 'Capture point', 0, self.add_segment),
                ('toggle_jog_speed', 'Toggle jog speed', 1, self.toggle_joystick_jog_speed),
                ('close_contour', 'Close contour', 2, self.close_contour),
                ('run_through_points', 'Run through points', 3, self.run_through_points),
            ],
            axes=[
                ('jog_x', 'Jog left/right',
                 {'axis': 1 if sys.platform.startswith('linux') else 4, 'sign': 1}),
                ('jog_y', 'Jog up/down',
                 {'axis': 0 if sys.platform.startswith('linux') else 3, 'sign': 1}),
            ],
        )

        self.m.s.bind(jog_ack_count=self.on_jog_ack)
        Clock.schedule_interval(self.send_joystick_jog_command, self.JOG_COMMAND_INTERVAL)

        self.clear()

    def on_enter(self):
        self.m.laser_on()
        self.pulse_poll = Clock.schedule_interval(self.update_pulse_opacity, 0.04)
        # Pick up any controller that (re)connected over Bluetooth since the
        # app booted, and keep checking while on this screen so a pad switched
        # on mid-session starts working without any further interaction
        # (Kivy 1.10.1 never opens joysticks that appear after startup).
        sdl_joystick_hotplug.open_new_joysticks()
        self.joystick_hotplug_poll = Clock.schedule_interval(
            lambda dt: sdl_joystick_hotplug.open_new_joysticks(), self.JOYSTICK_HOTPLUG_POLL_INTERVAL)
        self.input_map.activate()

    def on_leave(self, *args):
        self.m.laser_off()
        if self.pulse_poll:
            Clock.unschedule(self.pulse_poll)
        if self.joystick_hotplug_poll:
            Clock.unschedule(self.joystick_hotplug_poll)
        self.input_map.deactivate()

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

    def toggle_joystick_jog_speed(self):
        # Switches the joystick's own jogging between full and slow speed
        # (deliberately separate from the on-screen widget's speed toggle)
        self.joystick_slow_jog_active = not self.joystick_slow_jog_active

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
        # GRBL has responded (ok or error) to one of our outstanding commands,
        # freeing up a slot in our small lookahead window. Acks arrive in the
        # same order commands were sent, so the oldest sent-time is the one
        # this ack corresponds to.
        if self._jog_commands_in_flight > 0:
            self._jog_commands_in_flight -= 1
        latency = None
        if self._jog_command_sent_times:
            latency = time.time() - self._jog_command_sent_times.pop(0)
        if self.JOYSTICK_DEBUG_LOGGING:
            Logger.info("Trace app joystick: ack received after {}, {} still in flight".format(
                "{:.3f}s".format(latency) if latency is not None else "?",
                self._jog_commands_in_flight))

    def send_joystick_jog_command(self, *args):
        if self.sm.current != self.name:
            return

        joystick_x = self._apply_deadzone(self.input_map.get_axis('jog_x'))
        joystick_y = self._apply_deadzone(self.input_map.get_axis('jog_y'))

        if joystick_x == 0 and joystick_y == 0:
            # Only cancel a jog that the joystick itself started - otherwise this
            # would also cancel jogs started by holding a direction button.
            if self.joystick_active:
                self.joystick_active = False
                self._jog_commands_in_flight = 0
                self._jog_command_sent_times = []
                if self.m.s.m_state.lower() != 'idle':
                    self.m.quit_jog()
            return

        base_max_feed = self._max_joystick_feed()
        max_feed = base_max_feed / self.joystick_slow_jog_factor \
            if self.joystick_slow_jog_active else base_max_feed

        feedrate = int((abs(joystick_x) + abs(joystick_y)) * max_feed)
        feedrate = max(min(feedrate, max_feed), 1)

        if self._jog_commands_in_flight >= self.JOYSTICK_MAX_COMMANDS_IN_FLIGHT:
            # Window is full - let GRBL work through what's already queued
            # rather than piling on more. We deliberately do NOT try to cancel
            # and cut in early on a direction change here: quit_jog() is a
            # realtime command, but our serial layer drains the whole regular
            # command queue before the realtime queue on every pass, so a
            # "cancel, then immediately send the new direction" pair can
            # actually reach GRBL as [new command, new command, cancel] -
            # wiping out the fresh command along with the stale one. Instead,
            # just wait for the next free slot; because it always uses
            # whatever the stick is doing *then*, a direction change is still
            # picked up within one short segment, without the race.
            if time.time() - self._jog_command_last_sent_at > self.JOYSTICK_JOG_ACK_TIMEOUT:
                # Safety net: acks seem to have stopped arriving entirely.
                if self.JOYSTICK_DEBUG_LOGGING:
                    Logger.info("Trace app joystick: ack timeout, resetting in-flight count")
                self._jog_commands_in_flight = 0
                self._jog_command_sent_times = []
            else:
                return

        self.joystick_active = True

        # Distance = speed * time, so each jog command takes about
        # JOYSTICK_JOG_DT to run when direction/speed stays constant.
        distance = (feedrate / 60.0) * self.JOYSTICK_JOG_DT
        jog_x_dist = -joystick_x * distance
        jog_y_dist = -joystick_y * distance

        self._jog_commands_in_flight += 1
        self._jog_command_last_sent_at = time.time()
        self._jog_command_sent_times.append(self._jog_command_last_sent_at)

        jog_command = "$J=G91 X{:.2f} Y{:.2f} F{}".format(jog_x_dist, jog_y_dist, feedrate)
        if self.JOYSTICK_DEBUG_LOGGING:
            Logger.info("Trace app joystick: sending {} (stick=({:.2f}, {:.2f}), {} in flight)".format(
                jog_command, joystick_x, joystick_y, self._jog_commands_in_flight))
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

    def open_controller_pairing(self):
        popup_pairing.PopupControllerPairing(self.sm, self.l, input_map=self.input_map)

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
        container = self.ids.recent_points_container
        container.clear_widgets()

        if not self.points:
            container.add_widget(
                Label(text='None yet', font_size='18sp', halign='left', valign='middle',
                      color=color_provider.get_rgba('dark_grey')))
            return

        recent_points = self.points[-3:]
        first_point_number = len(self.points) - len(recent_points) + 1

        for offset, point in enumerate(recent_points):
            point_number = first_point_number + offset
            display_x = self.m.grbl_x_max_travel - point.x
            display_y = self.m.grbl_y_max_travel - point.y
            is_latest = point_number == len(self.points)
            chip = Factory.TraceActionButton(
                text="#{}  {:.0f}, {:.0f}".format(point_number, display_x, display_y),
                font_size='20sp',
                on_press=self.get_move_func(point))
            if is_latest:
                chip.bg_rgba = color_provider.get_rgba('secondary')
            else:
                chip.bg_rgba = color_provider.get_rgba('grey')
                chip.color = color_provider.get_rgba('dark_grey')
            container.add_widget(chip)

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
