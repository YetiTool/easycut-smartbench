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
from datetime import datetime

from asmcnc.apps.systemTools_app.screens.calibration import widget_sg_status_bar
from asmcnc.apps.systemTools_app.screens import widget_final_test_xy_move


# Kivy UI builder:
Builder.load_string("""

<StallJigScreen>:

    back_button : back_button
    run_button : run_button
    result_label : result_label
    reset_test_button : reset_test_button
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
                    id: reset_test_button
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


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))


class StallJigScreen(Screen):

    # ALL NUMBERS ARE DECLARED HERE, SO THAT THEY CAN BE EASILY EDITED AS/WHEN REQUIRED

    ## AXES, FEEDS, AND THRESHOLDS

    axes = ["X","Y","Z"]

    feed_dict = {

        "X": [8000,6000,4500,3000,2000,1200,600],
        "Y": [6000,5000,4000,3000,2000,1200,600],
        "Z": [750,600,500,400,300,150,75] 

    }

    # Min threshold, Max threshold, Step between thresholds

    threshold_dict = {

        "X": range(150, 350, 25),
        "Y": range(150, 350, 25),
        "Z": range(100, 240, 20) 

    }

    ## INDEX DICTIONARY

    ### This dictionary keeps track of which index we are "on"
    ### at any given stage

    ### This is used in conjunction with the feed and threshold dicts to extract values. 

    indices = {

        "axis": 0,
        "threshold": 0,
        "feed": 0

    }

    ## POSITIONS

    ### ABSOLUTE START POSITION OF ALL TESTS 
    ### RELATIVE TO TRUE HOME

    absolute_start_pos = {

        "X": -1100,
        "Y": -2400,
        "Z": -160

    }

    ### START POSITIONS WHEN HOMED AGAINST THE MAGNET JIG
    ### (SO NOT TRUE MACHINE COORDS)
    start_pos_x_test = {

        "X": -1100,
        "Y": -2400,
        "Z": -160

    }

    start_pos_y_test = {

        "X": -750,
        "Y": -2400,
        "Z": -160

    }

    start_pos_z_test = {

        "X": -1200,
        "Y": -2300,
        "Z": -140

    }

    start_positions = {

        "X": start_pos_x_test,
        "Y": start_pos_y_test,
        "Z": start_pos_z_test
    }


    ### CURRENT POSITION DEFINED IN CLASS INIT
    ### AS PULLS FUNCTIONS FROM ROUTER_MACHINE

    current_position = {}

    ## DEFAULT FEEDS

    fast_travel = {

        "X": 8000,
        "Y": 6000,
        "Z": 750

    }

    three_axis_max_feed = 6000

    ## ALL THE OTHER EXPERIMENTAL PARAMETERS

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

    limit_pull_off = {

        "X": -5,
        "Y": 5,
        "Z": 5

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


    ## DIS/ENABLE MOTORS DEFINED IN CLASS INIT
    ## AS PULLS FUNCTIONS FROM ROUTER_MACHINE

    disable_motors = {}
    enable_motors = {}

    ## FLAGS FOR TEST EVENTS

    setting_up_axis_for_test = False
    expected_limit_found = False
    threshold_reached = False
    all_tests_completed = False

    ## CLOCK OBJECTS

    poll_for_homing_completion_loop = None
    poll_for_ready_to_check_calibration = None
    poll_for_going_to_start_pos = None
    poll_to_set_travel = None
    poll_for_stall_position_found = None
    poll_for_threshold_detection = None
    poll_for_back_off_completion = None
    poll_to_relax_motors = None

    ## DATABASE OBJECTS

    id_stage = ""
    stall_test_events = []

    grid_button_objects = []
    
    def __init__(self, **kwargs):

        super(StallJigScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['systemtools']
        self.l=kwargs['localization']
        self.m=kwargs['machine']

        # FUNCTION DICTIONARIES

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


        # GUI SET UP

        ## FEED/THRESHOLD GRIDS FOR EACH AXIS
        self.populate_axis_grid(self.x_grid_container, 0)
        self.populate_axis_grid(self.y_grid_container, 1)
        self.populate_axis_grid(self.z_grid_container, 2)

        ## MOVE AND STATUS WIDGETS
        self.move_container.add_widget(widget_final_test_xy_move.FinalTestXYMove(machine=self.m, screen_manager=self.systemtools_sm.sm))
        self.status_container.add_widget(widget_sg_status_bar.SGStatusBar(machine=self.m, screen_manager=self.systemtools_sm.sm))


    # UNSCHEDULE ALL CLOCK OBJECTS --------------------------------------------------------------------------

    def unschedule_all_events(self):
        if self.poll_for_homing_completion_loop != None: Clock.unschedule(self.poll_for_homing_completion_loop)
        if self.poll_for_ready_to_check_calibration != None: Clock.unschedule(self.poll_for_ready_to_check_calibration)
        if self.poll_for_going_to_start_pos != None: Clock.unschedule(self.poll_for_going_to_start_pos)
        if self.poll_to_set_travel != None: Clock.unschedule(self.poll_to_set_travel)
        if self.poll_for_stall_position_found != None: Clock.unschedule(self.poll_for_stall_position_found)
        if self.poll_for_threshold_detection != None: Clock.unschedule(self.poll_for_threshold_detection)
        if self.poll_for_back_off_completion != None: Clock.unschedule(self.poll_for_back_off_completion)
        if self.poll_to_relax_motors != None: Clock.unschedule(self.poll_to_relax_motors)

    # RESET FLAGS -------------------------------------------------------------------------------------------

    def reset_flags(self):

        self.setting_up_axis_for_test = False
        self.expected_limit_found = False
        self.threshold_reached = False
        self.all_tests_completed = False

    ## DISABLE/ENABLE BUTTON FUNCTIONS ----------------------------------------------------------------------

    def disable_all_buttons_except_stop(self):

        self.disable_run(True)
        self.disable_most_buttons(True)

    def enable_all_buttons_except_run(self):

        self.disable_most_buttons(False)

    def disable_run(self, disable_bool):

        self.run_button.disabled = disable_bool

    def disable_most_buttons(self, disable_bool):

        self.back_button.disabled = disable_bool
        self.unlock_button.disabled = disable_bool
        self.home_button.disabled = disable_bool
        self.grbl_reset_button.disabled = disable_bool
        self.reset_test_button.disabled = disable_bool

        for b in self.grid_button_objects:
            b.disabled = disable_bool


    # SET UP FEED THRESHOLD GRIDS USING PRE-DEFINED DICTIONARIES ---------------------------------------------

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
                self.grid_button_objects.append(new_button)

            grid_container.add_widget(rows[tidx])


    ## FUNCTION THAT IS BOUND TO EACH GRID BUTTON TO CHOOSE TESTS

    def choose_test(self, axis_index, threshold_index, feed_index, instance=None):

        self.indices["axis"] = axis_index
        self.indices["threshold"] = threshold_index
        self.indices["feed"] = feed_index

        axis = self.axes[axis_index]
        feed = self.feed_dict[axis][feed_index]
        threshold = self.threshold_dict[axis][threshold_index]

        # BY SETTING THIS TRAVEL_TO_STALL_POS VALUE TO NONE,
        # RUN FUNCTION KNOWS TO SET UP THAT AXIS AGAIN & RE-"HOME" AND REPOSITION
        self.travel_to_stall_pos[axis] = None
        self.reset_flags()
        self.disable_run(False)

        log("CHOOSE TEST: " + str(axis) + ", " + str(feed) + ", " + str(threshold))

    # SCREEN MISC -------------------------------------------------------------------------------

    # RETURN TO FACTORY SETTINGS

    def back_to_fac_settings(self):
        self.systemtools_sm.open_factory_settings_screen()

    # SET UP SCREEN BEFORE ENTERING

    def on_pre_enter(self):

        self.test_status_label.text = self.l.get_str('STALL JIG') + '...'
        self.run_button.text = self.l.get_str('PREP TEST') + '...'
        log("Opening stall experiment wizard")

    # STALL/LIMIT EVENT DETECTION -----------------------------------------------------------------

    ## USE THE ON PRE-LEAVE FUNCTION TO DETECT IF THE SCREEN IS GOING TO CHANGE TO AN ALARM
    ## AND THEN THIS TRIGGERS CHECKS FOR WHETHER AN EXPECTED STALL ALARM OR A LIMIT

    def on_pre_leave(self):

        if not self.self.systemtools_sm.sm.current.startswith('alarm'):
            return

        self.systemtools_sm.sm.current = 'stall_jig'

        # UPDATE USER ON WHAT ALARM IS HAPPENING, IN CASE IT'S A GENERAL ONE
        self.test_status_label.text = self.m.s.alarm.alarm_code

        if self.expected_stall_alarm_detected():
            self.register_threshold_detection()

        if self.expected_limit_alarm():
            self.register_hard_limit_found()


    ## FUNCTIONS TO ANALYSE TRIGGERS AND UPDATE FOLLOWING FLAGS: 
    ## - THRESHOLD_REACHED 
    ## - EXPECTED_LIMIT_FOUND

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
        log("Threshold reached (imminent stall detected)")


    def expected_limit_alarm(self):
        if not self.axes[self.indices["axis"]] in self.m.s.alarm.limit_list:
            return False

        return True

    def register_hard_limit_found(self):
        self.m.resume_from_alarm()
        self.test_status_label.text = "LIMIT FOUND"
        self.expected_limit_found = True
        log("Hard limit found, position known")

    # HOMING --------------------------------------------------------------------------------------------

    def start_homing(self):

        log("Begin homing")

        # Issue homing commands
        normal_homing_sequence = ['$H']
        self.m.s.start_sequential_stream(normal_homing_sequence)

        # Due to polling timings, and the fact grbl doesn't issues status during homing, EC may have missed the 'home' status, so we tell it.
        self.m.set_state('Home') 
        self.test_status_label.text = "HOMING"

        # Check for completion - since it's a sequential stream, need a poll loop
        self.poll_for_homing_completion_loop = Clock.schedule_once(self.check_for_homing_completion, 2)
       
     
    def check_for_homing_completion(self, dt):

        # if alarm state is triggered which prevents homing from completing, stop checking for success
        if self.m.state().startswith('Alarm'):
            log("Poll for homing success unscheduled")
            if self.poll_for_homing_completion_loop != None: Clock.unschedule(self.poll_for_homing_completion_loop)
            self.test_status_label.text = "ALARM"
            return

        # if sequential_stream completes successfully
        if self.m.s.is_sequential_streaming == False:
            log("Homing detected as success!")
            if self.poll_for_homing_completion_loop != None: Clock.unschedule(self.poll_for_homing_completion_loop)
            self.test_status_label.text = "READY"
            return

        self.poll_for_homing_completion_loop = Clock.schedule_once(self.check_for_homing_completion, 2)


    # GENERAL ANCILLARY FUNCTIONS ------------------------------------------------------------------

    ## STOP BUTTON FUNCTION

    def stop(self):

        # This actually needs a popup, and a stop/reset
        self.unschedule_all_events()
        self.enable_all_buttons_except_run()

    ## RESET FROM ALARMS ETC.

    def grbl_reset(self):

        self.m.resume_from_alarm()
        self.test_status_label.text = "GRBL RESET"

    ## RESET CURRENT SUB-TEST (DOESN'T RESTART THOUGH - WAITS FOR USER INPUT)

    def reset_current_sub_test(self):

        self.choose_test(self.indices["axis"], self.indices["threshold"], self.indices["feed"])


    ## UNLOCK DATA SEND (IN CASE USER WANTS/NEEDS TO SEND INCOMPLETE DATA SET)

    def enable_data_send(self):

        if self.unlock_button.state == "down":
            self.unlock_button.text = "lock"
            self.send_data_button.disabled = False

        else:
            self.unlock_button.text = "unlock"
            self.send_data_button.disabled = True

    ## DO DATA SEND

    def do_data_send(self):
        pass


    # THE MAIN EVENT ----------------------------------------------------------------------------------------------------
    # HANDLES THE MANAGEMENT OF ALL STAGES OF THE TEST

    def run(self):

        self.disable_all_buttons_except_stop()
        self.threshold_reached = False

        log("Run next test")
        
        # If no tests have been started yet, SB will need to do a prep sequence instead
        if self.start_of_all_tests():
            return

        if self.end_of_all_tests():
            return

        axis = self.axes[self.indices["axis"]]

        if not self.travel_to_stall_pos[axis]:
            self.set_up_axis_for_test()
            return

        threshold_idx = self.indices["threshold"]
        feed_idx = self.indices["feed"]
        self.set_threshold_and_drive_into_barrier(axis, threshold_idx, feed_idx)
        self.poll_for_threshold_detection = Clock.schedule_once(self.sb_has_travelled_or_detected, 1)


    # CORE TEST FUNCTIONS -------------------------------------------------------------------------------------------

    ## FUNCTION TO NEATLY MOVE TO ABSOLUTE POSITION STORED IN WHATEVER POS DICTIONARY (AT MAX FEED)

    def move_all_axes(self, pos_dict):

        # CHANGE THIS  - WANT TO MOVE Z DOWN LAST
        ## AND ALSO - PROBABLY WANT TO MOVE Z UP FIRST, JUST IN CASE

        ## MIGHT ACTUALLY WANT SEQUENTIAL STREAMING HERE

        move_command = "G90 " + \
                        "X" + pos_dict["X"] + \
                        "Y" + pos_dict["Y"] + \
                        "Z" + pos_dict["Z"] + \
                        "F" + str(self.three_axis_max_feed)

        self.m.send_any_gcode_command(move_command)


    ## FUNCTION TO SET THE THRESHOLD AND CRASH INTO AN OBSTACLE

    def set_threshold_and_drive_into_barrier(self, axis, threshold_idx, feed_idx):

        threshold = self.threshold_dict[axis][threshold_idx]
        feed = self.feed_dict[axis][feed_idx]

        self.m.set_threshold_for_axis(axis, threshold)
        sleep(0.5)
        self.m.send_any_gcode_command("G91 " + axis + str(self.move_distance[axis]) + " F" + str(feed))


    ## REPOSITIONING PROCEDURE

        ## THESE FUNCTIONS ARE CALLED AS PART OF MULTIPLE PROCEDURES (E.G. AXIS SET UP, INDIVIDUAL EXPERIMENTS)
        ## ORDER OF EVENTS IS:
        ## - BACK OFF FROM THE CRASH SITE INTO A HARD LIMIT
        ## - USE THIS LIMIT TO PLACE SB FOR THE NEXT PROCEDURE
        ## - DE-ENERGIZE AND RE-ENERGIZE THE MOTORS (AS A MINI RE-SQUARE)
        ## - CARRY OUT ANY PROCEDURE/OUTCOME SPECIFIC FUNCTIONS (E.G. UNSETTING SETTING_UP FLAG OR STORING RESULT)
        ## - AND THEN CALL RUN FUNCTION AGAIN

    def back_off_and_find_position(self):

        self.m.enable_only_hard_limits()
        axis = self.axes[self.indices["axis"]]
        move_command = "G91 " + axis + str(self.back_off[axis]) + " F" + str(self.fast_travel[axis])
        self.m.send_any_gcode_command(move_command)
        self.poll_for_back_off_completion = Clock.schedule_once(lambda dt: self.back_off_completed(), 1)


    def back_off_completed(self):

        if self.expected_limit_found:
            self.m.disable_only_hard_limits()
            self.expected_limit_found = False
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
            self.finish_procedure_and_start_next_test()
            return

        self.poll_to_relax_motors = Clock.schedule_once(lambda dt: self.relax_motors(), 1)


    def finish_procedure_and_start_next_test(self):

        if self.setting_up_axis_for_test: 
            self.setting_up_axis_for_test = False

        elif self.threshold_reached:
            self.record_stall_event()
            self.go_to_next_threshold()

        else:
            self.go_to_next_feed_set()

        self.run()


    # START TEST SEQUENCE (PREP TEST): ----------------------------------------------------------------------------------

        ## HAPPENS BEFORE MAGNETS HAVE BEEN INSTALLED

        ## HOMES NORMALLY
        ## RUNS CALIBRATION CHECK (SO WE KNOW IN ADVANCE IF SOMETHING 
        ## IS GOING TO FAIL DUE TO DODGY CALIBRATION)
        ## DISABLE SOFT LIMITS
        ## MOVES
        ## TELL USER TO FIX MAGNETS
        ## USER WILL MANUALLY PRESS RUN

    def start_of_all_tests(self):

        if self.run_button.text == "RUN":
            return False

        log("Set up for all tests")

        self.start_homing()

        # CALIBRATION CHECK
        self.poll_for_ready_to_check_calibration = Clock.schedule_once(lambda dt: self.full_calibration_check(), 2)


    def full_calibration_check(self):
        if self.m.state().startswith("Idle"):
            self.m.check_x_y_z_calibration()
            Clock.schedule_interval(self.ready_to_run_tests, 5)
            return

        self.poll_for_ready_to_check_calibration = Clock.schedule_once(lambda dt: self.full_calibration_check(), 2)


    def ready_to_run_tests(self, dt):

        if self.m.checking_calibration_in_progress:
            return

        if self.m.checking_calibration_fail_info:
            self.test_status_label.text = "CAL CHECK FAIL"
            return

        if not self.m.state().startswith("Idle"):
            return

        self.m.disable_only_soft_limits()

        # go to absolute start position (relative to true home)
        self.move_all_axes(self.absolute_start_pos)

        # update labels for user input
        self.test_status_label.text = "FIX MAGNETS"
        self.run_button.text = "RUN"


    # NECESSARY SET UP THAT'S DONE EACH TIME A NEW AXIS IS TESTED ----------------------------------------------------------

    def set_up_axis_for_test(self):

        self.setting_up_axis_for_test = True

        # home against the fake magnets
        self.start_homing()

        # go to start pos for the axis (relative to the magnets)
        self.poll_for_going_to_start_pos = Clock.schedule_once(self.go_to_start_pos, 2)


    def go_to_start_pos(self, dt):

        if not self.m.state().startswith("Idle"):
            self.poll_for_going_to_start_pos = Clock.schedule_once(self.go_to_start_pos, 2)
            return

        # go to test start position, relative to faux home
        self.move_all_axes(self.start_positions[self.axes[self.indices["axis"]]])

        # when start pos set up, set travel for stall
        self.poll_to_set_travel = Clock.schedule_once(self.set_travel, 1)

    ## LOWER THE THRESHOLD AND MAX OUT THE FEED TO RECORD THE POSITION WHERE WE EXPECT SB TO STALL

    def set_travel(self):

        if not self.m.state().startswith("Idle"):
            self.poll_to_set_travel = Clock.schedule_once(self.set_travel, 1)
            return

        axis = self.axes[self.indices["axis"]]
        start_pos = self.current_position[axis]()

        self.set_threshold_and_drive_into_barrier(axis, 0, 0)
        self.poll_for_stall_position_found = Clock.schedule_once(lambda dt: self.stall_position_found(axis, start_pos), 1)


    def stall_position_found(self, axis, start_pos):

        if self.threshold_reached:
            self.travel_to_stall_pos[axis] = self.current_position[axis]() - start_pos
            self.back_off_and_find_position()
            return

        self.poll_for_stall_position_found = Clock.schedule_once(lambda dt: self.stall_position_found(axis, start_pos), 1)


    # PARSE RESULTS OF EXPERIMENT ------------------------------------------------------------------------------------------

    ## POLLED EVENT, WHEN SB IS NO LONGER MOVING AND ALARMS HAVE BEEN RESET, IT WILL START THE REPOSITIONING PROCEDURE
    def sb_has_travelled_or_detected(self, dt):

        if self.m.state().startswith("Idle"): self.back_off_and_find_position()
        else: self.poll_for_threshold_detection = Clock.schedule_once(self.sb_has_travelled_or_detected, 1)

    ## RECORD STALL EVENT TO SEND TO DATABASE AT END OF ALL EXPERIMENTS 
    ## NOTE THAT THIS IS ONLY CALLED IF THE TEST PASSES - WE DO NOT RECORD FAILED EXPERIMENT DATA IN THE DATABASE

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

        # Example data: 
        # ["ID, "X", 6000, 150, 5999, 170, -1100.4 ]

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


    ## IF TEST PASSES, GO TO NEXT THRESHOLD (UNLESS DONE ALL THRESHOLDS IN FEED SET)

    def go_to_next_threshold(self):

        if self.indices["threshold"] + 1 < len(self.threshold_dict[self.axes[self.indices["axis"]]]):
            self.indices["threshold"] = self.indices["threshold"] + 1

        else: 
            self.go_to_next_feed_set()

    # IF TEST FAILS, OR ALL THRESHOLDS TESTED FOR ONE FEED, GO TO NEXT FEED SET

    def go_to_next_feed_set(self):

        if self.indices["feed"] + 1 < len(self.feed_dict[self.axes[self.indices["axis"]]]):
            self.indices["feed"] = self.indices["feed"] + 1
            self.indices["threshold"] = 0

        else:
            self.go_to_next_axis()

    # IF AXIS COMPLETED, GO TO NEXT ONE
    ## IF ALL FEED SETS AND AXES ARE COMPLETED, 

    def go_to_next_axis(self):

        if self.indices["axis"] + 1 < len(self.axes):
            self.indices["axis"] = self.indices["axis"] + 1
            self.indices["feed"] = 0
            self.indices["threshold"] = 0

        else: 
            self.all_tests_completed = True

    # END OF ALL TESTS ------------------------------------------------------------------------------------

    ## WHEN ALL EXPERIMENTS ARE COMPLETE, DATA CAN BE SENT, AND SETTINGS REVERTED

    def end_of_all_tests(self):

        if self.all_tests_completed:

            self.m.enable_only_soft_limits()
            # acceleration back to normal
            self.test_status_label.text = "SENDING DATA"
            self.do_data_send()



    # add in functionality & do refactors that are in notebook
    # add in greater delays to prevent overshoot
    # more debug logging
    # testing

    # measurement creating & refactoring
    # set up database queries etc. 











