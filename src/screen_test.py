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

from asmcnc.core_UI.data_and_wifi.screens import wifi_and_data_consent_1


class ScreenTest(App):

	def build(self):

		sm = ScreenManager(transition=NoTransition())
		m = None
		alarm_1_screen = wifi_and_data_consent_1.WiFiAndDataConsentScreen1(name='final_test', screen_manager = sm, machine = m)
		sm.add_widget(alarm_1_screen)
		sm.current = 'final_test'
		return sm

ScreenTest().run()