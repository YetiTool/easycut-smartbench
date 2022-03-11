'''
Created on 12 December 2019
Landing Screen for the Calibration App

@author: Letty
'''

import gc

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock

# from asmcnc.calibration_app import screen_prep_calibration

Builder.load_string("""

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
        padding: 90,50
        spacing: 0
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.8

            Label:
                id: screen_text
                text_size: self.size
                font_size: '28sp'
                halign: 'center'
                valign: 'middle'
                text: '[color=455A64]Calibration Complete![/color]'
                markup: 'True'
""")

class FinishedCalScreenClass(Screen):
    
    screen_text = ObjectProperty()
    calibration_cancelled = True
    return_to_screen = StringProperty()
    
    screen_manager = ObjectProperty()
    machine = ObjectProperty()

    def __init__(self, **kwargs):
        super(FinishedCalScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def on_pre_enter(self):
        if self.calibration_cancelled == True:
            self.screen_text.text = '[color=455A64]Calibration Cancelled.[/color]'
        else: 
            self.screen_text.text = '[color=455A64]Calibration Complete![/color]'                   

        if self.screen_manager.has_screen('measurement'):
            self.screen_manager.remove_widget(self.screen_manager.get_screen('measurement'))
        if self.screen_manager.has_screen('backlash'):
            self.screen_manager.remove_widget(self.screen_manager.get_screen('backlash'))
        if self.screen_manager.has_screen('prep'):
            self.screen_manager.remove_widget(self.screen_manager.get_screen('prep'))
        if self.screen_manager.has_screen('wait'):
            self.screen_manager.remove_widget(self.screen_manager.get_screen('wait'))
        if self.screen_manager.has_screen('calibration_landing'):
            self.screen_manager.remove_widget(self.screen_manager.get_screen('calibration_landing'))
        if self.screen_manager.has_screen('tape_measure_alert'):
            self.screen_manager.remove_widget(self.screen_manager.get_screen('tape_measure_alert'))
            
    def on_enter(self):
        if self.calibration_cancelled == False:
            self.machine.write_calibration_settings(0, float(320*3600))
        self.poll_for_success = Clock.schedule_once(self.exit_screen, 1.5)
 
    def exit_screen(self, dt):
        if not self.screen_manager.current == 'alarmScreen':
            self.screen_manager.current = self.return_to_screen
        
    def on_leave(self):
        if self.screen_manager.has_screen('calibration_complete'):
            self.screen_manager.remove_widget(self.screen_manager.get_screen('calibration_complete'))
            
        gc.collect()