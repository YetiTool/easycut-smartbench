"""
Created on 17 August 2020
@author: Letty
widget to allow user to change touchplate offset
"""
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from asmcnc.apps.maintenance_app import popup_maintenance
from asmcnc.skavaUI import popup_info
Builder.load_string(
    """

<ZLubricationReminderWidget>
    
    hours_since_lubrication:hours_since_lubrication

    time_since_screw_lubricated_label : time_since_screw_lubricated_label

    BoxLayout:
        size_hint: (None, None)
        height: dp(0.416666666667*app.height)
        width: dp(0.725*app.width)
        pos: self.parent.pos
        orientation: 'vertical'
        padding: 0.025*app.width
        spacing: 0.0208333333333*app.height      

        Label:
            font_size: str(0.01875 * app.width) + 'sp'
            id: time_since_screw_lubricated_label
            color: 0,0,0,1
            font_size: dp(0.03*app.width)
            markup: True
            halign: "left"
            valign: "middle"
            text_size: self.size
            text: "[b]TIME SINCE LEAD SCREW LUBRICATED[/b]"

        BoxLayout: 
            orientation: 'horizontal'
            padding: [0,0.0104166666667*app.height,0,0]
            spacing: 0.0125*app.width
            size_hint: (None, None)
            height: dp(0.3125*app.height)
            width: dp(0.725*app.width) 

            # Put the image here
            BoxLayout: 
                size_hint: (None, None)
                # pos: self.parent.pos
                height: dp(0.24375*app.height)
                width: dp(0.05*app.width)

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
                height: dp(0.25*app.height)
                width: dp(0.4375*app.width)
                Label: 
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: hours_since_lubrication
                    color: 0,0,0,1
                    font_size: dp(0.125*app.width)
                    markup: True
                    halign: "center"
                    valign: "bottom"
                    text_size: self.size
                    text: "[b]50hrs[/b]"

            BoxLayout: 
                size_hint: (None, None)
                height: dp(0.25*app.height)
                width: dp(0.15*app.width)
                Button:
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: reset_0
                    on_press: root.reset_to_0()
                    size_hint: (None,None)
                    height: dp(0.25*app.height)
                    width: dp(0.15*app.width)
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
    hours_label = 'hours'
    default_time_label_font_size = 100

    def __init__(self, **kwargs):
        super(ZLubricationReminderWidget, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.update_strings()

    def update_time_left(self):
        self.update_strings()
        self.time_in_hours = int(self.m.
            time_since_z_head_lubricated_seconds / 3600)
        if self.time_in_hours < 30:
            self.hours_since_lubrication.text = '[color=4caf50ff]' + str(self
                .time_in_hours) + ' ' + self.hours_label + '[/color]'
        elif self.time_in_hours < 40:
            self.hours_since_lubrication.text = '[color=f9ce1dff]' + str(self
                .time_in_hours) + ' ' + self.hours_label + '[/color]'
        elif self.time_in_hours < 45:
            self.hours_since_lubrication.text = '[color=ff9903ff]' + str(self
                .time_in_hours) + ' ' + self.hours_label + '[/color]'
        else:
            self.hours_since_lubrication.text = '[color=e64a19ff]' + str(self
                .time_in_hours) + ' ' + self.hours_label + '[/color]'
        self.update_font_size(self.hours_since_lubrication)

    def reset_to_0(self):
        self.time_in_hours = 0
        self.hours_since_lubrication.text = '[color=4caf50ff]' + str(self.
            time_in_hours) + ' ' + self.hours_label + '[/color]'
        self.update_font_size(self.hours_since_lubrication)

    def update_strings(self):
        self.time_since_screw_lubricated_label.text = self.l.get_bold(
            'TIME SINCE LEAD SCREW LUBRICATED')
        self.hours_label = self.l.get_str('hours')
        self.update_label_font_size(self.time_since_screw_lubricated_label)

    def update_font_size(self, value):
        if len(value.text) < 8 + len('[color=4caf50ff]') + len('[/color]'):
            value.font_size = 90
        if len(value.text) > 7 + len('[color=4caf50ff]') + len('[/color]'):
            value.font_size = 80
        if len(value.text) > 8 + len('[color=4caf50ff]') + len('[/color]'):
            value.font_size = 75
        if len(value.text) > 9 + len('[color=4caf50ff]') + len('[/color]'):
            value.font_size = 70
        if len(value.text) > 10 + len('[color=4caf50ff]') + len('[/color]'):
            value.font_size = 60
        if len(value.text) > 11 + len('[color=4caf50ff]') + len('[/color]'):
            value.font_size = 50

    def update_label_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length > 45:
            value.font_size = 18
        elif text_length > 43:
            value.font_size = 22
        else:
            value.font_size = 24
