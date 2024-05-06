"""
Created on 4 March 2020
ApIs Screen for the Shape Cutter App

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty 

Builder.load_string(
    """

<ShapeCutterApIsScreenClass>:

    image_apt: image_apt
    image_is: image_is
        
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

            # Header
            
            BoxLayout: 
                size_hint: (None, None) 
                width: app.get_scaled_width(800.0)
                height: app.get_scaled_height(90.0)
                Label:
                    size_hint: (None,None)
                    height: app.get_scaled_height(90.0)
                    width: app.get_scaled_width(800.0)
                    text: "Shape Cutter"
                    font_size: app.get_scaled_width(30.0)
                    halign: "center"
                    valign: "middle"
                    markup: True
                    text_size: self.size
                    size: self.parent.size
                    pos: self.parent.pos
                   
            
            BoxLayout: 
                size_hint: (None, None) 
                width: app.get_scaled_width(800.0)
                height: app.get_scaled_height(330.0)
                orientation: "vertical"
                    
                BoxLayout:
                    size_hint: (None,None)
                    width: app.get_scaled_width(800.0)
                    height: app.get_scaled_height(84.9999999998)
                    padding: app.get_scaled_tuple([0.0, 10.0, 0.0, 0.0])
                    spacing: 0
                    Label:
                        size_hint: (None,None)
                        height: app.get_scaled_height(75.0)
                        width: app.get_scaled_width(800.0)
                        halign: "center"
                        valign: "bottom"
                        text: "Select a shape to define..."
                        color: 0,0,0,1
                        font_size: app.get_scaled_width(26.0)
                        markup: True
    
                BoxLayout:
                    size_hint: (None,None)
                    width: app.get_scaled_width(800.0)
                    height: app.get_scaled_height(225.0)
                    padding: app.get_scaled_tuple([150.0, 0.0, 150.0, 0.0])
                    spacing: 0
                    orientation: 'horizontal'
                    pos: self.parent.pos                
                    
                    BoxLayout:
                        size_hint: (None,None)
                        width: app.get_scaled_width(250.0)
                        height: app.get_scaled_height(225.0)
                        padding: app.get_scaled_tuple([23.0, 0.0, 20.0, 0.0])
                        pos: self.parent.pos
                        
                        # aperture
                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            size_hint: (None,None)
                            height: app.get_scaled_height(225.0)
                            width: app.get_scaled_width(207.0)
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
                                    source: "./asmcnc/apps/shapeCutter_app/img/apt_rect.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
                    BoxLayout:
                        size_hint: (None,None)
                        width: app.get_scaled_width(250.0)
                        height: app.get_scaled_height(225.0)
                        padding: app.get_scaled_tuple([20.0, 0.0, 23.0, 0.0])
                        pos: self.parent.pos
                        
                        # island
                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
                            size_hint: (None,None)
                            height: app.get_scaled_height(225.0)
                            width: app.get_scaled_width(207.0)
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
                                    source: "./asmcnc/apps/shapeCutter_app/img/is_rect.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True  
                BoxLayout:
                    size_hint: (None,None)
                    width: app.get_scaled_width(800.0)
                    height: app.get_scaled_height(20.0)
                    padding: app.get_scaled_tuple([150.0, 0.0, 150.0, 0.0])
                    spacing: 0
                    orientation: 'horizontal'
                    pos: self.parent.pos
                    BoxLayout:
                        size_hint: (None,None)
                        width: app.get_scaled_width(250.0)
                        height: app.get_scaled_height(20.0)
                        padding: app.get_scaled_tuple([23.0, 0.0, 20.0, 0.0])
                        pos: self.parent.pos
                        Label:
                            size_hint: (None,None)
                            height: app.get_scaled_height(20.0)
                            width: app.get_scaled_width(207.0)
                            halign: "center"
                            valign: "middle"
                            text: "Hole (cut an aperture)"
                            color: 0,0,0,1
                            font_size: app.get_scaled_width(20.0)
                            markup: True
                    BoxLayout:
                        size_hint: (None,None)
                        width: app.get_scaled_width(250.0)
                        height: app.get_scaled_height(20.0)
                        padding: app.get_scaled_tuple([20.0, 0.0, 23.0, 0.0])
                        pos: self.parent.pos
                        Label:
                            size_hint: (None,None)
                            height: app.get_scaled_height(20.0)
                            width: app.get_scaled_width(207.0)
                            halign: "center"
                            valign: "middle"
                            text: "Plate (cut an island)"
                            color: 0,0,0,1
                            font_size: app.get_scaled_width(20.0)
                            markup: True
                            
            # Info button
            BoxLayout:
                size_hint: (None,None)
                width: app.get_scaled_width(800.0)
                height: app.get_scaled_height(60.0)
                padding: app.get_scaled_tuple([20.0, 0.0, 0.0, 20.0])
                spacing: app.get_scaled_width(680.0)
                orientation: 'horizontal'
                pos: self.parent.pos
                Button:
                    font_size: app.get_scaled_sp('15.0sp')
                    id: info_button
                    size_hint: (None,None)
                    height: app.get_scaled_height(40.0)
                    width: app.get_scaled_width(40.0)
                    background_color: hex('#F4433600')
                    opacity: 0
#                     on_press: root.get_info()
#                     BoxLayout:
#                         padding: 0
#                         size: self.parent.size
#                         pos: self.parent.pos
#                         Image:
#                             source: "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
#                             center_x: self.parent.center_x
#                             y: self.parent.y
#                             size: self.parent.width, self.parent.height
#                             allow_stretch: True

                Button:
                    font_size: app.get_scaled_sp('15.0sp')
                    id: exit_button
                    size_hint: (None,None)
                    height: app.get_scaled_height(40.0)
                    width: app.get_scaled_width(40.0)
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


class ShapeCutterApIsScreenClass(Screen):
    info_button = ObjectProperty()
    shape = "circle"

    def __init__(self, **kwargs):
        super(ShapeCutterApIsScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs["shapecutter"]
        self.m = kwargs["machine"]
        self.j = kwargs["job_parameters"]

    def on_pre_enter(self):
        if self.j.shape_dict["shape"] == "circle":
            self.image_apt.source = "./asmcnc/apps/shapeCutter_app/img/apt_circ.png"
            self.image_is.source = "./asmcnc/apps/shapeCutter_app/img/is_circ.png"
        elif self.j.shape_dict["shape"] == "rectangle":
            self.image_apt.source = "./asmcnc/apps/shapeCutter_app/img/apt_rect.png"
            self.image_is.source = "./asmcnc/apps/shapeCutter_app/img/is_rect.png"

    def aperture(self):
        self.j.shape_dict["cut_type"] = "aperture"
        self.next_screen()

    def island(self):
        self.j.shape_dict["cut_type"] = "island"
        self.next_screen()

    def next_screen(self):
        self.shapecutter_sm.next_screen()

    def exit(self):
        self.shapecutter_sm.exit_shapecutter()
