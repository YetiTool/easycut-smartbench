from kivy.core.window import Window

"""
Created on 17 August 2020
@author: Letty
widget to allow user to change touchplate offset
"""
from kivy.lang import Builder
from kivy.uix.widget import Widget
from asmcnc.core_UI.scaling_utils import get_scaled_width

Builder.load_string("""
#:import LabelBase asmcnc.core_UI.components.labels.base_label

<ZLubricationReminderWidget>
    
    hours_since_lubrication:hours_since_lubrication

    time_since_screw_lubricated_label : time_since_screw_lubricated_label

    BoxLayout:
        size_hint: (None, None)
        height: app.get_scaled_height(200.0)
        width: app.get_scaled_width(580.0)
        pos: self.parent.pos
        orientation: 'vertical'
        padding: app.get_scaled_tuple([20.0, 20.0])
        spacing: app.get_scaled_width(10.0)

        LabelBase:
            id: time_since_screw_lubricated_label
            color: 0,0,0,1
            font_size: app.get_scaled_width(24.0)
            markup: True
            halign: "left"
            valign: "middle"
            text_size: self.size
            text: "[b]TIME SINCE LEAD SCREW LUBRICATED[/b]"

        BoxLayout: 
            orientation: 'horizontal'
            padding: app.get_scaled_tuple([0, 5.0, 0, 0])
            spacing: app.get_scaled_width(10.0)
            size_hint: (None, None)
            height: app.get_scaled_height(150.0)
            width: app.get_scaled_width(580.0)

            # Put the image here
            BoxLayout: 
                size_hint: (None, None)
                # pos: self.parent.pos
                height: app.get_scaled_height(117.0)
                width: app.get_scaled_width(40.0)

                Image:
                    id: lead_screw_image
                    source: "./asmcnc/apps/maintenance_app/img/z_lead_screw.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            # Text input
            BoxLayout: 
                size_hint: (None, None)
                height: app.get_scaled_height(120.0)
                width: app.get_scaled_width(350.0)
                LabelBase: 
                    id: hours_since_lubrication
                    color: 0,0,0,1
                    font_size: app.get_scaled_width(100.0)
                    markup: True
                    halign: "center"
                    valign: "bottom"
                    text_size: self.size
                    text: "[b]50hrs[/b]"

            BoxLayout: 
                size_hint: (None, None)
                height: app.get_scaled_height(120.0)
                width: app.get_scaled_width(120.0)
                Button:
                    font_size: app.get_scaled_sp('15.0sp')
                    id: reset_0
                    on_press: root.reset_to_0()
                    size_hint: (None,None)
                    height: app.get_scaled_height(120.0)
                    width: app.get_scaled_width(120.0)
                    background_color: [0,0,0,0]
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


class ZLubricationReminderWidget(Widget):
    time_in_hours = 0
    hours_label = "hours"
    default_time_label_font_size = 100

    def __init__(self, **kwargs):
        super(ZLubricationReminderWidget, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def update_time_left(self):
        self.update_strings()
        self.time_in_hours = int(self.m.time_since_z_head_lubricated_seconds / 3600)
        if self.time_in_hours < 30:
            self.hours_since_lubrication.text = (
                "[color=4caf50ff]"
                + str(self.time_in_hours)
                + " "
                + self.hours_label
                + "[/color]"
            )
        elif self.time_in_hours < 40:
            self.hours_since_lubrication.text = (
                "[color=f9ce1dff]"
                + str(self.time_in_hours)
                + " "
                + self.hours_label
                + "[/color]"
            )
        elif self.time_in_hours < 45:
            self.hours_since_lubrication.text = (
                "[color=ff9903ff]"
                + str(self.time_in_hours)
                + " "
                + self.hours_label
                + "[/color]"
            )
        else:
            self.hours_since_lubrication.text = (
                "[color=e64a19ff]"
                + str(self.time_in_hours)
                + " "
                + self.hours_label
                + "[/color]"
            )
        self.update_font_size(self.hours_since_lubrication)

    def reset_to_0(self):
        self.time_in_hours = 0
        self.hours_since_lubrication.text = (
            "[color=4caf50ff]"
            + str(self.time_in_hours)
            + " "
            + self.hours_label
            + "[/color]"
        )
        self.update_font_size(self.hours_since_lubrication)

    def update_strings(self):
        self.time_since_screw_lubricated_label.text = self.l.get_bold(
            "TIME SINCE LEAD SCREW LUBRICATED"
        )
        self.hours_label = self.l.get_str("hours")
        self.update_label_font_size(self.time_since_screw_lubricated_label)

    def update_font_size(self, value):
        if len(value.text) < 8 + len("[color=4caf50ff]") + len("[/color]"):
            value.font_size = 0.1125 * Window.width
        if len(value.text) > 7 + len("[color=4caf50ff]") + len("[/color]"):
            value.font_size = 0.1 * Window.width
        if len(value.text) > 8 + len("[color=4caf50ff]") + len("[/color]"):
            value.font_size = 0.09375 * Window.width
        if len(value.text) > 9 + len("[color=4caf50ff]") + len("[/color]"):
            value.font_size = 0.0875 * Window.width
        if len(value.text) > 10 + len("[color=4caf50ff]") + len("[/color]"):
            value.font_size = 0.075 * Window.width
        if len(value.text) > 11 + len("[color=4caf50ff]") + len("[/color]"):
            value.font_size = 0.0625 * Window.width

    def update_label_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length > 45:
            value.font_size = get_scaled_width(18)
        elif text_length > 43:
            value.font_size = get_scaled_width(22)
        else:
            value.font_size = get_scaled_width(24)
