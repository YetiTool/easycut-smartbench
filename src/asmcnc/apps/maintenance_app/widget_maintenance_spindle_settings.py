'''
Created on 19 August 2020
@author: Letty
widget to spindle settings
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from asmcnc.apps.maintenance_app import popup_maintenance
from asmcnc.skavaUI import popup_info

Builder.load_string("""

<SpindleSpinner@SpinnerOption>

    background_normal: ''
    background_color: [1,1,1,1]
    height: dp(40)
    color: 0,0,0,1
    halign: 'left'
    markup: 'True'

<SpindleSettingsWidget>

    spindle_brand: spindle_brand
    spindle_cooldown_speed: spindle_cooldown_speed
    spindle_cooldown_time: spindle_cooldown_time
    rpm_label: rpm_label
    seconds_label : seconds_label
    stylus_switch: stylus_switch

    
    GridLayout:
        cols: 2
        rows: 4
        size_hint: (None, None)
        height: dp(280)
        width: dp(580)
        cols_minimum: {0: dp(150), 1: dp(410)}
        rows_minimum: {0: dp(40), 1: dp(40), 2: dp(40), 3: dp(40)}
        spacing: [dp(0), dp(5)]


        # ROW 1

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(60)
            width: dp(150)
            padding: [dp(55), dp(3), dp(41), dp(3)]

            Image:
                id: spindle_image
                source: "./asmcnc/apps/maintenance_app/img/speed_dial.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(50)
            width: dp(410)
            padding: [dp(0), dp(5), dp(10), dp(5)]
            spacing: dp(10)
	        TextInput:
	            id: spindle_cooldown_speed
	            size_hint: (None, None)
	            height: dp(50)
	            width: dp(250)
                font_size: dp(30)
                valign: "bottom"
                markup: True
                halign: "left"
                input_filter: 'int'
                multiline: False

            Label:
                id: rpm_label
                color: 0,0,0,1
                font_size: dp(30)
                markup: True
                halign: "left"
                valign: "middle"
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos
                text: "RPM"

        # ROW 2

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(60)
            width: dp(150)
            padding: [dp(55), dp(3), dp(41), dp(3)]

            Image:
                id: countdown_image
                source: "./asmcnc/apps/maintenance_app/img/countdown_small.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(50)
            width: dp(410)
            padding: [dp(0), dp(5), dp(10), dp(5)]
            spacing: dp(10)
            TextInput:
                id: spindle_cooldown_time
                size_hint: (None, None)
                height: dp(50)
                width: dp(250)
                font_size: dp(30)
                valign: "bottom"
                markup: True
                halign: "left"
                input_filter: 'int'

            Label:
                id: seconds_label
                color: 0,0,0,1
                font_size: dp(30)
                markup: True
                halign: "left"
                valign: "middle"
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos

        # ROW 3

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(60)
            width: dp(150)
            padding: [dp(46), dp(5), dp(40), dp(5)] # 15 padding

            Image:
                id: spindle_image
                source: "./asmcnc/apps/maintenance_app/img/spindle_small.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(50)
            width: dp(410)
            padding: [dp(0), dp(5), dp(10), dp(5)]
            Spinner:
                id: spindle_brand
                halign: 'left'
                valign: 'middle'
                markup: True
                size_hint: (None, None)
                size: 380, 50
                text: 'spinner'
                font_size: '30sp'
                text_size: self.size
                multiline: False
                color: 0,0,0,1
                values: root.brand_list_sc1
                option_cls: Factory.get("SpindleSpinner")
                background_normal: './asmcnc/apps/maintenance_app/img/brand_dropdown.png'
                on_text: root.autofill_rpm_time()
                # background_color: [1,1,1,0]

        # ROW 4

        BoxLayout: 
            size_hint: (None, None)
            # pos: self.parent.pos
            height: dp(60)
            width: dp(150)
            padding: [dp(46), dp(3), dp(40), dp(3)]

            Image:
                id: stylus_image
                source: "./asmcnc/apps/maintenance_app/img/stylus_mini_logo.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True

        BoxLayout:
            size_hint: (None, None)
            pos: self.parent.pos
            height: dp(60)
            width: dp(90)
            Switch:
                id: stylus_switch
                background_color: [0,0,0,0]
                center_x: self.parent.center_x
                y: self.parent.y
                pos: self.parent.pos



""")

class SpindleSettingsWidget(Widget):

    brand_list_sc1 = [' YETI SC1 digital 230V', ' YETI SC1 digital 110V', ' AMB digital 230V', ' AMB manual 230V', ' AMB manual 110V']
    brand_list_sc2 = [' YETI SC2 digital 230V', ' YETI SC2 digital 110V'] + brand_list_sc1

    def __init__(self, **kwargs):
    
        super(SpindleSettingsWidget, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']

        self.rpm_override = self.m.spindle_cooldown_rpm_override
        self.spindle_cooldown_speed.bind(focus=self.on_focus)

        self.update_strings()

    def on_focus(self, instance, value):
        if not value:
            self.rpm_override = True

    def autofill_rpm_time(self):

        if 'AMB' in self.spindle_brand.text:
            self.spindle_cooldown_time.text = str(30)
            self.spindle_cooldown_speed.text = str(self.m.amb_cooldown_rpm_default)

        if 'YETI' in self.spindle_brand.text:
            self.spindle_cooldown_time.text = str(10)
            self.spindle_cooldown_speed.text = str(self.m.yeti_cooldown_rpm_default)

        if 'manual' in self.spindle_brand.text:
            self.spindle_cooldown_speed.disabled = True

        if 'digital' in self.spindle_brand.text:
            self.spindle_cooldown_speed.disabled = False

        self.rpm_override = False  

    def update_strings(self):
        self.rpm_label.text = self.l.get_str("RPM")
        self.seconds_label.text = self.l.get_str("seconds")

