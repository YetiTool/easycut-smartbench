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

            # Header
            
            BoxLayout: 
                size_hint: (None, None) 
                width: dp(1.0*app.width)
                height: dp(0.1875*app.height)            
                Label:
                    size_hint: (None,None)
                    height: dp(0.1875*app.height)
                    width: dp(1.0*app.width)
                    text: "Shape Cutter"
                    font_size: 0.0375*app.width
                    halign: "center"
                    valign: "middle"
                    markup: True
                    text_size: self.size
                    size: self.parent.size
                    pos: self.parent.pos
                   
            
            BoxLayout: 
                size_hint: (None, None) 
                width: dp(1.0*app.width)
                height: dp(0.6875*app.height)
                orientation: "vertical"
                    
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(1.0*app.width)
                    height: dp(0.177083333333*app.height)
                    padding:[0, dp(0.0208333333333)*app.height, 0, 0]
                    spacing: 0
                    Label:
                        size_hint: (None,None)
                        height: dp(0.15625*app.height)
                        width: dp(1.0*app.width)
                        halign: "center"
                        valign: "bottom"
                        text: "Select a shape to define..."
                        color: 0,0,0,1
                        font_size: 0.0325*app.width
                        markup: True
    
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(1.0*app.width)
                    height: dp(0.46875*app.height)
                    padding:[dp(0.1875)*app.width, 0, dp(0.1875)*app.width, 0]
                    spacing: 0
                    orientation: 'horizontal'
                    pos: self.parent.pos                
                    
                    BoxLayout:
                        size_hint: (None,None)
                        width: dp(0.3125*app.width)
                        height: dp(0.46875*app.height)
                        padding:[dp(0.02875)*app.width, 0, dp(0.025)*app.width, 0]
                        pos: self.parent.pos
                        
                        # aperture
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            size_hint: (None,None)
                            height: dp(0.46875*app.height)
                            width: dp(0.25875*app.width)
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
                        width: dp(0.3125*app.width)
                        height: dp(0.46875*app.height)
                        padding:[dp(0.025)*app.width, 0, dp(0.02875)*app.width, 0]
                        pos: self.parent.pos
                        
                        # island
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            size_hint: (None,None)
                            height: dp(0.46875*app.height)
                            width: dp(0.25875*app.width)
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
                    width: dp(1.0*app.width)
                    height: dp(0.0416666666667*app.height)
                    padding:[dp(0.1875)*app.width, 0, dp(0.1875)*app.width, 0]
                    spacing: 0
                    orientation: 'horizontal'
                    pos: self.parent.pos
                    BoxLayout:
                        size_hint: (None,None)
                        width: dp(0.3125*app.width)
                        height: dp(0.0416666666667*app.height)
                        padding:[dp(0.02875)*app.width, 0, dp(0.025)*app.width, 0]
                        pos: self.parent.pos
                        Label:
                            size_hint: (None,None)
                            height: dp(0.0416666666667*app.height)
                            width: dp(0.25875*app.width)
                            halign: "center"
                            valign: "middle"
                            text: "Hole (cut an aperture)"
                            color: 0,0,0,1
                            font_size: 0.025*app.width
                            markup: True
                    BoxLayout:
                        size_hint: (None,None)
                        width: dp(0.3125*app.width)
                        height: dp(0.0416666666667*app.height)
                        padding:[dp(0.025)*app.width, 0, dp(0.02875)*app.width, 0]
                        pos: self.parent.pos
                        Label:
                            size_hint: (None,None)
                            height: dp(0.0416666666667*app.height)
                            width: dp(0.25875*app.width)
                            halign: "center"
                            valign: "middle"
                            text: "Plate (cut an island)"
                            color: 0,0,0,1
                            font_size: 0.025*app.width
                            markup: True
                            
            # Info button
            BoxLayout:
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.125*app.height)
                padding:[dp(0.025)*app.width, 0, 0, dp(0.0416666666667)*app.height]
                spacing:0.85*app.width
                orientation: 'horizontal'
                pos: self.parent.pos
                Button:
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: info_button
                    size_hint: (None,None)
                    height: dp(0.0833333333333*app.height)
                    width: dp(0.05*app.width)
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


class ShapeCutterApIsScreenClass(Screen):
    info_button = ObjectProperty()
    shape = "circle"

    def __init__(self, **kwargs):
        self.shapecutter_sm = kwargs.pop("shapecutter")
        self.m = kwargs.pop("machine")
        self.j = kwargs.pop("job_parameters")
        super(ShapeCutterApIsScreenClass, self).__init__(**kwargs)

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
