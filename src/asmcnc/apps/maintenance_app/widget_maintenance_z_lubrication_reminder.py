'''
Created on 17 August 2020
@author: Letty
widget to allow user to change touchplate offset
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from asmcnc.apps.maintenance_app import popup_maintenance
from asmcnc.skavaUI import popup_info

Builder.load_string("""

<ZLubricationReminderWidget>
    
    hours_since_lubrication:hours_since_lubrication

    time_since_srew_lubricated_label : time_since_srew_lubricated_label

    BoxLayout:
        size_hint: (None, None)
        height: dp(200)
        width: dp(580)
        pos: self.parent.pos
        orientation: 'vertical'
        padding: 20
        spacing: 10      

        Label:
            id: time_since_srew_lubricated_label
            color: 0,0,0,1
            font_size: dp(24)
            markup: True
            halign: "left"
            valign: "middle"
            text_size: self.size
            text: "[b]TIME SINCE LEAD SCREW LUBRICATED[/b]"

        BoxLayout: 
            orientation: 'horizontal'
            padding: [0,dp(5),0,0]
            spacing: 10
            size_hint: (None, None)
            height: dp(150)
            width: dp(580) 

            # Put the image here
            BoxLayout: 
                size_hint: (None, None)
                # pos: self.parent.pos
                height: dp(117)
                width: dp(40)

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
                height: dp(120)
                width: dp(350)
                Label: 
                    id: hours_since_lubrication
                    color: 0,0,0,1
                    font_size: dp(100)
                    markup: True
                    halign: "center"
                    valign: "bottom"
                    text_size: self.size
                    text: "[b]50hrs[/b]"

            BoxLayout: 
                size_hint: (None, None)
                height: dp(120)
                width: dp(120)
                Button:
                    id: reset_0
                    on_press: root.reset_to_0()
                    size_hint: (None,None)
                    height: dp(120)
                    width: dp(120)
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


""")


class ZLubricationReminderWidget(Widget):

    time_in_hours = 0
    hours_label = "hours"
    default_time_label_font_size = 100

    def __init__(self, **kwargs):
    
        super(ZLubricationReminderWidget, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']

        self.update_strings()

    def update_time_left(self):
        self.time_in_hours = int((self.m.time_since_z_head_lubricated_seconds)/3600)

        if self.time_in_hours < 30: 
            self.hours_since_lubrication.text = '[color=4caf50ff]' + str(self.time_in_hours) + ' ' + self.hours_label + '[/color]'

        elif self.time_in_hours < 40:
            self.hours_since_lubrication.text = '[color=f9ce1dff]' + str(self.time_in_hours) + ' ' + self.hours_label + '[/color]'

        elif self.time_in_hours < 45:
            self.hours_since_lubrication.text = '[color=ff9903ff]' + str(self.time_in_hours) + ' ' + self.hours_label + '[/color]'

        else:
            self.hours_since_lubrication.text = '[color=e64a19ff]' + str(self.time_in_hours) + ' ' + self.hours_label + '[/color]'

        self.update_font_size(self.hours_since_lubrication)

    def reset_to_0(self):
        self.time_in_hours = 0
        self.hours_since_lubrication.text = '[color=4caf50ff]' + str(self.time_in_hours) + ' ' + self.hours_label + '[/color]'

    def update_strings(self):
        self.time_since_srew_lubricated_label.text = self.l.get_bold("TIME SINCE LEAD SCREW LUBRICATED")
        self.hours_label = self.l.get_str("hours")

    def update_font_size(self, value):
        if len(value.text) < (9 + len('[color=4caf50ff]') + len('[/color]')):
            value.font_size = dp(100)
        elif len(value.text) > (8 + len('[color=4caf50ff]') + len('[/color]')): 
            value.font_size = dp(98)
        if len(value.text) > (10 + len('[color=4caf50ff]') + len('[/color]')):
            value.font_size = dp(96)
        if len(value.text) > (12 + len('[color=4caf50ff]') + len('[/color]')):
            value.font_size = dp(94)
        if len(value.text) > (14 + len('[color=4caf50ff]') + len('[/color]')):
            value.font_size = dp(92)
