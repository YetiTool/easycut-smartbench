"""
Created on 5 March 2020
Job Cancelled Screen for the Shape Cutter App

@author: Letty
"""
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string(
    """

<ShapeCutterExitScreenClass>:
    
    BoxLayout:
        height: app.get_scaled_height(800.0)
        width: app.get_scaled_width(480.0)
        canvas:
            Rectangle: 
                pos: self.pos
                size: self.size
                source: "./asmcnc/apps/shapeCutter_app/img/landing_background.png"

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "vertical"       
                
            Label:
                size_hint: (None,None)
                height: app.get_scaled_height(90.0)
                width: app.get_scaled_width(800.0)
                text: "Leaving Shape Cutter..."
                font_size: app.get_scaled_width(30.0)
                halign: "center"
                valign: "bottom"
                markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: app.get_scaled_width(800.0)
                height: app.get_scaled_height(390.0)
                padding: app.get_scaled_tuple([0.0, 110.0, 0.0, 110.0])
                spacing: 0
                Label:
                    size_hint: (None,None)
                    height: app.get_scaled_height(170.0)
                    width: app.get_scaled_width(800.0)
                    halign: "center"
                    valign: "middle"
                    text: "Bye!"
                    color: 0,0,0,1
                    font_size: app.get_scaled_width(26.0)
                    markup: True

"""
)


class ShapeCutterExitScreenClass(Screen):
    info_button = ObjectProperty()

    def __init__(self, **kwargs):
        super(ShapeCutterExitScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs["shapecutter"]
        self.m = kwargs["machine"]

    def on_enter(self):
        self.poll_for_success = Clock.schedule_once(self.exit_screen, 1)

    def exit_screen(self, dt):
        self.shapecutter_sm.return_to_EC()
