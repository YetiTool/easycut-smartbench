'''
Created on 5 March 2020
Job Cancelled Screen for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty


Builder.load_string("""

<ShapeCutterCancelledScreenClass>:
    
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
                text: "Job Cancelled"
                font_size: 30
                halign: "center"
                valign: "bottom"
                markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(390)
                padding: 0,110,0,110
                spacing: 0
                Label:
                    size_hint: (None,None)
                    height: dp(170)
                    width: dp(800)
                    halign: "center"
                    valign: "middle"
                    text: "Bye!"
                    color: 0,0,0,1
                    font_size: 26
                    markup: True

#             BoxLayout:
#                 size_hint: (None,None)
#                 width: dp(800)
#                 height: dp(170)
#                 padding: (180,0,180,30)
#                 spacing: 0
#                 orientation: 'horizontal'
#                 pos: self.parent.pos                
#                 
#                 BoxLayout:
#                     size_hint: (None,None)
#                     width: dp(220)
#                     height: dp(171)
#                     padding: (28,0,20,0)
#                     pos: self.parent.pos
#                     
#                     # thumbs up button
#                     Button:
#                         size_hint: (None,None)
#                         height: dp(171)
#                         width: dp(172)
#                         background_color: hex('#F4433600')
#                         center: self.parent.center
#                         pos: self.parent.pos
#                         on_press: root.thumbs_up()
#                         BoxLayout:
#                             padding: 0
#                             size: self.parent.size
#                             pos: self.parent.pos
#                             Image:
#                                 source: "./asmcnc/shapeCutter_app/img/thumbs_up.png"
#                                 center_x: self.parent.center_x
#                                 y: self.parent.y
#                                 size: self.parent.width, self.parent.height
#                                 allow_stretch: True
#                 BoxLayout:
#                     size_hint: (None,None)
#                     width: dp(220)
#                     height: dp(171)
#                     padding: (20,0,28,0)
#                     pos: self.parent.pos
#                     
#                     # thumbs down button
#                     Button:
#                         size_hint: (None,None)
#                         height: dp(171)
#                         width: dp(172)
#                         background_color: hex('#F4433600')
#                         center: self.parent.center
#                         pos: self.parent.pos
#                         on_press: root.thumbs_down()
#                         BoxLayout:
#                             padding: 0
#                             size: self.parent.size
#                             pos: self.parent.pos
#                             Image:
#                                 source: "./asmcnc/shapeCutter_app/img/thumbs_down.png"
#                                 center_x: self.parent.center_x
#                                 y: self.parent.y
#                                 size: self.parent.width, self.parent.height
#                                 allow_stretch: True  
#             BoxLayout:
#                 size_hint: (None,None)
#                 width: dp(800)
#                 height: dp(80)
#                 padding: (740,0,0,20)
#                 spacing: 0
#                 orientation: 'horizontal'
#                 pos: self.parent.pos
""")

class ShapeCutterCancelledScreenClass(Screen):

    info_button = ObjectProperty()   
    
    def __init__(self, **kwargs):
        super(ShapeCutterCancelledScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
           
    def next_screen(self):
        self.sm.current = 'lobby'

