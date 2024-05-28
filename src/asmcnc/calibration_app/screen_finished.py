"""
Created on 12 December 2019
Landing Screen for the Calibration App

@author: Letty
"""

import gc
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock

Builder.load_string(
    """

<FinishedCalScreenClass>:

    screen_text:screen_text

    canvas:
        Color: 
            rgba: hex('##FAFAFA')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding:[dp(0.1125)*app.width, dp(0.104166666667)*app.height]
        spacing: 0
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.8

            Label:
                id: screen_text
                text_size: self.size
                font_size: str(0.035*app.width) + 'sp'
                halign: 'center'
                valign: 'middle'
                text: '[color=455A64]Calibration Complete![/color]'
                markup: 'True'
"""
)


class FinishedCalScreenClass(Screen):
    screen_text = ObjectProperty()
    calibration_cancelled = True
    return_to_screen = StringProperty()

    def __init__(self, **kwargs):
        self.sm = kwargs.pop("screen_manager")
        self.m = kwargs.pop("machine")
        super(FinishedCalScreenClass, self).__init__(**kwargs)

    def on_pre_enter(self):
        if self.calibration_cancelled == True:
            self.screen_text.text = "[color=455A64]Calibration Cancelled.[/color]"
        else:
            self.screen_text.text = "[color=455A64]Calibration Complete![/color]"
        if self.sm.has_screen("measurement"):
            self.sm.remove_widget(self.sm.get_screen("measurement"))
        if self.sm.has_screen("backlash"):
            self.sm.remove_widget(self.sm.get_screen("backlash"))
        if self.sm.has_screen("prep"):
            self.sm.remove_widget(self.sm.get_screen("prep"))
        if self.sm.has_screen("wait"):
            self.sm.remove_widget(self.sm.get_screen("wait"))
        if self.sm.has_screen("calibration_landing"):
            self.sm.remove_widget(self.sm.get_screen("calibration_landing"))
        if self.sm.has_screen("tape_measure_alert"):
            self.sm.remove_widget(self.sm.get_screen("tape_measure_alert"))

    def on_enter(self):
        if self.calibration_cancelled == False:
            self.m.write_calibration_settings(0, float(320 * 3600))
        self.poll_for_success = Clock.schedule_once(self.exit_screen, 1.5)

    def exit_screen(self, dt):
        if not self.sm.current == "alarmScreen":
            self.sm.current = self.return_to_screen

    def on_leave(self):
        if self.sm.has_screen("calibration_complete"):
            self.sm.remove_widget(self.sm.get_screen("calibration_complete"))
        gc.collect()
