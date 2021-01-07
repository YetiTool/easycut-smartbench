'''
Created January 2020
@author: Letty
widget to allow user to choose dust shoe safety settings
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from asmcnc.apps.maintenance_app import popup_maintenance
from asmcnc.skavaUI import popup_info

Builder.load_string("""

<DustShoeSafetyWidget>
    
    BoxLayout:
        size_hint: (None, None)
        height: dp(130)
        width: dp(230)
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
            text: "[b]DUST SHOE SAFETY[/b]"
            multiline: True

        BoxLayout: 
            orientation: 'horizontal'
            padding: [0,0,0,0]
            spacing: dp(20)
            size_hint: (None, None)
            height: dp(23)
            width: dp(190)

            BoxLayout: 
                size_hint: (None, None)
                pos: self.parent.pos
                height: dp(23)
                width: dp(85)
                Switch:
                    background_color: [0,0,0,0]
                    center_x: self.parent.center_x
                    y: self.parent.y
                    pos: self.parent.pos

            # Put the image here
            BoxLayout:
                size_hint: (None, None)
                # pos: self.parent.pos
                height: dp(82)
                width: dp(85)
                padding: [dp(21), 0, 0, 0]

                Image:
                    id: dust_shoe_image
                    source: "./asmcnc/apps/maintenance_app/img/dust_shoe_safety.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True



""")


class DustShoeSafetyWidget(Widget):

    def __init__(self, **kwargs):
    
        super(DustShoeSafetyWidget, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
