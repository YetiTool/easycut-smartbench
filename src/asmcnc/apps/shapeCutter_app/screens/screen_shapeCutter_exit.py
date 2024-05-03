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
        height: dp(1.66666666667*app.height)
        width: dp(0.6*app.width)
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
                height: dp(0.1875*app.height)
                width: dp(1.0*app.width)
                text: "Leaving Shape Cutter..."
                font_size: 0.0375*app.width
                halign: "center"
                valign: "bottom"
                markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.8125*app.height)
                padding:[0, dp(0.229166666667)*app.height, 0, dp(0.229166666667)*app.height]
                spacing: 0
                Label:
                    size_hint: (None,None)
                    height: dp(0.354166666667*app.height)
                    width: dp(1.0*app.width)
                    halign: "center"
                    valign: "middle"
                    text: "Bye!"
                    color: color_provider.get_rgba("black")
                    font_size: 0.0325*app.width
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
