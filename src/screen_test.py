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
from asmcnc.skavaUI import screen_lift_z_on_pause_decision


class ScreenTest(App):


    def build(self):

        sm = ScreenManager(transition=NoTransition())
        # Localization/language object
        l = localization.Localization()
        m = None
        lift_z_on_pause_decision_screen = screen_lift_z_on_pause_decision.LiftZOnPauseDecisionScreen(name = 'lift_z_on_pause_or_not', screen_manager = sm, machine =m, localization = l)
        sm.add_widget(lift_z_on_pause_decision_screen)

        sm.current = 'lift_z_on_pause_or_not'
        return sm

ScreenTest().run()