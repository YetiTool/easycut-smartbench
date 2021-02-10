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
from asmcnc.skavaUI import screen_squaring_active


class ScreenTest(App):


    def build(self):

        sm = ScreenManager(transition=NoTransition())
        # Localization/language object
        l = localization.Localization()
        m = None
        squaring_active_screen = screen_squaring_active.SquaringScreenActive(name = 'squaring_active', screen_manager = sm, machine =m, localization = l)
        sm.add_widget(squaring_active_screen)

        sm.current = 'squaring_active'
        return sm

ScreenTest().run()