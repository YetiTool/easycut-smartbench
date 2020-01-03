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

Builder.load_string("""

<CalibrationLandingScreenClass>:

    canvas:
        Color: 
            rgba: hex('#0d47a1FF')
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
                text: 'Do you want to calibrate SmartBench?'
                markup: True

            Label:
                text_size: self.size
                font_size: '18sp'
                halign: 'center'
                valign: 'middle'
                text: 'We calibrate SmartBench in the factory, but if it has had a bumpy journey, or you have been using it a lot, we recommend you re-calibrate to be sure.'

            Label:
                text_size: self.size
                font_size: '18sp'
                halign: 'center'
                valign: 'middle'
                text: 'Calibration can take 10 minutes. You will need an accurate tape measure.'
                
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
                    # background_color: hex('#a80000FF')
                    on_release: 
                        root.skip_to_lobby()
                        
                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            font_size: '20sp'
                            text: 'No, skip'

                Button:
                    size_hint_y:0.9
                    id: getout_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: False
                    # background_color: hex('#a80000FF')
                    on_release: 
                        root.next_screen()
                        
                    BoxLayout:
                        padding: 5
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            #size_hint_y: 1
                            font_size: '20sp'
                            text: 'Yes, calibrate'
            
""")

class CalibrationLandingScreenClass(Screen):
    
    def __init__(self, **kwargs):
        super(CalibrationLandingScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def skip_to_lobby(self):
        self.sm.current = 'lobby'
        
    def next_screen(self):
        
        wait_screen = screen_wait.WaitScreenClass(name = 'wait', screen_manager = self.sm, machine = self.m)
        self.sm.add_widget(wait_screen)
        
        if not self.sm.has_screen('prep'):
            prep_screen = screen_prep_calibration.PrepCalibrationScreenClass(name = 'prep', screen_manager = self.sm, machine = self.m)
            self.sm.add_widget(prep_screen)
        self.sm.current = 'prep'
 