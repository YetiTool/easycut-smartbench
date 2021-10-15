# -*- coding: utf-8 -*-
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

<StartingSmartBenchScreen>:

    starting_label: starting_label

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
                id: starting_label
                text_size: self.size
                font_size: '40sp'
                halign: 'center'
                valign: 'middle'
                markup: 'True'
                color: hex('#455A64ff')
""")


def log(message):
    
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)


class StartingSmartBenchScreen(Screen):
    
    start_in_warranty_mode = False
    
    def __init__(self, **kwargs):
        
        super(WelcomeScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.set=kwargs['settings']
        self.db=kwargs['database']
        self.am = kwargs['app_manager']
        self.l=kwargs['localization']
        self.update_strings()

        if self.m.trigger_setup and os.path.isfile("/home/pi/smartbench_activation_code.txt"):
            self.start_in_warranty_mode = True

        else:
            self.start_in_warranty_mode = False

    def on_enter(self):

        self.set.refresh_all()

        if self.m.s.is_connected():
    
            # RasPi boot timings
            if sys.platform != 'win32':
                
                # Allow kivy to have fully loaded before doing any calls which require scheduling
                Clock.schedule_once(self.m.s.start_services, 4)

                # Allow time for machine reset sequence
                # Then start up UI in relevant mode
                if self.start_in_warranty_mode: 
                    Clock.schedule_once(lambda dt: self.am.start_warranty_app(), 6)

                else:
                    # start pika connection if warranty does not need activating
                    self.db.start_connection_to_database_thread()
                    Clock.schedule_once(self.go_to_safety_screen, 6)

                # Set settings that are relevant to the GUI, but which depend on getting machine settings first
                Clock.schedule_once(self.set_machine_value_driven_user_settings,6.2)


            # PC boot timings
            else:
                # Allow kivy to have fully loaded before doing any calls which require scheduling
                Clock.schedule_once(self.m.s.start_services, 1)

                # Allow time for machine reset sequence
                if self.start_in_warranty_mode: 
                    Clock.schedule_once(lambda dt: self.am.start_warranty_app(), 2)

                else:
                    self.db.start_connection_to_database_thread()
                    Clock.schedule_once(self.go_to_safety_screen, 2)



        elif sys.platform == 'win32' or sys.platform == 'darwin':
            if self.start_in_warranty_mode: 
                Clock.schedule_once(lambda dt: self.am.start_warranty_app(), 1)

            else:
                self.db.start_connection_to_database_thread()
                Clock.schedule_once(self.go_to_safety_screen, 1)

    def go_to_safety_screen(self, dt):
        self.sm.current = 'safety'
        
    def set_machine_value_driven_user_settings(self, dt):

        # Laser settings
        if self.m.is_laser_enabled == True: self.sm.get_screen('home').default_datum_choice = 'laser'
        else: self.sm.get_screen('home').default_datum_choice = 'spindle'


        # SW Update available?
        if (self.set.sw_version) != self.set.latest_sw_version and not self.set.latest_sw_version.endswith('beta') and not self.set.sw_branch == 'master':
            self.sm.get_screen('lobby').trigger_update_popup = True


    def update_strings(self):
        self.starting_label.text = self.l.get_str('Starting SmartBench') + '...'