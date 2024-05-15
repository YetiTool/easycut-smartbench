"""
Created on 12 December 2019
Landing Screen for the Calibration App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.properties import (
    ObjectProperty,
    ListProperty,
    NumericProperty,
    StringProperty,
)
from kivy.uix.widget import Widget
from asmcnc.calibration_app import screen_prep_calibration
from asmcnc.calibration_app import screen_wait
from asmcnc.calibration_app import screen_finished
from asmcnc.calibration_app import screen_tape_measure

Builder.load_string(
    """

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

        BoxLayout:
            orientation: 'horizontal'
            padding: app.get_scaled_tuple([90.0, 50.0, 30.0, 50.0])
            spacing: 0
            size_hint_x: 1

            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.8
                # spacing: app.get_scaled_width(10)
                
                Label:
                    size_hint_y: 1
                    font_size: app.get_scaled_sp('35.0sp')
                    text: '[color=263238]Do you want to calibrate SmartBench?[/color]'
                    markup: True

                Label:
                    id: user_instruction
                    size_hint_y: 2
                    text_size: self.size
                    font_size: app.get_scaled_sp('18.0sp')
                    halign: 'center'
                    valign: 'middle'
                    markup: True

                Label:
                    text_size: self.size
                    font_size: app.get_scaled_sp('18.0sp')
                    halign: 'center'
                    valign: 'middle'
                    text: '[color=546E7A]Calibration can take 10 minutes. You will need an accurate tape measure.[/color]'
                    markup: True
                    
                BoxLayout:
                    orientation: 'horizontal'
                    padding: app.get_scaled_tuple([0, 0])
                    spacing: app.get_scaled_width(20.0)
                
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
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
                            padding: app.get_scaled_tuple([5.0, 5.0])
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                #size_hint_y: 1
                                font_size: app.get_scaled_sp('20.0sp')
                                text: '[color=455A64]No, skip[/color]'
                                markup: True

                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
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
                            padding: app.get_scaled_tuple([5.0, 5.0])
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Label:
                                #size_hint_y: 1
                                font_size: app.get_scaled_sp('20.0sp')
                                text: '[color=455A64]Yes, calibrate[/color]'
                                markup: True

        BoxLayout:
            size_hint_x: 0.1
            padding: app.get_scaled_tuple([0, 0, 0, 400.0])

            Button:
                font_size: app.get_scaled_sp('15.0sp')
                id: exit_button
                size_hint: (None,None)
                height: app.get_scaled_height(40.0)
                width: app.get_scaled_width(40.0)
                background_color: hex('#F4433600')
                opacity: 1
                on_press: root.skip_to_lobby()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/exit_icon.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
"""
)


class CalibrationLandingScreenClass(Screen):
    user_instruction = ObjectProperty()
    return_to_screen = StringProperty()

    def __init__(self, **kwargs):
        super(CalibrationLandingScreenClass, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.user_instruction.text = """[color=546E7A]We calibrate SmartBench in the factory, but we recommend you re-calibrate if:

- it has had a bumpy journey;
- if you have been using it a lot;
- or if the ambient temperature is hotter or cooler than usual.[/color]"""

    def skip_to_lobby(self):
        self.sm.current = self.return_to_screen

    def next_screen(self):
        if not self.sm.has_screen("wait"):
            wait_screen = screen_wait.WaitScreenClass(
                name="wait", screen_manager=self.sm, machine=self.m
            )
            self.sm.add_widget(wait_screen)
        if not self.sm.has_screen("tape_measure_alert"):
            tape_measure_screen = screen_tape_measure.TapeMeasureScreenClass(
                name="tape_measure_alert", screen_manager=self.sm, machine=self.m
            )
            self.sm.add_widget(tape_measure_screen)
        if not self.sm.has_screen("calibration_complete"):
            final_screen = screen_finished.FinishedCalScreenClass(
                name="calibration_complete", screen_manager=self.sm, machine=self.m
            )
            self.sm.add_widget(final_screen)
        if not self.sm.has_screen("prep"):
            prep_screen = screen_prep_calibration.PrepCalibrationScreenClass(
                name="prep", screen_manager=self.sm, machine=self.m
            )
            self.sm.add_widget(prep_screen)
        self.sm.current = "prep"

    def on_leave(self):
        if self.sm.current != "alarmScreen" and self.sm.current != "errorScreen":
            self.sm.remove_widget(self.sm.get_screen("calibration_landing"))
