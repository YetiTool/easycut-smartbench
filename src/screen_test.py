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
# from asmcnc.comms import localization

# JOB DATA IMPORT
# from asmcnc.job import job_data
# from asmcnc.skavaUI import screen_job_incomplete
# from asmcnc.skavaUI import screen_job_feedback

from asmcnc.tests.z_head_qc_home import ZHeadQCHome
from asmcnc.tests.z_head_qc_1 import ZHeadQC1

class ScreenTest(App):

	def build(self):

		sm = ScreenManager(transition=NoTransition())
		m = None
		# l = localization.Localization()
		# jd = job_data.JobData()
		db = None

		z_head_qc_home = ZHeadQCHome(name='qchome', sm = sm)
		sm.add_widget(z_head_qc_home)

		z_head_qc_1 = ZHeadQC1(name='qc1', sm = sm)
		sm.add_widget(z_head_qc_1)

		sm.current = 'qchome'

		return sm

ScreenTest().run()


