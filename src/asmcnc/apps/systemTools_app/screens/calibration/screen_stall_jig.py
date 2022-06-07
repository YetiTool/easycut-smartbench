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
from time import sleep

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
                    padding: [0,10]

                    BoxLayout:
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

    stall_tolerance_xy = 3
    stall_tolerance_z = 1

    overjog_xy = 8
    overjog_z = 8

    backoff_x = 10
    backoff_y = -10
    backoff_z = 10

    fast_x = 8000
    fast_y = 6000
    fast_z = 750

    move_distance = {

        "X": 10 + overjog_xy,
        "Y": 10 + overjog_xy,
        "Z": 10 + overjog_z

    }

    threshold_reached = False

    poll_for_completion_loop = None
    poll_for_threshold_detection = None
    poll_for_back_off_completion = None

    id_stage = ""

    stall_test_events = []
    
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

        self.m.resume_from_alarm()
        self.result_label.text = "THRESHOLD REACHED"
        self.result_label.background_color = [51/255, 255/255, 0, 1]
        self.threshold_reached = True


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
        
        # If no tests have been started yet, SB will need to do a prep sequence instead
        if self.start_of_all_tests():
            return

        axis = self.axes[self.indices["axis"]]
        threshold = self.threshold_dict[axis][self.indices["threshold"]]
        feed = self.feed_dict[axis][self.indices["feed"]]

        self.m.set_threshold_for_axis(axis, threshold)
        sleep(0.5)
        self.m.send_any_gcode_command("G91 " + axis + str(self.move_distance[axis]) + " F" + feed)
        self.poll_for_threshold_detection = Clock.schedule_once(self.sb_has_travelled_or_detected, 1)


    def sb_has_travelled_or_detected(self):

        if self.m.state().startswith("Idle"): self.back_off()
        else: self.poll_for_threshold_detection = Clock.schedule_once(self.sb_has_travelled_or_detected, 1)

        # if self.threshold_reached: self.pass_condition()
        # elif self.m.state().startswith("Idle"): self.fail_condition()
        # else: self.poll_for_threshold_detection = Clock.schedule_once(self.sb_has_travelled_or_detected, 1)


    def start_of_all_tests(self):

        if not (self.indices["axis"] == 0 and
            self.indices["threshold"] == 0 and
            self.indices["feed"] == 0):
            return False
            
        # start calibration/set up sequence here

        # HOME
        # CALIBRATION CHECK
        # SET STALL POSITION FOR X

        return True


    def pass_condition(self):

        self.pass_sub_test = True

        

    def back_off(self):

        # refactor
        if self.indices["axis"] == 0: 
            final_pos = self.m.mpos_x() + backoff_x
            feed = "F" + str(fast_x)

        if self.indices["axis"] == 1:
            final_pos = self.m.mpos_y() + backoff_y 
            feed = "F" + str(fast_y)

        if self.indices["axis"] == 2:
            final_pos = self.m.mpos_z() + backoff_z
            feed = "F" + str(fast_z)

        self.m.send_any_gcode_command("G91 " + self.axes[self.indices["axis"]] + str(final_pos) + feed)
        self.poll_for_back_off_completion = Clock.schedule_once(lambda dt: self.back_off_completed(final_pos), 1)


    def back_off_completed(self, final_pos):

        if self.indices["axis"] == 0: pos = self.m.mpos_x()
        if self.indices["axis"] == 1: pos = self.m.mpos_y()
        if self.indices["axis"] == 2: pos = self.m.mpos_z()

        if round(pos, 1) == round(final_pos, 1) and self.m.state().startswith("Idle"):

            self.start_stalling_or_homing()
            return

        self.poll_for_back_off_completion = Clock.schedule_once(lambda dt: self.back_off_completed(final_pos), 1)


    def start_stalling_or_homing(self):
        pass # TBC


    def relax_motors(self):
        # write dedicated funcs for this in router_machine
        pass


    def reposition_for_next_test(self):
        pass



    def record_stall_event(self):

        # Calculate feed rate at stall
        if self.indices["axis"] == 0: 
            step_rate = self.m.s.setting_100
            stall_coord = self.m.s.last_stall_x_coord

        if self.indices["axis"] == 1: 
            step_rate = self.m.s.setting_101
            stall_coord = self.m.s.last_stall_y_coord

        if self.indices["axis"] == 2: 
            step_rate = self.m.s.setting_102
            stall_coord = self.m.s.last_stall_z_coord

        step_us = self.m.s.last_stall_motor_step_size
        rpm = 60*(1000000.0/step_us)/3200
        reported_feed = 3200.0 / step_rate * rpm


        last_test_pass = [

            id_stage,
            self.axes[self.indices["axis"]],
            self.feed_dict[axis][self.indices["feed"]],
            self.threshold_dict[axis][self.indices["threshold"]],
            reported_feed,
            self.m.s.last_stall_load,
            stall_coord
        ]

        self.stall_test_events.append(last_test_pass)



    def start_next_test(self):

        self.record_stall_event()
        self.threshold_reached = False

        if self.indices["threshold"] + 1 < len(self.threshold_dict[self.axes[self.indices["axis"]]]):
            self.indices["threshold"] = self.indices["threshold"] + 1

        elif self.indices["feed"] + 1 < len(self.feed_dict[self.axes[self.indices["axis"]]]):
            self.indices["feed"] = self.indices["feed"] + 1
            self.indices["threshold"] = 0

        elif self.indices["axis"] + 1 < len(self.axes):
            self.indices["axis"] = self.indices["axis"] + 1
            self.indices["feed"] = 0
            self.indices["threshold"] = 0

        else: 
            self.end_of_tests()



    def fail_condition(self):

        self.pass_sub_test = False



    def go_to_next_feed_set(self):

        if self.indices["feed"] + 1 < len(self.feed_dict[self.axes[self.indices["axis"]]]):
            self.indices["feed"] = self.indices["feed"] + 1
            self.indices["threshold"] = 0

        elif self.indices["axis"] + 1 < len(self.axes):
            self.indices["axis"] = self.indices["axis"] + 1
            self.indices["feed"] = 0
            self.indices["threshold"] = 0

        else: 
            self.end_of_tests()




    def end_of_tests(self):

        self.test_status_label.text = "SENDING DATA"
        self.do_data_send()


    def unschedule_all_events(self):
        pass


































