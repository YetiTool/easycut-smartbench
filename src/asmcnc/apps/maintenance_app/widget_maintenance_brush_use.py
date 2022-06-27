'''
Created on 17 August 2020
@author: Letty
widget to hold brush use input and buttons
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.clock import Clock

from asmcnc.apps.maintenance_app import popup_maintenance
from asmcnc.skavaUI import popup_info

Builder.load_string("""

<BrushUseWidget>
    
    restore_button:restore_button
    reset_0:reset_0
    brush_use:brush_use

    brush_use_label : brush_use_label
    hours_label : hours_label
    
    BoxLayout:
        size_hint: (None, None)
        height: dp(250)
        width: dp(280)
        pos: self.parent.pos
        orientation: 'vertical'
        padding: [13.3,10,13.3,10]
        spacing: 10

        BoxLayout: 
            orientation: 'vertical'
            spacing: dp(5)
            size_hint: (None, None)
            height: dp(100)
            width: dp(280)         

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
                padding: [0,dp(5),0,0]
                spacing: 10
                size_hint: (None, None)
                height: dp(53)
                width: dp(280) 

                # Text input
                TextInput:
                    id: brush_use
                    size_hint: (None, None)
                    height: dp(50)
                    width: dp(120)
                    font_size: dp(28)
                    input_filter: 'int'
                    multiline: False

                Label:
                    id: hours_label
                    color: 0,0,0,1
                    font_size: dp(28)
                    markup: True
                    halign: "left"
                    valign: "middle"
                    text_size: self.size
                    text: "hrs"

        GridLayout:
            cols: 2
            rows: 1
            spacing: 13.3
            size_hint: (None, None)
            height: dp(120)
            width: dp(253.3)

            BoxLayout: 
                size: self.parent.size
                pos: self.parent.pos
                ToggleButton:
                    id: restore_button
                    on_press: root.restore()
                    size_hint: (None,None)
                    height: dp(120)
                    width: dp(120)
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
                    id: reset_0
                    on_press: root.reset_to_0()
                    size_hint: (None,None)
                    height: dp(120)
                    width: dp(120)
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


""")


class BrushUseWidget(Widget):

    default_font_size = 24

    def __init__(self, **kwargs):
    
        super(BrushUseWidget, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']

        self.update_strings()
        
    def restore(self):
        try:
            if self.m.s.setting_51:
                self.m.s.write_command('M3 S0')
                Clock.schedule_once(self.get_restore_info, 1)
                self.wait_popup = popup_info.PopupWait(self.sm, self.l)
                return
        except:
            pass
        self.brush_use.text = str(int(self.m.spindle_brush_use_seconds/3600)) # convert back to hrs for user

    def get_restore_info(self, dt):
        self.m.s.write_protocol(self.m.p.GetDigitalSpindleInfo(), "GET DIGITAL SPINDLE INFO")
        Clock.schedule_once(self.read_restore_info, 1)

    def read_restore_info(self, dt):
        self.m.s.write_command('M5')
        self.wait_popup.popup.dismiss()
        # If info was not obtained successfully, spindle production year will equal 99
        # Update this code if the year is 2099
        if self.m.s.spindle_production_year != 99:
            self.brush_use.text = str(int(self.m.s.spindle_brush_run_time_seconds/3600))
        else:
            popup_info.PopupError(self.sm, self.l, "Could not get info - spindle not plugged in!")

    def reset_to_0(self):
        self.brush_use.text = '0'

    def update_strings(self):
        self.brush_use_label.text = self.l.get_bold("BRUSH USE")
        self.hours_label.text = self.l.get_str("hours")

        self.update_font_size(self.brush_use_label)

    def update_font_size(self, value):
        if len(value.text) <= 27:
            value.font_size = self.default_font_size
        if len(value.text) > 27:
            value.font_size = self.default_font_size - 3
        if len(value.text) > 30:
            value.font_size = self.default_font_size - 6
        if len(value.text) > 35:
            value.font_size = self.default_font_size - 7










