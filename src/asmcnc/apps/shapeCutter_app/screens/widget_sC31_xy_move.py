"""
Created on 1 Feb 2018
@author: Ed
"""
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.clock import Clock
from asmcnc.apps.shapeCutter_app.screens import popup_input_error
from asmcnc.skavaUI import popup_info

Builder.load_string(
    """

#:import hex kivy.utils.get_color_from_hex

<SC31XYMove>

    jogModeButtonImage:jogModeButtonImage
    
    BoxLayout:
    
        size: self.parent.size
        pos: self.parent.pos      
        orientation: 'vertical'
        padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
        spacing:0.0208333333333*app.height
        
        GridLayout:
            cols: 3
            orientation: 'horizontal'
            spacing: 0
            size_hint_y: None
            height: self.width
    

            # go x datum
            BoxLayout:
                padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                size: self.parent.size
                pos: self.parent.pos          
            


            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                background_color: color_provider.get_rgba("invisible")
                always_release: True
                on_release: 
                    root.cancelXYJog()
                    self.background_color = hex('#F4433600')
                on_press: 
                    root.buttonJogXY('X+')
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/xy_arrow_up.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True                                    

            # go y datum
            BoxLayout:
                padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                size: self.parent.size
                pos: self.parent.pos
                            
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                background_color: color_provider.get_rgba("invisible")
                always_release: True
                on_release: 
                    root.cancelXYJog()
                    self.background_color = hex('#F4433600')
                on_press: 
                    root.buttonJogXY('Y+')
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/xy_arrow_left.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True                                    
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                background_color: color_provider.get_rgba("invisible")
                on_release: 
                    self.background_color = hex('#F4433600')
                on_press:
                    root.jogModeCycled()
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: jogModeButtonImage
                        source: "./asmcnc/skavaUI/img/jog_mode_infinity.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True  
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                background_color: color_provider.get_rgba("invisible")
                always_release: True
                on_release: 
                    root.cancelXYJog()
                    self.background_color = hex('#F4433600')
                on_press: 
                    root.buttonJogXY('Y-')
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos  
                    Image:
                        source: "./asmcnc/skavaUI/img/xy_arrow_right.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True                                    

            # set x datum
            BoxLayout:
                padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                size: self.parent.size
                pos: self.parent.pos                 
#                 Button:
#                     background_color: color_provider.get_rgba("invisible")
#                     on_release: 
#                         root.set_x_datum()
#                         self.background_color = hex('#F4433600')
#                     on_press: 
#                         self.background_color = hex('#F44336FF')
#                     BoxLayout:
#                         size: self.parent.size
#                         pos: self.parent.pos  
#                         Image:
#                             source: "./asmcnc/skavaUI/img/set_datum_x.png"
#                             center_x: self.parent.center_x
#                             y: self.parent.y
#                             size: self.parent.width, self.parent.height
#                             allow_stretch: True               

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                background_color: color_provider.get_rgba("invisible")
                always_release: True
                on_release:
                    root.cancelXYJog()
                    self.background_color = hex('#F4433600')
                on_press: 
                    root.buttonJogXY('X-')
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos      
                    Image:
                        source: "./asmcnc/skavaUI/img/xy_arrow_down.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True                                    

            # set y datum
            BoxLayout:
                padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                size: self.parent.size
                pos: self.parent.pos
#                 Button:
#                     background_color: color_provider.get_rgba("invisible")
#                     on_release: 
#                         root.set_y_datum()
#                         self.background_color = hex('#F4433600')
#                     on_press: 
#                         self.background_color = hex('#F44336FF')
#                     BoxLayout:
#                         padding: 0
#                         size: self.parent.size
#                         pos: self.parent.pos  
#                         Image:
#                             source: "./asmcnc/skavaUI/img/set_datum_y.png"
#                             center_x: self.parent.center_x
#                             y: self.parent.y
#                             size: self.parent.width, self.parent.height
#                             allow_stretch: True   
                
        BoxLayout:
            orientation: 'horizontal'
            spacing:0.0125*app.width

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                background_color: color_provider.get_rgba("invisible")
                on_release: 
                    self.background_color = hex('#F4433600')
                on_press:
                    root.set_standby_to_pos()
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos      
                    Image:
                        source: "./asmcnc/skavaUI/img/set_park.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True            
            BoxLayout:
                size_hint_x: 2
#                 id: virtual_bed_container
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                background_color: color_provider.get_rgba("invisible")
                disabled: True
                opacity: 0
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos      
                    Image:
                        source: "./asmcnc/skavaUI/img/set_jobstart.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True  
                        opacity: 0        
"""
)


