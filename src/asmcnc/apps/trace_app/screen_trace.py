"""
Created on 18 Aug 2024
Trace app concept screen

@author: Benji
"""
import svgwrite
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

from src.asmcnc.apps.maintenance_app import widget_maintenance_xy_move
from src.asmcnc.skavaUI import widget_virtual_bed

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.clock import Clock

Builder.load_string("""
#:import color_provider asmcnc.core_UI.utils.color_provider

<TraceScreenClass>:
    xy_move_container: xy_move_container
    virtual_bed_container: virtual_bed_container
    svg_container: svg_container
    
    canvas.before:
        Color:
            rgba: 0.9, 0.9, 0.9, 1  # Light grey color
        Rectangle:
            pos: self.pos
            size: self.size
    
    GridLayout:
        cols: 2
        row_default_height: 270
        
        ### Top ###
        
        # Buttons
        BoxLayout:
            size_hint_x: None
            height: dp(768 * 0.5)
            width: dp(600)
            orientation: 'vertical'
            
            GridLayout:
                cols: 2
                
                Button:
                    text: 'Home'
                    allow_stretch: False
                    size_hint_x: 1
                    on_press: root.home()
                    
                Button:
                    text: 'Capture Point'
                    allow_stretch: False
                    size_hint_x: 1
                    on_press: root.add_segment()
                    
                Button:
                    text: 'Clear'
                    size_hint_x: 1
                    on_press: root.clear()
                
                Button:
                    text: 'Close contour'
                    size_hint_x: 1
                    on_press: root.close_contour()
                    
                Button:
                    text: 'Exit'
                    size_hint_x: 1
                    on_press: root.exit()
                    
                Button:
                    text: 'Export SVG'
                    size_hint_x: 1
                    on_press: root.print_svg_string()
                
        # SVG container - second column
        BoxLayout:
            id: svg_container
            
        ### Bottom ###
        
        # XY move widget
        BoxLayout:
            id: xy_move_container
            orientation: 'vertical'
            size_hint: (None, None)
            height: dp(0.6875 * app.height)
            width: dp(0.35 * app.width)
            
        # Virtual bed widget
        BoxLayout:
            orientation: 'vertical'
            padding: [dp(0.025) * app.width, dp(0.0416666666667) * app.height]
            spacing: dp(0.0416666666667) * app.height
            canvas:
                Color:
                    rgba: hex('#E5E5E5FF')
                Rectangle:
                    size: self.size
                    pos: self.pos
        
            BoxLayout:
                id: virtual_bed_container
                size_hint_y: 1
                padding: [dp(0.0125) * app.width, dp(0.0208333333333) * app.height]
                canvas:
                    Color:
                        rgba: 1, 1, 1, 1
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos
        
""")


class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)


class Segment:
    def __init__(self, start, end, radius_x=None, radius_y=None):
        self.start = Point(start.x, start.y)  # Create a copy of the start point
        self.end = Point(end.x, end.y)  # Create a copy of the end point
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
        self.cs = self.m.cs

        # Widgets
        self.xy_move_widget = widget_maintenance_xy_move.MaintenanceXYMove(
            machine=self.m, screen_manager=self.sm
        )
        self.xy_move_container.add_widget(self.xy_move_widget)
        self.virtual_bed_container.add_widget(
            widget_virtual_bed.VirtualBed(machine=self.m, screen_manager=self.sm)
        )

    def exit(self):
        self.sm.current = 'lobby'
        self.clear()

    def clear(self):
        self.geometry_segments = []
        self.previous_point = None
        self.svg_container.clear_widgets()

    def home(self):
        self.m.request_homing_procedure('trace', 'trace')

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

    def close_contour(self):
        if self.previous_point:
            self.geometry_segments.append(Segment(self.previous_point, self.geometry_segments[0].get_start(invert_xy=True)))
        self.plot_geometry()

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
        patch = patches.PathPatch(path, facecolor='yellow', edgecolor='blue', linewidth=3)

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
