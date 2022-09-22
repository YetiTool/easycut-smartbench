# -*- coding: utf-8 -*-
'''
Created June 2022

@author: Letty

Stall detection experiment
'''
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from  kivy.uix.boxlayout import BoxLayout
from  kivy.uix.label import Label
from  kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
import sys, os
from functools import partial
from time import sleep, time
from datetime import datetime

from asmcnc.apps.systemTools_app.screens.calibration import widget_sg_status_bar
from asmcnc.apps.systemTools_app.screens import widget_final_test_xy_move
from asmcnc.apps.systemTools_app.screens.popup_system import PopupStopStallJig
from asmcnc.production.database.calibration_database import CalibrationDatabase
from asmcnc.skavaUI.popup_info import PopupMiniInfo

# Kivy UI bsystemTools_sm.uilder:
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
    # reset_tmc_regs : reset_tmc_regs
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
                    background_color: root.pass_green
                    text: "PREP TEST"
                    on_press: root.run()

                Button:
                    id: result_label
                    size_hint_y: 1
                    background_normal: ""
                    background_down: ""
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
                        on_press: root.start_stall_jig_data_send()

                    ToggleButton: 
                        id: unlock_button
                        size_hint_x: 1
                        text: "unlock"
                        on_press: root.enable_data_send()
                Label:
                    id: test_status_label
                    size_hint_y: 1

            BoxLayout: 
                size_hint_x: 0.35
                orientation: "vertical"

                BoxLayout: 
                    size_hint_y: 1
                    orientation: "horizontal"

                    Button:
                        id: stop_button
                        text: "STOP"
                        background_normal: ""
                        background_color: root.stop_red
                        on_press: root.stop()

                    # Button: 
                    #     id: reset_tmc_regs
                    #     text: "RESET FW SETTINGS"
                    #     on_press: root.reset_tmcs()
                    #     font_size: '12sp'

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
                        background_color: root.easycut_blue
                        on_press: root.start_homing()

                    Button:
                        id: grbl_reset_button
                        size_hint_x: 0.5
                        text: "GRBL RESET"
                        on_press: root.grbl_reset()


            BoxLayout: 
                size_hint_x: 0.4
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

    dev_mode = True

    # ALL NUMBERS ARE DECLARED HERE, SO THAT THEY CAN BE EASILY EDITED AS/WHEN REQUIRED

    ## AXES, FEEDS, AND THRESHOLDS

    axes = ["X","Y","Z"]

    # # MICRO TEST

    # feed_dict = {

    #     "X": [8000,6000],
    #     "Y": [6000,5000],
    #     "Z": [750,600] 

    # }

    # # Min threshold, Max threshold, Step between thresholds

    # # FILTERED FW

    # threshold_dict = {

    #     "X": range(200, 275, 25),
    #     "Y": range(150, 225, 25),
    #     "Z": range(100, 160, 20) 

    # }

    feed_dict = {

        "X": [8000,6000,4500,3000,2000,1200,600],
        "Y": [6000,5000,4000,3000,2000,1200,600],
        "Z": [750,600,500,400,300,150,75] 

    }

    # Min threshold, Max threshold, Step between thresholds

    # FILTERED FW

    threshold_dict = {

        "X": range(100, 375, 25),
        "Y": range(100, 375, 25),
        "Z": range(100, 220, 20) 

    }

    # UNFILTERED FW

    # threshold_dict = {

    #     "X": range(250, 400, 25),
    #     "Y": range(275, 450, 25),
    #     "Z": range(160, 300, 20) 

    # }


    ## INDEX DICTIONARY

    ### This dictionary keeps track of which index we are "on"
    ### at any given stage

    ### This is used in conjunction with the feed and threshold dicts to extract values. 

    indices = {

        "axis": 0,
        "threshold": 0,
        "feed": 0

    }

    minimum_threshold_index = {

        "X": 0,
        "Y": 0,
        "Z": 0,

    }

    ## POSITIONS

    ### ABSOLUTE START POSITION OF ALL TESTS 
    ### RELATIVE TO TRUE HOME

    absolute_start_pos = {

        "X": -1299,
        "Y": -2501,
        "Z": -1

    }

    ### START POSITIONS WHEN HOMED AGAINST THE MAGNET JIG
    ### (SO NOT TRUE MACHINE COORDS)

    start_pos_x_test = {

        "X": -1300,
        "Y": -2501,
        "Z": -70

    }

    start_pos_y_test = {

        "X": -1210,
        "Y": -2502,
        "Z": -70

    }

    start_pos_z_test = {

        "X": -1299,
        "Y": -2405,
        "Z": 0

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

    ## ALL THE OTHER EXPERIMENTAL PARAMETERS

    stall_tolerance = {

        "X": 10,     # 3
        "Y": 10,    # 3
        "Z": -3     # -1

    }

    back_off = {

        "X": -430,  #  -400, 
        "Y": -120,   #  -70,
        "Z": 100     #  76

    }

    limit_pull_off = {

        "X": 300,   # 5
        "Y": 5,     # 5
        "Z": -2     # 5

    }

    crash_distance = {

        "X": 101,   # 381
        "Y": 75,   # 65
        "Z": -73    # -70

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
    false_stall_happened = False
    all_tests_completed = False
    test_stopped = False
    test_passed = False

    ## CLOCK OBJECTS

    poll_for_homing_completion_loop = None    
    poll_for_ready_to_check_calibration = None
    poll_for_ready_to_run_tests = None        
    poll_for_going_to_start_pos = None        
    poll_to_find_travel_from_start_pos = None 
    poll_for_stall_position_found = None      
    poll_for_threshold_detection = None       
    poll_for_back_off_completion = None       
    poll_to_relax_motors = None               
    stadib_event = None                       
    move_to_start_pos_event = None            
    poll_to_prepare_to_find_stall_pos = None  
    tell_user_ready_event = None              
    poll_to_move_to_axis_start = None         
    ensure_alarm_resumed_event = None         
    threshold_detection_event = None          
    hard_limit_found_event = None
    poll_to_start_back_off = None             
    drive_into_barrier_event = None           
    move_all_axes_event = None                
    poll_for_setting_up_axis_for_test = None  
    get_alarm_info_event = None               
    run_event = None                          
    limits_acceleration_event = None          
    post_move_all_axes_event = None           
    restore_settings_event = None             
    poll_to_finish_procedure = None           
    data_send_event = None                    
    resume_from_alarm_event = None            
    poll_to_deenergize_motors = None
    poll_to_energize_motors = None
    poll_to_reenable_hard_limits_and_go_to_next_test = None
    poll_ready_to_start_moving = None
    populate_and_transfer_logs_event = None
    send_logs_event = None

    ## DATABASE OBJECTS

    id_stage = ""
    stall_test_events = []
    stall_test_data_col_names = [

            "ID Stage: ",
            "Axis: ",
            "Test Feed: ",
            "Threshold: ",
            "Reported Feed: ",
            "Load at detection: ",
            "Stall coordinate: "
    ]

    stage_id = 9

    data_send_complete = False
    log_send_complete = False
    
    ## STORE ALL THE GRID BUTTONS

    grid_button_objects = {}

    ## COLOURS: 

    false_stall_amber = [245./255, 183./255, 23./255, 1]
    fail_orange = [245./255, 127./255, 23./255, 1]
    pass_green = [0./255, 204./255, 51./255, 1]
    bright_pass_green = [51./255, 255./255, 0./255, 1]
    highlight_yellow = [1, 1, 0, 1]
    stop_red = [1, 0, 0, 1]
    easycut_blue = [25./255, 118./255, 210./255, 1]

    VERBOSE = True # For debugging

    
    def __init__(self, **kwargs):

        super(StallJigScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['systemtools']
        self.l=kwargs['localization']
        self.m=kwargs['machine']
        self.calibration_db = kwargs['calibration_db']

        self.sn_for_db = 'ys6' + str(self.m.serial_number()).split('.')[0]
        self.combined_id = (self.sn_for_db + str(self.stage_id))[2:]

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

        self.detection_too_late = { # this may need changing depending on direction that X axis travels

            "X": self.if_more_than_expected_pos,
            "Y": self.if_more_than_expected_pos,
            "Z": self.if_less_than_expected_pos

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

        self.unschedule_event_if_it_exists(self.poll_for_homing_completion_loop)
        self.unschedule_event_if_it_exists(self.poll_for_ready_to_check_calibration)
        self.unschedule_event_if_it_exists(self.poll_for_ready_to_run_tests)
        self.unschedule_event_if_it_exists(self.poll_for_going_to_start_pos)
        self.unschedule_event_if_it_exists(self.poll_to_find_travel_from_start_pos)
        self.unschedule_event_if_it_exists(self.poll_for_stall_position_found)
        self.unschedule_event_if_it_exists(self.poll_for_threshold_detection)
        self.unschedule_event_if_it_exists(self.poll_for_back_off_completion)
        self.unschedule_event_if_it_exists(self.poll_to_relax_motors)
        self.unschedule_event_if_it_exists(self.stadib_event)
        self.unschedule_event_if_it_exists(self.move_to_start_pos_event)
        self.unschedule_event_if_it_exists(self.poll_to_prepare_to_find_stall_pos)
        self.unschedule_event_if_it_exists(self.tell_user_ready_event)
        self.unschedule_event_if_it_exists(self.poll_to_move_to_axis_start)
        self.unschedule_event_if_it_exists(self.ensure_alarm_resumed_event)
        self.unschedule_event_if_it_exists(self.threshold_detection_event)
        self.unschedule_event_if_it_exists(self.hard_limit_found_event)
        self.unschedule_event_if_it_exists(self.poll_to_start_back_off)
        self.unschedule_event_if_it_exists(self.drive_into_barrier_event)
        self.unschedule_event_if_it_exists(self.move_all_axes_event)
        self.unschedule_event_if_it_exists(self.poll_for_setting_up_axis_for_test)
        self.unschedule_event_if_it_exists(self.get_alarm_info_event)
        self.unschedule_event_if_it_exists(self.run_event)
        self.unschedule_event_if_it_exists(self.limits_acceleration_event)
        self.unschedule_event_if_it_exists(self.post_move_all_axes_event)
        self.unschedule_event_if_it_exists(self.restore_settings_event)
        self.unschedule_event_if_it_exists(self.poll_to_finish_procedure)
        self.unschedule_event_if_it_exists(self.data_send_event)
        self.unschedule_event_if_it_exists(self.resume_from_alarm_event)
        self.unschedule_event_if_it_exists(self.poll_to_deenergize_motors)
        self.unschedule_event_if_it_exists(self.poll_to_energize_motors)
        self.unschedule_event_if_it_exists(self.poll_to_reenable_hard_limits_and_go_to_next_test)
        self.unschedule_event_if_it_exists(self.poll_ready_to_start_moving)
        self.unschedule_event_if_it_exists(self.populate_and_transfer_logs_event)
        self.unschedule_event_if_it_exists(self.send_logs_event)        

        log("Unschedule all events")

    def unschedule_event_if_it_exists(self, event):
        if event != None: Clock.unschedule(event)


    # RESET FLAGS -------------------------------------------------------------------------------------------

    def reset_flags(self):

        self.setting_up_axis_for_test = False
        self.expected_limit_found = False
        self.threshold_reached = False
        self.all_tests_completed = False
        self.test_stopped = False
        self.test_passed = False
        log("Reset flags")

    ## DISABLE/ENABLE BUTTON FUNCTIONS ----------------------------------------------------------------------

    def disable_all_buttons_except_stop(self):

        self.disable_run(True)
        self.disable_most_buttons(True)

    def enable_all_buttons_except_run(self):

        self.disable_most_buttons(False)

    def enable_all_buttons(self):

        self.disable_run(False)
        self.disable_most_buttons(False)

    def disable_run(self, disable_bool):

        self.run_button.disabled = disable_bool

    def disable_most_buttons(self, disable_bool):

        self.back_button.disabled = disable_bool
        self.unlock_button.disabled = disable_bool
        self.home_button.disabled = disable_bool
        self.grbl_reset_button.disabled = disable_bool
        self.reset_test_button.disabled = disable_bool

        for key in self.grid_button_objects:
            self.grid_button_objects[key].disabled = disable_bool


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
            min_threshold_func = partial(self.increase_min_threshold, tidx, self.axes[axis])
            rows[tidx].add_widget(ToggleButton(text = str(i), size_hint_x = 1, group = self.axes[axis], on_press = min_threshold_func))

            for fidx, j in enumerate(self.feed_dict[self.axes[axis]]):

                new_button = Button(size_hint_x = 1)
                test_func = partial(self.choose_test, axis, tidx, fidx)
                new_button.bind(on_press = test_func)
                rows[tidx].add_widget(new_button)
                self.store_button(axis, tidx, fidx, new_button)

            grid_container.add_widget(rows[tidx])

    ##  FUNCTIONS FOR HANDLING/ACCESSING GRID BUTTONS

    def generate_grid_key(self, aidx, tidx, fidx):

        return (str(aidx) + str(tidx) + str(fidx))

    def store_button(self, aidx, tidx, fidx, button):

        self.grid_button_objects[self.generate_grid_key(aidx, tidx, fidx)] = button

    def get_grid_button(self, aidx, tidx, fidx):

        return self.grid_button_objects[self.generate_grid_key(aidx, tidx, fidx)]

    def colour_current_grid_button(self, colour, button_object = None):

        if not button_object: 
            aidx = self.indices["axis"]
            tidx = self.indices["threshold"]
            fidx = self.indices["feed"]
            button_object = self.get_grid_button(aidx, tidx, fidx)

        button_object.background_normal = ''
        button_object.background_color = colour
        button_object.background_disabled_normal = ''

    def grey_out_given_grid_button_if_yellow(self, button_object):

        if button_object.background_color != self.highlight_yellow:
            return 

        button_object.background_normal = 'atlas://data/images/defaulttheme/button'
        button_object.background_color = [1, 1, 1, 1]
        button_object.background_disabled_normal = 'atlas://data/images/defaulttheme/button_disabled'

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
        self.result_label.text = ""
        self.result_label.background_color = [0,0,0,1]
        log("CHOOSE TEST: " + str(axis) + ", " + str(feed) + ", " + str(threshold))
        self.test_status_label.text = str(axis) + ", " + str(feed) + ", " + str(threshold)

        for key in self.grid_button_objects:
            self.grey_out_given_grid_button_if_yellow(self.grid_button_objects[key])

        self.colour_current_grid_button(self.highlight_yellow, button_object=instance)

    ## FUNCTION TO INCREASE MINIMUM THRESHOLD

    def increase_min_threshold(self, tidx, axis, instance=None):

        if instance.state == "down":
            self.minimum_threshold_index[axis] = tidx

        else: 
            self.minimum_threshold_index[axis] = 0

        log("Minimum threshold set for " + str(axis) + ": " + \
            str(self.threshold_dict[axis][self.minimum_threshold_index[axis]]))


    # SCREEN MISC -------------------------------------------------------------------------------

    # RETURN TO FACTORY SETTINGS

    def back_to_fac_settings(self):

        self.set_default_thresholds()
        self.restore_acceleration_and_soft_limits()
        self.systemtools_sm.open_factory_settings_screen()
        log("Return to factory settings")

    # SET UP SCREEN BEFORE ENTERING

    def on_pre_enter(self):
        log("Opening stall experiment wizard")

    # STALL/LIMIT EVENT DETECTION -----------------------------------------------------------------

    ## USE THE ON PRE-LEAVE FUNCTION TO DETECT IF THE SCREEN IS GOING TO CHANGE TO AN ALARM
    ## AND THEN THIS TRIGGERS CHECKS FOR WHETHER AN EXPECTED STALL ALARM OR A LIMIT

    def on_leave(self):

        if not self.systemtools_sm.sm.current.startswith('alarm'):
            log("Leaving stall jig...")
            self.restore_acceleration_and_soft_limits()
            return

        self.systemtools_sm.sm.current = 'stall_jig'

        # UPDATE USER ON WHAT ALARM IS HAPPENING, IN CASE IT'S A GENERAL ONE
        self.test_status_label.text = self.m.s.alarm.alarm_code
        # Alarm screens should automatically handle the GRBL reset
        self.get_alarm_info_event = Clock.schedule_once(self.get_alarm_info, 1)
        log("Stall jig has registered an alarm")

    def get_alarm_info(self, dt):

        if self.m.is_grbl_waiting_for_reset():
            if self.VERBOSE: log("GRBL locked, can't get alarm info yet")
            self.get_alarm_info_event = Clock.schedule_once(self.get_alarm_info, 0.5)
            return

        log("GRBL reset, getting alarm info")
 
        if self.expected_stall_alarm_detected():
            self.threshold_detection_event = Clock.schedule_once(lambda dt: self.register_threshold_detection(), 0.5)

        if self.expected_limit_alarm():
            self.hard_limit_found_event = Clock.schedule_once(lambda dt: self.register_hard_limit_found(), 0.5)

        log("Resume from alarm")
        self.resume_from_alarm_event = Clock.schedule_once(lambda dt: self.m.resume_from_alarm(), 2)


    ## FUNCTIONS TO ANALYSE TRIGGERS AND UPDATE FOLLOWING FLAGS: 
    ## - THRESHOLD_REACHED 
    ## - EXPECTED_LIMIT_FOUND

    def ensure_alarm_resumed(self, limit_found_at_time):

        if self.m.state().startswith('Alarm'):
            if time() > limit_found_at_time + 15: 
                self.m.resume_from_alarm() # For some reason, GRBL did not unlock properly, so try again
                limit_found_at_time = time()

            if self.VERBOSE: log("Poll for resuming alarm")
            self.ensure_alarm_resumed_event = Clock.schedule_once(lambda dt: self.ensure_alarm_resumed(limit_found_at_time), 1)
            return

    def expected_stall_alarm_detected(self):

        if not (
            self.m.s.alarm.sg_alarm and
            self.current_axis() in self.m.s.alarm.stall_axis
            ):
            return False

        log("Imminent stall detected: " + self.m.s.alarm.stall_axis)
        self.m.s.alarm.sg_alarm = False
        self.m.s.alarm.stall_axis = "W"
        self.threshold_reached = True
        log("Set threshold reached flag")
        return True

    def register_threshold_detection(self):

        limit_found_at_time = time()
        self.alert_user_to_detection()
        self.ensure_alarm_resumed_event = Clock.schedule_once(lambda dt: self.ensure_alarm_resumed(limit_found_at_time), 1)

    def expected_limit_alarm(self):

        if self.m.s.alarm.alarm_code != "ALARM:1":
            if self.VERBOSE: log("Alarm that is not stall or limit! " + self.m.s.alarm.alarm_code)
            return False

        if self.VERBOSE: log("Possible limit alarm: Is " + self.current_axis() + " in " + str(self.get_limits()))
        return True

    def register_hard_limit_found(self):
        
        if not self.current_axis() in self.get_limits():
            return False

        self.expected_limit_found = True
        if self.VERBOSE: log("Expected limit found!")
        self.test_status_label.text = "LIMIT FOUND"
        limit_found_at_time = time()
        self.ensure_alarm_resumed_event = Clock.schedule_once(lambda dt: self.ensure_alarm_resumed(limit_found_at_time), 1)

    def alert_user_to_detection(self):
        self.result_label.text = "THRESHOLD REACHED"
        self.result_label.background_color = self.highlight_yellow
        self.test_status_label.text = "ANALYSING"
        log("Threshold reached (imminent stall detected)")

    ## LIMITS

    def get_limits(self):

        limit_list = []

        if self.m.s.limit_x or self.m.s.limit_X:
            limit_list.append(self.l.get_str('X'))

        if self.m.s.limit_Y_axis: 
            limit_list.append(self.l.get_str('Y'))

        if self.m.s.limit_z: 
            limit_list.append(self.l.get_str('Z'))

        return limit_list

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
            self.test_status_label.text = "ALARM"
            return

        # if sequential_stream completes successfully
        if self.m.s.is_sequential_streaming == False:
            log("Homing detected as success!")
            if self.test_status_label.text != "CHECK CALIBRATION":
                self.test_status_label.text = "READY"
            return

        if self.VERBOSE: log("Poll for homing completion")
        self.poll_for_homing_completion_loop = Clock.schedule_once(self.check_for_homing_completion, 2)


    # GENERAL ANCILLARY FUNCTIONS ------------------------------------------------------------------

    ## DETECT WHETHER THE CURRENT POSITION (i.e. AFTER DRIVING INTO BARRIER) IS LESS THAN OR MORE THAN 
    ## THE EXPECTED STALL POSITION

    def if_less_than_expected_pos(self, expected_pos):

        log("CURRENT POS: " + str(self.current_position[self.current_axis()]()))
        log("EXPECTED POS: " + str(expected_pos))
        log("DIFFERENCE: " + str(self.current_position[self.current_axis()]() - expected_pos))

        if self.current_position[self.current_axis()]() < expected_pos: return True
        else: return False

    def if_more_than_expected_pos(self, expected_pos):

        log("CURRENT POS: " + str(self.current_position[self.current_axis()]()))
        log("EXPECTED POS: " + str(expected_pos))
        log("DIFFERENCE: " + str(self.current_position[self.current_axis()]() - expected_pos))

        if self.current_position[self.current_axis()]() > expected_pos: return True
        else: return False

    ## STOP BUTTON FUNCTION

    def stop(self):
        self.test_stopped = True
        self.m.stop_measuring_running_data()
        PopupStopStallJig(self.m, self.systemtools_sm.sm, self.l, self)
        log("Tests stopped")

    ## RESET FROM ALARMS ETC.

    def grbl_reset(self):

        self.m.resume_from_alarm()
        self.test_status_label.text = "GRBL RESET"
        log("GRBL RESET")

    def smartbench_is_not_ready_for_next_command(self, ignore_alarm = False):

        if not self.m.state().startswith("Idle") and not ignore_alarm:
            return True

        if self.test_stopped:
            return True

        if self.m.s.is_sequential_streaming:
            return True

        if self.m.s.write_command_buffer: 
            return True

        if self.m.s.write_realtime_buffer: 
            return True

        if self.m.s.write_protocol_buffer: 
            return True

        if int(self.m.s.serial_blocks_available) != self.m.s.GRBL_BLOCK_SIZE:
            return True

        if int(self.m.s.serial_chars_available) != self.m.s.RX_BUFFER_SIZE:
            return True

        if self.m.s.grbl_waiting_for_reset:
            return True

        return False

    ## RESET CURRENT SUB-TEST (DOESN'T RESTART THOUGH - WAITS FOR USER INPUT)

    def reset_current_sub_test(self):
        self.test_status_label.text = "TEST RESET"
        self.choose_test(self.indices["axis"], self.indices["threshold"], self.indices["feed"])
        log("Current test reset")

    ## UNLOCK DATA SEND (IN CASE USER WANTS/NEEDS TO SEND INCOMPLETE DATA SET)

    def enable_data_send(self):

        if self.unlock_button.state == "down":
            self.unlock_button.text = "lock"
            self.send_data_button.disabled = False
            log("Data send enabled")

        else:
            self.unlock_button.text = "unlock"
            self.send_data_button.disabled = True
            log("Data send disabled")

    ## DO DATA SEND

    def start_stall_jig_data_send(self):
        
        self.send_data_button.disabled = True
        self.test_status_label.text = "SENDING RESULTS"
        log("Sending data...")
        self.data_send_complete = False
        self.log_send_complete = False
        self.m.stop_measuring_running_data()
        Clock.schedule_once(self.do_stall_jig_data_send, 0.5)
        self.populate_and_transfer_logs_event = Clock.schedule_once(lambda dt: self.populate_and_transfer_logs(), 1)


    def do_stall_jig_data_send(self, dt):
        
        # STARTS A SEPARATE THREAD TO PROCESS STATUSES INTO DB READY FORMAT
        self.calibration_db.process_status_running_data_for_database_insert(self.m.measured_running_data(), self.sn_for_db)
        
        # SENDS STALL EXPERIMENT EVENTS
        results_send_successful = self.calibration_db.insert_stall_experiment_results(self.stall_test_events)

        # SEND STATUSES ONCE THEY HAVE BEEN PROCESSED
        self.send_stall_jig_statuses_when_ready(results_send_successful)


    def send_stall_jig_statuses_when_ready(self, results_send_successful):

        if self.calibration_db.processing_running_data:
            log("Poll for sending stall jig statuses when ready")
            Clock.schedule_once(lambda dt: self.send_stall_jig_statuses_when_ready(results_send_successful), 1)
            return

        self.test_status_label.text = "SENDING STATUSES"
        log("Sending statuses")

        try:
            self.calibration_db.insert_final_test_stage(self.sn_for_db, 9)
            self.calibration_db.insert_final_test_stage(self.sn_for_db, 10)

        except:
            log("Could not insert final test stage into DB!!")
            print(traceback.format_exc())


        data_send_successful = self.calibration_db.send_data_through_publisher(self.sn_for_db, 9)
        cal_data_send_successful = self.calibration_db.send_data_through_publisher(self.sn_for_db, 10)

        self.send_data_button.disabled = False

        if data_send_successful and cal_data_send_successful and results_send_successful:
            self.test_status_label.text = "DATA SENT!"

        elif data_send_successful or cal_data_send_successful or results_send_successful:
            self.test_status_label.text = "PARTIAL DATA SEND!"

        else: 
            self.test_status_label.text = "DATA NOT SENT!"
        
        self.enable_all_buttons()


    def populate_and_transfer_logs(self):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll to get registers for logs")
            self.populate_and_transfer_logs_event = Clock.schedule_once(lambda dt: self.populate_and_transfer_logs(), 1)
            return

        log("Get registers into logs")
        self.m.tmc_handshake()
        self.send_logs()


    def send_logs(self):

        if self.smartbench_is_not_ready_for_next_command() and not self.m.TMC_registers_have_been_read_in():
            if self.VERBOSE: log("Poll to send logs once registers are in")
            self.send_logs_event = Clock.schedule_once(lambda dt: self.send_logs(), 1)
            return

        log("Registers are in, ready to send logs")



    # THE MAIN EVENT ----------------------------------------------------------------------------------------------------
    # HANDLES THE MANAGEMENT OF ALL STAGES OF THE TEST

    def run(self):

        self.disable_all_buttons_except_stop()
        if self.smartbench_is_not_ready_for_next_command():

            if self.run_button.disabled:
                self.test_status_label.text = "CAN'T START"
                return

            if self.VERBOSE: log("Poll to start next run")
            self.run_event = Clock.schedule_once(lambda dt: self.run(), 2)
            return

        self.test_passed = False
        self.threshold_reached = False
        self.false_stall_happened = False
        self.expected_limit_found = False
        self.result_label.text = ""
        self.result_label.background_color = [0,0,0,1]

        log("Run next test")
        self.test_status_label.text = "RUNNING"
        
        # If no tests have been started yet, SB will need to do a prep sequence instead
        if self.start_of_all_tests():
            return

        if self.end_of_all_tests():
            return

        if not self.travel_to_stall_pos[self.current_axis()]:
            self.set_grbl_settings_for_experiment(False)
            return

        self.colour_current_grid_button(self.highlight_yellow)
        threshold_idx = self.indices["threshold"]
        feed_idx = self.indices["feed"]
        self.m.continue_measuring_running_data()
        self.set_threshold_and_drive_into_barrier(self.current_axis(), threshold_idx, feed_idx)


    # CORE TEST FUNCTIONS -------------------------------------------------------------------------------------------

    ## RETURN CURRENT AXIS AS "X" "Y" OR "Z"

    def current_axis(self): return self.axes[self.indices["axis"]]

    ## PUT ACCELERATION BACK TO NORMAL

    def restore_acceleration_and_soft_limits(self):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll to restore grbl settings")
            self.restore_settings_event = Clock.schedule_once(lambda dt: self.restore_acceleration_and_soft_limits(), 0.5)
            return

        log("Enable soft limits and restore acceleration")

        default_acceleration_values = [

                '$20=1',        # Soft limits
                '$21=1',        # Enable hard limits
                '$53=0',        # Disable stall guard
                '$120=130.0',   # X Acceleration, mm/sec^2
                '$121=130.0'    #Y Acceleration, mm/sec^2

                ]

        self.m.s.start_sequential_stream(default_acceleration_values, reset_grbl_after_stream = True)
        log("Enabling soft limits")
        log("Disabling stall guard")
        log("Restoring acceleration values for X and Y (to 130)")

    def disable_soft_limits_and_max_acceleration_values(self):

        settings_list_to_stream = [

                '$20=0',        # Disable soft limits
                '$21=1',        # Enable hard limits
                '$53=1',        # Enable stall guard
                '$120=1300.0',  # X Acceleration, mm/sec^2
                '$121=1300.0'   # Y Acceleration, mm/sec^2
                ]

        self.m.s.start_sequential_stream(settings_list_to_stream, reset_grbl_after_stream = True)
        log("Disabling soft limits")
        log("Enabling stall guard")
        log("Maxing out acceleration values for X and Y (to 1300)")
        log("Move to start position")

    ## FUNCTION TO NEATLY MOVE TO ABSOLUTE POSITION STORED IN WHATEVER POS DICTIONARY (AT MAX FEED)

    def move_all_axes(self, pos_dict, next_func, disable_hard_limits = False):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll to move all axes")
            self.move_all_axes_event = Clock.schedule_once(lambda dt: self.move_all_axes(pos_dict, next_func, disable_hard_limits), 0.5)
            return  

        # Move Z up, 
        # Move to XY position
        # Move Z back down

        log("Moving all axes...")

        move_sequence = []

        if disable_hard_limits: 
            if self.VERBOSE: log("DISABLE HARD LIMITS")
            move_sequence.append("$21=0")
        move_sequence.append("G0 G53 Z-" + str(self.m.s.setting_27))
        move_sequence.append("G53 " + "X" + str(pos_dict["X"]) + " Y" + str(pos_dict["Y"]) + " F" + str(self.fast_travel["Y"]))
        move_sequence.append("G53 " + "Z" + str(pos_dict["Z"]) + " F" + str(self.fast_travel["Z"]))
        self.m.s.start_sequential_stream(move_sequence)

        # IMPORTANT THAT THE FUNCTION PASSED ACCEPTS CLOCK TIME AS AN ARGUMENT
        self.post_move_all_axes_event = Clock.schedule_once(next_func, 1)


    ## FUNCTION TO SET THE THRESHOLD AND CRASH INTO AN OBSTACLE

    def set_threshold_and_drive_into_barrier(self, axis, threshold_idx, feed_idx):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll for setting threshold before driving into barrier")
            self.stadib_event = Clock.schedule_once(lambda dt: self.set_threshold_and_drive_into_barrier(axis, threshold_idx, feed_idx), 0.5)
            return

        threshold = self.threshold_dict[axis][threshold_idx]
        feed = self.feed_dict[axis][feed_idx]
        start_pos = self.current_position[axis]()

        log("Setting threshold to " + str(threshold) + " for " + axis + ", and drive into barrier at feed: " + str(feed))
        self.test_status_label.text = "THR: " + str(threshold)
        self.m.set_threshold_for_axis(axis, threshold)
        self.drive_into_barrier_event = Clock.schedule_once(lambda dt: self.drive_into_barrier(axis, feed, start_pos), 1)

    def drive_into_barrier(self, axis, feed, start_pos):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll for driving into barrier")
            self.drive_into_barrier_event = Clock.schedule_once(lambda dt: self.drive_into_barrier(axis, feed, start_pos), 0.5)
            return

        try: expected_pos = start_pos + self.travel_to_stall_pos[axis] + self.stall_tolerance[axis]
        except: pass

        log("Drive into barrier")
        self.test_status_label.text = "CRASH TIME!"
        move_sequence = ["G01 G91 " + axis + str(self.crash_distance[axis]) + " F" + str(feed)]
        self.m.s.start_sequential_stream(move_sequence)

        if self.setting_up_axis_for_test:
            log("Setting up axis, so look for stall position")
            self.poll_for_stall_position_found = Clock.schedule_once(lambda dt: self.stall_position_found(axis, start_pos), 0.5)

        else:
            log("Start poll for SB travelling or exceeding threshold")
            self.poll_for_threshold_detection = Clock.schedule_once(lambda dt: self.sb_has_travelled_or_detected(expected_pos), 0.5)


    ## REPOSITIONING PROCEDURE

        ## THESE FUNCTIONS ARE CALLED AS PART OF MULTIPLE PROCEDURES (E.G. AXIS SET UP, INDIVIDUAL EXPERIMENTS)
        ## ORDER OF EVENTS IS:
        ## - BACK OFF FROM THE CRASH SITE INTO A HARD LIMIT
        ## - USE THIS LIMIT TO PLACE SB FOR THE NEXT PROCEDURE
        ## - DE-ENERGIZE AND RE-ENERGIZE THE MOTORS (AS A MINI RE-SQUARE)
        ## - CARRY OUT ANY PROCEDURE/OUTCOME SPECIFIC FUNCTIONS (E.G. UNSETTING SETTING_UP FLAG OR STORING RESULT)
        ## - AND THEN CALL RUN FUNCTION AGAIN

    def back_off_and_find_position(self):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll to start backing off")
            self.poll_to_start_back_off = Clock.schedule_once(lambda dt: self.back_off_and_find_position(), 0.5)
            return

        log("Back off and find position")
        self.test_status_label.text = "REFIND POS"
        self.expected_limit_found = False
        move_command = ["G01 G91 " + self.current_axis() + str(self.back_off[self.current_axis()]) + " F" + str(self.fast_travel[self.current_axis()])]
        self.m.s.start_sequential_stream(move_command)
        self.poll_for_back_off_completion = Clock.schedule_once(lambda dt: self.back_off_completed(), 1)


    def back_off_completed(self):

        if self.smartbench_is_not_ready_for_next_command():

            if self.VERBOSE: log("Poll for back off completion")
            self.poll_for_back_off_completion = Clock.schedule_once(lambda dt: self.back_off_completed(), 0.5)
            return

        if self.threshold_reached:

            self.false_stall_happened = True
            self.threshold_reached = False
            if self.VERBOSE: log("FALSE STALL DETECTED!! Temporarily increasing threshold")
            self.result_label.text = "FALSE STALL"
            self.result_label.background_color = self.false_stall_amber
            self.test_status_label.text = "REFIND POS"
            self.m.set_threshold_for_axis(self.current_axis(), 300) # set the threshold high so that it completes the move
            self.poll_to_start_back_off = Clock.schedule_once(lambda dt: self.back_off_and_find_position(), 1)
            return

        if not self.expected_limit_found:

            if self.VERBOSE: log("Expected limit not found, no threshold exceeded. Confused :(")
            self.test_status_label.text = "POS LOST :("
            return

        log("Position found")
        self.test_status_label.text = "POS FOUND"

        log("Turn off hard limits, and pull off from limit")
        move_command = "G01 G91 " + self.current_axis() + str(self.limit_pull_off[self.current_axis()]) + " F" + str(self.fast_travel[self.current_axis()])
        grbl_sequence = ['$21=0', move_command]
        self.m.s.start_sequential_stream(grbl_sequence)
        self.expected_limit_found = False
        self.poll_to_relax_motors = Clock.schedule_once(lambda dt: self.relax_motors(), 1)

    def relax_motors(self):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll for relax motors")
            self.poll_to_relax_motors = Clock.schedule_once(lambda dt: self.relax_motors(), 0.5)
            return

        self.poll_to_deenergize_motors = Clock.schedule_once(lambda dt: self.deenergize_motors(), 1)

    def deenergize_motors(self):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll for deenergize motors")
            self.poll_to_deenergize_motors = Clock.schedule_once(lambda dt: self.deenergize_motors(), 0.5)
            return

        log("De-energize motors")
        self.test_status_label.text = "MOTORS OFF"
        self.disable_motors[self.current_axis()]()
        self.poll_to_energize_motors = Clock.schedule_once(lambda dt: self.energize_motors(), 1)


    def energize_motors(self):

        if self.smartbench_is_not_ready_for_next_command() and not self.test_stopped:
            if self.VERBOSE: log("Poll for energize motors")
            self.poll_to_energize_motors = Clock.schedule_once(lambda dt: self.energize_motors(), 0.5)
            return

        log("Energize motors")
        self.test_status_label.text = "MOTORS ON"
        self.enable_motors[self.current_axis()]()
        self.poll_to_reenable_hard_limits_and_go_to_next_test = Clock.schedule_once(lambda dt: self.reenable_hard_limits_and_go_to_next_test(), 1)

    def reenable_hard_limits_and_go_to_next_test(self):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll for reenable hard limits and start next test")
            self.poll_to_reenable_hard_limits_and_go_to_next_test = Clock.schedule_once(lambda dt: self.reenable_hard_limits_and_go_to_next_test(), 0.5)
            return

        self.m.enable_only_hard_limits()
        self.reset_entire_pcb()

    # INSERT AXIS DISABLE HERE

    def reset_entire_pcb(self):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll to hard reset PCB before starting next test")
            self.poll_to_reset_entire_pcb = Clock.schedule_once(lambda dt: self.reset_entire_pcb(), 0.5)
            return

        self.m.hard_reset_pcb_sequence()
        self.finish_procedure_and_start_next_test()

    def finish_procedure_and_start_next_test(self):

        if self.smartbench_is_not_ready_for_next_command() or not self.m.TMC_registers_have_been_read_in():
            if self.VERBOSE: log("Poll to finish procedure and start next test")
            self.poll_to_finish_procedure = Clock.schedule_once(lambda dt: self.finish_procedure_and_start_next_test(), 0.5)
            return

        log("Procedure finished...")

        self.test_status_label.text = "RECORDING RESULT"

        if self.setting_up_axis_for_test: 
            self.test_status_label.text = "AXIS READY"
            log("Axis set up")
            self.setting_up_axis_for_test = False

        elif self.false_stall_happened and self.test_passed:
            self.false_stall_happened = False
            log("False stall happened - test failed")
            self.colour_current_grid_button(self.false_stall_amber)
            self.go_to_next_threshold()

        elif self.test_passed:
            log("Recording stall detection event - test passed")
            self.colour_current_grid_button(self.pass_green)
            self.record_stall_event()
            self.go_to_next_threshold()

        else:
            log("Stall was not detected - test failed")
            self.colour_current_grid_button(self.fail_orange)
            self.go_to_next_feed_set()

        log("Moved to next test indices - starting new run")
        self.run()


    # START TEST SEQUENCE (PREP TEST): ----------------------------------------------------------------------------------

        ## HAPPENS BEFORE MAGNETS HAVE BEEN INSTALLED

        ## HOMES NORMALLY
        ## RUNS CALIBRATION CHECK (SO WE KNOW IN ADVANCE IF SOMETHING 
        ## IS GOING TO FAIL DUE TO DODGY CALIBRATION)
        ## DISABLE SOFT LIMITS
        ## MOVES
        ## TELL USER TO INSTALL JIGS
        ## USER WILL MANUALLY PRESS RUN

    def start_of_all_tests(self):

        if self.run_button.text == "RUN":
            return False

        log("Set up for all tests")
        self.test_status_label.text = "SETTING UP"
        self.choose_test(0,0,0)

        # GET REGISTERS
        self.m.tmc_handshake()
        self.poll_ready_to_start_moving = Clock.schedule_once(lambda dt: self.start_moving(), 1)
        return True
    
    def start_moving(self):

        if self.smartbench_is_not_ready_for_next_command() or not self.m.TMC_registers_have_been_read_in():
            if self.VERBOSE: log("Poll for registers having been read in, and ready to move")
            self.poll_ready_to_start_moving = Clock.schedule_once(lambda dt: self.start_moving(), 1)
            return

        self.start_homing()

        # CALIBRATION CHECK
        self.poll_for_ready_to_check_calibration = Clock.schedule_once(lambda dt: self.full_calibration_check(), 1)

    def full_calibration_check(self):
        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll for ready to check calibration")
            self.poll_for_ready_to_check_calibration = Clock.schedule_once(lambda dt: self.full_calibration_check(), 0.5)
            return

        self.test_status_label.text = "CHECK CALIBRATION"
        self.m.start_measuring_running_data(10)
        log("Run a calibration check in all axes")
        if not self.dev_mode: 
            self.m.cal_check_threshold_x_min = -2001
            self.m.cal_check_threshold_x_max = 2001
            self.m.cal_check_threshold_y_min = -2001
            self.m.cal_check_threshold_y_max = 2001
            self.m.cal_check_threshold_z_min = -2001
            self.m.cal_check_threshold_z_max = 2001
            self.m.check_x_y_z_calibration(do_reset=True)
        self.poll_for_ready_to_run_tests = Clock.schedule_once(self.ready_to_run_tests, 1)

    def ready_to_run_tests(self, dt):

        if self.m.checking_calibration_in_progress or self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll for ready to run tests")
            self.poll_for_ready_to_run_tests = Clock.schedule_once(self.ready_to_run_tests, 1)
            return

        if self.m.checking_calibration_fail_info:
            self.test_status_label.text = "CAL CHECK FAIL"
            return

        self.m.change_stage_measuring_running_data(9)
        log("Ready to run tests, disabling limits & maxing acceleration")
        self.set_grbl_settings_for_experiment(True)

    ## MAX OUT ACCELERATION

    def set_grbl_settings_for_experiment(self, start_pos_bool):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll to disable soft limits and max out acceleration")
            self.limits_acceleration_event = Clock.schedule_once(lambda dt: self.set_grbl_settings_for_experiment(start_pos_bool), 0.5)
            return

        self.disable_soft_limits_and_max_acceleration_values()

        # go to absolute start position (relative to true home)
        if start_pos_bool:
            self.move_to_start_pos_event = Clock.schedule_once(lambda dt: self.move_all_axes(self.absolute_start_pos, self.tell_user_that_SB_is_ready_to_run_tests), 0.5)
            return

        self.poll_for_setting_up_axis_for_test = Clock.schedule_once(lambda dt: self.set_up_axis_for_test(), 0.5)


    def tell_user_that_SB_is_ready_to_run_tests(self, dt):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll to tell user that SB is ready")
            self.tell_user_ready_event = Clock.schedule_once(self.tell_user_that_SB_is_ready_to_run_tests, 0.5)
            return

        log("Tell user to put the magnets on to set up fake home")
        self.test_status_label.text = "INSTALL JIGS"
        self.run_button.text = "RUN"
        self.enable_all_buttons_except_run()
        self.disable_run(False)

    # NECESSARY SET UP THAT'S DONE EACH TIME A NEW AXIS IS TESTED ----------------------------------------------------------

    def set_up_axis_for_test(self):

        self.setting_up_axis_for_test = True
        self.test_status_label.text = "SET UP AXIS"

        if self.smartbench_is_not_ready_for_next_command(ignore_alarm = True):
            if self.VERBOSE: log("Poll for setting up axis for test")
            self.poll_for_setting_up_axis_for_test = Clock.schedule_once(lambda dt: self.set_up_axis_for_test(), 0.5)
            return

        log("Set up axis for test")
        log("Home against the magnets that give fake home position")
        self.start_homing()

        # go to start pos for the axis (relative to the magnets)
        self.poll_for_going_to_start_pos = Clock.schedule_once(self.go_to_start_pos, 1)


    def go_to_start_pos(self, dt): # may want to set this to 0,0,0 and turn off limits

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll for going to start position")
            self.poll_for_going_to_start_pos = Clock.schedule_once(self.go_to_start_pos, 0.5)
            return

        log("Go to start pos for the axis (relative to the magnets)")
        self.test_status_label.text = "GO TO START POS"

        # disable hard limits and go to test start position, relative to faux home
        self.move_all_axes(self.start_positions[self.current_axis()], self.find_travel_from_start_pos, disable_hard_limits = True)

    ## LOWER THE THRESHOLD AND MAX OUT THE FEED TO RECORD THE POSITION WHERE WE EXPECT SB TO STALL

    def find_travel_from_start_pos(self, dt):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll for setting travel")
            self.poll_to_find_travel_from_start_pos = Clock.schedule_once(self.find_travel_from_start_pos, 0.5)
            return

        log("Set expected travel to stall position")
        self.test_status_label.text = "SET TRAVEL"

        log("Pull off from limit")
        move_command = ["G91 " + self.current_axis() + str(self.limit_pull_off[self.current_axis()]) + " F" + str(self.fast_travel[self.current_axis()])]
        self.m.s.start_sequential_stream(move_command)
        self.poll_to_prepare_to_find_stall_pos = Clock.schedule_once(lambda dt: self.prepare_to_find_stall_pos(self.current_axis()), 0.5)

    def prepare_to_find_stall_pos(self, axis):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll to prepare to find stall pos")
            self.poll_to_prepare_to_find_stall_pos = Clock.schedule_once(lambda dt: self.prepare_to_find_stall_pos(self.current_axis()), 0.5)
            return

        self.m.enable_only_hard_limits()
        self.set_threshold_and_drive_into_barrier(self.current_axis(), 0, 0)

    def stall_position_found(self, axis, start_pos):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll for finding stall position")
            self.poll_for_stall_position_found = Clock.schedule_once(lambda dt: self.stall_position_found(axis, start_pos), 0.5)
            return

        if self.threshold_reached: 
            self.threshold_reached = False
            self.test_status_label.text = "STALL POS FOUND"
            log("Stall position found")
            self.travel_to_stall_pos[axis] = self.current_position[axis]() - start_pos
            self.back_off_and_find_position()
            return

        maximum_pos = float(start_pos) + float(self.crash_distance[axis]) - 0.05 # 0.05mm tolerance for positional error
        if self.detection_too_late[self.current_axis()](maximum_pos):
            self.test_status_label.text = "NO STALL POS?"
            self.m.stop_from_soft_stop_cancel()
            self.unschedule_all_events()
            self.restore_acceleration_and_soft_limits()
            self.enable_all_buttons_except_run()
            return

        self.poll_for_stall_position_found = Clock.schedule_once(lambda dt: self.stall_position_found(axis, start_pos), 0.5)
        self.test_status_label.text = "NO DETECT YET"


    # PARSE RESULTS OF EXPERIMENT ------------------------------------------------------------------------------------------

    ## POLLED EVENT, WHEN SB IS NO LONGER MOVING AND ALARMS HAVE BEEN RESET, IT WILL START THE REPOSITIONING PROCEDURE
    def sb_has_travelled_or_detected(self, expected_pos):

        if self.smartbench_is_not_ready_for_next_command():
            if self.VERBOSE: log("Poll for threshold detection")
            self.poll_for_threshold_detection = Clock.schedule_once(lambda dt: self.sb_has_travelled_or_detected(expected_pos), 0.5)
            return

        log("SB has either completed its move command, or it has detected that a limit has been reached!")
        self.test_passed = self.determine_test_result(expected_pos)
        if self.test_passed is not None: self.back_off_and_find_position()

    ## WORK OUT AND DELIVER TEST RESULTS

    def determine_test_result(self, expected_pos):

        if self.detection_too_late[self.current_axis()](expected_pos):
            return self.test_did_fail()

        if self.threshold_reached: 
            return self.test_did_pass()
        
        # If threshold not reached, but hasn't travelled too far, maybe just haven't registered alarm result yet: 
        self.poll_for_threshold_detection = Clock.schedule_once(lambda dt: self.sb_has_travelled_or_detected(expected_pos), 0.5)
        self.test_status_label.text = "NO DETECT YET"

    def test_did_pass(self):

        log("TEST PASSED")
        self.threshold_reached = False
        self.result_label.text = "THRESHOLD REACHED"
        self.result_label.background_color = self.bright_pass_green
        self.test_status_label.text = "PASS"
        return True

    def test_did_fail(self):

        log("TEST FAILED")
        self.threshold_reached = False
        self.result_label.text = "THRESHOLD NOT REACHED"
        self.result_label.background_color = self.fail_orange
        self.test_status_label.text = "TEST FAILED"
        return False


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

        step_us = float(self.m.s.last_stall_motor_step_size)
        rpm = 60.0*(1000000.0/step_us)/3200.0
        reported_feed = 3200.0 / float(step_rate) * float(rpm)

        # Example data: 
        # ["ID, 0, 6000, 150, 5999, 170, -1100.4 ]

        last_test_pass = [

            self.combined_id,
            self.indices["axis"], # X = 0, Y = 1, Z = 2
            self.feed_dict[self.current_axis()][self.indices["feed"]],
            self.threshold_dict[self.current_axis()][self.indices["threshold"]],
            reported_feed,
            self.m.s.last_stall_load,
            stall_coord
        ]

        self.stall_test_events.append(last_test_pass)

        log("Stall event: ")
        for i in range(len(last_test_pass)):
            log(str(self.stall_test_data_col_names[i]) + str(last_test_pass[i]))


    ## IF TEST PASSES, GO TO NEXT THRESHOLD (UNLESS DONE ALL THRESHOLDS IN FEED SET)

    def go_to_next_threshold(self):

        if self.indices["threshold"] + 1 < len(self.threshold_dict[self.current_axis()]):
            self.indices["threshold"] = self.indices["threshold"] + 1
            log("Next threshold index: " + str(self.indices["threshold"]))

        else: 
            self.go_to_next_feed_set()

    # IF TEST FAILS, OR ALL THRESHOLDS TESTED FOR ONE FEED, GO TO NEXT FEED SET

    def go_to_next_feed_set(self):

        if self.indices["feed"] + 1 < len(self.feed_dict[self.current_axis()]):
            self.indices["feed"] = self.indices["feed"] + 1
            self.indices["threshold"] = self.minimum_threshold_index[self.current_axis()]

            log("Next feed index: " + str(self.indices["feed"]))
            log("Next threshold index: " + str(self.indices["threshold"]))

        else:
            self.go_to_next_axis()

    # IF AXIS COMPLETED, GO TO NEXT ONE
    ## IF ALL FEED SETS AND AXES ARE COMPLETED, 

    def go_to_next_axis(self):

        if self.indices["axis"] + 1 < len(self.axes):
            self.indices["axis"] = self.indices["axis"] + 1
            self.indices["feed"] = 0
            self.indices["threshold"] = 0
            self.travel_to_stall_pos[self.current_axis()] = None

            log("Next feed index: " + str(self.indices["feed"]))
            log("Next threshold index: " + str(self.indices["threshold"]))
            log("Next axis index: " + str(self.indices["axis"]))

        else: 
            self.all_tests_completed = True

    # END OF ALL TESTS ------------------------------------------------------------------------------------

    ## WHEN ALL EXPERIMENTS ARE COMPLETE, DATA CAN BE SENT, AND SETTINGS REVERTED

    def end_of_all_tests(self):

        if self.all_tests_completed:

            log("All tests completed!!")
            self.m.stop_measuring_running_data()
            self.set_default_thresholds()
            self.restore_acceleration_and_soft_limits()
            self.test_status_label.text = "TESTS COMPLETE"
            log("Send data")
            self.data_send_event = Clock.schedule_once(lambda dt: self.start_stall_jig_data_send(), 1)
            return True

    def set_default_thresholds(self):
        self.m.set_threshold_for_axis("X", 250)
        self.m.set_threshold_for_axis("Y", 250)
        self.m.set_threshold_for_axis("Z", 175)











