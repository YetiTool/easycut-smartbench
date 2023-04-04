# -*- coding: utf-8 -*-
'''
Created July 2020

@author: Letty

Spindle cooldown screen
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from kivy.clock import Clock
from datetime import datetime

from math import sqrt

Builder.load_string("""

<SpindleHealthCheckActiveScreen>:

    countdown: countdown
    cool_down_label : cool_down_label

    BoxLayout: 
        spacing: 0
        padding: 20
        orientation: 'vertical'
        size_hint: (None, None)
        height: 480
        width: 800
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
                font_size: '30px' 
                valign: 'middle'
                halign: 'center'
                size:self.texture_size
                text_size: self.size

            BoxLayout: 
                spacing: 0
                padding: [100, 0, 100, 130]
                orientation: 'horizontal'          
                size_hint: (None, None)
                height: 251
                width: 800
                pos: self.parent.pos


                BoxLayout: 
                    spacing: 0
                    padding: [8, 0, 57, 0]
                    orientation: 'horizontal'          
                    size_hint: (None, None)
                    height: 121
                    width: 180
                    Image:
                        id: spindle_icon
                        source: "./asmcnc/core_UI/job_go/img/spindle_check.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
                        size_hint: (None, None)
                        height: dp(121)
                        width: dp(115) 

                BoxLayout: 
                    spacing: 0
                    padding: [0, 0, 0, 0]
                    orientation: 'horizontal'          
                    size_hint: (None, None)
                    height: 121
                    width: 200
                    Label:
                        id: countdown
                        markup: True
                        font_size: '100px' 
                        valign: 'middle'
                        halign: 'center'
                        size:self.texture_size
                        text_size: self.size  
                        text: '10'
                        color: [0,0,0,1]

                BoxLayout: 
                    spacing: 0
                    padding: [70, 0, 10, 3]
                    orientation: 'horizontal'          
                    size_hint: (None, None)
                    height: 121
                    width: 180
                    Image:
                        id: countdown_icon
                        source: "./asmcnc/skavaUI/img/countdown_big.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
                        size_hint: (None, None)
                        height: dp(118)
                        width: dp(100) 


""")


class SpindleHealthCheckActiveScreen(Screen):
    return_screen = 'go'
    max_seconds = 6
    seconds = 6
    update_timer_event = None

    def __init__(self, **kwargs):

        super(SpindleHealthCheckActiveScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.seconds = self.max_seconds

        self.cool_down_label.text = self.l.get_str('Running spindle motor health check…') + "\n" + \
                                    self.l.get_str('SmartBench is raising the Z axis.')

    def on_pre_enter(self):
        # health check if not called from elsewhere
        self.seconds = self.max_seconds
        self.countdown.text = str(self.seconds)

    def on_enter(self):
        self.run_spindle_health_check()
        self.cool_down_label.text = self.l.get_str('Running spindle motor health check…') + "\n" + \
                                    self.l.get_str('SmartBench is raising the Z axis.')

    def start_timer(self):
        self.update_timer_event = Clock.schedule_interval(self.update_timer, 1)
        self.cool_down_label.text = self.l.get_str('Running spindle motor health check…')

    def exit_screen(self, dt=0):
        self.sm.current = self.return_screen

    def update_timer(self, dt):
        if self.seconds > 0:
            self.seconds = self.seconds - 1
            self.countdown.text = str(self.seconds)

    def on_leave(self):
        # self.m.spindle_off()
        # self.m.vac_off()
        if self.update_timer_event != None: Clock.unschedule(self.update_timer_event)
        self.seconds = self.max_seconds
        self.countdown.text = str(self.seconds)

    passed_spindle_health_check = False
    spindle_health_check_max_w = 550  # 550
    start_after_pass = False

    def run_spindle_health_check(self):
        self.m.s.spindle_health_check_data[:] = []

        def pass_test(free_load):
            print("Spindle health check passed - free load: " + str(free_load))

            self.m.spindle_health_check_failed = False
            self.m.spindle_health_check_passed = True
            self.exit_screen()

            if self.sm.has_screen('go') and self.start_after_pass:
                self.sm.get_screen('go')._start_running_job()
                self.sm.current = 'go'

            self.m.s.yp.set_free_load(free_load)

        def show_fail_screen(reason):
            self.m.stop_for_a_stream_pause(reason)

            if self.sm.has_screen('go'):
                self.sm.get_screen('go').raise_pause_screens_if_paused(override=True)

        def fail_test(reason):
            print("Spindle health check failed - " + reason)
            self.m.spindle_health_check_failed = True
            self.m.spindle_health_check_passed = False
            show_fail_screen(reason)

        def check_average():
            average_load = sum(self.m.s.spindle_health_check_data) / (len(self.m.s.spindle_health_check_data) or 1)
            average_load_w = self.m.spindle_voltage * 0.1 * sqrt(average_load) if average_load != 0 else 0

            if average_load_w > self.spindle_health_check_max_w:
                fail_test('spindle_health_check_failed')
                return
            elif average_load_w == 0:
                fail_test('yetipilot_spindle_data_loss')
                return

            pass_test(round(average_load_w))

        def stop_test():
            self.m.s.write_command('M5')
            self.m.s.spindle_health_check = False

        def start_test():
            if self.m.smartbench_is_busy():
                Clock.schedule_once(lambda dt: start_test(), 0.5)
                return

            self.start_timer()
            self.m.s.spindle_health_check = True
            self.m.s.write_command('M3 S24000')
            Clock.schedule_once(lambda dt: stop_test(), 6)
            Clock.schedule_once(lambda dt: check_average(), 6)

        self.m._grbl_soft_reset()
        self.m.resume_from_a_soft_door()

        Clock.schedule_once(lambda dt: self.m.zUp(), 1)
        Clock.schedule_once(lambda dt: start_test(), 1)
