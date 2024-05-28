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
                text: "Would you like to do this again?"
                font_size: 0.0375*app.width
                halign: "center"
                valign: "bottom"
                markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.291666666667*app.height)
                padding: 0
                spacing: 0
                Label:
                    size_hint: (None,None)
                    height: dp(0.354166666667*app.height)
                    width: dp(1.0*app.width)
                    halign: "center"
                    valign: "middle"
                    text: ""
                    color: 0,0,0,1
                    font_size: 0.0325*app.width
                    markup: True

            BoxLayout:
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.354166666667*app.height)
                padding:[dp(0.125)*app.width, 0, dp(0.125)*app.width, dp(0.0625)*app.height]
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos                
                
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.25*app.width)
                    height: dp(0.35625*app.height)
                    padding:[dp(0.02)*app.width, 0, dp(0.02)*app.width, 0]
                    pos: self.parent.pos
                    
                    # Repeat
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint: (None,None)
                        height: dp(0.35625*app.height)
                        width: dp(0.21*app.width)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.repeat()
                        BoxLayout:
                            padding: 0
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
                    width: dp(0.25*app.width)
                    height: dp(0.35625*app.height)
                    padding:[dp(0.02)*app.width, 0, dp(0.02)*app.width, 0]
                    pos: self.parent.pos
                    
                    # New
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint: (None,None)
                        height: dp(0.35625*app.height)
                        width: dp(0.21*app.width)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.new_cut()
                        BoxLayout:
                            padding: 0
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
                    width: dp(0.25*app.width)
                    height: dp(0.35625*app.height)
                    padding:[dp(0.02)*app.width, 0, dp(0.02)*app.width, 0]
                    pos: self.parent.pos
                    
                    # Next
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint: (None,None)
                        height: dp(0.35625*app.height)
                        width: dp(0.21*app.width)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.exit()
                        BoxLayout:
                            padding: 0
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
                width: dp(1.0*app.width)
                height: dp(0.166666666667*app.height)
                padding:[dp(0.925)*app.width, 0, 0, dp(0.0416666666667)*app.height]
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos
"""
)


class ShapeCutterRepeatScreenClass(Screen):
    exiting = False

    def __init__(self, **kwargs):
        self.shapecutter_sm = kwargs.pop("shapecutter")
        self.m = kwargs.pop("machine")
        super(ShapeCutterRepeatScreenClass, self).__init__(**kwargs)

    def repeat(self):
        self.shapecutter_sm.repeat_cut()

    def new_cut(self):
        self.shapecutter_sm.landing()

    def exit(self):
        self.shapecutter_sm.exit_shapecutter()
