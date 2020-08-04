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

from asmcnc.skavaUI import screen_z_head_diagnostics


class ScreenTest(App):


	def build(self):

		sm = ScreenManager(transition=NoTransition())
		z_head_diagnostics_screen = screen_z_head_diagnostics.ZHeadDiagnosticsScreen(name = 'z_head_diagnostics', screen_manager = sm)
		sm.add_widget(z_head_diagnostics_screen)
		sm.current = 'z_head_diagnostics'
		return sm

ScreenTest().run()