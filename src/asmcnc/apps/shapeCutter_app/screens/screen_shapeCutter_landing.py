"""
Created on 19 February 2020
Landing Screen for the Shape Cutter App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from asmcnc.apps.shapeCutter_app.screens import popup_info
Builder.load_string(
    """

<ShapeCutterLandingScreenClass>:
    
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
                text: "Welcome to Shape Cutter"
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
                    text: "Select a shape to cut..."
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
                    height: dp(0.354166666667*app.height)
                    padding:(0.03125*app.width,0,0.03375*app.width,0)
                    pos: self.parent.pos
                    
                    # Circle button
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint: (None,None)
                        height: dp(0.35*app.height)
                        width: dp(0.21*app.width)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.cut_circle()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/cut_circle.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.275*app.width)
                    height: dp(0.354166666667*app.height)
                    padding:(0.03375*app.width,0,0.03125*app.width,0)
                    pos: self.parent.pos
                    
                    # rectangle button
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint: (None,None)
                        height: dp(0.35*app.height)
                        width: dp(0.21*app.width)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.cut_rectangle()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/cut_rectangle.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True  
            # Info button
            BoxLayout:
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.166666666667*app.height)
                padding:(0.025*app.width,0,0,0.0416666666667*app.height)
                spacing: 0.85*app.width
                orientation: 'horizontal'
                pos: self.parent.pos
                Button:
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: info_button
                    size_hint: (None,None)
                    height: dp(0.0833333333333*app.height)
                    width: dp(0.05*app.width)
                    background_color: hex('#F4433600')
                    opacity: 1
                    on_press: root.get_info()
                    BoxLayout:
                        padding: 0
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
                Button:
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: exit_button
                    size_hint: (None,None)
                    height: dp(0.0833333333333*app.height)
                    width: dp(0.05*app.width)
                    background_color: hex('#F4433600')
                    opacity: 1
                    on_press: root.exit()
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


class ShapeCutterLandingScreenClass(Screen):
    info_button = ObjectProperty()

    def __init__(self, **kwargs):
        super(ShapeCutterLandingScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs['shapecutter']
        self.m = kwargs['machine']
        self.j = kwargs['job_parameters']

    def on_pre_enter(self):
        self.m.get_grbl_settings()

    def get_info(self):
        popup_info.PopupTutorial(self.shapecutter_sm)

    def cut_rectangle(self):
        self.j.shape_dict['shape'] = 'rectangle'
        self.next_screen()

    def cut_circle(self):
        self.j.shape_dict['shape'] = 'circle'
        self.next_screen()

    def next_screen(self):
        self.shapecutter_sm.next_screen()

    def exit(self):
        self.shapecutter_sm.exit_shapecutter()
