'''
Created on 12 December 2019
Landing Screen for the Calibration App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock

# from asmcnc.calibration_app import screen_prep_calibration

Builder.load_string("""

<WaitScreenClass>:

    canvas:
        Color: 
            rgba: hex('#DCEDC8')
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
                text_size: self.size
                font_size: '18sp'
                halign: 'center'
                valign: 'middle'
                text: '[color=546E7A]Moving to the next measurement point...[/color]'
                markup: 'True'
""")

class WaitScreenClass(Screen):
    
    return_to_screen = StringProperty()
    
    def __init__(self, **kwargs):
        super(WaitScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def on_enter(self):
        self.poll_for_success = Clock.schedule_interval(self.wait_for_movement_to_complete, 2)
        
    def wait_for_movement_to_complete(self, dt):
        print (self.m.state)
        if not self.m.state == 'Jog':
            Clock.unschedule(self.poll_for_success)
            self.sm.current = self.return_to_screen