"""
Created on 18 Aug 2024
Trace app concept screen

@author: Benji
"""
import svgwrite
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from kivy.clock import Clock
from matplotlib.path import Path

from asmcnc.apps.trace_app import widget_xy_move_trace
from asmcnc.skavaUI import widget_virtual_bed
from asmcnc.skavaUI import popup_info

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

Builder.load_string("""
#:import color_provider asmcnc.core_UI.utils.color_provider

<TraceScreenClass>:
    xy_move_container: xy_move_container
    virtual_bed_container: virtual_bed_container
    svg_container: svg_container
    
    canvas.before:
        Color:
            rgba: color_provider.get_rgba('shapes_white')
        Rectangle:
            pos: self.pos
            size: self.size
    
    GridLayout:
        cols: 2
        row_default_height: 768*0.5
        row_force_default: True
        
        ### Top ###
        
        # Buttons            
        BoxLayout:
            padding: [10, 10]
            spacing: 10
            size_hint_x: None
            size_hint_y: None
            height: dp(app.height * 0.5)
            width: self.height
            orientation: 'vertical'
            
            GridLayout:
                cols: 2
                
                Button:
                    text: 'Home machine'
                    allow_stretch: False
                    size_hint_x: 1
                    font_size: sp(20)
                    on_press: root.home()
                    
                Button:
                    text: 'Capture Point'
                    allow_stretch: False
                    size_hint_x: 1
                    font_size: sp(20)
                    on_press: root.add_segment()
                    
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
                    on_press: root.print_svg_string()
                    
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
                
        # SVG container
        BoxLayout:
            id: svg_container
            size_hint_y: 1
            canvas:
                Color:
                    rgba: color_provider.get_rgba('shapes_white')
                Rectangle:
                    size: self.size
                    pos: self.pos
            Label:
                text: 'Awaiting geometry...'
                font_size: sp(38)
                color: color_provider.get_rgba('black')
            
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
            # padding: [dp(0.025) * app.width, dp(0.0416666666667) * app.height]
            # spacing: dp(0.0416666666667) * app.height
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


class Point:
    def __init__(self, x, y):
        self.x = round(x, 1)
        self.y = round(y, 1)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)


class Segment:
    def __init__(self, start, end, radius_x=None, radius_y=None):
        self.start = Point(start.x, start.y)
        self.end = Point(end.x, end.y)
        self.radius_x = radius_x
        self.radius_y = radius_y

        self.type = self.determine_type(radius_x, radius_y)

        # If the segment is an arc, but only one radius is given, assume its circular not elliptical
        if self.type == 'arc' and not radius_y:
            self.radius_y = radius_x

        self.convert_to_svg_coordinate_space()

    def get_start(self, invert_xy=False):
        if invert_xy:
            return Point(self.start.y, self.start.x)
        return self.start

    def get_end(self):
        return self.end

    def __str__(self):
        return "({}, {})".format(self.start, self.end)

    @staticmethod
    def determine_type(radius_x, radius_y):
        if radius_x or radius_y:
            return 'arc'
        else:
            return 'line'

    def build_svg_string(self):
        if self.type == 'arc':
            return "A {} {} 0 0 1 {} {}".format(self.radius_x, self.radius_y, self.end.x, self.end.y)
        else:
            return "L {} {}".format(self.end.x, self.end.y)

    def convert_to_svg_coordinate_space(self):
        # Make coordinates positive
        self.start.x = abs(self.start.x)
        self.start.y = abs(self.start.y)
        self.end.x = abs(self.end.x)
        self.end.y = abs(self.end.y)

        # Swap X and Y axes to match SVG coordinate space
        self.start.x, self.start.y = self.start.y, self.start.x
        self.end.x, self.end.y = self.end.y, self.end.x

    def get_matplotlib_data(self):
        points = [(self.end.x, self.end.y)]
        codes = [Path.LINETO]
        return points, codes


class TraceScreenClass(Screen):
    geometry_segments = [Segment(Point(-1300, -2500), Point(0, 0))]
    previous_point = None

    def __init__(self, **kwargs):
        super(TraceScreenClass, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.l = kwargs["localization"]
        self.cs = self.m.cs

        # Joystick variables
        self.joystick_axis_max = 32768
        self.joystick_x_value = 0.0
        self.joystick_y_value = 0.0
        self.joystick_jog_feedrate = 0
        self.joystick_max_feed = 8000
        self.movement_vector_max = 15
        self.joystick_raw_deadzone = 100
        jog_command_interval = 0.2

        # Widgets
        self.xy_move_widget = widget_xy_move_trace.XYMoveTrace(
            machine=self.m, localization=self.l, screen_manager=self.sm
        )
        self.xy_move_container.add_widget(self.xy_move_widget)
        self.virtual_bed_container.add_widget(
            widget_virtual_bed.VirtualBed(machine=self.m, screen_manager=self.sm)
        )

        Window.bind(on_joy_axis=self.on_joy_axis)
        Clock.schedule_interval(self.send_joystick_jog_command, jog_command_interval)

        Window.bind(on_joy_button_down=self.on_joy_button_down)

        self.clear()

    def on_joy_axis(self, window, stick_id, axis_id, value):
        # Axis 1 is the X axis, axis 0 is the Y axis
        if axis_id == 1:
            self.joystick_x_value = (float(value) / self.joystick_axis_max) if abs(value) > self.joystick_raw_deadzone else 0
        elif axis_id == 0:
            self.joystick_y_value = (float(value) / self.joystick_axis_max) if abs(value) > self.joystick_raw_deadzone else 0
        else:
            return # Ignore other axes

        # Invert axes
        self.joystick_x_value = -self.joystick_x_value
        self.joystick_y_value = -self.joystick_y_value

        # Calculate feed rate based on joystick throw
        self.joystick_jog_feedrate = int((abs(self.joystick_x_value) + abs(self.joystick_y_value)) * self.joystick_max_feed)
        self.joystick_jog_feedrate = max(min(self.joystick_jog_feedrate, self.joystick_max_feed), 0)

    def send_joystick_jog_command(self, *args):
        jog_x_dist = self.joystick_x_value * self.movement_vector_max
        jog_y_dist = self.joystick_y_value * self.movement_vector_max

        if (self.m.s.m_state.lower() == 'idle' or self.m.s.m_state.lower() == 'jog') and self.sm.current == 'trace':
            if abs(jog_x_dist) > 0.02 or abs(jog_y_dist) > 0.02:
                jog_command = "$J=G91 X{:.2f} Y{:.2f} F{}".format(jog_x_dist, jog_y_dist, self.joystick_jog_feedrate)
                self.m.s.write_command(jog_command)

    def on_joy_button_down(self, window, stick_id, button_id):
        if button_id == 0:
            self.add_segment()
        elif button_id == 1:
            self.close_contour()
        elif button_id == 2:
            self.clear()
        elif button_id == 3:
            self.exit()

    def exit(self):
        self.sm.current = 'lobby'
        self.joystick_x_pos, self.joystick_y_pos = 0, 0
        self.clear()

    def clear(self):
        self.geometry_segments = []
        self.previous_point = None
        self.svg_container.clear_widgets()
        self.svg_container.add_widget(Label(text='Awaiting geometry...', font_size=38, color=(0, 0, 0, 1)))
        self.ids.recent_points_container.clear_widgets()
        self.ids.recent_points_container.add_widget(
            Label(text='Awaiting geometry...', font_size=20, color=(0, 0, 0, 1)))

    def home(self):
        self.m.request_homing_procedure('trace', 'trace')

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)

    def capture_point(self):
        # Make sure the machine has stopped moving
        if self.m.s.m_state.lower() == 'idle':
            current_x, current_y = self.cs.laser_position.get_x(), self.cs.laser_position.get_y()
            return Point(abs(current_x), abs(current_y))
        else:
            return None

    def add_segment(self):
        new_point = self.capture_point()
        if new_point:
            if self.previous_point and self.previous_point.__str__() != new_point.__str__():
                if not self.previous_point:
                    self.previous_point = new_point
                self.geometry_segments.append(Segment(self.previous_point, new_point))
            self.previous_point = new_point
        self.plot_geometry()
        self.display_recent_points()

    def display_recent_points(self):
        if not self.geometry_segments and not self.previous_point:
            return

        recent_segments = self.geometry_segments[-3:]

        # If there are fewer than 3 segments, prepend a dummy segment from the first point
        if len(recent_segments) < 3:
            if self.geometry_segments:
                dummy_segment = Segment(Point(0, 0), self.geometry_segments[0].get_start())
            else:
                dummy_segment = Segment(Point(0, 0), self.previous_point)
            dummy_segment.convert_to_svg_coordinate_space()
            recent_segments.insert(0, dummy_segment)

        # Display the points as buttons
        self.ids.recent_points_container.clear_widgets()
        for i, segment in enumerate(recent_segments):
            # Capture the segment coordinates in the closure
            end_point = segment.get_end()
            x, y = -end_point.y, -end_point.x
            move_function = self.get_move_func(x, y)

            # Convert coordinates to display format
            m_coordinates = int(2502 - end_point.x), int(1298 - end_point.y)
            button_text = "{}, {}".format(m_coordinates[0], m_coordinates[1])
            button = Button(text=button_text, font_size=20, on_press=move_function)
            self.ids.recent_points_container.add_widget(button)

    def get_move_func(self, x, y):
        def move(*args):
            self.m.s.write_command('G0 G53 X{} Y{} F8000'.format(x, y))

        return move

    def close_contour(self):
        if self.previous_point:
            self.geometry_segments.append(
                Segment(self.previous_point, self.geometry_segments[0].get_start(invert_xy=True)))
        self.plot_geometry()
        self.display_recent_points()

    def geometry_continuous(self):
        previous_segment = None
        for segment in self.geometry_segments:
            if previous_segment:
                if segment.start.__str__() != previous_segment.end.__str__():
                    return False
            previous_segment = segment
        return True

    def print_geometry(self):
        for segment in self.geometry_segments:
            print(segment)

    def build_svg_string(self):
        if not self.geometry_segments:
            return

        dwg = svgwrite.Drawing(filename="geometry.svg", size=('2500mm', '1300mm'), viewBox='0 0 2500 1300')

        path_data = []
        start_point = self.geometry_segments[0].get_start()
        x, y = start_point.x, start_point.y
        path_data.append("M {} {}".format(x, y))
        for segment in self.geometry_segments:
            path_data.append(segment.build_svg_string())

        path_string = " ".join(path_data)
        path = dwg.path(d=path_string, fill='yellow', stroke='blue', stroke_width=5)
        dwg.add(path)

        dwg.save()
        self.plot_geometry()
        return dwg.tostring()

    def print_svg_string(self):
        print(self.build_svg_string())

    def plot_geometry(self):
        if not self.geometry_segments:
            return

        # Build path data for matplotlib
        vertices = []
        codes = []

        start_point = self.geometry_segments[0].get_start()
        x, y = start_point.x, start_point.y
        vertices.append((x, y))
        codes.append(Path.MOVETO)

        for segment in self.geometry_segments:
            segment_points, segment_codes = segment.get_matplotlib_data()
            vertices.extend(segment_points)
            codes.extend(segment_codes)

        vertices = [(2500 - v[0], 1300 - v[1]) for v in vertices]  # Flip axes for matplotlib
        path = Path(vertices, codes)

        fig, ax = plt.subplots()
        patch = patches.PathPatch(path, facecolor='yellow', edgecolor='blue', linewidth=1)

        ax.add_patch(patch)
        ax.set_xlim(0, 2500)
        ax.set_ylim(0, 1300)
        ax.set_aspect('equal')
        # plt.gca().invert_yaxis()
        plt.gca().invert_xaxis()

        # Save the plot as a PNG file
        fig.savefig('geometry.png', dpi=300, bbox_inches='tight', transparent=True)
        plt.close(fig)

        # Display the PNG in the Kivy widget
        self.display_png()

    def display_png(self):
        # Remove any existing images
        self.svg_container.clear_widgets()

        # Create an Image widget to display the PNG
        img = Image(source='geometry.png')

        # Reload the image to ensure it updates
        img.reload()

        self.svg_container.add_widget(img)
