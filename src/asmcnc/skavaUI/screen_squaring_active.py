# -*- coding: utf-8 -*-
"""
Created March 2019

@author: Ed

Squaring decision: manual or auto?
"""
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from kivy.clock import Clock

Builder.load_string(
    """

<SquaringScreenActive>:

    overdrive_label: overdrive_label
    squaring_label: squaring_label

    canvas:
        Color: 
            rgba: hex('#E5E5E5FF')
        Rectangle: 
            size: self.size
            pos: self.pos         

    BoxLayout: 
        spacing: 0
        padding: app.get_scaled_tuple([20.0, 20.0])
        orientation: 'vertical'

        Label:
            font_size: app.get_scaled_sp('15.0sp')
            size_hint_y: 1

        BoxLayout:
            padding: app.get_scaled_tuple([20.0, 0.0])
            orientation: 'horizontal'
            spacing: app.get_scaled_width(30.0)
            size_hint_y: 1.5

            Button:
                font_size: app.get_scaled_sp('15.0sp')
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.windows_cheat_to_procede()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/squaring_icon_big.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
            Label:
                id: squaring_label
                size_hint_x: 1.1
                markup: True
                font_size: str(0.0375*app.width) + 'px' 
                valign: 'middle'
                halign: 'center'
                size:self.texture_size
                # text_size: self.size
                color: hex('#333333ff')
                        
            Button:
                font_size: app.get_scaled_sp('15.0sp')
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.stop_button_press()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/stop_big.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
            
        Label:
            id: overdrive_label
            size_hint_y: 2
            markup: True
            font_size: str(0.035*app.width) + 'px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            color: hex('#333333ff')           


"""
)


class SquaringScreenActive(Screen):
    return_to_screen = "lobby"
    cancel_to_screen = "lobby"
    poll_for_completion_loop = None
    expected_next_screen = "homing_active"

    def __init__(self, **kwargs):
        super(SquaringScreenActive, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def on_pre_enter(self):
        if self.m.homing_interrupted:
            self.go_to_cancel_to_screen()
            return
        if not self.m.homing_in_progress:
            self.return_to_ec_if_homing_not_in_progress()

    def on_enter(self):
        if sys.platform == "win32" or sys.platform == "darwin":
            return
        self.poll_for_completion_loop = Clock.schedule_once(
            self.poll_for_squaring_status_func, 0.2
        )

    def on_leave(self):
        self.cancel_poll()

    def poll_for_squaring_status_func(self, dt=0):
        if self.m.homing_interrupted:
            self.cancel_squaring()
            return
        if not self.m.homing_in_progress:
            self.return_to_ec_if_homing_not_in_progress()
            return
        if not self.m.i_am_auto_squaring():
            self.return_to_homing_active_screen()
            return
        self.poll_for_completion_loop = Clock.schedule_once(
            self.poll_for_squaring_status_func, 0.2
        )

    def stop_button_press(self):
        self.cancel_squaring()
        self.go_to_cancel_to_screen()

    def go_to_cancel_to_screen(self):
        self.m.homing_interrupted = False
        self.sm.current = self.cancel_to_screen

    def cancel_squaring(self):
        self.cancel_poll()
        if self.m.homing_in_progress:
            self.m.cancel_homing_sequence()

    def return_to_ec_if_homing_not_in_progress(self):
        self.sm.current = self.return_to_screen
        self.m.homing_interrupted = False

    def return_to_homing_active_screen(self):
        self.sm.get_screen("homing_active").cancel_to_screen = self.cancel_to_screen
        self.sm.get_screen("homing_active").return_to_screen = self.return_to_screen
        self.sm.current = "homing_active"

    def cancel_poll(self):
        if self.poll_for_completion_loop:
            self.poll_for_completion_loop.cancel()

    def update_strings(self):
        self.overdrive_label.text = self.l.get_str(
            "This operation will over-drive the X beam into the legs, creating a stalling noise. This is normal."
        )
        self.squaring_label.text = self.l.get_bold("Squaring") + "..."

    def windows_cheat_to_procede(self):
        if sys.platform == "win32" or sys.platform == "darwin":
            self.return_to_homing_active_screen()
        else:
            pass
