'''
Created on 4 March 2020
ApIs Screen for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty # @UnresolvedImport

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
                source: "./asmcnc/apps/shapeCutter_app/img/landing_background.png"

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "vertical"       

            # Header
            
            BoxLayout: 
                size_hint: (None, None) 
                width: dp(800)
                height: dp(90)            
                Label:
                    size_hint: (None,None)
                    height: dp(90)
                    width: dp(800)
                    text: "Shape Cutter"
                    font_size: 30
                    halign: "center"
                    valign: "middle"
                    markup: True
                    text_size: self.size
                    size: self.parent.size
                    pos: self.parent.pos
                   
            
            BoxLayout: 
                size_hint: (None, None) 
                width: dp(800)
                height: dp(330)
                orientation: "vertical"
                    
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(800)
                    height: dp(85)
                    padding: (0,10,0,0)
                    spacing: 0
                    Label:
                        size_hint: (None,None)
                        height: dp(75)
                        width: dp(800)
                        halign: "center"
                        valign: "bottom"
                        text: "Select a shape to define..."
                        color: 0,0,0,1
                        font_size: 26
                        markup: True
    
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(800)
                    height: dp(225)
                    padding: (150,0,150,0)
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
                                    source: "./asmcnc/apps/shapeCutter_app/img/apt_rect.png"
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
                                    source: "./asmcnc/apps/shapeCutter_app/img/is_rect.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True  
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(800)
                    height: dp(20)
                    padding: (150,0,150,0)
                    spacing: 0
                    orientation: 'horizontal'
                    pos: self.parent.pos
                    BoxLayout:
                        size_hint: (None,None)
                        width: dp(250)
                        height: dp(20)
                        padding: (23,0,20,0)
                        pos: self.parent.pos
                        Label:
                            size_hint: (None,None)
                            height: dp(20)
                            width: dp(207)
                            halign: "center"
                            valign: "middle"
                            text: "Hole (cut an aperture)"
                            color: 0,0,0,1
                            font_size: 20
                            markup: True
                    BoxLayout:
                        size_hint: (None,None)
                        width: dp(250)
                        height: dp(20)
                        padding: (20,0,23,0)
                        pos: self.parent.pos
                        Label:
                            size_hint: (None,None)
                            height: dp(20)
                            width: dp(207)
                            halign: "center"
                            valign: "middle"
                            text: "Plate (cut an island)"
                            color: 0,0,0,1
                            font_size: 20
                            markup: True
                            
            # Info button
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(60)
                padding: (20,0,0,20)
                spacing: 680
                orientation: 'horizontal'
                pos: self.parent.pos
                Button:
                    id: info_button
                    size_hint: (None,None)
                    height: dp(40)
                    width: dp(40)
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
                    id: exit_button
                    size_hint: (None,None)
                    height: dp(40)
                    width: dp(40)
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

""")

class ShapeCutterApIsScreenClass(Screen):

    info_button = ObjectProperty()   
    shape = 'circle'
    
    def __init__(self, **kwargs):
        super(ShapeCutterApIsScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs['shapecutter']
        self.m=kwargs['machine']
        self.j=kwargs['job_parameters']
        
    def on_pre_enter(self):
        if self.j.shape_dict["shape"] == "circle":
            self.image_apt.source = ("./asmcnc/apps/shapeCutter_app/img/apt_circ.png")
            self.image_is.source = ("./asmcnc/apps/shapeCutter_app/img/is_circ.png")
        
        elif self.j.shape_dict["shape"] == 'rectangle':
            self.image_apt.source = ("./asmcnc/apps/shapeCutter_app/img/apt_rect.png")
            self.image_is.source = ("./asmcnc/apps/shapeCutter_app/img/is_rect.png")
      
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
    