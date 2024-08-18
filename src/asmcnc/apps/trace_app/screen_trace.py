"""
Created on 18 Aug 2024
Trace app concept screen

@author: Benji
"""
import svgwrite

from src.asmcnc.apps.maintenance_app import widget_maintenance_xy_move

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.graphics.svg import Svg

from src.asmcnc.skavaUI import widget_virtual_bed

Builder.load_string("""
#:import color_provider asmcnc.core_UI.utils.color_provider

<TraceScreenClass>:
    xy_move_container:xy_move_container
    virtual_bed_container:virtual_bed_container
    svg_container:svg_container
    
    canvas.before:
        Color:
            rgba: 0.9, 0.9, 0.9, 1  # Light grey color
        Rectangle:
            pos: self.pos
            size: self.size
    
    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            orientation: 'vertical'
            
            BoxLayout:
                orientation: 'horizontal'
                padding: dp(5)
                spacing: dp(10)
                
                Button:
                    # source: './asmcnc/apps/trace_app/img/home_button.png'
                    text: 'Home'
                    allow_stretch: False
                    size_hint_x: 1
                    on_press: root.home()
                    
                Button:
                    # source: './asmcnc/apps/trace_app/img/capture_point_button.png'
                    text: 'Capture Point'
                    allow_stretch: False
                    size_hint_x: 1
                    on_press: root.add_segment()
                    
                Button:
                    text: 'Clear'
                    size_hint_x: 1
                    on_press: root.geometry_segments = []
                
                Button:
                    text: 'Finish'
                    size_hint_x: 1
                    on_press: root.print_svg_string()
                    
            BoxLayout:
                id: svg_container
                
        BoxLayout:
            orientation: 'horizontal'
        
            BoxLayout:
                id: xy_move_container
                orientation: 'vertical'
                size_hint: (None,None)
                height: dp(0.6875*app.height)
                width: dp(0.35*app.width)
                
            BoxLayout:
                orientation: 'vertical'
                padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                spacing:0.0416666666667*app.height
                canvas:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos

                BoxLayout:
                    id: virtual_bed_container
                    size_hint_y: 5
                    padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                    canvas:
                        Color:
                            rgba: 1,1,1,1
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

    def get_start(self):
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


class TraceScreenClass(Screen):
    geometry_segments = []
    previous_point = Point(-1250, -2500)

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
                self.geometry_segments.append(Segment(self.previous_point, new_point))
            self.previous_point = new_point
        if self.geometry_continuous():
            self.print_geometry()
        else:
            print("Break in geometry")

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
        dwg = svgwrite.Drawing(filename="geometry.svg", size=('2500mm', '1250mm'), viewBox=('0 0 2500 1250'))

        path_data = []
        start_point = self.geometry_segments[0].get_start()
        x, y = start_point.x, start_point.y
        path_data.append("M {} {}".format(x, y))
        for segment in self.geometry_segments:
            path_data.append(segment.build_svg_string())

        path_string = " ".join(path_data)
        path = dwg.path(d=path_string, fill='none', stroke='blue', stroke_width=5)
        dwg.add(path)

        dwg.save()
        self.display_svg()
        return dwg.tostring()

    def print_svg_string(self):
        print(self.build_svg_string())

    def display_svg(self):
        # Clear the svg_container before adding new content
        self.svg_container.clear_widgets()

        # Add the SVG file using the Svg class
        with self.svg_container.canvas:
            svg = Svg("geometry.svg")
