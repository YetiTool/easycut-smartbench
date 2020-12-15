'''
Created on 19 August 2020
@author: Letty
widget to hold z lead & probe maintenance save and info
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from asmcnc.apps.maintenance_app import popup_maintenance
from asmcnc.skavaUI import popup_info

Builder.load_string("""

<ZMiscSaveWidget>

    BoxLayout:
        size_hint: (None, None)
        height: dp(350)
        width: dp(160)
        pos: self.parent.pos
        orientation: 'vertical'

        BoxLayout: 
	        size_hint: (None, None)
	        height: dp(175)
	        width: dp(160)
            padding: [26,21.5,12,21.5]
            ToggleButton:
                id: save_button
                on_press: root.save()
                size_hint: (None,None)
                height: dp(132)
                width: dp(132)
                background_color: [0,0,0,0]
                center: self.parent.center
                pos: self.parent.pos
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: save_image
                        source: "./asmcnc/apps/maintenance_app/img/save_button_132.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

        BoxLayout: 
	        size_hint: (None, None)
	        height: dp(175)
	        width: dp(160)
            padding: [50,0,50,57.5]
	        Button:
	            background_color: hex('#F4433600')
	            on_press: root.get_info()
	            BoxLayout:
	                size_hint: (None,None)
	                height: dp(60)
	                width: dp(60)
	                pos: self.parent.pos
	                Image:
	                    source: "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
	                    center_x: self.parent.center_x
	                    y: self.parent.y
	                    size: self.parent.width, self.parent.height
	                    allow_stretch: True

""")

class ZMiscSaveWidget(Widget):

    def __init__(self, **kwargs):
    
        super(ZMiscSaveWidget, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def get_info(self):

        spindle_settings_info = "[b]Spindle cooldown[/b]\nThe spindle needs to cool down after a job to prevent it from overheating, and to extend its lifetime. " + \
        "We recommend the following cooldown settings:\n\n" + \
        "       Yeti: 20,000 RPM; 10 seconds\n" + \
        "       AMB: 10,000 RPM; 30 seconds\n\n" + \
        "[b]Spindle brand[/b]\n" + \
        "SmartBench will operate slightly differently depending on the type of spindle you are using. " + \
        "It is important that you choose the option that matches the voltage and digital/manual specifications of your spindle."

        popup_info.PopupInfo(self.sm, 750, spindle_settings_info)

    def save(self):
        pass