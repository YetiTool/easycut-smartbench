'''
Created on 4 March 2020
ApIs Screen for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

Builder.load_string("""

<ShapeCutterApIsScreenClass>:

    image_apt: image_apt
    image_is: image_is
        
    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas:
            Rectangle: 
                pos: self.pos
                size: self.size
                source: "./asmcnc/shapeCutter_app/img/landing_background.png"

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "vertical"       
                
            Label:
                size_hint: (None,None)
                height: dp(90)
                width: dp(800)
                text: "Shape Cutter"
                font_size: 30
                halign: "center"
                valign: "bottom"
                markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(115)
                padding: 0
                spacing: 0
                Label:
                    size_hint: (None,None)
                    height: dp(100)
                    width: dp(800)
                    halign: "center"
                    valign: "middle"
                    text: "Select a shape to define..."
                    color: 0,0,0,1
                    font_size: 26
                    markup: True

            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(240)
                padding: (150,0,150,15)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos                
                
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(250)
                    height: dp(225)
                    padding: (23,0,20,0)
                    pos: self.parent.pos
                    
                    # aperture
                    Button:
                        size_hint: (None,None)
                        height: dp(225)
                        width: dp(207)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.aperture()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_apt
                                source: "./asmcnc/shapeCutter_app/img/apt_rect.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(250)
                    height: dp(225)
                    padding: (20,0,23,0)
                    pos: self.parent.pos
                    
                    # island
                    Button:
                        size_hint: (None,None)
                        height: dp(225)
                        width: dp(207)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.island()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_is
                                source: "./asmcnc/shapeCutter_app/img/is_rect.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True  
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(50)
                padding: (150,0,150,20)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(250)
                    height: dp(50)
                    padding: (23,0,20,0)
                    pos: self.parent.pos
                    Label:
                        size_hint: (None,None)
                        height: dp(50)
                        width: dp(207)
                        halign: "center"
                        valign: "middle"
                        text: "Outer (cut an aperture)"
                        color: 0,0,0,1
                        font_size: 20
                        markup: True
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(250)
                    height: dp(50)
                    padding: (20,0,23,0)
                    pos: self.parent.pos
                    Label:
                        size_hint: (None,None)
                        height: dp(50)
                        width: dp(207)
                        halign: "center"
                        valign: "middle"
                        text: "Inner (cut an island)"
                        color: 0,0,0,1
                        font_size: 20
                        markup: True
""")

class ShapeCutterApIsScreenClass(Screen):

    info_button = ObjectProperty()   
    shape = 'circle'
    
    def __init__(self, **kwargs):
        super(ShapeCutterApIsScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.j=kwargs['job_parameters']
        
    def on_pre_enter(self):
        if self.j.shape_dict["shape"] == "circle":
            self.image_apt.source = ("./asmcnc/shapeCutter_app/img/apt_circ.png")
            self.image_is.source = ("./asmcnc/shapeCutter_app/img/is_circ.png")
        
        elif self.j.shape_dict["shape"] == 'rectangle':
            self.image_apt.source = ("./asmcnc/shapeCutter_app/img/apt_rect.png")
            self.image_is.source = ("./asmcnc/shapeCutter_app/img/is_rect.png")
      
    def aperture(self):
        self.j.shape_dict["cut_type"] = "aperture"
        self.next_screen()
    
    def island(self):
        self.j.shape_dict["cut_type"] = "island"
        self.next_screen()

    def next_screen(self):
        self.sm.current = 'sCdimensions'