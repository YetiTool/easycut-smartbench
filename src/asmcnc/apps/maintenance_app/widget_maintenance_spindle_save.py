'''
Created on 19 August 2020
@author: Letty
widget to hold brush maintenance save and info
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from asmcnc.apps.maintenance_app import popup_maintenance
from asmcnc.skavaUI import popup_info

Builder.load_string("""

<SpindleSaveWidget>

    BoxLayout:
        size_hint: (None, None)
        height: dp(280)
        width: dp(160)
        pos: self.parent.pos
        orientation: 'vertical'

        BoxLayout: 
	        size_hint: (None, None)
	        height: dp(140)
	        width: dp(160)
            padding: [22,20,18,0]
            ToggleButton:
                id: save_button
                on_press: root.save()
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
                        id: save_image
                        source: "./asmcnc/apps/maintenance_app/img/save_button_132.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

        BoxLayout: 
	        size_hint: (None, None)
	        height: dp(140)
	        width: dp(160)
            padding: [50,0,50,40]
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

class SpindleSaveWidget(Widget):

    def __init__(self, **kwargs):
    
        super(SpindleSaveWidget, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def get_info(self):
        popup_info.PopupInfo(self.sm, 500, 'stuff')

    def save(self):

        [brand, digital, voltage] = (self.sm.get_screen('maintenance').spindle_settings_widget.spindle_brand.text).split()
        time = float(self.sm.get_screen('maintenance').spindle_settings_widget.spindle_cooldown_time.text)
        speed = float(self.sm.get_screen('maintenance').spindle_settings_widget.spindle_cooldown_speed.text)

        voltage = voltage.strip('V')

        print brand

        if digital == 'digital': digital = True
        elif digital =='manual': digital = False
        else:
            popup_info.PopupError(self.sm, 'screaming brand')
            return            

        if (time >= 10 or time <= 60): pass
        else:             
            popup_info.PopupError(self.sm, 'screaming time')
            return

        if (speed >= 10000 or speed <= 20000): pass
        else:             
            popup_info.PopupError(self.sm, 'screaming speed')
            return


        self.m.write_spindle_cooldown_settings(brand, voltage, digital, time, speed)

        # brands = ['YETI digital 230V', 'YETI digital 110V', 'YETI manual 230V', 'YETI manual 110V', 'AMB digital 230V', 'AMB manual 230V', 'AMB manual 110V']


    # spindle_brand = 'YETI' # String to hold brand name
    # spindle_voltage = 230 # Options are 230V or 110V
    # spindle_digital = False #spindle can be manual or digital
    # spindle_cooldown_time_seconds = 10 # YETI value is 10 seconds
    # spindle_cooldown_rpm = 20000 # YETI value is 20k 


# Mafell (YETI) - digital or manual; each one of those 110 or 230V - 4 variants total.

# AMB - 110V or 230V manual, 230V digital


















