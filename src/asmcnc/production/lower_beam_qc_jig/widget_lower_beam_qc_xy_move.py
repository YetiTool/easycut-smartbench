"""
Created on 1 Feb 2018
@author: Ed
"""

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    ObjectProperty,
    ListProperty,
    NumericProperty,
)  # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.clock import Clock
from asmcnc.skavaUI import popup_info


Builder.load_string(
    """

#:import hex kivy.utils.get_color_from_hex

<LowerBeamQCXYMove>

    jogModeButtonImage:jogModeButtonImage

    BoxLayout:
    
        size: self.parent.size
        pos: self.parent.pos      
        orientation: 'vertical'
        padding: 10
        spacing: 10

        GridLayout:
            cols: 3
            orientation: 'horizontal'
            spacing: 0
            size_hint_y: None
            height: self.width
    

            BoxLayout:
                padding: 10
                size: self.parent.size
                pos: self.parent.pos                               

            Button:
                background_color: hex('#F4433600')
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

            BoxLayout:
                padding: 10
                size: self.parent.size
                pos: self.parent.pos                 
                            
            Button:
                background_color: hex('#F4433600')
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
                background_color: hex('#F4433600')
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
                background_color: hex('#F4433600')
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

            BoxLayout:
                padding: 10
                size: self.parent.size
                pos: self.parent.pos  

            Button:
                background_color: hex('#F4433600')
                always_release: True
                on_release:
                    print('release')
                    root.cancelXYJog()
                    self.background_color = hex('#F4433600')
                on_press: 
                    print('press')
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

            BoxLayout:
                padding: 10
                size: self.parent.size
                pos: self.parent.pos 
"""
)


class LowerBeamQCXYMove(Widget):
    def __init__(self, **kwargs):
        super(LowerBeamQCXYMove, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]

    feedSpeedJogX = 1200
    feedSpeedJogY = 1200

    jogMode = "free"
    jog_mode_button_press_counter = 0

    def jogModeCycled(self):
        self.jog_mode_button_press_counter += 1
        if self.jog_mode_button_press_counter % 5 == 0:
            self.jogMode = "free"
            self.jogModeButtonImage.source = (
                "./asmcnc/skavaUI/img/jog_mode_infinity.png"
            )
        if self.jog_mode_button_press_counter % 5 == 1:
            self.jogMode = "plus_10"
            self.jogModeButtonImage.source = "./asmcnc/skavaUI/img/jog_mode_10.png"
        if self.jog_mode_button_press_counter % 5 == 2:
            self.jogMode = "plus_1"
            self.jogModeButtonImage.source = "./asmcnc/skavaUI/img/jog_mode_1.png"
        if self.jog_mode_button_press_counter % 5 == 3:
            self.jogMode = "plus_0-1"
            self.jogModeButtonImage.source = "./asmcnc/skavaUI/img/jog_mode_0-1.png"
        if self.jog_mode_button_press_counter % 5 == 4:
            self.jogMode = "plus_0-01"
            self.jogModeButtonImage.source = "./asmcnc/skavaUI/img/jog_mode_0-01.png"

    def buttonJogXY(self, case):
        x_feed_speed = self.feedSpeedJogX
        y_feed_speed = self.feedSpeedJogY

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
            job_box = self.sm.get_screen("home").job_box
            job_x_range = job_box.range_x[1] - job_box.range_x[0]
            job_y_range = job_box.range_y[1] - job_box.range_y[0]

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
