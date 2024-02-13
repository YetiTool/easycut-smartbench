from kivy.core.window import Window

from asmcnc.core_UI import scaling_utils

"""
Created on 17 August 2020
@author: Letty
widget to hold brush use input and buttons
"""
from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string(
    """

<BrushUseWidget>
    
    restore_button:restore_button
    reset_0:reset_0
    brush_use:brush_use

    brush_use_label : brush_use_label
    hours_label : hours_label
    
    BoxLayout:
        size_hint: (None, None)
        height: dp(app.get_scaled_height(250))
        width: dp(app.get_scaled_width(280))
        pos: self.parent.pos
        orientation: 'vertical'
        padding:(dp(app.get_scaled_width(13.3)),dp(app.get_scaled_height(10)),dp(app.get_scaled_width(13.3)),dp(app.get_scaled_height(10)))
        spacing:0.0208333333333*app.height

        BoxLayout: 
            orientation: 'vertical'
            spacing:app.get_scaled_height(5)
            size_hint: (None, None)
            height: dp(app.get_scaled_height(100))
            width: dp(app.get_scaled_width(280))         

            Label:
                id: brush_use_label
                color: 0,0,0,1
                font_size: root.default_font_size
                markup: True
                halign: "left"
                valign: "middle"
                text_size: self.size
                text: "[b]BRUSH USE[/b]"

            BoxLayout: 
                orientation: 'horizontal'
                padding:(dp(0),dp(app.get_scaled_height(5)),dp(0),dp(0))
                spacing:0.0125*app.width
                size_hint: (None, None)
                height: dp(app.get_scaled_height(53))
                width: dp(app.get_scaled_width(280)) 

                # Text input
                TextInput:
                    id: brush_use
                    size_hint: (None, None)
                    height: dp(app.get_scaled_height(50))
                    width: dp(app.get_scaled_width(120))
                    font_size: dp(app.get_scaled_width(28))
                    input_filter: 'int'
                    multiline: False

                Label:
                    id: hours_label
                    color: 0,0,0,1
                    font_size: dp(app.get_scaled_width(28))
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
            height: dp(app.get_scaled_height(120))
            width: dp(app.get_scaled_width(253.3))

            BoxLayout: 
                size: self.parent.size
                pos: self.parent.pos
                ToggleButton:
                    font_size: str(get_scaled_width(15)) + 'sp'
                    id: restore_button
                    on_press: root.restore()
                    size_hint: (None,None)
                    height: dp(app.get_scaled_height(120))
                    width: dp(app.get_scaled_width(120))
                    background_color: [0,0,0,0]
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
                    font_size: str(get_scaled_width(15)) + 'sp'
                    id: reset_0
                    on_press: root.reset_to_0()
                    size_hint: (None,None)
                    height: dp(app.get_scaled_height(120))
                    width: dp(app.get_scaled_width(120))
                    background_color: [0,0,0,0]
                    center: self.parent.center
                    pos: self.parent.pos
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos      
                        Image:
                            id: reset_0_image
                            source: "./asmcnc/apps/maintenance_app/img/reset_0.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True 


"""
)


class BrushUseWidget(Widget):
    default_font_size = scaling_utils.get_scaled_width(24)

    def __init__(self, **kwargs):
        super(BrushUseWidget, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def restore(self):
        self.brush_use.text = str(int(self.m.spindle_brush_use_seconds / 3600))

    def reset_to_0(self):
        self.brush_use.text = "0"

    def update_strings(self):
        self.brush_use_label.text = self.l.get_bold("BRUSH USE")
        self.hours_label.text = self.l.get_str("hours")
        self.update_font_size(self.brush_use_label)

    def update_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length <= 20:
            value.font_size = self.default_font_size
        if text_length > 20:
            value.font_size = self.default_font_size - 0.00375 * Window.width
        if text_length > 23:
            value.font_size = self.default_font_size - 0.0075 * Window.width
        if text_length > 28:
            value.font_size = self.default_font_size - 0.00875 * Window.width
