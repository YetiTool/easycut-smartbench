"""
Created on 19 August 2020
@author: Letty
widget to hold brush maintenance save and info
"""

from kivy.lang import Builder
from kivy.uix.widget import Widget
from asmcnc.core_UI.custom_popups import PopupBrushInfo

Builder.load_string(
    """

<BrushSaveWidget>

    BoxLayout:
        pos: self.parent.pos
        size: self.parent.size
        orientation: 'vertical'

        BoxLayout:
            padding:[dp(0.0625)*app.width, dp(0.0625)*app.height]
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
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
            padding:[dp(0.025)*app.width, dp(0.0208333333333)*app.height]
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
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
        PopupBrushInfo(self.sm, self.l)

    def save(self):
        use_str = self.sm.get_screen("maintenance").brush_use_widget.brush_use.text
        lifetime_str = self.sm.get_screen(
            "maintenance"
        ).brush_life_widget.brush_life.text
        try:
            use = float(use_str) * 3600
            lifetime = float(lifetime_str) * 3600
            if 0 <= use <= 999 * 3600:
                pass
            else:
                main_string = (
                    self.l.get_str(
                        "The number of hours the brushes have been used for should be between 0 and 999."
                    )
                    + "\n\n"
                    + self.l.get_str("Please enter a new value.")
                )
                self.sm.pm.show_error_popup(main_string)
                return
            if 100 * 3600 <= lifetime <= 999 * 3600:
                pass
            else:
                main_string = (
                    self.l.get_str(
                        "The maximum brush lifetime should be between 100 and 999 hours."
                    )
                    + "\n\n"
                    + self.l.get_str("Please enter a new value.")
                )
                self.sm.pm.show_error_popup(main_string)
                return
            if use <= lifetime:
                pass
            else:
                main_string = (
                    self.l.get_str(
                        "The brush use hours should be less than or equal to the lifetime!"
                    )
                    + "\n\n"
                    + self.l.get_str("Please check your values.")
                )
                self.sm.pm.show_error_popup(main_string)
                return
            if self.m.write_spindle_brush_values(use, lifetime):
                saved_success = self.l.get_str("Settings saved!")
                self.sm.pm.show_mini_info_popup(saved_success)
            else:
                main_string = (
                    self.l.get_str("There was a problem saving your settings.")
                    + "\n\n"
                    + self.l.get_str(
                        "Please check your settings and try again, or if the problem persists please contact the YetiTool support team."
                    )
                )
                self.sm.pm.show_error_popup(main_string)
            value = 1 - float(
                self.m.spindle_brush_use_seconds / self.m.spindle_brush_lifetime_seconds
            )
            self.sm.get_screen("maintenance").brush_monitor_widget.set_percentage(value)
        except:
            main_string = (
                self.l.get_str("There was a problem saving your settings.")
                + "\n\n"
                + self.l.get_str(
                    "Please check your settings and try again, or if the problem persists please contact the YetiTool support team."
                )
            )
            self.sm.pm.show_error_popup(main_string)
            return
