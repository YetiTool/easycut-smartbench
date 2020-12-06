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

from asmcnc.apps import screen_measurement_jig
from asmcnc.comms import router_machine

Cmport = 'COM3'

class ScreenTest(App):


	def build(self):

		sm = ScreenManager(transition=NoTransition())
		m = router_machine.RouterMachine(Cmport, sm)
		door_test_screen = screen_measurement_jig.JigScreen(name = 'door', screen_manager = sm, machine = m)
		sm.add_widget(door_test_screen)
		sm.current = 'door'
		return sm

ScreenTest().run()