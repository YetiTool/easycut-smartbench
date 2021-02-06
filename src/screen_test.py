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

from asmcnc.tests import screen_unicode_test


class ScreenTest(App):


	def build(self):

		sm = ScreenManager(transition=NoTransition())
		m = None
		jobstart_warning_screen = screen_unicode_test.ScreenClass(name='jobstart_warning', screen_manager = sm, machine = m)
		sm.add_widget(jobstart_warning_screen)
		sm.current = 'jobstart_warning'
		return sm

ScreenTest().run()