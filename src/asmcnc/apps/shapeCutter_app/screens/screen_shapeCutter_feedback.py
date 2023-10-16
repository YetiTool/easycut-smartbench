"""
Created on 4 March 2020
Feedback Screen for the Shape Cutter App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
Builder.load_string(
    """

<ShapeCutterFeedbackScreenClass>:
    
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
                text: "Feedback"
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
                    text: "Was your job successful?"
                    color: 0,0,0,1
                    font_size: 0.0325*app.width
                    markup: True

            BoxLayout:
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.354166666667*app.height)
                padding:(0.225*app.width,0,0.225*app.width,0.0625*app.height)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos                
                
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.275*app.width)
                    height: dp(0.35625*app.height)
                    padding:(0.035*app.width,0,0.025*app.width,0)
                    pos: self.parent.pos
                    
                    # thumbs up button
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint: (None,None)
                        height: dp(0.35625*app.height)
                        width: dp(0.215*app.width)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.thumbs_up()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/thumbs_up.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.275*app.width)
                    height: dp(0.35625*app.height)
                    padding:(0.025*app.width,0,0.035*app.width,0)
                    pos: self.parent.pos
                    
                    # thumbs down button
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint: (None,None)
                        height: dp(0.35625*app.height)
                        width: dp(0.215*app.width)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.thumbs_down()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/thumbs_down.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True  
            BoxLayout:
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.166666666667*app.height)
                padding:(0.925*app.width,0,0,0.0416666666667*app.height)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos
"""
    )


class ShapeCutterFeedbackScreenClass(Screen):
    info_button = ObjectProperty()

    def __init__(self, **kwargs):
        super(ShapeCutterFeedbackScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs['shapecutter']
        self.m = kwargs['machine']

    def thumbs_up(self):
        self.next_screen()

    def thumbs_down(self):
        self.next_screen()

    def next_screen(self):
        self.shapecutter_sm.next_screen()
