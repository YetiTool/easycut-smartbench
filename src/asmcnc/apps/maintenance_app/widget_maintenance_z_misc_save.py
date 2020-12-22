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
            padding: [15,21.5,13,21.5]
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

    def get_info(self): # Rewrite me!

        z_misc_settings_info = (
        "[b]Touchplate offset[/b]\n" + \
        "Update the offset here to make setting the Z datum even more precise.\n" + \
        "Make sure you press the save button to save your settings.\n\n" + \

        "[b]Time since lead screw lubricated[/b]\n" + \
        "If you have just lubricated the Z head lead screw, reset the hours since it was last lubricated here.\n" + \
        "This will reset the time until SmartBench gives you the next reminder.\n" + \
        "Make sure you press the save button to save your settings."
        )


        popup_info.PopupInfo(self.sm, 750, z_misc_settings_info)


    def save(self):

        if self.save_touchplate_offset() and self.save_z_head_maintenance():
            popup_info.PopupMiniInfo(self.sm,"Settings saved!")
        
        else:
            warning_message = "There was a problem saving your settings.\n\nPlease check your settings and try again, or if the probem persists" + \
            " please contact the YetiTool support team."
            popup_info.PopupError(self.sm, warning_message)

    def save_touchplate_offset(self):
        # Set offset
        try: 
            touchplate_offset = float(self.sm.get_screen('maintenance').touchplate_offset_widget.touchplate_offset.text)
            if (touchplate_offset < 1) or (touchplate_offset > 2):
                warning_message = "Your touchplate offset should be inbetween 1 and 2 mm.\n\nPlease check your settings and try again, or if the probem persists" + \
                " please contact the YetiTool support team."
                popup_info.PopupError(self.sm, warning_message)
                return False
            else:
                if self.m.write_z_touch_plate_thickness(touchplate_offset): return True
                else: return False

        except: 
            return False


    def save_z_head_maintenance(self):
        # Reset lubrication time
        time_since_lubrication = self.sm.get_screen('maintenance').z_lubrication_reminder_widget.time_in_hours

        if time_since_lubrication == 0:
            
            if self.m.write_z_head_maintenance_settings(time_since_lubrication):
                return True

            else:
                return False
        else: 
            return True
