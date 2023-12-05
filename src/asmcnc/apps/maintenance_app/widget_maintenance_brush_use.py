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
                padding:[0, dp(0.0104166666667)*app.height, 0, 0]
                spacing:0.0125*app.width
                size_hint: (None, None)
                height: dp(0.110416666667*app.height)
                width: dp(0.35*app.width) 

                # Text input
                TextInput:
                    id: brush_use
                    size_hint: (None, None)
                    height: dp(0.104166666667*app.height)
                    width: dp(0.15*app.width)
                    font_size: dp(0.035*app.width)
                    input_filter: 'int'
                    multiline: False

                Label:
                    id: hours_label
                    color: 0,0,0,1
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
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: reset_0
                    on_press: root.reset_to_0()
                    size_hint: (None,None)
                    height: dp(0.25*app.height)
                    width: dp(0.15*app.width)
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
    default_font_size = 24

    def __init__(self, **kwargs):
        super(BrushUseWidget, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.update_strings()

    def restore(self):
        self.brush_use.text = str(int(self.m.spindle_brush_use_seconds / 3600))

    def reset_to_0(self):
        self.brush_use.text = '0'

    def update_strings(self):
        self.brush_use_label.text = self.l.get_bold('BRUSH USE')
        self.hours_label.text = self.l.get_str('hours')
        self.update_font_size(self.brush_use_label)

    def update_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length <= 20:
            value.font_size = self.default_font_size
        if text_length > 20:
            value.font_size = self.default_font_size - 3
        if text_length > 23:
            value.font_size = self.default_font_size - 6
        if text_length > 28:
            value.font_size = self.default_font_size - 7
