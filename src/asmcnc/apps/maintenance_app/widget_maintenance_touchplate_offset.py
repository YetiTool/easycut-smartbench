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
        height: app.get_scaled_height(130.0)
        width: app.get_scaled_width(580.0)
        pos: self.parent.pos
        orientation: 'vertical'
        padding: app.get_scaled_tuple([15.0, 15.0])
        spacing: app.get_scaled_width(9.99999999998)

        LabelBase:
            id: touchplate_offset_label
            color: 0,0,0,1
            font_size: app.get_scaled_width(24.0)
            markup: True
            halign: "left"
            valign: "middle"
            text_size: self.size
            text: "[b]TOUCHPLATE OFFSET[/b]"

        BoxLayout: 
            orientation: 'horizontal'
            padding: app.get_scaled_tuple([0.0, 5.0, 0.0, 0.0])
            spacing: app.get_scaled_width(30.0)
            size_hint: (None, None)
            height: app.get_scaled_height(60.0)
            width: app.get_scaled_width(580.0)

            # Put the image here
            BoxLayout: 
                size_hint: (None, None)
                # pos: self.parent.pos
                height: app.get_scaled_height(60.0)
                width: app.get_scaled_width(145.0)

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
                height: app.get_scaled_height(50.0000000002)
                width: app.get_scaled_width(120.0)
                font_size: app.get_scaled_width(28.0)
                input_filter: 'float'
                multiline: False

            LabelBase: 
                color: 0,0,0,1
                font_size: app.get_scaled_width(28.0)
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
