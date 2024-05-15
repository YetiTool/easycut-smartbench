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
        height: app.get_scaled_height(800)
        width: app.get_scaled_width(480)
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
                height: app.get_scaled_height(90)
                width: app.get_scaled_width(800)
                text: "Feedback"
                font_size: app.get_scaled_width(30)
                halign: "center"
                valign: "bottom"
                markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: app.get_scaled_width(800)
                height: app.get_scaled_height(140)
                padding: 0
                spacing: 0
                Label:
                    size_hint: (None,None)
                    height: app.get_scaled_height(170)
                    width: app.get_scaled_width(800)
                    halign: "center"
                    valign: "middle"
                    text: "Was your job successful?"
                    color: 0,0,0,1
                    font_size: app.get_scaled_width(26)
                    markup: True

            BoxLayout:
                size_hint: (None,None)
                width: app.get_scaled_width(800)
                height: app.get_scaled_height(170)
                padding: app.get_scaled_tuple([180, 0, 180, 30])
                spacing: 0
                orientation: 'horizontal'
                pos: self.parent.pos                
                
                BoxLayout:
                    size_hint: (None,None)
                    width: app.get_scaled_width(220)
                    height: app.get_scaled_height(171)
                    padding: app.get_scaled_tuple([28, 0, 20, 0])
                    pos: self.parent.pos
                    
                    # thumbs up button
                    Button:
                        size_hint: (None,None)
                        height: app.get_scaled_height(171)
                        width: app.get_scaled_width(172)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.thumbs_up()
                        BoxLayout:
                            padding: 0
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
                    width: app.get_scaled_width(220)
                    height: app.get_scaled_height(171)
                    padding: app.get_scaled_tuple([20, 0, 28, 0])
                    pos: self.parent.pos
                    
                    # thumbs down button
                    Button:
                        size_hint: (None,None)
                        height: app.get_scaled_height(171)
                        width: app.get_scaled_width(172)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.thumbs_down()
                        BoxLayout:
                            padding: 0
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
                width: app.get_scaled_width(800)
                height: app.get_scaled_height(80)
                padding: app.get_scaled_tuple([740, 0, 0, 20])
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
