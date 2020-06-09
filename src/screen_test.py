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

from asmcnc.apps.maintenance_app import screen_maintenance


class ScreenTest(App):


	def build(self):

		sm = ScreenManager(transition=NoTransition())
		maintenance_screen = screen_maintenance.MaintenanceScreenClass(name = 'maintenance', screen_manager = sm)
		sm.add_widget(maintenance_screen)
		sm.current = 'maintenance'
		return sm

ScreenTest().run()