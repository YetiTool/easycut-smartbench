from kivy.uix.screenmanager import ScreenManager, Screen
import os
from asmcnc.apps.start_up_sequence.welcome_to_smartbench_app.screens import screen_language_select

class ScreenManagerWelcomeToSmartBench(object):

	def __init__(self, screen_manager, localization):
		self.sm = screen_manager
		self.l = localization

	def open_welcome_app(self):
		if not self.sm.has_screen('language_select'):
			language_select_screen = screen_language_select.LanguageSelectScreen(name = 'language_select', screen_manager = self.sm, localization = self.l)
			self.sm.add_widget(language_select_screen)

		self.sm.current = 'language_select'