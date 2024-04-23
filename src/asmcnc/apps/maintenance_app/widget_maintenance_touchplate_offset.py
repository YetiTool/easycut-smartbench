"""
Created on 17 August 2020
@author: Letty
widget to allow user to change touchplate offset
"""
from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string("""
#:import LabelBase asmcnc.core_UI.components.labels.base_label

<TouchplateOffsetWidget>

    touchplate_offset:touchplate_offset

    touchplate_offset_label : touchplate_offset_label
    
    BoxLayout:
        size_hint: (None, None)
        height: dp(0.270833333333*app.height)
        width: dp(0.725*app.width)
        pos: self.parent.pos
        orientation: 'vertical'
        padding:[dp(0.01875)*app.width, dp(0.03125)*app.height]
        spacing:0.0208333333333*app.height

        LabelBase:
            id: touchplate_offset_label
            color: 0,0,0,1
            font_size: dp(0.03*app.width)
            markup: True
            halign: "left"
            valign: "middle"
            text_size: self.size
            text: "[b]TOUCHPLATE OFFSET[/b]"

        BoxLayout: 
            orientation: 'horizontal'
            padding:[0, dp(0.0104166666667)*app.height, 0, 0]
            spacing:0.0375*app.width
            size_hint: (None, None)
            height: dp(0.125*app.height)
            width: dp(0.725*app.width) 

            # Put the image here
            BoxLayout: 
                size_hint: (None, None)
                # pos: self.parent.pos
                height: dp(0.125*app.height)
                width: dp(0.18125*app.width)

                Image:
                    id: touchplate_image
                    source: "./asmcnc/apps/maintenance_app/img/touchplate_offset.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            # Text input
            TextInput:
                id: touchplate_offset
                size_hint: (None, None)
                height: dp(0.104166666667*app.height)
                width: dp(0.15*app.width)
                font_size: dp(0.035*app.width)
                input_filter: 'float'
                multiline: False

            LabelBase: 
                color: 0,0,0,1
                font_size: dp(0.035*app.width)
                markup: True
                halign: "left"
                valign: "middle"
                text_size: self.size
                text: "mm"


"""
)


class TouchplateOffsetWidget(Widget):
    def __init__(self, **kwargs):
        super(TouchplateOffsetWidget, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def update_strings(self):
        self.touchplate_offset_label.text = self.l.get_bold("TOUCHPLATE OFFSET")
