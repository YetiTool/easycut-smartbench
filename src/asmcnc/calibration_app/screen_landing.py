'''
Created on 12 December 2019
Landing Screen for the Calibration App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget

from asmcnc.calibration_app import screen_prep_calibration
from asmcnc.calibration_app import screen_wait
from asmcnc.calibration_app import screen_finished

Builder.load_string("""

<CalibrationLandingScreenClass>:

    user_instruction: user_instruction
    
    canvas:
        Color: 
            rgba: hex('#FFFFFF')
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
            # spacing: 10
             
            Label:
                size_hint_y: 1
                font_size: '35sp'
                text: '[color=263238]Do you want to calibrate SmartBench?[/color]'
                markup: True

            Label:
                id: user_instruction
                size_hint_y: 2
                text_size: self.size
                font_size: '18sp'
                halign: 'center'
                valign: 'middle'
                markup: True

            Label:
                text_size: self.size
                font_size: '18sp'
                halign: 'center'
                valign: 'middle'
                text: '[color=546E7A]Calibration can take 10 minutes. You will need an accurate tape measure.[/color]'
                markup: True
                
            BoxLayout:
                orientation: 'horizontal'
                padding: 0, 0
                spacing: 20
            
                Button:
                    size_hint_y:0.9
                    id: getout_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: False
                    background_normal: ''
                    background_color: hex('#FFCDD2')
                    on_press: 
                        root.skip_to_lobby()
                        
                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            font_size: '20sp'
                            text: '[color=455A64]No, skip[/color]'
                            markup: True

                Button:
                    size_hint_y:0.9
                    id: getout_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: False
                    background_normal: ''
                    background_color: hex('#C5E1A5')
                    on_press: 
                        root.next_screen()
                        
                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            font_size: '20sp'
                            text: '[color=455A64]Yes, calibrate[/color]'
                            markup: True
            
""")

class CalibrationLandingScreenClass(Screen):
    
    user_instruction = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(CalibrationLandingScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        
        self.user_instruction.text  = '[color=546E7A]We calibrate SmartBench in the factory, but we recommend you re-calibrate if:\n\n' \
                                '- it has had a bumpy journey;\n' \
                                '- if you have been using it a lot;\n' \
                                '- or if the ambient temperature is hotter or cooler than usual.[/color]'

    def skip_to_lobby(self):
        self.sm.current = 'lobby'
        
    def next_screen(self):
        
        wait_screen = screen_wait.WaitScreenClass(name = 'wait', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(wait_screen)
        final_screen = screen_finished.FinishedCalScreenClass(name = 'calibration_complete', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(final_screen)
        
        if not self.sm.has_screen('prep'):
            prep_screen = screen_prep_calibration.PrepCalibrationScreenClass(name = 'prep', screen_manager = self.sm, machine = self.m)
            self.sm.add_widget(prep_screen)
        self.sm.current = 'prep'

    def on_leave(self):
        self.sm.remove_widget(self.sm.get_screen('calibration_landing'))