'''
Created on 19 Aug 2017

@author: Ed
'''
# config

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.video import Video

import sys, os

Builder.load_string("""

<InitialScreen>:
    video:video

""")

GRBL_STATUS_INTERVAL = 0.2

class InitialScreen(Screen):

    def __init__(self, **kwargs):
        super(InitialScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.video.bind(eos=self.loop_video)

    def loop_video(self, *args, **kwargs):
        self.video.state = 'stop'
        self.go_to_lobby(0)
    
    def on_enter(self):
        if sys.platform == "win32": # TO SKIP VIDEO
            Clock.schedule_once(self.go_to_lobby, 1) # Delay for grbl to initialize 
    
    def refresh_serial_status(self, dt):
        if self.m.is_connected():
            self.home_button.disabled = False
            self.message_label.text = '[color=000000]Tap the logo to home[/color]'
        else:
            self.home_button.disabled = True
            self.message_label.text = '[color=f44336]No serial - check the cable.[/color]'

    def refresh_grbl_status(self, dt):
        if self.m.is_connected():
            self.status_label.text = 'Status: ' + self.m.state()

    def home_and_listen_for_idle(self):
        self.home_button.disabled = True
        self.message_label.text = "[color=4caf50ff]Homing...[/color]"
        self.m.home_all()
        self.detect_idle = Clock.schedule_interval(self.detect_homing_complete, 1)

    def detect_homing_complete(self, dt):
        if self.m.state() == 'Idle': 
            self.detect_idle.cancel()
            self.go_to_home_screen()
