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
        height: app.get_scaled_height(250.0)
        width: app.get_scaled_width(280.0)
        pos: self.parent.pos
        orientation: 'vertical'
        padding: app.get_scaled_tuple([13.3, 10.0, 13.3, 10.0])
        spacing: app.get_scaled_width(10.0)

        BoxLayout: 
            orientation: 'vertical'
            spacing: app.get_scaled_width(5.0)
            size_hint: (None, None)
            height: app.get_scaled_height(100.0)
            width: app.get_scaled_width(280.0)

            LabelBase:
                id: brush_reminder_label
                color: 0,0,0,1
                font_size: root.default_font_size
                markup: True
                halign: "left"
                valign: "middle"
                text_size: self.size
                text: "[b]BRUSH REMINDER[/b]"

            BoxLayout: 
                orientation: 'horizontal'
                padding: app.get_scaled_tuple([0.0, 5.0, 0.0, 0.0])
                spacing: app.get_scaled_width(10.0)
                size_hint: (None, None)
                height: app.get_scaled_height(53.0)
                width: app.get_scaled_width(280.0)

                # Text input
                TextInput:
                    id: brush_life
                    size_hint: (None, None)
                    height: app.get_scaled_height(50.0)
                    width: app.get_scaled_width(120.0)
                    font_size: app.get_scaled_width(28.0)
                    input_filter: 'int'
                    multiline: False

                LabelBase: 
                    id: hours_label
                    color: 0,0,0,1
                    font_size: app.get_scaled_width(28.0)
                    markup: True
                    halign: "left"
                    valign: "middle"
                    text_size: self.size
                    text: "hrs"

        GridLayout:
            cols: 2
            rows: 1
            spacing: app.get_scaled_width(13.3)
            size_hint: (None, None)
            height: app.get_scaled_height(120.0)
            width: app.get_scaled_width(253.3)

            BoxLayout: 
                size: self.parent.size
                pos: self.parent.pos
                ToggleButton:
                    font_size: app.get_scaled_sp('15.0sp')
                    id: restore_button
                    on_press: root.restore()
                    size_hint: (None,None)
                    height: app.get_scaled_height(120.0)
                    width: app.get_scaled_width(120.0)
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
                    font_size: app.get_scaled_sp('15.0sp')
                    id: reset_120
                    on_press: root.reset_to_120()
                    size_hint: (None,None)
                    height: app.get_scaled_height(120.0)
                    width: app.get_scaled_width(120.0)
                    background_color: [0,0,0,0]
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
