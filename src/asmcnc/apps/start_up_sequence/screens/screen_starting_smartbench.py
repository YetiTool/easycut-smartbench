"""
Created on 12 December 2019
Landing Screen for the Calibration App

@author: Letty
"""
import sys
from datetime import datetime

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string(
    """

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
        padding:[dp(0.1125)*app.width, dp(0.104166666667)*app.height]
        spacing: 0
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.8

            Label:
                id: starting_label
                text_size: self.size
                font_size: str(0.05*app.width) + 'sp'
                halign: 'center'
                valign: 'middle'
                markup: 'True'
                color: hex('#455A64ff')
"""
)


def log(message):
    timestamp = datetime.now()
    print timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + message


class StartingSmartBenchScreen(Screen):
    start_in_warranty_mode = False

    def __init__(self, **kwargs):
        super(StartingSmartBenchScreen, self).__init__(**kwargs)
        self.start_seq = kwargs['start_sequence']
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.set = kwargs['settings']
        self.db = kwargs['database']
        self.l = kwargs['localization']
        self.update_strings()

    def on_enter(self):
        if self.m.s.is_connected():
            try:
                self.start_seq.update_check_config_flag()
            except:
                pass
            self.set.refresh_all()
            if sys.platform != 'win32':
                Clock.schedule_once(self.m.s.start_services, 4)
                self.db.start_connection_to_database_thread()
                Clock.schedule_once(self.next_screen, 6)
                Clock.schedule_once(self.
                                    set_machine_value_driven_user_settings, 6.2)
            else:
                Clock.schedule_once(self.m.s.start_services, 1)
                self.db.start_connection_to_database_thread()
                Clock.schedule_once(self.next_screen, 2)
        elif sys.platform == 'win32' or sys.platform == 'darwin':
            self.db.start_connection_to_database_thread()
            Clock.schedule_once(self.next_screen, 1)

    def next_screen(self, dt):
        self.start_seq.next_in_sequence()

    def set_machine_value_driven_user_settings(self, dt):
        if self.m.is_laser_enabled == True:
            self.sm.get_screen('home').default_datum_choice = 'laser'
        else:
            self.sm.get_screen('home').default_datum_choice = 'spindle'
        if (self.set.sw_version != self.set.latest_sw_version and not self.
                set.latest_sw_version.endswith('beta') and not self.set.
                                                                       sw_branch == 'master'):
            self.sm.get_screen('lobby').trigger_update_popup = True

    def update_strings(self):
        self.starting_label.text = self.l.get_str('Starting SmartBench'
                                                  ) + '...'
