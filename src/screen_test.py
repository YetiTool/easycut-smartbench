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

from asmcnc.skavaUI import screen_spindle_cooldown


class ScreenTest(App):


	def build(self):

		sm = ScreenManager(transition=NoTransition())
		spindle_cooldown_screen = screen_spindle_cooldown.SpindleCooldownScreen(name = 'spindle_cooldown', screen_manager = sm)
		sm.add_widget(spindle_cooldown_screen)
		sm.current = 'spindle_cooldown'
		return sm

ScreenTest().run()