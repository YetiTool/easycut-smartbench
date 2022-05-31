# -*- coding: utf-8 -*-
'''
Created Mayh 2019

@author: Letty

Basic screen 
'''
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import sys, os

from asmcnc.apps.systemTools_app.screens.calibration import widget_sg_status_bar
from asmcnc.apps.systemTools_app.screens import widget_final_test_xy_move
from asmcnc.apps.systemTools_app.screens.calibration import widget_feed_threshold_grid

# Kivy UI builder:
Builder.load_string("""

<StallJigScreen>:

    stall_jig_label: stall_jig_label
    move_container : move_container

    x_grid_container : x_grid_container

    console_status_text : console_status_text
    status_container : status_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: 0.92
            orientation: 'vertical'


            BoxLayout: 
                size_hint_y: 1
                orientation: 'horizontal'

                Button:
                    size_hint_x: 0.25
                    text: "<< Back"

                Button:
                    size_hint_x: 0.25
                    text: "Home"

                Button:
                    size_hint_x: 0.5
                    text: "STOP"


            BoxLayout: 
                size_hint_y: 5
                orientation: 'horizontal'

                BoxLayout: 
                    size_hint_x: 0.25
                    orientation: "vertical"


                    Button: 
                        size_hint_y: 1

                    Label:
                        size_hint_y: 1

                    Button: 
                        size_hint_y: 1

                    BoxLayout: 
                        size_hint_y: 1
                        orientation: "horizontal"

                        Button: 
                            size_hint_x: 2

                        Button: 
                            size_hint_x: 1
                    Label:
                        id: stall_jig_label
                        size_hint_y: 1


                BoxLayout: 
                    size_hint_x: 0.5
                    orientation: "vertical"

                    BoxLayout:
                        size_hint_y: 4
                        id: move_container

                    ScrollableLabelStatus:
                        size_hint_y: 1
                        id: console_status_text
                        text: "status update" 

                BoxLayout: 
                    size_hint_x: 0.25

                    BoxLayout: 
                        id: x_grid_container
                        size_hint_y: 1

                    BoxLayout: 
                        size_hint_y: 1

                    BoxLayout: 
                        size_hint_y: 1

        BoxLayout:
            size_hint_y: 0.08
            id: status_container        

""")

class StallJigScreen(Screen):
    
    def __init__(self, **kwargs):
        super(StallJigScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.l=kwargs['localization']
        self.m=kwargs['machine']

        self.status_container.add_widget(widget_sg_status_bar.SGStatusBar(machine=self.m, screen_manager=self.sm))
        self.move_container.add_widget(widget_final_test_xy_move.FinalTestXYMove(machine=self.m, screen_manager=self.sm))
        self.x_grid_container.add_widget(widget_feed_threshold_grid.FeedThresholdGrid(machine=self.m, screen_manager=self.sm, parent_screen=self))

        self.stall_jig_label.text = self.l.get_str('STALL JIG') + '...'

    def update_status_text(self, dt):
        try: self.console_status_text.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text
        except: self.console_status_text.text = "dev\ndev\ndev"
    
    def on_pre_enter(self):
        self.stall_jig_label.text = self.l.get_str('STALL JIG') + '...'
        self.poll_for_status = Clock.schedule_interval(self.update_status_text, 0.4)

    def on_pre_leave(self):
        if self.sm.current.startswith('alarm'):
            self.sm.current = 'stall_jig'
            self.stall_jig_label.text = self.l.get_str('NUH UHHHH') + '...'
            return

    def on_leave(self):
        Clock.unschedule(self.poll_for_status)

