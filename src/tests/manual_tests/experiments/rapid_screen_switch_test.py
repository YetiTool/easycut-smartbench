 # -*- coding: utf-8 -*-

from kivy.config import Config
from kivy.clock import Clock
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'maxfps', '60')
Config.set('kivy', 'KIVY_CLOCK', 'interrupt')
Config.write()

'''
########################################################
IMPORTANT!!
Run from easycut-smartbench folder, with 
python -m tests.manual_tests.experiments.rapid_screen_switch_test

'''

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.clock import Clock


Builder.load_string("""
<MenuScreen>:
	BoxLayout:
		Button:
			text: 'Goto settings'
			on_press: root.manager.current = 'settings'
		Button:
			text: 'Quit'

<SettingsScreen>:
	BoxLayout:
		Button:
			text: 'My settings button'
		Button:
			text: 'Back to menu'
			on_press: root.manager.current = 'menu'
""")

# Declare both screens
class SettingsScreen(Screen):
	pass

class MenuScreen(Screen):

	def __init__(self, **kwargs):
		super(MenuScreen, self).__init__(**kwargs)
		self.sm = kwargs['sm']

	def on_enter(self):
		Clock.schedule_once(self.go_to_settings, 1)

	def go_to_settings(self, dt):
		self.sm.current = 'settings'

	def on_leave(self):
		self.sm.current = 'menu'	


class TestApp(App):

	def build(self):
		# Create the screen manager
		sm = ScreenManager()
		sm.add_widget(SettingsScreen(name='settings'))
		sm.add_widget(MenuScreen(name='menu', sm=sm))

		sm.current = 'menu'

		return sm

if __name__ == '__main__':
	TestApp().run()