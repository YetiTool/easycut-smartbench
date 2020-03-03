'''
Created on 19 February 2020
Landing Screen for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

from asmcnc.shapeCutter_app import screen_shapeCutter_1
from asmcnc.shapeCutter_app import screen_shapeCutter_10
from asmcnc.shapeCutter_app import screen_shapeCutter_16
from asmcnc.shapeCutter_app import screen_shapeCutter_26
from asmcnc.shapeCutter_app import screen_shapeCutter_34

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
                        on_press: root.cut_circle()
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
                                source: "./asmcnc/shapeCutter_app/img/cut_rectangle.png"
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
                            source: "./asmcnc/shapeCutter_app/img/info_icon.png"
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
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
    
    def get_info(self):
        self.sm.current = 'sCtutorial'
      
    def cut_rectangle(self):
        pass
    
    def cut_circle(self):
        pass

    def on_pre_leave(self):
        if not self.sm.has_screen('sC1'):
            sC1_screen = screen_shapeCutter_1.ShapeCutter1ScreenClass(name = 'sC1', screen_manager = self.sm, machine = self.m)
            self.sm.add_widget(sC1_screen)
        if not self.sm.has_screen('sC10'):
            sC10_screen = screen_shapeCutter_10.ShapeCutter10ScreenClass(name = 'sC10', screen_manager = self.sm, machine = self.m)
            self.sm.add_widget(sC10_screen)
        if not self.sm.has_screen('sC26'):
            sC26_screen = screen_shapeCutter_26.ShapeCutter26ScreenClass(name = 'sC26', screen_manager = self.sm, machine = self.m)
            self.sm.add_widget(sC26_screen)