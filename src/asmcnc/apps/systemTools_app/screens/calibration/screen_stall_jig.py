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
                    text: "PREP TEST"
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

    stall_tolerance = {

        "X": 3,
        "Y": 3,
        "Z": 1

    }

    overjog = {

        "X": 8,
        "Y": 8,
        "Z": 8

    }

    backoff = {

        "X": 10,
        "Y": -10,
        "Z": 10

    }

    fast_travel = {

        "X": 8000,
        "Y": 6000,
        "Z": 750

    }


    initial_move_distance = {

        "X": -10,
        "Y": 10,
        "Z": -10

    }

    travel_to_stall_pos = {

        "X": None,
        "Y": None,
        "Z": None

    }

    limit_pull_off = {

        "X": -5,
        "Y": 5,
        "Z": 5

    }


    start_pos_x_test = {

        "X": -1100,
        "Y": - 2400,
        "Z": -160

    }


    start_pos_y_test = {

        "X": -750,
        "Y": - 2400,
        "Z": -160

    }

    start_pos_z_test = {

        "X": -1200,
        "Y": - 2300,
        "Z": -140

    }

    current_position = {}

    threshold_reached = False
    setting_up_axis_for_test = False
    og_homed = False

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
    

        self.current_position = {

            "X": self.m.mpos_x,
            "Y": self.m.mpos_y,
            "Z": self.m.mpos_z

        }

        self.disable_motors = {

            "X": self.m.disable_x_motors,
            "Y": self.m.disable_y_motors,
            "Z": self.m.disable_z_motor

        }

        self.enable_motors = {

            "X": self.m.enable_x_motors,
            "Y": self.m.enable_y_motors,
            "Z": self.m.enable_z_motor

        }


    def on_pre_enter(self):
        self.test_status_label.text = self.l.get_str('STALL JIG') + '...'

    def on_pre_leave(self):

        if not self.self.systemtools_sm.sm.current.startswith('alarm'):
            return

        self.systemtools_sm.sm.current = 'stall_jig'

        if self.expected_stall_alarm_detected():
            self.register_threshold_detection()

        if self.expected_limit_alarm():
            self.register_hard_limit_found()


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
            self.m.s.alarm.sg_alarm and
            self.axes[self.indices["axis"]] in self.m.s.alarm.stall_axis
            ):
            return False

        self.m.s.alarm.sg_alarm = False
        self.m.s.alarm.stall_axis = "W"
        return True


    def register_threshold_detection(self):

        self.m.resume_from_alarm()
        self.result_label.text = "THRESHOLD REACHED"
        self.result_label.background_color = [51/255, 255/255, 0, 1]
        self.threshold_reached = True


    def expected_limit_alarm(self):
        if not self.axes[self.indices["axis"]] in self.m.s.alarm.limit_list:
            return False

        return True


    def register_hard_limit_found(self):
        self.m.resume_from_alarm()
        self.test_status_label.text = "STALL POS FOUND"
        self.expected_limit_found = True


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
            self.test_status_label.text = "ALARM"

        # if sequential_stream completes successfully
        elif self.m.s.is_sequential_streaming == False:
            print "Homing detected as success!"
            self.test_status_label.text = "READY"
            self.og_homed = True



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

        self.threshold_reached = False
        
        # If no tests have been started yet, SB will need to do a prep sequence instead
        if self.start_of_all_tests():
            return

        if self.end_of_all_tests():
            return

        axis = self.axes[self.indices["axis"]]

        if not self.travel_to_stall_pos[axis]:
            self.set_travel()
            return

        threshold = self.threshold_dict[axis][self.indices["threshold"]]
        feed = self.feed_dict[axis][self.indices["feed"]]

        self.m.set_threshold_for_axis(axis, threshold)
        sleep(0.5)
        self.m.send_any_gcode_command("G91 " + axis + str(self.move_distance[axis]) + " F" + str(feed))
        self.poll_for_threshold_detection = Clock.schedule_once(self.sb_has_travelled_or_detected, 1)


    def start_of_all_tests(self):

        if not (self.indices["axis"] == 0 and
            self.indices["threshold"] == 0 and
            self.indices["feed"] == 0 and
            not self.travel_to_stall_pos["X"]):
            return False

        # start calibration/set up sequence here

        # HOME
        if not self.og_homed: self.start_homing()

        # CALIBRATION CHECK
        self.poll_for_ready_to_check_calibration = Clock.schedule_once(lambda dt: self.full_calibration_check(), 2)

        # DISABLE SOFT LIMITS
        # TELL USER TO FIX MAGNETS



    def full_calibration_check(self):
        if self.m.state().startswith("Idle"):
            self.m.check_x_y_z_calibration()


        # clock ready to run tests


    def ready_to_run_tests(self):
        pass

        # if idle: 
            # disable soft limits
            # go to start position
            # tell user to fix magnets
            # self.run_button.text = "RUN"




    def end_of_all_tests(self):

        if not (self.indices["axis"] + 1 < len(self.axes) and
            self.indices["threshold"] + 1 < len(self.threshold_dict[self.axes[self.indices["axis"]]]) and
            self.indices["feed"] + 1 < len(self.feed_dict[self.axes[self.indices["axis"]]])):
            return False

        self.test_status_label.text = "SENDING DATA"
        self.do_data_send()


    def sb_has_travelled_or_detected(self, dt):

        if self.m.state().startswith("Idle"): self.back_off_and_find_position()
        else: self.poll_for_threshold_detection = Clock.schedule_once(self.sb_has_travelled_or_detected, 1)


    def back_off_and_find_position(self):

        self.m.enable_only_hard_limits()
        axis = self.axes[self.indices["axis"]]
        move_command = "G91 " + axis + str(self.back_off[axis]) + " F" + str(self.fast_travel[axis])
        self.m.send_any_gcode_command(move_command)
        self.poll_for_back_off_completion = Clock.schedule_once(lambda dt: self.back_off_completed(), 1)


    def back_off_completed(self):

        if self.expected_limit_found:
            self.m.disable_only_hard_limits()
            axis = self.axes[self.indices["axis"]]
            move_command = "G91 " + axis + str(self.limit_pull_off[axis]) + " F" + str(self.fast_travel[axis])
            self.m.send_any_gcode_command(move_command)
            self.poll_to_relax_motors = Clock.schedule_once(lambda dt: self.relax_motors(), 1)
            return

        self.poll_for_back_off_completion = Clock.schedule_once(lambda dt: self.back_off_completed(), 1)


    def relax_motors(self):

        if self.m.state().startswith("Idle"):
            self.disable_motors[self.axes[self.indices["axis"]]]()
            sleep(1)
            self.enable_motors[self.axes[self.indices["axis"]]]()
            sleep(1)
            self.m.enable_only_hard_limits()
            self.pass_or_fail_test()
            return

        self.poll_to_relax_motors = Clock.schedule_once(lambda dt: self.relax_motors(), 1)


    def pass_or_fail_test(self):

        if setting_up_axis_for_test: 
            pass

        elif self.threshold_reached:
            self.record_stall_event()
            self.go_to_next_threshold()

        else:
            self.go_to_next_feed_set()

        self.run()


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


    def go_to_next_threshold(self):

        if self.indices["threshold"] + 1 < len(self.threshold_dict[self.axes[self.indices["axis"]]]):
            self.indices["threshold"] = self.indices["threshold"] + 1

        elif self.indices["feed"] + 1 < len(self.feed_dict[self.axes[self.indices["axis"]]]):
            self.indices["feed"] = self.indices["feed"] + 1
            self.indices["threshold"] = 0

        elif self.indices["axis"] + 1 < len(self.axes):
            self.indices["axis"] = self.indices["axis"] + 1
            self.indices["feed"] = 0
            self.indices["threshold"] = 0


    def go_to_next_feed_set(self):

        if self.indices["feed"] + 1 < len(self.feed_dict[self.axes[self.indices["axis"]]]):
            self.indices["feed"] = self.indices["feed"] + 1
            self.indices["threshold"] = 0

        elif self.indices["axis"] + 1 < len(self.axes):
            self.indices["axis"] = self.indices["axis"] + 1
            self.indices["feed"] = 0
            self.indices["threshold"] = 0


    def set_travel(self):

        if not self.m.state().startswith("Idle"):
            self.test_status_label.text = "NOT IDLE!"
            return

        axis = self.axes[self.indices["axis"]]
        threshold = self.threshold_dict[axis][0]

        start_pos = self.current_position[axis]()

        self.m.set_threshold_for_axis(axis, threshold)
        sleep(0.5)
        self.m.send_any_gcode_command("G91 " + axis + str(self.move_distance[axis]) + " F" + str(feed))
        self.poll_for_stall_position_found = Clock.schedule_once(lambda dt: self.stall_position_found(axis, start_pos), 1)


    def stall_position_found(self, axis, start_pos):

        if self.threshold_reached:
            self.travel_to_stall_pos[axis] = self.current_position[axis]() - start_pos
            self.back_off_and_find_position()
            return

        self.poll_for_stall_position_found = Clock.schedule_once(lambda dt: self.stall_position_found(axis, start_pos), 1)


    def unschedule_all_events(self):
        pass























