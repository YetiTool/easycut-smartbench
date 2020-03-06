'''
Created on 4 March 2020
Repeat? Screen for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty


Builder.load_string("""

<ShapeCutterRepeatScreenClass>:
    
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
                text: "Would you like to do this again?"
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
                    text: ""
                    color: 0,0,0,1
                    font_size: 26
                    markup: True

            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(170)
                padding: (100,0,100,30)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos                
                
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(200)
                    height: dp(171)
                    padding: (16,0,16,0)
                    pos: self.parent.pos
                    
                    # Repeat
                    Button:
                        size_hint: (None,None)
                        height: dp(171)
                        width: dp(168)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.repeat()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/shapeCutter_app/img/button_repeat.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(200)
                    height: dp(171)
                    padding: (16,0,16,0)
                    pos: self.parent.pos
                    
                    # New
                    Button:
                        size_hint: (None,None)
                        height: dp(171)
                        width: dp(168)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.new_cut()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/shapeCutter_app/img/button_new.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(200)
                    height: dp(171)
                    padding: (16,0,16,0)
                    pos: self.parent.pos
                    
                    # Next
                    Button:
                        size_hint: (None,None)
                        height: dp(171)
                        width: dp(168)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.exit()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/shapeCutter_app/img/button_exit.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True  
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(80)
                padding: (740,0,0,20)
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos
""")

class ShapeCutterRepeatScreenClass(Screen):

    exiting = False 
    
    def __init__(self, **kwargs):
        super(ShapeCutterRepeatScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
    
    def repeat(self):
        self.sm.current = 'sC26'
        
    def new_cut(self):
        self.sm.current = 'sClanding'
        
    def exit(self):
        self.sm.current = 'sCexit'
