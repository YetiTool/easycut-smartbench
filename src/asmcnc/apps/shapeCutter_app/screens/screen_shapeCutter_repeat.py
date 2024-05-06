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
        height: app.get_scaled_height(800.000000002)
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
                text: "Would you like to do this again?"
                font_size: app.get_scaled_width(30.0)
                halign: "center"
                valign: "bottom"
                markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: app.get_scaled_width(800.0)
                height: app.get_scaled_height(140.0)
                padding: 0
                spacing: 0
                Label:
                    size_hint: (None,None)
                    height: app.get_scaled_height(170.0)
                    width: app.get_scaled_width(800.0)
                    halign: "center"
                    valign: "middle"
                    text: ""
                    color: 0,0,0,1
                    font_size: app.get_scaled_width(26.0)
                    markup: True

            BoxLayout:
                size_hint: (None,None)
                width: app.get_scaled_width(800.0)
                height: app.get_scaled_height(170.0)
                padding: app.get_scaled_tuple([100.0, 0.0, 100.0, 30.0])
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos                
                
                BoxLayout:
                    size_hint: (None,None)
                    width: app.get_scaled_width(200.0)
                    height: app.get_scaled_height(171.0)
                    padding: app.get_scaled_tuple([16.0, 0.0, 16.0, 0.0])
                    pos: self.parent.pos
                    
                    # Repeat
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        size_hint: (None,None)
                        height: app.get_scaled_height(171.0)
                        width: app.get_scaled_width(168.0)
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
                    width: app.get_scaled_width(200.0)
                    height: app.get_scaled_height(171.0)
                    padding: app.get_scaled_tuple([16.0, 0.0, 16.0, 0.0])
                    pos: self.parent.pos
                    
                    # New
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        size_hint: (None,None)
                        height: app.get_scaled_height(171.0)
                        width: app.get_scaled_width(168.0)
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
                    width: app.get_scaled_width(200.0)
                    height: app.get_scaled_height(171.0)
                    padding: app.get_scaled_tuple([16.0, 0.0, 16.0, 0.0])
                    pos: self.parent.pos
                    
                    # Next
                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        size_hint: (None,None)
                        height: app.get_scaled_height(171.0)
                        width: app.get_scaled_width(168.0)
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
                width: app.get_scaled_width(800.0)
                height: app.get_scaled_height(80.0000000002)
                padding: app.get_scaled_tuple([740.0, 0.0, 0.0, 20.0])
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
