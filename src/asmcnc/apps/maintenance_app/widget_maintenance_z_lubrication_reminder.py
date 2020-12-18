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

    BoxLayout:
        size_hint: (None, None)
        height: dp(200)
        width: dp(580)
        pos: self.parent.pos
        orientation: 'vertical'
        padding: 20
        spacing: 10      

        Label: 
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

    def __init__(self, **kwargs):
    
        super(ZLubricationReminderWidget, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    def update_time_left(self):
        time_in_hours = int((self.m.time_since_z_head_lubricated_seconds)/3600)

        if time_in_hours < 30: 
            # self.hours_since_lubrication.color = hex('#4caf50ff')
            self.hours_since_lubrication.text = '[color=4caf50ff]' + str(time_in_hours) + ' hrs' + '[/color]'

        elif time_in_hours < 40:
            # self.hours_since_lubrication.color = hex('#f9ce1dff')
            self.hours_since_lubrication.text = '[color=f9ce1dff]' + str(time_in_hours) + ' hrs' + '[/color]'

        elif time_in_hours < 45:
            # self.hours_since_lubrication.color = hex('#ff9903ff')
            self.hours_since_lubrication.text = '[color=ff9903ff]' + str(time_in_hours) + ' hrs' + '[/color]'

        else:
            # self.hours_since_lubrication.color = hex('#e64a19ff')
            self.hours_since_lubrication.text = '[color=e64a19ff]' + str(time_in_hours) + ' hrs' + '[/color]'

    def reset_to_0(self):
        # self.hours_since_lubrication.color = hex('#4caf50ff')
        self.hours_since_lubrication.text = '0' + ' hrs'



