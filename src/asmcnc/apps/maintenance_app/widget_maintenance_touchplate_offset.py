"""
Created on 17 August 2020
@author: Letty
widget to allow user to change touchplate offset
"""
from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string(
    """

<TouchplateOffsetWidget>

    touchplate_offset:touchplate_offset

    touchplate_offset_label : touchplate_offset_label
    
    BoxLayout:
        size_hint: (None, None)
        height: dp(app.get_scaled_height(130))
        width: dp(app.get_scaled_width(580))
        pos: self.parent.pos
        orientation: 'vertical'
        padding:(dp(app.get_scaled_width(15)),dp(app.get_scaled_height(15)))
        spacing:0.0208333333333*app.height

        Label:
            id: touchplate_offset_label
            color: 0,0,0,1
            font_size: dp(app.get_scaled_width(24))
            markup: True
            halign: "left"
            valign: "middle"
            text_size: self.size
            text: "[b]TOUCHPLATE OFFSET[/b]"

        BoxLayout: 
            orientation: 'horizontal'
            padding:(dp(0),dp(app.get_scaled_height(5)),dp(0),dp(0))
            spacing:0.0375*app.width
            size_hint: (None, None)
            height: dp(app.get_scaled_height(60))
            width: dp(app.get_scaled_width(580)) 

            # Put the image here
            BoxLayout: 
                size_hint: (None, None)
                # pos: self.parent.pos
                height: dp(app.get_scaled_height(60))
                width: dp(app.get_scaled_width(145))

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
                height: dp(app.get_scaled_height(50))
                width: dp(app.get_scaled_width(120))
                font_size: dp(app.get_scaled_width(28))
                input_filter: 'float'
                multiline: False

            Label: 
                color: 0,0,0,1
                font_size: dp(app.get_scaled_width(28))
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
