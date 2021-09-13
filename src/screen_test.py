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
from asmcnc.skavaUI import screen_file_loading
from asmcnc.tests import loading_screen_test

from asmcnc.core_UI.data_and_wifi.screens import wifi_and_data_consent_1
from asmcnc.core_UI.data_and_wifi.screens import wifi_and_data_consent_2


class ScreenTest(App):

	def build(self):

		sm = ScreenManager(transition=NoTransition())
		m = None
		alarm_1_screen = wifi_and_data_consent_1.WiFiAndDataConsentScreen1(name='wifi1', screen_manager = sm, machine = m)
		sm.add_widget(alarm_1_screen)
		alarm_2_screen = wifi_and_data_consent_2.WiFiAndDataConsentScreen2(name='wifi2', screen_manager = sm, machine = m)
		sm.add_widget(alarm_2_screen)
		sm.current = 'wifi1'
		return sm

ScreenTest().run()