 # -*- coding: utf-8 -*-

from kivy.config import Config
from kivy.clock import Clock
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'maxfps', '60')
Config.set('kivy', 'KIVY_CLOCK', 'interrupt')
Config.write()

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from asmcnc.comms import localization

# JOB DATA IMPORT
from asmcnc.job import job_data
from asmcnc.skavaUI import screen_job_incomplete
from asmcnc.skavaUI import screen_job_feedback



class ScreenTest(App):

	def build(self):

		sm = ScreenManager(transition=NoTransition())
		m = None
		l = localization.Localization()
		jd = job_data.JobData()
		db = None

		alarm_1_screen = screen_job_incomplete.JobIncompleteScreen(name='wifi1', screen_manager = sm, machine = m, localization = l, job = jd, database = db)
		sm.add_widget(alarm_1_screen)
		alarm_2_screen = screen_job_feedback.JobFeedbackScreen(name='wifi2', screen_manager = sm, machine = m, localization = l, job = jd, database = db)
		sm.add_widget(alarm_2_screen)
		sm.current = 'wifi1'
		return sm

ScreenTest().run()


