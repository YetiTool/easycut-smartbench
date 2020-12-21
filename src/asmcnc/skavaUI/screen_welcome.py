'''
Created on 12 December 2019
Landing Screen for the Calibration App

@author: Letty
'''

import sys, os

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock
from datetime import datetime

from asmcnc.skavaUI import popup_info
# from asmcnc.calibration_app import screen_prep_calibration

Builder.load_string("""

<WelcomeScreenClass>:


    canvas:
        Color: 
            rgba: hex('##FAFAFA')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding: 90,50
        spacing: 0
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.8

            Label:
                text_size: self.size
                font_size: '40sp'
                halign: 'center'
                valign: 'middle'
                text: '[color=455A64]Starting SmartBench...[/color]'
                markup: 'True'
""")


def log(message):
    
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)


class WelcomeScreenClass(Screen):
    
    
    def __init__(self, **kwargs):
        
        super(WelcomeScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.set=kwargs['settings']
        self.set.refresh_all()


    def on_enter(self):

        if self.m.s.is_connected():

            # PC boot timings
            if sys.platform == 'win32':
                # Allow kivy to have fully loaded before doing any calls which require scheduling
                Clock.schedule_once(self.m.s.start_services, 1)
                # Allow time for machine reset sequence
                Clock.schedule_once(self.go_to_next_screen, 2)
    
            # RasPi boot timings: note test on hard boot, since hard boot takes longer
            if sys.platform != 'win32':
                # Allow kivy to have fully loaded before doing any calls which require scheduling
                Clock.schedule_once(self.m.s.start_services, 4)
                # Allow time for machine reset sequence
                Clock.schedule_once(self.go_to_next_screen, 6)
                # Set settings that are relevant to the GUI, but which depend on getting machine settings first                
                Clock.schedule_once(self.set_machine_value_driven_user_settings,6.2)
                
        elif sys.platform == 'win32' or sys.platform == 'darwin':
            Clock.schedule_once(self.go_to_next_screen, 1)


    def go_to_next_screen(self, dt):
        self.sm.current = 'safety'
        
    def set_machine_value_driven_user_settings(self, dt):

        # Laser settings
        if self.m.is_laser_enabled == True: self.sm.get_screen('home').default_datum_choice = 'laser'
        else: self.sm.get_screen('home').default_datum_choice = 'spindle'


        # SW Update available?
        if (self.set.sw_version) != self.set.latest_sw_version and not self.set.latest_sw_version.endswith('beta') and not self.set.sw_branch == 'master':
            update_message = "New software update available for download!\n\n" + \
            "Please use the [b]Update[/b] app to get the latest version."

            popup_info.PopupInfo(self.sm, 450, update_message)


