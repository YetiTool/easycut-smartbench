#made on 06/01/2022 - Archie

#config setup
from kivy.config import Config

Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'maxfps', '60')
Config.set('kivy', 'KIVY_CLOCK', 'interrupt')

#import kivy requirements
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.clock import Clock

#various required objects
from settings import settings_manager
from asmcnc.comms import localization
from asmcnc.job import job_data

#screen imports
from asmcnc.skavaUI import screen_job_incomplete
from asmcnc.skavaUI import screen_file_loading

from asmcnc.skavaUI import screen_error

from mock import Mock, MagicMock


class TestSuite(App):
    def build(self):
        #general setup
        self.sm = ScreenManager(transition=NoTransition())
        self.l = localization.Localization()
        self.sett = settings_manager.Settings(self.sm)
        self.jd = job_data.JobData(localization = self.l, settings_manager = self.sett)

        #required?
        self.m = None
        self.db = Mock()

        go_screen = Screen(name='go')

        #two test screens:
        #file load
        #alarm screen?

        alarm_screen = screen_job_incomplete.JobIncompleteScreen(name='wifi', screen_manager = self.sm, machine = self.m, localization = self.l, job = self.jd, database = self.db)
        self.sm.add_widget(alarm_screen)
        self.sm.add_widget(go_screen)
        self.sm.current = 'wifi'

        # alarm_screen.run_test_suite()

        def change_job_incomplete_event_type():

            # self.error_dict = screen_error.ERROR_CODES
            self.event_number = 1

            def next_event_number(dt):

                self.sm.get_screen('wifi').prep_this_screen("Error", "error:" + str(self.event_number))
                self.sm.get_screen('wifi').update_strings()

                if self.event_number < 49:
                    self.event_number += 1


            Clock.schedule_interval(next_event_number, 1)

        change_job_incomplete_event_type()


        return self.sm

TestSuite().run()


