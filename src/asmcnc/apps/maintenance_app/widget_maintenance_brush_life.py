'''
Created on 19 August 2020
@author: Letty
widget to hold brush life input and buttons
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from asmcnc.apps.maintenance_app import popup_maintenance
from asmcnc.skavaUI import popup_info

Builder.load_string("""

<BrushLifeWidget>
    
    restore_button:restore_button
    reset_120:reset_120
    brush_life:brush_life
    
    BoxLayout:
        size_hint: (None, None)
        height: dp(250)
        width: dp(280)
        pos: self.parent.pos
        orientation: 'vertical'
        padding: [13.3,10,13.3,10]
        spacing: 10

        BoxLayout: 
            orientation: 'vertical'
            spacing: dp(5)
            padding: [dp(0), 10, 0, 0]
            size_hint: (None, None)
            height: dp(100)
            width: dp(280)         

            Label: 
                color: 0,0,0,1
                font_size: dp(24)
                markup: True
                halign: "left"
                valign: "middle"
                text_size: self.size
                text: "[b]BRUSH LIFE[/b]"

            BoxLayout: 
                orientation: 'horizontal'
                padding: [0,dp(5),0,0]
                spacing: 10
                size_hint: (None, None)
                height: dp(53)
                width: dp(280) 

                # Text input
                TextInput:
                    id: brush_life
                    size_hint: (None, None)
                    height: dp(50)
                    width: dp(120)
                    font_size: dp(28)
                    input_filter: 'int'

                Label: 
                    color: 0,0,0,1
                    font_size: dp(28)
                    markup: True
                    halign: "left"
                    valign: "middle"
                    text_size: self.size
                    text: "hrs"

        GridLayout:
            cols: 2
            rows: 1
            spacing: 13.3
            size_hint: (None, None)
            height: dp(120)
            width: dp(253.3)

            BoxLayout: 
                size: self.parent.size
                pos: self.parent.pos
                ToggleButton:
                    id: restore_button
                    on_press: root.restore()
                    size_hint: (None,None)
                    height: dp(120)
                    width: dp(120)
                    background_color: [0,0,0,0]
                    center: self.parent.center
                    pos: self.parent.pos
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: restore_image
                            source: "./asmcnc/apps/maintenance_app/img/restore.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True  

            BoxLayout: 
                size: self.parent.size
                pos: self.parent.pos
                ToggleButton:
                    id: reset_120
                    on_press: root.reset_to_120()
                    size_hint: (None,None)
                    height: dp(120)
                    width: dp(120)
                    background_color: [0,0,0,0]
                    center: self.parent.center
                    pos: self.parent.pos
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos      
                        Image:
                            id: reset_0_image
                            source: "./asmcnc/apps/maintenance_app/img/reset_120.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True 


""")


class BrushLifeWidget(Widget):

    def __init__(self, **kwargs):
    
        super(BrushLifeWidget, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def restore(self):
        self.brush_life.text = int(self.m.spindle_brush_lifetime_seconds/3600)

    def reset_to_120(self):
        self.brush_life.text = 120










