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
                height: dp(140)
                padding: 0
                spacing: 0
                Label:
                    size_hint: (None,None)
                    height: dp(170)
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
                height: dp(200)
                padding: (150,0,150,0)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos                
                
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(250)
                    height: dp(200)
                    padding: (23,0,20,0)
                    pos: self.parent.pos
                    
                    # aperture
                    Button:
                        size_hint: (None,None)
                        height: dp(200)
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
                                source: "./asmcnc/shapeCutter_app/img/apt_rect.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(250)
                    height: dp(200)
                    padding: (20,0,23,0)
                    pos: self.parent.pos
                    
                    # island
                    Button:
                        size_hint: (None,None)
                        height: dp(200)
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
                                source: "./asmcnc/shapeCutter_app/img/is_rect.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True  
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(50)
                padding: (740,0,0,20)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos
""")

class ShapeCutterApIsScreenClass(Screen):

    info_button = ObjectProperty()   
    
    def __init__(self, **kwargs):
        super(ShapeCutterApIsScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
      
    def aperture(self):
        self.next_screen()
    
    def island(self):
        self.next_screen()
            
    def next_screen(self):
        self.sm.current = 'sC1'