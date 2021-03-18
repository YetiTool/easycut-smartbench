'''
Created on 16 March 2021
Screen to help production move through final test more quickly

@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from asmcnc.skavaUI import widget_status_bar, widget_gcode_monitor
from asmcnc.apps.systemTools_app.screens import widget_final_test_xy_move

import os, sys

Builder.load_string("""

<FinalTestScreen>

    move_container : move_container
    gcode_monitor_container : gcode_monitor_container
    status_container : status_container

    BoxLayout:
        padding: 0
        spacing: 0
        orientation: "vertical"
        canvas:
            Color:
                rgba: hex('#E5E5E5FF')
            Rectangle:
                size: self.size
                pos: self.pos
        BoxLayout:
            size_hint_y: 0.92
            padding: 0
            spacing: 10
            orientation: "vertical"

            GridLayout: 
                pos: self.parent.pos
                size_hint_y: 0.13
                rows: 1
                cols: 6
                spacing: 5

                Button:
                    text: "G91 G0 X1150.3"
                    on_press: root.X_plus()

                Button:
                	text: "G91 G0 X-1150.3"
                    on_press: root.X_minus()

                Button:
					text: "G91 G0 Y1636.6"
                    on_press: root.Y_plus()

                Button:
                	text: "G91 G0 Y-1636.6"
                    on_press: root.Y_minus()

                Button:
                    text: "G91 G0 X575.0"
                    on_press: root.X_575()

                Button:
                    text: "Factory Settings"
                    on_press: root.go_back()

                # Button:
                #     text: "Lobby"
                #     on_press: root.exit_app()

            BoxLayout:
                size_hint_y: 0.64
                orientation: 'horizontal'
                BoxLayout:
                    height: self.parent.height
                    size_hint_x: 0.7
                    id: move_container
                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos
                BoxLayout:
                    height: self.parent.height
                    id: gcode_monitor_container
        BoxLayout:
            size_hint_y: 0.08
            id: status_container



""")

class FinalTestScreen(Screen):

    def __init__(self, **kwargs):
        super(FinalTestScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.m = kwargs['machine']

        # WIDGET SETUP
        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.systemtools_sm.sm))
        self.gcode_monitor_container.add_widget(widget_gcode_monitor.GCodeMonitor(machine=self.m, screen_manager=self.systemtools_sm.sm))
        self.move_container.add_widget(widget_final_test_xy_move.FinalTestXYMove(machine=self.m, screen_manager=self.systemtools_sm.sm))

    def on_enter(self):
        self.m.send_any_gcode_command("AZ")
        self.m.set_led_colour('BLUE')

    def on_leave(self):
        self.m.send_any_gcode_command("AX")

    def go_back(self):
        self.systemtools_sm.open_factory_settings_screen()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    def X_plus(self):
    	self.m.send_any_gcode_command("G91 G0 X1150.3")
        self.m.set_led_colour('BLUE')

    def X_minus(self):
    	self.m.send_any_gcode_command("G91 G0 X-1150.3")
        self.m.set_led_colour('BLUE')

    def Y_plus(self):
    	self.m.send_any_gcode_command("G91 G0 Y1636.6")
        self.m.set_led_colour('BLUE')

    def Y_minus(self):
    	self.m.send_any_gcode_command("G91 G0 Y-1636.6")
        self.m.set_led_colour('BLUE')

    def X_575(self):
        self.m.send_any_gcode_command("G91 G0 X575.0")
        self.m.set_led_colour('BLUE')

