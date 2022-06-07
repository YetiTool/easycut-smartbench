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


# Kivy UI builder:
Builder.load_string("""

<StallJigScreen>:

    back_button : back_button
    run_button : run_button
    result_label : result_label
    reset_test_label : reset_test_label
    send_data_button : send_data_button
    unlock_button : unlock_button
    test_status_label : test_status_label

    stop_button : stop_button
    move_container : move_container
    home_button : home_button
    grbl_reset_button : grbl_reset_button


    x_grid_container : x_grid_container
    y_grid_container : y_grid_container
    z_grid_container : z_grid_container

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
                    id: back_button
                    size_hint_y: 1
                    text: "<< Back"

                Button: 
                    id: run_button
                    size_hint_y: 1

                Label:
                    id: result_label
                    size_hint_y: 1

                Button: 
                    id: reset_test_label
                    size_hint_y: 1

                BoxLayout: 
                    size_hint_y: 1
                    orientation: "horizontal"

                    Button:
                        id: send_data_button 
                        size_hint_x: 2

                    Button: 
                        id: unlock_button
                        size_hint_x: 1
                Label:
                    id: test_status_label
                    size_hint_y: 1

            BoxLayout: 
                size_hint_x: 0.4
                orientation: "vertical"

                Button:
                    id: stop_button
                    size_hint_y: 1
                    text: "STOP"

                BoxLayout:
                    size_hint_y: 4
                    id: move_container

                BoxLayout: 
                    size_hint_y: 1
                    orientation: 'horizontal'

                    Button:
                        id: home_button
                        size_hint_x: 0.5
                        text: "Home"

                    Button:
                        id: grbl_reset_button
                        size_hint_x: 0.5
                        text: "GRBL RESET"


            BoxLayout: 
                size_hint_x: 0.35
                orientation: "vertical"

                BoxLayout: 
                    id: x_grid_container
                    size_hint_y: len(root.threshold_dict["X"])
                    orientation: "vertical"

                BoxLayout: 
                    id: y_grid_container
                    size_hint_y: len(root.threshold_dict["Y"])
                    orientation: "vertical"

                BoxLayout: 
                    id: z_grid_container
                    size_hint_y: len(root.threshold_dict["Z"])
                    orientation: "vertical"

        BoxLayout:
            size_hint_y: 0.08
            id: status_container        

""")

class StallJigScreen(Screen):

    feed_dict = {

        "X": [8000,6000,4500,3000,2000,1200,600],
        "Y": [6000,5000,4000,3000,2000,1200,600],
        "Z": [750,600,500,400,300,150,75] 

    }

    threshold_dict = {

        "X": range(150, 350, 25),
        "Y": range(150, 350, 25),
        "Z": range(100, 240, 20) 

    }
    
    def __init__(self, **kwargs):
        super(StallJigScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.l=kwargs['localization']
        self.m=kwargs['machine']

        self.status_container.add_widget(widget_sg_status_bar.SGStatusBar(machine=self.m, screen_manager=self.sm))
        self.move_container.add_widget(widget_final_test_xy_move.FinalTestXYMove(machine=self.m, screen_manager=self.sm))

        self.test_status_label.text = self.l.get_str('STALL JIG') + '...'

        # self.populate_axis_grid(self.x_grid_container, "X")
        # self.populate_axis_grid(self.y_grid_container, "Y")
        # self.populate_axis_grid(self.z_grid_container, "Z")
    
    def on_pre_enter(self):
        self.test_status_label.text = self.l.get_str('STALL JIG') + '...'

    def on_pre_leave(self):
        if self.sm.current.startswith('alarm'):
            self.sm.current = 'stall_jig'
            self.test_status_label.text = self.l.get_str('NUH UHHHH') + '...'
            return

    def on_leave(self):
        Clock.unschedule(self.poll_for_status)

    def populate_axis_grid(self, grid_container, axis):
        
        first_row = BoxLayout(orientation = "horizontal")
        first_row.add_widget(Label(text = axis, size_hint_x = 1))
        rows = []

        for i in self.feed_dict[axis]:

            first_row.add_widget(Label(text = str(i), size_hint_x = 1))

        grid_container.add_widget(first_row)

        for idx, i in enumerate(self.threshold_dict[axis]): 
            rows.append(BoxLayout(orientation = "horizontal"))
            rows[idx].add_widget(Label(text = str(i), size_hint_x = 1))

            for j in self.feed_dict[axis]:

                new_button = Button(size_hint_x = 1)
                test_func = partial(self.choose_test, i, j)
                new_button.bind(on_press = test_func)
                rows[idx].add_widget(new_button)

            grid_container.add_widget(rows[idx])

    def choose_test(self, threshold, feed, instance):

        try: 
            threshold = int(threshold)
            feed = int(feed)

            print("TEST: " + str(threshold) + ", " + str(feed))

        except: 
            print("no dice")














































