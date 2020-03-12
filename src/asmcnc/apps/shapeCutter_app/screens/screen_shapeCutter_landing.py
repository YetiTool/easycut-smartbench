'''
Created on 19 February 2020
Landing Screen for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

from asmcnc.apps.shapeCutter_app.screens import popup_tutorial

Builder.load_string("""

<ShapeCutterLandingScreenClass>:
    
    BoxLayout:
        height: dp(800)
        width: dp(480)
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
                height: dp(90)
                width: dp(800)
                text: "Welcome to Shape Cutter"
                font_size: 30
                halign: "center"
                valign: "bottom"
                markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(140)
                padding: 0
                spacing: 0
                Label:
                    size_hint: (None,None)
                    height: dp(170)
                    width: dp(800)
                    halign: "center"
                    valign: "middle"
                    text: "Select a shape to cut..."
                    color: 0,0,0,1
                    font_size: 26
                    markup: True

            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(170)
                padding: (180,0,180,30)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos                
                
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(220)
                    height: dp(170)
                    padding: (25,0,27,0)
                    pos: self.parent.pos
                    
                    # Circle button
                    Button:
                        size_hint: (None,None)
                        height: dp(168)
                        width: dp(168)
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
                    width: dp(220)
                    height: dp(170)
                    padding: (27,0,25,0)
                    pos: self.parent.pos
                    
                    # rectangle button
                    Button:
                        size_hint: (None,None)
                        height: dp(168)
                        width: dp(168)
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
                width: dp(800)
                height: dp(80)
                padding: (740,0,0,20)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos
                Button:
                    id: info_button
                    size_hint: (None,None)
                    height: dp(40)
                    width: dp(40)
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
""")

class ShapeCutterLandingScreenClass(Screen):

    info_button = ObjectProperty()   
#     user_instruction = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(ShapeCutterLandingScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs['shapecutter']
        self.m=kwargs['machine']
        self.j=kwargs['job_parameters']
        
    def get_info(self):
        popup_tutorial.PopupTutorial(self.shapecutter_sm)
      
    def cut_rectangle(self):
        self.j.shape_dict["shape"] = "rectangle"
        self.next_screen()
    
    def cut_circle(self):
        self.j.shape_dict["shape"] = "circle"
        self.next_screen()
    
    def next_screen(self):
        self.shapecutter_sm.next_screen()

