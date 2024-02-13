'''
Created on 4 March 2020
Feedback Screen for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty


Builder.load_string("""

<ShapeCutterFeedbackScreenClass>:
    
    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas:
            Rectangle: 
                pos: self.pos
                size: self.size
                source: "./asmcnc/apps/shapeCutter_app/img/landing_background.png"

        BoxLayout:
            padding:dp(0)
            spacing: 0
            orientation: "vertical"       
                
            Label:
                size_hint: (None,None)
                height: dp(90)
                width: dp(800)
                text: "Feedback"
                font_size:dp(30)
                halign: "center"
                valign: "bottom"
                markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(140)
                padding:dp(0)
                spacing: 0
                Label:
                    size_hint: (None,None)
                    height: dp(170)
                    width: dp(800)
                    halign: "center"
                    valign: "middle"
                    text: "Was your job successful?"
                    color: 0,0,0,1
                    font_size:dp(26)
                    markup: True

            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(170)
                padding:(dp(180),dp(0),dp(180),dp(30))
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos                
                
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(220)
                    height: dp(171)
                    padding:(dp(28),dp(0),dp(20),dp(0))
                    pos: self.parent.pos
                    
                    # thumbs up button
                    Button:
                        size_hint: (None,None)
                        height: dp(171)
                        width: dp(172)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.thumbs_up()
                        BoxLayout:
                            padding:dp(0)
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/thumbs_up.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout:
                    size_hint: (None,None)
                    width: dp(220)
                    height: dp(171)
                    padding:(dp(20),dp(0),dp(28),dp(0))
                    pos: self.parent.pos
                    
                    # thumbs down button
                    Button:
                        size_hint: (None,None)
                        height: dp(171)
                        width: dp(172)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.thumbs_down()
                        BoxLayout:
                            padding:dp(0)
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/thumbs_down.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True  
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(80)
                padding:(dp(740),dp(0),dp(0),dp(20))
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos
""")

class ShapeCutterFeedbackScreenClass(Screen):

    info_button = ObjectProperty()   
    
    def __init__(self, **kwargs):
        super(ShapeCutterFeedbackScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs['shapecutter']
        self.m=kwargs['machine']
      
    def thumbs_up(self):
        self.next_screen()
    
    def thumbs_down(self):
        self.next_screen()
            
    def next_screen(self):
        self.shapecutter_sm.next_screen()
