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
        height: dp(app.get_scaled_height(800))
        width: dp(app.get_scaled_width(480))
        canvas:
            Rectangle: 
                pos: self.pos
                size: self.size
                source: "./asmcnc/apps/shapeCutter_app/img/landing_background.png"

        BoxLayout:
            padding:dp(0)
            spacing: 0
            orientation: "vertical"       
                
            Label:
                size_hint: (None,None)
                height: dp(app.get_scaled_height(90))
                width: dp(app.get_scaled_width(800))
                text: "Leaving Shape Cutter..."
                font_size:dp(0.0375*app.width)
                halign: "center"
                valign: "bottom"
                markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(app.get_scaled_width(800))
                height: dp(app.get_scaled_height(390))
                padding:(dp(0),dp(app.get_scaled_height(110)),dp(0),dp(app.get_scaled_height(110)))
                spacing: 0
                Label:
                    size_hint: (None,None)
                    height: dp(app.get_scaled_height(170))
                    width: dp(app.get_scaled_width(800))
                    halign: "center"
                    valign: "middle"
                    text: "Bye!"
                    color: 0,0,0,1
                    font_size:dp(0.0325*app.width)
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
