'''
Created on 19 August 2020
@author: Letty
widget to spindle settings
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from asmcnc.apps.maintenance_app import popup_maintenance
from asmcnc.skavaUI import popup_info

Builder.load_string("""

<SpindleSettingsWidget>

    GridLayout:
        cols: 2
        rows: 3
        size_hint: (None, None)
        height: dp(240)
        width: dp(580)
        cols_minimum: {0: dp(160), 1: dp(470)}
        spacing: dp(10)

        # ROW 1

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(70)
            width: dp(160)
            padding: [dp(51), 8, dp(51), 0]

            Image:
                id: spindle_image
                source: "./asmcnc/apps/maintenance_app/img/spindle_small.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(70)
            width: dp(300)
            padding: [dp(0), 10, dp(20), 0]
	        TextInput:
	            id: brush_life
	            size_hint: (None, None)
	            height: dp(60)
	            width: dp(300)

        # ROW 2

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(64)
            width: dp(160)
            padding: [dp(48.5), 0, dp(48.5), 0]

            Image:
                id: countdown_image
                source: "./asmcnc/apps/maintenance_app/img/countdown_small.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(60)
            width: dp(300)
            padding: [dp(0), 0, dp(20), 0]
	        TextInput:
	            id: brush_life
	            size_hint: (None, None)
	            height: dp(60)
	            width: dp(300)

        # ROW 3

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(70)
            width: dp(160)
            padding: [dp(48), dp(11), dp(48), dp(21)]

            Image:
                id: spindle_image
                source: "./asmcnc/apps/maintenance_app/img/speed_dial.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(70)
            width: dp(300)
            padding: [dp(0), 0, dp(20), 10]
	        TextInput:
	            id: brush_life
	            size_hint: (None, None)
	            height: dp(60)
	            width: dp(300)




""")

class SpindleSettingsWidget(Widget):

    def __init__(self, **kwargs):
    
        super(SpindleSettingsWidget, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']