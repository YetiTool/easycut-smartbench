"""
Created on 4 March 2020
Repeat? Screen for the Shape Cutter App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

Builder.load_string(
    """

<ShapeCutterRepeatScreenClass>:
    
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
                text: "Would you like to do this again?"
                font_size:dp(0.0375*app.width)
                halign: "center"
                valign: "bottom"
                markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(app.get_scaled_width(800))
                height: dp(app.get_scaled_height(140))
                padding:dp(0)
                spacing: 0
                Label:
                    size_hint: (None,None)
                    height: dp(app.get_scaled_height(170))
                    width: dp(app.get_scaled_width(800))
                    halign: "center"
                    valign: "middle"
                    text: ""
                    color: 0,0,0,1
                    font_size:dp(0.0325*app.width)
                    markup: True

            BoxLayout:
                size_hint: (None,None)
                width: dp(app.get_scaled_width(800))
                height: dp(app.get_scaled_height(170))
                padding:(dp(app.get_scaled_width(100)),dp(0),dp(app.get_scaled_width(100)),dp(app.get_scaled_height(30)))
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos                
                
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(app.get_scaled_width(200))
                    height: dp(app.get_scaled_height(171))
                    padding:(dp(app.get_scaled_width(16)),dp(0),dp(app.get_scaled_width(16)),dp(0))
                    pos: self.parent.pos
                    
                    # Repeat
                    Button:
                        font_size: str(get_scaled_width(15)) + 'sp'
                        size_hint: (None,None)
                        height: dp(app.get_scaled_height(171))
                        width: dp(app.get_scaled_width(168))
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.repeat()
                        BoxLayout:
                            padding:dp(0)
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/button_repeat.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(app.get_scaled_width(200))
                    height: dp(app.get_scaled_height(171))
                    padding:(dp(app.get_scaled_width(16)),dp(0),dp(app.get_scaled_width(16)),dp(0))
                    pos: self.parent.pos
                    
                    # New
                    Button:
                        font_size: str(get_scaled_width(15)) + 'sp'
                        size_hint: (None,None)
                        height: dp(app.get_scaled_height(171))
                        width: dp(app.get_scaled_width(168))
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.new_cut()
                        BoxLayout:
                            padding:dp(0)
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/button_new.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(app.get_scaled_width(200))
                    height: dp(app.get_scaled_height(171))
                    padding:(dp(app.get_scaled_width(16)),dp(0),dp(app.get_scaled_width(16)),dp(0))
                    pos: self.parent.pos
                    
                    # Next
                    Button:
                        font_size: str(get_scaled_width(15)) + 'sp'
                        size_hint: (None,None)
                        height: dp(app.get_scaled_height(171))
                        width: dp(app.get_scaled_width(168))
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.exit()
                        BoxLayout:
                            padding:dp(0)
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/button_exit.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True  
            BoxLayout:
                size_hint: (None,None)
                width: dp(app.get_scaled_width(800))
                height: dp(app.get_scaled_height(80))
                padding:(dp(app.get_scaled_width(740)),dp(0),dp(0),dp(app.get_scaled_height(20)))
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos
"""
)


class ShapeCutterRepeatScreenClass(Screen):
    exiting = False

    def __init__(self, **kwargs):
        super(ShapeCutterRepeatScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs["shapecutter"]
        self.m = kwargs["machine"]

    def repeat(self):
        self.shapecutter_sm.repeat_cut()

    def new_cut(self):
        self.shapecutter_sm.landing()

    def exit(self):
        self.shapecutter_sm.exit_shapecutter()
