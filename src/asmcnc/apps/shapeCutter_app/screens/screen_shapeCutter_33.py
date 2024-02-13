"""
Created on 4 March 2020
Screen 33 for the Shape Cutter App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from asmcnc.apps.shapeCutter_app.screens import (
    widget_sC_work_coordinates,
    widget_sC_virtual_bed,
)
from asmcnc.geometry import job_envelope

Builder.load_string(
    """

<ShapeCutter33ScreenClass>

    info_button: info_button
    virtual_bed_container: virtual_bed_container
    work_coords_container: work_coords_container
    
    BoxLayout:
        size_hint: (None,None)
        width: dp(app.get_scaled_width(800))
        height: dp(app.get_scaled_height(480))
        padding:dp(0)
        spacing: 0
        orientation: "vertical"

        BoxLayout:
            size_hint: (None,None)
            width: dp(app.get_scaled_width(800))
            height: dp(app.get_scaled_height(90))
            padding:dp(0)
            spacing: 0
            orientation: "horizontal"

            Button:
                font_size: str(get_scaled_width(15)) + 'sp'
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(142))
                on_press: root.prepare()
                BoxLayout:
                    padding:dp(0)
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/prepare_tab_blue.png"
                        size: self.parent.size
                        allow_stretch: True
            Button:
                font_size: str(get_scaled_width(15)) + 'sp'
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(142))
                on_press: root.load()
                BoxLayout:
                    padding:dp(0)
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/load_tab_blue.png"
                        size: self.parent.size
                        allow_stretch: True
            Button:
                font_size: str(get_scaled_width(15)) + 'sp'
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(142))
                on_press: root.define()
                BoxLayout:
                    padding:dp(0)
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/define_job_tab_blue.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                font_size: str(get_scaled_width(15)) + 'sp'
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(142))
                on_press: root.position()
                BoxLayout:
                    padding:dp(0)
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/position_tab_blue.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                font_size: str(get_scaled_width(15)) + 'sp'
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(142))
                on_press: root.check()
                BoxLayout:
                    padding:dp(0)
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/check_tab_grey.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            Button:
                font_size: str(get_scaled_width(15)) + 'sp'
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(90))
                on_press: root.exit()
                BoxLayout:
                    padding:dp(0)
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/exit_cross.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True                    
                    
        BoxLayout:
            size_hint: (None,None)
            padding:dp(0)
            height: dp(app.get_scaled_height(390))
            width: dp(app.get_scaled_width(800))
            canvas:
                Rectangle: 
                    pos: self.pos
                    size: self.size
                    source: "./asmcnc/apps/shapeCutter_app/img/background.png"
            
            BoxLayout:
                orientation: "vertical"
                padding:dp(0)
                spacing: 0
                    
                BoxLayout: #Header
                    size_hint: (None,None)
                    height: dp(app.get_scaled_height(60))
                    width: dp(app.get_scaled_width(800))
                    padding:(dp(app.get_scaled_width(20)),dp(0),dp(0),dp(0))
                    orientation: "horizontal"
                    
                    BoxLayout: #Screen number
                        size_hint: (None,None)
                        padding:dp(0)
                        height: dp(app.get_scaled_height(40))
                        width: dp(app.get_scaled_width(40))
                        canvas:
                            Rectangle: 
                                pos: self.pos
                                size: self.size
                                source: "./asmcnc/apps/shapeCutter_app/img/number_box.png"
                        Label:
                            text: root.screen_number
                            valign: "middle"
                            halign: "center"
                            font_size:dp(0.0325*app.width)
                            markup: True
                                
                                
                        
                    BoxLayout: #Title
                        size_hint: (None,None)
                        height: dp(app.get_scaled_height(60))
                        width: dp(app.get_scaled_width(740))
                        padding:(dp(app.get_scaled_width(20)),dp(app.get_scaled_height(20)),dp(0),dp(0))
                        
                        Label:
                            text: root.title_label
                            color: 0,0,0,1
                            font_size:dp(0.035*app.width)
                            markup: True
                            halign: "left"
                            valign: "bottom"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                        
                    
                BoxLayout: #Body
                    size_hint: (None,None)
                    height: dp(app.get_scaled_height(330))
                    width: dp(app.get_scaled_width(800))
                    padding:(dp(0),dp(0),dp(0),dp(0))
                    orientation: "horizontal"
                    
                    # Text box layout for user instructions (at least 40 high)
                    BoxLayout: 
                        size_hint: (None,None)
                        height: dp(app.get_scaled_height(330))
                        width: dp(app.get_scaled_width(675))
                        padding:(dp(0),dp(app.get_scaled_height(20)),dp(0),dp(0))
                        orientation: "vertical"
                        
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(50))
                            width: dp(app.get_scaled_width(675))
                            padding:(dp(app.get_scaled_width(80)),dp(0),dp(0),dp(0))
                            Label:
                                text: root.user_instructions
                                color: 0,0,0,1
                                font_size:dp(0.025*app.width)
                                markup: True
                                halign: "left"
                                valign: "top"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos

                        BoxLayout:
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(260))
                            width: dp(app.get_scaled_width(675))
                            padding:(dp(0),dp(0),dp(0),dp(0))
                            orientation: "horizontal"
                     
                            BoxLayout: # two buttons
                                size_hint: (None,None)
                                height: dp(app.get_scaled_height(260))
                                width: dp(app.get_scaled_width(250))
                                padding:(dp(app.get_scaled_width(95)),dp(app.get_scaled_height(15)),dp(app.get_scaled_width(95)),dp(app.get_scaled_height(15)))
                                spacing:0.0208333333333*app.height
                                orientation: "vertical"
                                BoxLayout: # button
                                    size_hint: (None,None)
                                    height: dp(app.get_scaled_height(100))
                                    width: dp(app.get_scaled_width(100))
                                    padding:(dp(0),dp(0),dp(0),dp(0))
                                    Button:
                                        font_size: str(get_scaled_width(15)) + 'sp'
                                        on_press: root.trace_job()
                                        background_color: 1, 1, 1, 0 
                                        BoxLayout:
                                            padding:(dp(app.get_scaled_width(10)),dp(app.get_scaled_height(10)))
                                            size: self.parent.size
                                            pos: self.parent.pos      
                                            Image:
                                                source: "./asmcnc/apps/shapeCutter_app/img/go_trace.png"
                                                center_x: self.parent.center_x
                                                y: self.parent.y
                                                size: self.parent.width, self.parent.height
                                                allow_stretch: True                                    
                                BoxLayout: # button
                                    size_hint: (None,None)
                                    height: dp(app.get_scaled_height(100))
                                    width: dp(app.get_scaled_width(100))
                                    padding:(dp(0),dp(0),dp(0),dp(0))
                                    Button:
                                        font_size: str(get_scaled_width(15)) + 'sp'
                                        on_press: root.stop_jog()
                                        background_color: 1, 1, 1, 0 
                                        BoxLayout:
                                            padding:(dp(app.get_scaled_width(10)),dp(app.get_scaled_height(10)))
                                            size: self.parent.size
                                            pos: self.parent.pos      
                                            Image:
                                                source: "./asmcnc/skavaUI/img/stop.png"
                                                center_x: self.parent.center_x
                                                y: self.parent.y
                                                size: self.parent.width, self.parent.height
                                                allow_stretch: True                                                    
                            BoxLayout: # bench widget
                                size_hint: (None,None)
                                height: dp(app.get_scaled_height(260))
                                width: dp(app.get_scaled_width(425))
                                padding:(dp(0),dp(0),dp(0),dp(0))
                                orientation: "vertical"
                                BoxLayout: 
                                    id: virtual_bed_container
                                    size_hint: (None,None)
                                    height: dp(app.get_scaled_height(200))
                                    width: dp(app.get_scaled_width(425))
                                    padding:(dp(0),dp(0),dp(0),dp(0))
                                BoxLayout: 
                                    id: work_coords_container
                                    size_hint: (None,None)
                                    height: dp(app.get_scaled_height(60))
                                    width: dp(app.get_scaled_width(425))
                                    padding:(dp(app.get_scaled_width(7.5)),dp(app.get_scaled_height(5)),dp(app.get_scaled_width(7.5)),dp(app.get_scaled_height(5)))

                    BoxLayout: #action box
                        size_hint: (None,None)
                        height: dp(app.get_scaled_height(310))
                        width: dp(app.get_scaled_width(125))
                        padding:(dp(0),dp(0),dp(0),dp(app.get_scaled_height(34)))
                        spacing:0.0708333333333*app.height
                        orientation: "vertical"
                        
                        BoxLayout: 
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(67))
                            width: dp(app.get_scaled_width(88))
                            padding:(dp(app.get_scaled_width(24)),dp(0),dp(app.get_scaled_width(24)),dp(app.get_scaled_height(34)))
                            Button:
                                font_size: str(get_scaled_width(15)) + 'sp'
                                id: info_button
                                size_hint: (None,None)
                                height: dp(app.get_scaled_height(40))
                                width: dp(app.get_scaled_width(40))
                                background_color: hex('#F4433600')
                                opacity: 1
                                on_press: root.get_info()
                                BoxLayout:
                                    padding:dp(0)
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        source: "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
                                        center_x: self.parent.center_x
                                        y: self.parent.y
                                        size: self.parent.width, self.parent.height
                                        allow_stretch: True

                        Button: 
                            font_size: str(get_scaled_width(15)) + 'sp'
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(67))
                            width: dp(app.get_scaled_width(88))
                            background_color: hex('#F4433600')
                            on_press: root.go_back()
                            BoxLayout:
                                padding:dp(0)
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/shapeCutter_app/img/arrow_back.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                        Button: 
                            font_size: str(get_scaled_width(15)) + 'sp'
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(67))
                            width: dp(app.get_scaled_width(88))
                            background_color: hex('#F4433600')
                            on_press: root.next_screen()
                            BoxLayout:
                                padding:dp(0)
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/shapeCutter_app/img/arrow_next.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True               

