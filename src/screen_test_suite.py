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

import Queue as queue
import threading


class TestSuite(App):
    def build(self):
        #general setup
        self.sm = ScreenManager(transition=NoTransition())
        self.l = localization.Localization()
        self.sett = settings_manager.Settings(self.sm)
        self.jd = job_data.JobData(localization = self.l, settings_manager = self.sett)

        go_screen = Screen(name='go')
        home_screen = Screen(name='home')

        self.sm.add_widget(home_screen)
        self.sm.add_widget(go_screen)

        #required?
        self.m = None
        self.db = Mock()

        self.start_test_procedure()

        return self.sm

    def start_test_procedure(self):
        self.start_screen_job_incomplete_test()
        self.start_file_loading_test()

    def start_screen_job_incomplete_test(self):
        alarm_screen = screen_job_incomplete.JobIncompleteScreen(name='wifi', screen_manager = self.sm, machine = self.m, localization = self.l, job = self.jd, database = self.db)
        self.sm.add_widget(alarm_screen)
        self.sm.current = 'wifi'

        alarm_screen.run_test_suite()

    def start_file_loading_test(self):
        file_loading_screen = screen_file_loading.LoadingScreen(name = 'loading', screen_manager = self.sm, machine =self.m, job = self.jd, localization = self.l)
        self.sm.add_widget(file_loading_screen)
        self.sm.current = 'loading'

TestSuite().run()


