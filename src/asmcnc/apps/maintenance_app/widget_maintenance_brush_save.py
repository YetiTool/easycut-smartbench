"""
Created on 19 August 2020
@author: Letty
widget to hold brush maintenance save and info
"""
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from asmcnc.apps.maintenance_app import popup_maintenance
from asmcnc.skavaUI import popup_info

Builder.load_string(
    """

<BrushSaveWidget>

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


class BrushSaveWidget(Widget):
    def __init__(self, **kwargs):
        self.sm = kwargs.pop("screen_manager")
        self.m = kwargs.pop("machine")
        self.l = kwargs.pop("localization")
        super(BrushSaveWidget, self).__init__(**kwargs)

    def get_info(self):
        popup_maintenance.PopupBrushInfo(self.sm, self.l)

    def save(self):
        use_str = self.sm.get_screen("maintenance").brush_use_widget.brush_use.text
        lifetime_str = self.sm.get_screen(
            "maintenance"
        ).brush_life_widget.brush_life.text
        try:
            use = float(use_str) * 3600
            lifetime = float(lifetime_str) * 3600
            if use >= 0 and use <= 999 * 3600:
                pass
            else:
                brush_use_validation_error = (
                    self.l.get_str(
                        "The number of hours the brushes have been used for should be between 0 and 999."
                    )
                    + "\n\n"
                    + self.l.get_str("Please enter a new value.")
                )
                popup_info.PopupError(self.sm, self.l, brush_use_validation_error)
                return
            if lifetime >= 100 * 3600 and lifetime <= 999 * 3600:
                pass
            else:
                brush_life_validation_error = (
                    self.l.get_str(
                        "The maximum brush lifetime should be between 100 and 999 hours."
                    )
                    + "\n\n"
                    + self.l.get_str("Please enter a new value.")
                )
                popup_info.PopupError(self.sm, self.l, brush_life_validation_error)
                return
            if use <= lifetime:
                pass
            else:
                brush_both_validation_error = (
                    self.l.get_str(
                        "The brush use hours should be less than or equal to the lifetime!"
                    )
                    + "\n\n"
                    + self.l.get_str("Please check your values.")
                )
                popup_info.PopupError(self.sm, self.l, brush_both_validation_error)
                return
            if self.m.write_spindle_brush_values(use, lifetime):
                saved_success = self.l.get_str("Settings saved!")
                popup_info.PopupMiniInfo(self.sm, self.l, saved_success)
            else:
                warning_message = (
                    self.l.get_str("There was a problem saving your settings.")
                    + "\n\n"
                    + self.l.get_str(
                        "Please check your settings and try again, or if the problem persists please contact the YetiTool support team."
                    )
                )
                popup_info.PopupError(self.sm, self.l, warning_message)
            value = 1 - float(
                self.m.spindle_brush_use_seconds / self.m.spindle_brush_lifetime_seconds
            )
            self.sm.get_screen("maintenance").brush_monitor_widget.set_percentage(value)
        except:
            warning_message = (
                self.l.get_str("There was a problem saving your settings.")
                + "\n\n"
                + self.l.get_str(
                    "Please check your settings and try again, or if the problem persists please contact the YetiTool support team."
                )
            )
            popup_info.PopupError(self.sm, self.l, warning_message)
            return
