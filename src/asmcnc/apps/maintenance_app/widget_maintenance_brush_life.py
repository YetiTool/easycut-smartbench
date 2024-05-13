from kivy.core.window import Window

from asmcnc.core_UI import scaling_utils

"""
Created on 19 August 2020
@author: Letty
widget to hold brush life input and buttons
"""
from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string("""
#:import LabelBase asmcnc.core_UI.components.labels.base_label

<BrushLifeWidget>
    
    restore_button:restore_button
    reset_120:reset_120
    brush_life:brush_life

    brush_reminder_label : brush_reminder_label
    hours_label : hours_label
    
    BoxLayout:
        size_hint: (None, None)
        height: dp(0.520833333333*app.height)
        width: dp(0.35*app.width)
        pos: self.parent.pos
        orientation: 'vertical'
        padding:[dp(0.016625)*app.width, dp(0.0208333333333)*app.height, dp(0.016625)*app.width, dp(0.0208333333333)*app.height]
        spacing:0.0208333333333*app.height

        BoxLayout: 
            orientation: 'vertical'
            spacing:dp(0.0104166666667)*app.height
            size_hint: (None, None)
            height: dp(0.208333333333*app.height)
            width: dp(0.35*app.width)         

            LabelBase:
                id: brush_reminder_label
                color: color_provider.get_rgba("black")
                font_size: root.default_font_size
                markup: True
                halign: "left"
                valign: "middle"
                text_size: self.size
                text: "[b]BRUSH REMINDER[/b]"

            BoxLayout: 
                orientation: 'horizontal'
                padding:[0, dp(0.0104166666667)*app.height, 0, 0]
                spacing:0.0125*app.width
                size_hint: (None, None)
                height: dp(0.110416666667*app.height)
                width: dp(0.35*app.width) 

                # Text input
                TextInput:
                    id: brush_life
                    size_hint: (None, None)
                    height: dp(0.104166666667*app.height)
                    width: dp(0.15*app.width)
                    font_size: dp(0.035*app.width)
                    input_filter: 'int'
                    multiline: False

                LabelBase: 
                    id: hours_label
                    color: color_provider.get_rgba("black")
                    font_size: dp(0.035*app.width)
                    markup: True
                    halign: "left"
                    valign: "middle"
                    text_size: self.size
                    text: "hrs"

        GridLayout:
            cols: 2
            rows: 1
            spacing:0.016625*app.width
            size_hint: (None, None)
            height: dp(0.25*app.height)
            width: dp(0.316625*app.width)

            BoxLayout: 
                size: self.parent.size
                pos: self.parent.pos
                ToggleButton:
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: restore_button
                    on_press: root.restore()
                    size_hint: (None,None)
                    height: dp(0.25*app.height)
                    width: dp(0.15*app.width)
                    background_color: color_provider.get_rgba("transparent")
                    center: self.parent.center
                    pos: self.parent.pos
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: restore_image
                            source: "./asmcnc/apps/maintenance_app/img/restore.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True  

            BoxLayout: 
                size: self.parent.size
                pos: self.parent.pos
                ToggleButton:
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: reset_120
                    on_press: root.reset_to_120()
                    size_hint: (None,None)
                    height: dp(0.25*app.height)
                    width: dp(0.15*app.width)
                    background_color: color_provider.get_rgba("transparent")
                    center: self.parent.center
                    pos: self.parent.pos
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos      
                        Image:
                            id: reset_0_image
                            source: "./asmcnc/apps/maintenance_app/img/reset_120.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True 


"""
)


class BrushLifeWidget(Widget):
    default_font_size = scaling_utils.get_scaled_width(24)

    def __init__(self, **kwargs):
        super(BrushLifeWidget, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def restore(self):
        self.brush_life.text = str(int(self.m.spindle_brush_lifetime_seconds / 3600))

    def reset_to_120(self):
        self.brush_life.text = "120"

    def update_strings(self):
        self.brush_reminder_label.text = self.l.get_bold("BRUSH REMINDER")
        self.hours_label.text = self.l.get_str("hours")
        self.update_font_size(self.brush_reminder_label)

    def update_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length <= 18:
            value.font_size = self.default_font_size
        if text_length > 18:
            value.font_size = self.default_font_size - 0.00375 * Window.width
        if text_length > 23:
            value.font_size = self.default_font_size - 0.0075 * Window.width
        if text_length > 28:
            value.font_size = self.default_font_size - 0.00875 * Window.width
