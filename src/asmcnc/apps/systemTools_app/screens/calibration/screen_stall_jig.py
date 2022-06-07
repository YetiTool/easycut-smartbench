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
                    on_press: root.back_to_fac_settings()

                Button: 
                    id: run_button
                    size_hint_y: 1
                    background_normal: ""
                    background_color: hex('#4CAF50FF')
                    text: "RUN"
                    on_press: root.run()

                Button:
                    id: result_label
                    size_hint_y: 1
                    background_normal: ""
                    background_color: [0,0,0,1]

                Button: 
                    id: reset_test_label
                    size_hint_y: 1
                    text: "RESET CURRENT SUB-TEST"
                    on_press: root.reset_current_sub_test()

                BoxLayout: 
                    size_hint_y: 1
                    orientation: "horizontal"

                    Button:
                        id: send_data_button 
                        size_hint_x: 2
                        disabled: True
                        text: "SEND DATA"
                        on_press: root.do_data_send()

                    ToggleButton: 
                        id: unlock_button
                        size_hint_x: 1
                        text: "unlock"
                        on_press: root.enable_data_send()
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
                    background_normal: ""
                    background_color: [1,0,0,1]
                    on_press: root.stop()

                BoxLayout:
                    size_hint_y: 4
                    id: move_container

                BoxLayout: 
                    size_hint_y: 1
                    orientation: 'horizontal'

                    Button:
                        id: home_button
                        size_hint_x: 0.5
                        text: "HOME"
                        background_normal: ""
                        background_color: hex('#1976d2ff')
                        on_press: root.start_homing()

                    Button:
                        id: grbl_reset_button
                        size_hint_x: 0.5
                        text: "GRBL RESET"
                        on_press: root.grbl_reset()


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

    axes = ["X","Y","Z"]

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

    indices = {

        "axis": 0,
        "threshold": 0,
        "feed": 0
    }

    threshold_reached = False

    poll_for_completion_loop = None
    
    def __init__(self, **kwargs):

        super(StallJigScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['systemtools']
        self.l=kwargs['localization']
        self.m=kwargs['machine']

        self.status_container.add_widget(widget_sg_status_bar.SGStatusBar(machine=self.m, screen_manager=self.systemtools_sm.sm))
        self.move_container.add_widget(widget_final_test_xy_move.FinalTestXYMove(machine=self.m, screen_manager=self.systemtools_sm.sm))

        self.test_status_label.text = self.l.get_str('STALL JIG') + '...'

        self.populate_axis_grid(self.x_grid_container, 0)
        self.populate_axis_grid(self.y_grid_container, 1)
        self.populate_axis_grid(self.z_grid_container, 2)
    

    def on_pre_enter(self):
        self.test_status_label.text = self.l.get_str('STALL JIG') + '...'


    def on_pre_leave(self):
        if self.expected_stall_alarm_detected():
            self.systemtools_sm.sm.current = 'stall_jig'
            self.register_threshold_detection()
            return


    def back_to_fac_settings(self):
        self.systemtools_sm.open_factory_settings_screen()


    def populate_axis_grid(self, grid_container, axis):
        
        first_row = BoxLayout(orientation = "horizontal")
        first_row.add_widget(Label(text = self.axes[axis], size_hint_x = 1))
        rows = []

        for i in self.feed_dict[self.axes[axis]]:

            first_row.add_widget(Label(text = str(i), size_hint_x = 1))

        grid_container.add_widget(first_row)

        for tidx, i in enumerate(self.threshold_dict[self.axes[axis]]): 
            rows.append(BoxLayout(orientation = "horizontal"))
            rows[tidx].add_widget(Label(text = str(i), size_hint_x = 1))

            for fidx, j in enumerate(self.feed_dict[self.axes[axis]]):

                new_button = Button(size_hint_x = 1)
                test_func = partial(self.choose_test, axis, tidx, fidx)
                new_button.bind(on_press = test_func)
                rows[tidx].add_widget(new_button)

            grid_container.add_widget(rows[tidx])


    def choose_test(self, axis, threshold_index, feed_index, instance):

        self.indices["axis"] = axis
        self.indices["threshold"] = threshold_index
        self.indices["feed"] = feed_index


    def expected_stall_alarm_detected(self):

        if not (
            self.systemtools_sm.sm.current.startswith('alarm') and
            self.m.s.alarm.sg_alarm and
            self.axes[self.indices["axis"]] in self.m.s.alarm.stall_axis
            ):

            return False

        return True


    def register_threshold_detection(self):

        self.threshold_reached = True
        self.m.resume_from_alarm()
        self.result_label.text = "THRESHOLD REACHED"
        self.result_label.background_color = [51/255, 255/255, 0, 1]


    def start_homing(self):

        # Issue homing commands
        normal_homing_sequence = ['$H']
        self.m.s.start_sequential_stream(normal_homing_sequence)

        # Due to polling timings, and the fact grbl doesn't issues status during homing, EC may have missed the 'home' status, so we tell it.
        self.m.set_state('Home') 
        self.test_status_label.text = "HOMING"

        # Check for completion - since it's a sequential stream, need a poll loop
        self.poll_for_completion_loop = Clock.schedule_interval(self.check_for_successful_completion, 0.2)
       
     
    def check_for_successful_completion(self, dt):

        # if alarm state is triggered which prevents homing from completing, stop checking for success
        if self.m.state().startswith('Alarm'):
            print "Poll for homing success unscheduled"
            if self.poll_for_completion_loop != None: self.poll_for_completion_loop.cancel()

        # if sequential_stream completes successfully
        elif self.m.s.is_sequential_streaming == False:
            print "Homing detected as success!"
            self.homing_detected_as_complete()


    def grbl_reset(self):

        self.m.resume_from_alarm()
        self.test_status_label.text = "GRBL RESET"


    def enable_data_send(self):

        if self.unlock_button.state == "down":
            self.unlock_button.text = "lock"
            self.send_data_button.disabled = False

        else:
            self.unlock_button.text = "unlock"
            self.send_data_button.disabled = True


    def do_data_send(self):
        pass

    def stop(self):
        pass

    def reset_current_sub_test(self):
        pass

    def run(self):
        pass











































