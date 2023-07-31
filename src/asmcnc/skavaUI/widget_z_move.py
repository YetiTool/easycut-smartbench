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
from asmcnc.skavaUI import widget_z_height
from kivy.clock import Clock
Builder.load_string(
    """

<ZMove>

    virtual_z_container:virtual_z_container

    BoxLayout:

        size: self.parent.size
        pos: self.parent.pos      
        padding: 20
        spacing: 10
        orientation: 'horizontal'
        
        BoxLayout:
            spacing: 10
            orientation: "vertical"
            
            BoxLayout:
                size_hint_y: 3.4
                id: virtual_z_container
                
            Button:
                size_hint_y: 1
                background_color: hex('#F4433600')
                on_release: 
                    self.background_color = hex('#F4433600')
                on_press: 
                    root.set_jobstart_z()
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/z_set_0.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True     

    
    
    
        BoxLayout:
            spacing: 10
            orientation: "vertical"
            
            Button:
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
                        
            Button:
                size_hint_y: 1
                background_color: hex('#F4433600')
                on_release: 
                    self.background_color = hex('#F4433600')
                on_press: 
                    root.go_to_jobstart_z()
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/z_goto_0.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True   
                        
    FloatLayout:
        
        Label:
            x: 662
            y: 420
            size_hint: None, None            
            height: 30
            width: 30
            text: 'Z'
            markup: True
            bold: True
            color: 0,0,0,0.2
            font_size: 20     
        
"""
    )


class ZMove(Widget):

    def __init__(self, **kwargs):
        super(ZMove, self).__init__(**kwargs)
        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']
        self.jd = kwargs['job']
        self.virtual_z_container.add_widget(widget_z_height.VirtualZ(
            machine=self.m, screen_manager=self.sm, job=self.jd))

    def jog_z(self, case):
        self.m.set_led_colour('WHITE')
        feed_speed = self.sm.get_screen('home'
            ).common_move_widget.feedSpeedJogZ
        if self.sm.get_screen('home').xy_move_widget.jogMode == 'free':
            if case == 'Z-':
                self.m.jog_absolute_single_axis('Z', self.m.
                    z_min_jog_abs_limit, feed_speed)
            if case == 'Z+':
                self.m.jog_absolute_single_axis('Z', self.m.
                    z_max_jog_abs_limit, feed_speed)
        elif self.sm.get_screen('home').xy_move_widget.jogMode == 'plus_0-01':
            if case == 'Z+':
                self.m.jog_relative('Z', 0.01, feed_speed)
            if case == 'Z-':
                self.m.jog_relative('Z', -0.01, feed_speed)
        elif self.sm.get_screen('home').xy_move_widget.jogMode == 'plus_0-1':
            if case == 'Z+':
                self.m.jog_relative('Z', 0.1, feed_speed)
            if case == 'Z-':
                self.m.jog_relative('Z', -0.1, feed_speed)
        elif self.sm.get_screen('home').xy_move_widget.jogMode == 'plus_1':
            if case == 'Z+':
                self.m.jog_relative('Z', 1, feed_speed)
            if case == 'Z-':
                self.m.jog_relative('Z', -1, feed_speed)
        elif self.sm.get_screen('home').xy_move_widget.jogMode == 'plus_10':
            if case == 'Z+':
                self.m.jog_relative('Z', 10, feed_speed)
            if case == 'Z-':
                self.m.jog_relative('Z', -10, feed_speed)
        elif self.sm.get_screen('home').xy_move_widget.jogMode == 'job':
            if case == 'Z-':
                self.m.jog_absolute_single_axis('Z', self.m.
                    z_min_jog_abs_limit, feed_speed)
            if case == 'Z+':
                self.m.jog_absolute_single_axis('Z', self.m.
                    z_max_jog_abs_limit, feed_speed)

    def quit_jog_z(self):
        if self.sm.get_screen('home').xy_move_widget.jogMode == 'free':
            self.m.quit_jog()
        elif self.sm.get_screen('home').xy_move_widget.jogMode == 'job':
            self.m.quit_jog()

    def probe_z(self):
        self.m.probe_z()
        self.disable_z_datum_reminder()

    def set_jobstart_z(self):
        self.m.set_jobstart_z()
        self.disable_z_datum_reminder()

    def go_to_jobstart_z(self):
        self.m.go_to_jobstart_z()

    def disable_z_datum_reminder(self):
        self.sm.get_screen('home').has_datum_been_reset = True
