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
from datetime import datetime
Builder.load_string(
    """

<HomingScreenActive>:
    
    homing_label: homing_label

    canvas:
        Color: 
            rgba: hex('#E5E5E5FF')
        Rectangle: 
            size: self.size
            pos: self.pos         

    BoxLayout: 
        spacing: 0
        padding: 0.05*app.width
        orientation: 'vertical'

        Label:
            font_size: str(0.01875 * app.width) + 'sp'
            size_hint_y: 1

        BoxLayout:
            orientation: 'horizontal'
            spacing: 0.025*app.width
            size_hint_y: 1.5

            Button:
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.windows_cheat_to_procede()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/home_big.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
            Label:
                id: homing_label
                size_hint_x: 1.1
                markup: True
                font_size: '30px' 
                valign: 'middle'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')
                        
            Button:
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
            font_size: str(0.01875 * app.width) + 'sp'
            size_hint_y: 1                

"""
    )


def log(message):
    timestamp = datetime.now()
    print timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message)


class HomingScreenActive(Screen):
    return_to_screen = 'lobby'
    cancel_to_screen = 'lobby'
    poll_for_completion_loop = None
    expected_next_screen = 'squaring_active'

    def __init__(self, **kwargs):
        super(HomingScreenActive, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.update_strings()

    def on_pre_enter(self):
        log('Open homing screen')
        if self.m.homing_interrupted:
            self.go_to_cancel_to_screen()
            return

    def on_enter(self):
        if sys.platform == 'win32' or sys.platform == 'darwin':
            return
        if self.m.homing_interrupted:
            return
        if not self.m.homing_in_progress:
            self.m.do_standard_homing_sequence()
        self.poll_for_completion_loop = Clock.schedule_once(self.
            poll_for_homing_status_func, 0.2)

    def return_to_ec_if_homing_not_in_progress(self):
        self.sm.current = self.return_to_screen
        self.m.homing_interrupted = False

    def on_leave(self):
        self.cancel_poll()
        self.update_strings()

    def poll_for_homing_status_func(self, dt=0):
        if not self.m.homing_in_progress:
            self.return_to_ec_if_homing_not_in_progress()
            return
        if self.m.homing_interrupted:
            self.cancel_homing()
            return
        if self.m.i_am_auto_squaring():
            self.go_to_auto_squaring_screen()
            return
        self.poll_for_completion_loop = Clock.schedule_once(self.
            poll_for_homing_status_func, 0.2)

    def go_to_auto_squaring_screen(self, dt=0):
        if self.m.homing_task_idx > self.m.auto_squaring_idx:
            return
        self.sm.get_screen('squaring_active'
            ).cancel_to_screen = self.cancel_to_screen
        self.sm.get_screen('squaring_active'
            ).return_to_screen = self.return_to_screen
        self.sm.current = 'squaring_active'

    def stop_button_press(self):
        log('Homing cancelled by user')
        self.cancel_homing()
        self.go_to_cancel_to_screen()

    def go_to_cancel_to_screen(self):
        self.m.homing_interrupted = False
        self.sm.current = self.cancel_to_screen

    def cancel_homing(self):
        self.cancel_poll()
        if self.m.homing_in_progress:
            self.m.cancel_homing_sequence()

    def cancel_poll(self):
        if self.poll_for_completion_loop:
            self.poll_for_completion_loop.cancel()

    def update_strings(self):
        self.homing_label.text = self.l.get_str('Homing') + '...'

    def windows_cheat_to_procede(self):
        if sys.platform == 'win32' or sys.platform == 'darwin':
            self.return_to_ec_if_homing_not_in_progress()
        else:
            pass
