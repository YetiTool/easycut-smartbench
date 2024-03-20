# -*- coding: utf-8 -*-
"""
Created July 2020

@author: Letty

Spindle cooldown screen
"""
from math import sqrt, ceil

from asmcnc.comms.logging_system.logging_system import Logger
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string(
    """

<SpindleHealthCheckActiveScreen>:

    countdown: countdown
    cool_down_label : cool_down_label

    BoxLayout: 
        spacing: 0
        padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
        orientation: 'vertical'
        size_hint: (None, None)
        height: 1.0*app.height
        width: 1.0*app.width
        canvas:
            Color: 
                rgba: hex('#E5E5E5FF')
            Rectangle: 
                size: self.size
                pos: self.pos         

        BoxLayout: 
            spacing: 0
            padding: 
            orientation: 'vertical'
            canvas:
                Color: 
                    rgba: [1,1,1,1]
                RoundedRectangle:
                    size: self.size
                    pos: self.pos    
            
            Label:
                id: cool_down_label
                size_hint_y: 1
                color: [0,0,0,1]
                markup: True
                font_size: str(0.0375*app.width) + 'px' 
                valign: 'middle'
                halign: 'center'
                size:self.texture_size
                text_size: self.size

            BoxLayout: 
                spacing: 0
                padding:[dp(0.125)*app.width, 0, dp(0.125)*app.width, dp(0.270833333333)*app.height]
                orientation: 'horizontal'          
                size_hint: (None, None)
                height: dp(251.0/480.0)*app.height
                width: 1.0*app.width
                pos: self.parent.pos


                BoxLayout: 
                    spacing: 0
                    padding:[dp(0.01)*app.width, 0, dp(0.07125)*app.width, 0]
                    orientation: 'horizontal'          
                    size_hint: (None, None)
                    height: dp(121.0/480.0)*app.height
                    width: 0.225*app.width
                    Image:
                        id: spindle_icon
                        source: "./asmcnc/core_UI/job_go/img/spindle_check.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
                        size_hint: (None, None)
                        height: dp(0.252083333333*app.height)
                        width: dp(0.14375*app.width) 

                BoxLayout: 
                    spacing: 0
                    padding:[0, 0, 0, 0]
                    orientation: 'horizontal'          
                    size_hint: (None, None)
                    height: dp(121.0/480.0)*app.height
                    width: 0.25*app.width
                    Label:
                        id: countdown
                        markup: True
                        font_size: str(0.125*app.width) + 'px' 
                        valign: 'middle'
                        halign: 'center'
                        size:self.texture_size
                        text_size: self.size  
                        text: '10'
                        color: [0,0,0,1]

                BoxLayout: 
                    spacing: 0
                    padding:[dp(0.0875)*app.width, 0, dp(0.0125)*app.width, dp(0.00625)*app.height]
                    orientation: 'horizontal'          
                    size_hint: (None, None)
                    height: dp(121.0/480.0)*app.height
                    width: 0.225*app.width
                    Image:
                        id: countdown_icon
                        source: "./asmcnc/skavaUI/img/countdown_big.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
                        size_hint: (None, None)
                        height: dp(0.245833333333*app.height)
                        width: dp(0.125*app.width) 


"""
)


class SpindleHealthCheckActiveScreen(Screen):
    return_screen = "go"
    max_seconds = 6
    seconds = 6
    update_timer_event = None
    health_check_rpm = 24000

    def __init__(self, **kwargs):
        super(SpindleHealthCheckActiveScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.seconds = self.max_seconds
        self.cool_down_label.text = (
            self.l.get_str("Running Spindle motor health check…")
            + "\n"
            + self.l.get_str("SmartBench is raising the Z axis.")
        )

    def on_pre_enter(self):
        # health check if not called from elsewhere
        self.seconds = self.max_seconds
        self.countdown.text = str(self.seconds)

    def on_enter(self):
        self.run_spindle_health_check()
        self.cool_down_label.text = (
            self.l.get_str("Running Spindle motor health check…")
            + "\n"
            + self.l.get_str("SmartBench is raising the Z axis.")
        )

    def start_timer(self):
        self.update_timer_event = Clock.schedule_interval(self.update_timer, 1)
        self.cool_down_label.text = self.l.get_str(
            "Running Spindle motor health check…"
        )

    def exit_screen(self, dt=0):
        self.sm.current = self.return_screen

    def update_timer(self, dt):
        if self.seconds > 0:
            self.seconds = self.seconds - 1
            self.countdown.text = str(self.seconds)

    def on_leave(self):
        if self.update_timer_event != None:
            Clock.unschedule(self.update_timer_event)
        self.seconds = self.max_seconds
        self.countdown.text = str(self.seconds)

    passed_spindle_health_check = False
    spindle_health_check_max_w = 550
    start_after_pass = False
    return_to_advanced_tab = False

    def run_spindle_health_check(self):
        self.m.s.spindle_health_check_data[:] = []

        def round_up_to_ten(n):
            return int(ceil(n / 10.0)) * 10

        def pass_test(free_load):
            Logger.info("Spindle health check passed - free load: " + str(free_load))
            self.m.spindle_health_check_failed = False
            self.m.spindle_health_check_passed = True
            self.m.s.yp.set_free_load(free_load)
            if self.return_to_advanced_tab and self.sm.has_screen("go"):
                self.sm.get_screen("go").yp_widget.open_yp_settings()
            self.exit_screen()
            if (
                self.sm.has_screen("go")
                and self.start_after_pass
                and not self.return_to_advanced_tab
            ):
                self.sm.get_screen("go")._start_running_job()
                self.sm.current = "go"

        def show_fail_screen(reason):
            self.m.stop_for_a_stream_pause(reason)
            if self.sm.has_screen("go"):
                self.sm.get_screen("go").raise_pause_screens_if_paused(override=True)

        def fail_test(reason):
            Logger.info("Spindle health check failed - " + reason)
            self.m.spindle_health_check_failed = True
            self.m.spindle_health_check_passed = False
            show_fail_screen(reason)

        def check_average():
            average_load = sum(self.m.s.spindle_health_check_data) / (
                len(self.m.s.spindle_health_check_data) or 1
            )
            average_load_w = (
                self.m.spindle_voltage * 0.1 * sqrt(average_load)
                if average_load != 0
                else 0
            )
            if average_load_w > self.spindle_health_check_max_w:
                fail_test("spindle_health_check_failed")
                return
            elif average_load_w == 0:
                fail_test("yetipilot_spindle_data_loss")
                return
            pass_test(round_up_to_ten(average_load_w))

        def stop_test():
            self.m.turn_off_spindle()
            self.m.s.spindle_health_check = False

        def start_test():
            if self.m.smartbench_is_busy():
                Clock.schedule_once(lambda dt: start_test(), 0.5)
                return
            self.start_timer()
            self.m.s.spindle_health_check = True
            self.m.turn_on_spindle(self.health_check_rpm)
            Clock.schedule_once(lambda dt: stop_test(), 6)
            Clock.schedule_once(lambda dt: check_average(), 6)

        self.m._grbl_soft_reset()
        self.m.resume_from_a_soft_door()
        Clock.schedule_once(lambda dt: self.m.raise_z_axis_for_collet_access(), 1)
        Clock.schedule_once(lambda dt: start_test(), 1)
