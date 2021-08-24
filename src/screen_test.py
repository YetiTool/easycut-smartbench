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

from asmcnc.skavaUI import screen_fake_job_end


class ScreenTest(App):

	def build(self):

		sm = ScreenManager(transition=NoTransition())
		m = None
		test_screen_widget = screen_fake_job_end.FakeJobEndScreen(name='test_screen', screen_manager = sm, machine = m)
		sm.add_widget(test_screen_widget)
		sm.current = 'test_screen'
		return sm

ScreenTest().run()


# class TestScreen(Screen):

#     def __init__(self, **kwargs):
#         super(TestScreen, self).__init__(**kwargs)
#         self.sm = kwargs['screen_manager']
#         self.m = kwargs['machine']
