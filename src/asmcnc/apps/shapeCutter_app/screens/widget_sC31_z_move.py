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
from asmcnc.apps.shapeCutter_app.screens import widget_sC31_z_height

Builder.load_string(
    """

<SC31ZMove>

    virtual_z_container:virtual_z_container

    BoxLayout:

        size: self.parent.size
        pos: self.parent.pos      
        padding: app.get_scaled_tuple([20.0, 20.0])
        spacing: app.get_scaled_width(10.0)
        orientation: 'horizontal'
        
        BoxLayout:
            spacing: app.get_scaled_width(9.99999999998)
            orientation: "vertical"
            
            BoxLayout:
                size_hint_y: 3.4
                height: self.parent.height
                id: virtual_z_container

        BoxLayout:
            spacing: app.get_scaled_width(9.99999999998)
            orientation: "vertical"
            
            Button:
                font_size: app.get_scaled_sp('15.0sp')
                size_hint_y: 1
                background_color: hex('#F4433600')
                on_release:
                    root.quit_jog_z()
                    self.background_color = hex('#F4433600')
                on_press:
                    root.jog_z('Z+') 
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

            Button:
                font_size: app.get_scaled_sp('15.0sp')
                size_hint_y: 1
                background_color: hex('#F4433600')
                on_release: 
                    root.quit_jog_z()
                    self.background_color = hex('#F4433600')
                on_press:
                    root.jog_z('Z-') 
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/z_jog_down.png"
                        source: "./asmcnc/skavaUI/img/xy_arrow_down.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True   
                        
            Button:
                font_size: app.get_scaled_sp('15.0sp')
                size_hint_y: 1
                background_color: hex('#F4433600')
                on_release: 
                    self.background_color = hex('#F4433600')
                on_press:
                    root.probe_z()
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/z_probe.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True   
        
"""
)


class SC31ZMove(Widget):
    def __init__(self, **kwargs):
        super(SC31ZMove, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.j = kwargs["job_parameters"]
        self.vitrtual_z_height_widget = widget_sC31_z_height.VirtualZ31(
            machine=self.m, screen_manager=self.sm, job_parameters=self.j
        )
        self.virtual_z_container.add_widget(self.vitrtual_z_height_widget)

    def jog_z(self, case):
        feed_speed = self.sm.get_screen("sC31").z_set_go_widget.feedSpeedJogZ
        if self.sm.get_screen("home").xy_move_widget.jogMode == "free":
            if case == "Z-":
                self.m.jog_absolute_single_axis(
                    "Z", self.m.z_min_jog_abs_limit, feed_speed
                )
            if case == "Z+":
                self.m.jog_absolute_single_axis(
                    "Z", self.m.z_max_jog_abs_limit, feed_speed
                )
        elif self.sm.get_screen("home").xy_move_widget.jogMode == "plus_0-01":
            if case == "Z+":
                self.m.jog_relative("Z", 0.01, feed_speed)
            if case == "Z-":
                self.m.jog_relative("Z", -0.01, feed_speed)
        elif self.sm.get_screen("home").xy_move_widget.jogMode == "plus_0-1":
            if case == "Z+":
                self.m.jog_relative("Z", 0.1, feed_speed)
            if case == "Z-":
                self.m.jog_relative("Z", -0.1, feed_speed)
        elif self.sm.get_screen("home").xy_move_widget.jogMode == "plus_1":
            if case == "Z+":
                self.m.jog_relative("Z", 1, feed_speed)
            if case == "Z-":
                self.m.jog_relative("Z", -1, feed_speed)
        elif self.sm.get_screen("home").xy_move_widget.jogMode == "plus_10":
            if case == "Z+":
                self.m.jog_relative("Z", 10, feed_speed)
            if case == "Z-":
                self.m.jog_relative("Z", -10, feed_speed)
        elif self.sm.get_screen("home").xy_move_widget.jogMode == "job":
            if case == "Z-":
                self.m.jog_absolute_single_axis(
                    "Z", self.m.z_min_jog_abs_limit, feed_speed
                )
            if case == "Z+":
                self.m.jog_absolute_single_axis(
                    "Z", self.m.z_max_jog_abs_limit, feed_speed
                )

    def quit_jog_z(self):
        if self.sm.get_screen("home").xy_move_widget.jogMode == "free":
            self.m.quit_jog()
        elif self.sm.get_screen("home").xy_move_widget.jogMode == "job":
            self.m.quit_jog()

    def probe_z(self):
        self.m.probe_z()
