# -*- coding: utf-8 -*-
'''
Created Mayh 2019

@author: Letty

Basic screen 
'''
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from  kivy.uix.boxlayout import BoxLayout
from  kivy.uix.label import Label
from  kivy.uix.button import Button
from kivy.clock import Clock
import sys, os
from functools import partial

from asmcnc.apps.systemTools_app.screens.calibration import widget_sg_status_bar
from asmcnc.apps.systemTools_app.screens import widget_final_test_xy_move
from asmcnc.apps.systemTools_app.screens.calibration import widget_feed_threshold_grid

# Kivy UI builder:
Builder.load_string("""

<StallJigScreen>:

    stall_jig_label: stall_jig_label
    move_container : move_container

    x_grid_container : x_grid_container
    y_grid_container : y_grid_container

    status_container : status_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: 0.92
            orientation: 'horizontal'

            BoxLayout: 
                size_hint_x: 0.25
                orientation: "vertical"

                Button:
                    size_hint_y: 1
                    text: "<< Back"

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

                Button:
                    size_hint_y: 1
                    text: "STOP"

                BoxLayout:
                    size_hint_y: 4
                    id: move_container

                BoxLayout: 
                    size_hint_y: 1
                    orientation: 'horizontal'

                    Button:
                        size_hint_x: 0.5
                        text: "Home"

                    Button:
                        size_hint_x: 0.5
                        text: "GRBL RESET"


            BoxLayout: 
                size_hint_x: 0.25
                orientation: "vertical"

                BoxLayout: 
                    id: x_grid_container
                    size_hint_y: 1

                BoxLayout: 
                    id: y_grid_container
                    size_hint_y: 1
                    orientation: "vertical"

                BoxLayout: 
                    size_hint_y: 1

        BoxLayout:
            size_hint_y: 0.08
            id: status_container        

""")

class StallJigScreen(Screen):


    y_feeds = [6000,5000,4000,3000,1200,600]
    y_thresholds = range(150, 350, 25)
    
    def __init__(self, **kwargs):
        super(StallJigScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.l=kwargs['localization']
        self.m=kwargs['machine']

        self.status_container.add_widget(widget_sg_status_bar.SGStatusBar(machine=self.m, screen_manager=self.sm))
        self.move_container.add_widget(widget_final_test_xy_move.FinalTestXYMove(machine=self.m, screen_manager=self.sm))
        self.x_grid_container.add_widget(widget_feed_threshold_grid.FeedThresholdGrid(machine=self.m, screen_manager=self.sm, parent_screen=self))

        self.stall_jig_label.text = self.l.get_str('STALL JIG') + '...'

        self.populate_y_grid()
    
    def on_pre_enter(self):
        self.stall_jig_label.text = self.l.get_str('STALL JIG') + '...'

    def on_pre_leave(self):
        if self.sm.current.startswith('alarm'):
            self.sm.current = 'stall_jig'
            self.stall_jig_label.text = self.l.get_str('NUH UHHHH') + '...'
            return

    def on_leave(self):
        Clock.unschedule(self.poll_for_status)

    def choose_test(self, feed, threshold, instance):
        if not isinstance(feed,int) or not isinstance(threshold, int):
            return

        print("THINGS")
        print(feed)
        print(threshold)


    def populate_y_grid(self):
        
        first_row = BoxLayout(orientation = "horizontal")
        first_row.add_widget(Label(text = "Y", size_hint_x = 1))
        rows = []

        for i in self.y_feeds:

            first_row.add_widget(Label(text = str(i), size_hint_x = 1))

        self.y_grid_container.add_widget(first_row)

        for idx, i in enumerate(self.y_thresholds): 
            rows.append(BoxLayout(orientation = "horizontal"))
            rows[idx].add_widget(Label(text = str(i), size_hint_x = 1))

            for j in self.y_feeds:

                new_button = Button(size_hint_x = 1)
                test_func = partial(self.choose_test, j, i)
                new_button.bind(on_press = test_func)
                rows[idx].add_widget(new_button)


            self.y_grid_container.add_widget(rows[idx])















































