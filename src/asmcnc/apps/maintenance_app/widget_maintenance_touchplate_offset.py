'''
Created December 2020
@author: Letty
widget to allow user to change touchplate offset
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from asmcnc.apps.maintenance_app import popup_maintenance
from asmcnc.skavaUI import popup_info

Builder.load_string("""

<TouchplateOffsetWidget>

    touchplate_offset:touchplate_offset
    
    BoxLayout:
        size_hint: (None, None)
        height: dp(130)
        width: dp(310)
        pos: self.parent.pos
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(6)      

        Label: 
            color: 0,0,0,1
            font_size: dp(24)
            markup: True
            halign: "left"
            valign: "top"
            text_size: self.size
            text: "[b]TOUCHPLATE OFFSET[/b]"

        BoxLayout: 
            orientation: 'horizontal'
            padding: [0,0,0,0]
            spacing: 10
            size_hint: (None, None)
            height: dp(60)
            width: dp(290) 

            # Put the image here
            BoxLayout: 
                size_hint: (None, None)
                # pos: self.parent.pos
                height: dp(60)
                width: dp(145)

                Image:
                    id: touchplate_image
                    source: "./asmcnc/apps/maintenance_app/img/touchplate_offset.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            # Text input
            TextInput:
                id: touchplate_offset
                size_hint: (None, None)
                height: dp(50)
                width: dp(70)
                font_size: dp(28)
                input_filter: 'float'
                multiline: False

            Label: 
                color: 0,0,0,1
                font_size: dp(28)
                markup: True
                halign: "left"
                valign: "middle"
                text_size: self.size
                text: "mm"


""")


class TouchplateOffsetWidget(Widget):

    def __init__(self, **kwargs):
    
        super(TouchplateOffsetWidget, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