"""
)


class ShapeCutter33ScreenClass(Screen):
    info_button = ObjectProperty()
    screen_number = StringProperty("[b]33[/b]")
    title_label = StringProperty("[b]Trace bounding box[/b]")
    user_instructions = StringProperty(
        "Press the [b]Trace[/b] button to make the machine walk around the outline of the job before it starts. "
    )

    def __init__(self, **kwargs):
        super(ShapeCutter33ScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs["shapecutter"]
        self.m = kwargs["machine"]
        self.j = kwargs["job_parameters"]
        self.virtual_bed_widget = widget_sC_virtual_bed.SCVirtualBed(
            machine=self.m, job_parameters=self.j, screen_manager=self.shapecutter_sm.sm
        )
        self.virtual_bed_container.add_widget(self.virtual_bed_widget)
        self.work_coords_widget = widget_sC_work_coordinates.WorkCoordinates(
            machine=self.m, screen_manager=self.shapecutter_sm.sm
        )
        self.work_coords_container.add_widget(self.work_coords_widget)

    def on_pre_enter(self):
        self.info_button.opacity = 0
        self.m.laser_on()

    def on_pre_leave(self):
        self.m.laser_off()

# Action buttons

    def get_info(self):
        pass

    def go_back(self):
        if not self.m.state().startswith("Jog"):
            self.shapecutter_sm.previous_screen()
        else:
            pass

    def next_screen(self):
        if not self.m.state().startswith("Jog"):
            self.shapecutter_sm.next_screen()
        else:
            pass
    
# Tab functions

    def prepare(self):
        if not self.m.state().startswith("Jog"):
            self.shapecutter_sm.prepare_tab()
        else:
            pass

    def load(self):
        if not self.m.state().startswith("Jog"):
            self.shapecutter_sm.load_tab()
        else:
            pass

    def define(self):
        if not self.m.state().startswith("Jog"):
            self.shapecutter_sm.define_tab()
        else:
            pass

    def position(self):
        if not self.m.state().startswith("Jog"):
            self.shapecutter_sm.position_tab()
        else:
            pass

    def check(self):
        if not self.m.state().startswith("Jog"):
            self.shapecutter_sm.check_tab()
        else:
            pass

    def exit(self):
        self.shapecutter_sm.exit_shapecutter()

# Screen specific:
    def trace_job(self): #(need to generate gcode in advance)
        if not self.m.state().startswith("Jog"):
            self.m.go_x_datum()
            self.m.go_y_datum()
#            Previously this call returned a VERY SLOW feedrate:
#             xy_feed_speed = self.j.parameter_dict["feed rates"]["xy feed rate"]
#            Assuming a conversion error. As quick fix, hardcoding to force a G0 equivalent
#            Needs investigation tho to ensure core job code is stable
            xy_feed_speed = 8000
            job_x_range = self.j.range_x[1] - self.j.range_x[0]
            job_y_range = self.j.range_y[1] - self.j.range_y[0]
            if self.j.shape_dict["shape"] == "rectangle":
                self.m.jog_relative("X", job_x_range, xy_feed_speed)
                self.m.jog_relative("Y", job_y_range, xy_feed_speed)
                self.m.jog_relative("X", -job_x_range, xy_feed_speed)
                self.m.jog_relative("Y", -job_y_range, xy_feed_speed)
            elif self.j.shape_dict["shape"] == "circle":
                self.m.jog_relative("X", self.j.range_x[0], xy_feed_speed)
                self.m.jog_relative("Y", self.j.range_y[0], xy_feed_speed)
                self.m.jog_relative("X", job_x_range, xy_feed_speed)
                self.m.jog_relative("Y", job_y_range, xy_feed_speed)
                self.m.jog_relative("X", -job_x_range, xy_feed_speed)
                self.m.jog_relative("Y", -job_y_range, xy_feed_speed)
        else:
            pass

    def stop_jog(self):
        self.m.quit_jog()
