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

<SpindleSpinner@SpinnerOption>

    background_normal: ''
    background_color: [1,1,1,1]
    height: dp(40)
    color: 0,0,0,1
    halign: 'left'
    markup: 'True'

<SpindleSettingsWidget>

    GridLayout:
        cols: 2
        rows: 3
        size_hint: (None, None)
        height: dp(280)
        width: dp(580)
        cols_minimum: {0: dp(160), 1: dp(400)}
        rows_minimum: {0: dp(70), 1: dp(70), 2: dp(70)}
        spacing: [dp(20), dp(17.5)]

        # ROW 1

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(70) # 62 high image
            width: dp(160)
            padding: [dp(51), 4, dp(51), 4] # 15 padding

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
            width: dp(320)
            padding: [dp(0), dp(0), dp(20), 0]
            Spinner:
                id: spindle_brand
                halign: 'left'
                valign: 'top'
                markup: True
                size_hint: (None, None)
                size: 200, 24
                text: 'spinner'
                font_size: '20sp'
                text_size: self.size
                multiline: False
                color: 0,0,0,1
                # values: root.SSID_list
                option_cls: Factory.get("SpindleSpinner")
                background_normal: ''
                background_color: [1,1,1,0]

        # ROW 2

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(70)
            width: dp(160)
            padding: [dp(53), dp(3), dp(53), dp(3)]

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
            height: dp(70)
            width: dp(320)
            padding: [dp(0), 0, dp(20), 0]
	        TextInput:
	            id: brush_life
	            size_hint: (None, None)
	            height: dp(70)
	            width: dp(300)

        # ROW 3

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(70)
            width: dp(160)
            padding: [dp(48), dp(16), dp(48), dp(16)]

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
            width: dp(320)
            padding: [dp(0), 0, dp(20), dp(0)]
	        TextInput:
	            id: brush_life
	            size_hint: (None, None)
	            height: dp(70)
	            width: dp(300)




""")

class SpindleSettingsWidget(Widget):

    def __init__(self, **kwargs):
    
        super(SpindleSettingsWidget, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']