class SC31XYMove(Widget):
    def __init__(self, **kwargs):
        super(SC31XYMove, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.j = kwargs["job_parameters"]
        self.l = kwargs["localization"]

    jogMode = "free"
    jog_mode_button_press_counter = 0

    def jogModeCycled(self):
        self.jog_mode_button_press_counter += 1
        if self.jog_mode_button_press_counter % 6 == 0:
            self.jogMode = "free"
            self.jogModeButtonImage.source = (
                "./asmcnc/skavaUI/img/jog_mode_infinity.png"
            )
        if self.jog_mode_button_press_counter % 6 == 1:
            self.jogMode = "job"
            self.jogModeButtonImage.source = "./asmcnc/skavaUI/img/jog_mode_box.png"
        if self.jog_mode_button_press_counter % 6 == 2:
            self.jogMode = "plus_10"
            self.jogModeButtonImage.source = "./asmcnc/skavaUI/img/jog_mode_10.png"
        if self.jog_mode_button_press_counter % 6 == 3:
            self.jogMode = "plus_1"
            self.jogModeButtonImage.source = "./asmcnc/skavaUI/img/jog_mode_1.png"
        if self.jog_mode_button_press_counter % 6 == 4:
            self.jogMode = "plus_0-1"
            self.jogModeButtonImage.source = "./asmcnc/skavaUI/img/jog_mode_0-1.png"
        if self.jog_mode_button_press_counter % 6 == 5:
            self.jogMode = "plus_0-01"
            self.jogModeButtonImage.source = "./asmcnc/skavaUI/img/jog_mode_0-01.png"

    def buttonJogXY(self, case):
        x_feed_speed = self.sm.get_screen("sC31").z_set_go_widget.feedSpeedJogX
        y_feed_speed = self.sm.get_screen("sC31").z_set_go_widget.feedSpeedJogY
        if self.jogMode == "free":
            if case == "X-":
                self.m.jog_absolute_single_axis(
                    "X", self.m.x_min_jog_abs_limit, x_feed_speed
                )
            if case == "X+":
                self.m.jog_absolute_single_axis(
                    "X", self.m.x_max_jog_abs_limit, x_feed_speed
                )
            if case == "Y-":
                self.m.jog_absolute_single_axis(
                    "Y", self.m.y_min_jog_abs_limit, y_feed_speed
                )
            if case == "Y+":
                self.m.jog_absolute_single_axis(
                    "Y", self.m.y_max_jog_abs_limit, y_feed_speed
                )
        elif self.jogMode == "plus_0-01":
            if case == "X+":
                self.m.jog_relative("X", 0.01, x_feed_speed)
            if case == "X-":
                self.m.jog_relative("X", -0.01, x_feed_speed)
            if case == "Y+":
                self.m.jog_relative("Y", 0.01, y_feed_speed)
            if case == "Y-":
                self.m.jog_relative("Y", -0.01, y_feed_speed)
        elif self.jogMode == "plus_0-1":
            if case == "X+":
                self.m.jog_relative("X", 0.1, x_feed_speed)
            if case == "X-":
                self.m.jog_relative("X", -0.1, x_feed_speed)
            if case == "Y+":
                self.m.jog_relative("Y", 0.1, y_feed_speed)
            if case == "Y-":
                self.m.jog_relative("Y", -0.1, y_feed_speed)
        elif self.jogMode == "plus_1":
            if case == "X+":
                self.m.jog_relative("X", 1, x_feed_speed)
            if case == "X-":
                self.m.jog_relative("X", -1, x_feed_speed)
            if case == "Y+":
                self.m.jog_relative("Y", 1, y_feed_speed)
            if case == "Y-":
                self.m.jog_relative("Y", -1, y_feed_speed)
        elif self.jogMode == "plus_10":
            if case == "X+":
                self.m.jog_relative("X", 10, x_feed_speed)
            if case == "X-":
                self.m.jog_relative("X", -10, x_feed_speed)
            if case == "Y+":
                self.m.jog_relative("Y", 10, y_feed_speed)
            if case == "Y-":
                self.m.jog_relative("Y", -10, y_feed_speed)
        elif self.jogMode == "job":
            job_x_range = self.j.range_x[1] - self.j.range_x[0]
            job_y_range = self.j.range_y[1] - self.j.range_y[0]
            if case == "X+":
                self.m.jog_relative("X", job_x_range, x_feed_speed)
            if case == "X-":
                self.m.jog_relative("X", -job_x_range, x_feed_speed)
            if case == "Y+":
                self.m.jog_relative("Y", job_y_range, y_feed_speed)
            if case == "Y-":
                self.m.jog_relative("Y", -job_y_range, y_feed_speed)

    def cancelXYJog(self):
        if self.jogMode == "free":
            self.m.quit_jog()

    def set_workzone_to_pos_xy(self):
        self.m.set_workzone_to_pos_xy()

    def set_standby_to_pos(self):
        warning = "Is this where you want to set your\nstandby position?"
        popup_info.PopupPark(self.sm, self.m, self.l, warning)

    def go_x_datum(self):
        if self.m.is_machine_homed == False:
            popup_info.PopupHomingWarning(self.sm, self.m, self.l, "sC31", "sC31")
        else:
            self.m.go_x_datum()

    def go_y_datum(self):
        if self.m.is_machine_homed == False:
            popup_info.PopupHomingWarning(self.sm, self.m, self.l, "sC31", "sC31")
        else:
            self.m.go_y_datum()

    def set_x_datum(self):
        warning = "Is this where you want to set your\n[b]X[/b] datum?"
        popup_input_error.PopupDatum(self.sm, self.m, self.l, "X", warning)

    def set_y_datum(self):
        warning = "Is this where you want to set your\n[b]Y[/b] datum?"
        popup_input_error.PopupDatum(self.sm, self.m, self.l, "Y", warning)
