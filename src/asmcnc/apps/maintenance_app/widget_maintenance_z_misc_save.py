"""
Created on 19 August 2020
@author: Letty
widget to hold z lead & probe maintenance save and info
"""
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from asmcnc.apps.maintenance_app import popup_maintenance
from asmcnc.skavaUI import popup_info

Builder.load_string(
    """

<ZMiscSaveWidget>

    BoxLayout:
        pos: self.parent.pos
        size: self.parent.size
        orientation: 'vertical'

        BoxLayout:
            padding: [dp(50), dp(30)]
	        Button:
	            on_press: root.get_info()
	            background_color: [0,0,0,0]
	            BoxLayout:
                    size: self.parent.size
	                pos: self.parent.pos
	                Image:
	                    source: "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
	                    center_x: self.parent.center_x
	                    y: self.parent.y
	                    size: self.parent.width, self.parent.height
	                    allow_stretch: True

        BoxLayout:
            size_hint_y: 1.2
            padding: [dp(20), dp(10)]
            Button:
                on_press: root.save()
                background_color: [0,0,0,0]
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

"""
)


class ZMiscSaveWidget(Widget):
    def __init__(self, **kwargs):
        self.sm = kwargs.pop("screen_manager")
        self.m = kwargs.pop("machine")
        self.l = kwargs.pop("localization")
        super(ZMiscSaveWidget, self).__init__(**kwargs)

    def get_info(self):
        z_misc_settings_info = (
            self.l.get_bold("Touchplate offset")
            + "\n"
            + self.l.get_str(
                "Update the offset to make setting the Z datum even more precise."
            )
            + "\n"
            + self.l.get_str(
                "Make sure you press the save button to save your settings."
            )
            + "\n\n"
            + self.l.get_bold("Time since lead screw lubricated")
            + "\n"
            + self.l.get_str(
                "If you have just lubricated the Z head lead screw, reset the hours since it was last lubricated."
            )
            + "\n"
            + self.l.get_str(
                "This will reset the time until SmartBench gives you the next reminder."
            )
            + "\n"
            + self.l.get_str(
                "Make sure you press the save button to save your settings."
            )
        )
        popup_info.PopupInfo(self.sm, self.l, 750, z_misc_settings_info)

    def save(self):
        self.show_popup = True
        if self.save_touchplate_offset() and self.save_z_head_maintenance():
            saved_success = self.l.get_str("Settings saved!")
            popup_info.PopupMiniInfo(self.sm, self.l, saved_success)
        elif self.show_popup:
            warning_message = (
                self.l.get_str("There was a problem saving your settings.")
                + "\n\n"
                + self.l.get_str(
                    "Please check your settings and try again, or if the problem persists please contact the YetiTool support team."
                )
            )
            popup_info.PopupError(self.sm, self.l, warning_message)

    def save_touchplate_offset(self):
        try:
            touchplate_offset = float(
                self.sm.get_screen(
                    "maintenance"
                ).touchplate_offset_widget.touchplate_offset.text
            )
            if touchplate_offset < 1 or touchplate_offset > 2:
                warning_message = (
                    self.l.get_str(
                        "Your touchplate offset should be inbetween 1 and 2 mm."
                    )
                    + "\n\n"
                    + self.l.get_str(
                        "Please check your settings and try again, or if the problem persists please contact the YetiTool support team."
                    )
                )
                popup_info.PopupError(self.sm, self.l, warning_message)
                self.show_popup = False
                return False
            elif self.m.write_z_touch_plate_thickness(touchplate_offset):
                return True
            else:
                return False
        except:
            return False

    def save_z_head_maintenance(self):
        time_since_lubrication = self.sm.get_screen(
            "maintenance"
        ).z_lubrication_reminder_widget.time_in_hours
        if time_since_lubrication == 0:
            if self.m.write_z_head_maintenance_settings(time_since_lubrication):
                return True
            else:
                return False
        else:
            return True
