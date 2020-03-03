'''
Created on 19 February 2020
Landing Screen for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

Builder.load_string("""

<ShapeCutterLandingScreenClass>:
    
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
                padding: (116,0,116,30)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos                
                
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(400)
                    height: dp(170)
                    padding: (20,0,0,0)
                    pos: self.parent.pos
                    
                    # Circle button
                    Button:
                        size_hint: (None,None)
                        height: dp(168)
                        width: dp(168)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        #on_press: 
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/shapeCutter_app/img/cut_circle.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(400)
                    height: dp(170)
                    padding: (0,0,20,0)
                    pos: self.parent.pos
                    
                    # Square button
                    Button:
                        size_hint: (None,None)
                        height: dp(168)
                        width: dp(168)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/shapeCutter_app/img/cut_square.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True  
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(80)
                padding: (700,0,0,20)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/shapeCutter_app/img/info_icon.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    #size: self.parent.width, self.parent.height
                    #allow_stretch: True                 
                          

            
""")

class ShapeCutterLandingScreenClass(Screen):
    
#     user_instruction = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(ShapeCutterLandingScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

        
    def cut_square(self):
        pass
    
    def cut_circle(self):
        pass

    def on_leave(self):
        self.sm.remove_widget(self.sm.get_screen('sClanding'))