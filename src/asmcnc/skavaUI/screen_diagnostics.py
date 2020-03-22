'''
Created on 19 Aug 2017

@author: Ed
'''
# config

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from __builtin__ import file, True
from kivy.clock import Clock, mainthread

import os, sys

from asmcnc.skavaUI import widget_virtual_bed, widget_status_bar,\
    widget_z_move, widget_xy_move, widget_common_move,\
    widget_quick_commands, widget_virtual_bed_control, widget_gcode_monitor,\
    widget_network_setup, widget_z_height, popup_stop_press,\
    widget_feed_override
from asmcnc.geometry import job_envelope
from kivy.properties import ObjectProperty, NumericProperty, StringProperty # @UnresolvedImport

# from asmcnc.skavaUI import widget_tabbed_panel


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex

<DiagnosticsScreen>:

    status_container:status_container
    
    limit_x_label:limit_x_label
    limit_X_label:limit_X_label
    limit_y_label:limit_y_label
    limit_Y_label:limit_Y_label
    limit_z_label:limit_z_label
    probe_label:probe_label
    dust_shoe_cover_label:dust_shoe_cover_label

    BoxLayout:
        padding: 0
        spacing: 0
        orientation: "vertical"

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Label:
                text: 'LED ring:'
            Button:
                text: 'Red'
                on_release: root.led('RED')
            Button:
                text: 'Green'
                on_release: root.led('GREEN')
            Button:
                text: 'Blue'
                on_release: root.led('BLUE')
            Button:
                text: 'OFF'
                on_release: root.led('off')

            Label:
                id: probe_label
                text: 'Probe'
            Label:
                id: dust_shoe_cover_label
                text: 'Dust cover'
                
        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Label:
                text: 'X axis:'
            Button:
                text: '-'
                on_release: root.move('x-')
            Button:
                text: '+'
                on_release: root.move('x+')
            Label:
                id: limit_x_label
                text: 'X Min'
            Label:
                id: limit_X_label
                text: 'X Max'

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Label:
                text: 'Y axis:'
            Button:
                text: '-'
                on_release: root.move('y-')
            Button:
                text: '+'
                on_release: root.move('y+')
            Label:
                id: limit_y_label
                text: 'Y Min'
            Label:
                id: limit_Y_label
                text: 'Y Max'

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "horizontal"

            Label:
                text: 'Z axis:'
            Button:
                text: '-'
                on_release: root.move('z-')
            Button:
                text: '+'
                on_release: root.move('z+')
            Label:
                id: limit_z_label
                text: 'Z Min'
            Label:
                text: ''

        Button:
            text: 'Return to home'
            on_release: root.return_to_home()
            
        BoxLayout:
            id: status_container

""")


class DiagnosticsScreen(Screen):


    def __init__(self, **kwargs):

        super(DiagnosticsScreen, self).__init__(**kwargs)

        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        
        # Status bar
        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm))
        Clock.schedule_interval(self.limit_switch_check, 0.2)

    def on_enter(self):
        
        self.m.disable_limit_switches()
        
    def on_leave(self):
        self.m.enable_limit_switches()

    
    def led(self, command):
        
        self.m.set_led_colour(command)


    def move(self, case):
        
        xy_distance = 4
        z_distance = 2
        
        xy_feed = 200
        z_feed = 100
        
        if case == 'x-':  self.m.jog_relative('X-', str(xy_distance), xy_feed)
        if case == 'x+':  self.m.jog_relative('X', str(xy_distance), xy_feed)
        if case == 'y-':  self.m.jog_relative('Y-', str(xy_distance), xy_feed)
        if case == 'y+':  self.m.jog_relative('Y', str(xy_distance), xy_feed)
        if case == 'z-':  self.m.jog_relative('Z-', str(z_distance), z_feed)
        if case == 'z+':  self.m.jog_relative('Z', str(z_distance), z_feed)


    def limit_switch_check(self, dt):
        
        switch_states = self.m.get_switch_states()
       
        if 'limit_x' in switch_states: self.limit_x_label.text = 'X min - OK'
        else: self.limit_x_label.text = 'X min'

        if 'limit_X' in switch_states: self.limit_X_label.text = 'X max - OK'
        else: self.limit_X_label.text = 'X max'

        if 'limit_y' in switch_states: self.limit_y_label.text = 'Y min - OK'
        else: self.limit_y_label.text = 'Y min'

        if 'limit_Y' in switch_states: self.limit_Y_label.text = 'Y max - OK'
        else: self.limit_Y_label.text = 'Y max'

        if 'limit_z' in switch_states: self.limit_z_label.text = 'Z min - OK'
        else: self.limit_z_label.text = 'Z min'

        if 'probe' in switch_states: self.probe_label.text = 'Probe - OK'
        else: self.probe_label.text = 'Probe'

        if 'dust_shoe_cover' in switch_states: self.dust_shoe_cover_label.text = 'Dust cover - OK'
        else: self.dust_shoe_cover_label.text = 'Dust cover'


    def return_to_home(self):
        self.sm.current = 'home'