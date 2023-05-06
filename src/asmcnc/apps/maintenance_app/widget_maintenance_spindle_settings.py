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
    seconds_label: seconds_label
    stylus_label: stylus_label
    stylus_switch: stylus_switch

    
    BoxLayout:
        orientation: 'vertical'
        pos: self.parent.pos
        size: self.parent.size
        spacing: dp(15)

        # ROW 1

        BoxLayout:
            orientation: 'horizontal'
            padding: dp(5)

            canvas:
                Color:
                    rgba: 1,1,1,1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos

            BoxLayout:
                size_hint_x: 0.2

                Image:
                    id: spindle_image
                    source: "./asmcnc/apps/maintenance_app/img/spindle_small.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            BoxLayout:
                padding: dp(5)

                Spinner:
                    id: spindle_brand
                    halign: 'left'
                    valign: 'middle'
                    markup: True
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

        # ROW 2

        BoxLayout:
            orientation: 'horizontal'
            padding: dp(5)

            canvas:
                Color:
                    rgba: 1,1,1,1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos

            BoxLayout:
                orientation: 'horizontal'

                BoxLayout:
                    padding: dp(10)

                    Image:
                        id: spindle_image
                        source: "./asmcnc/apps/maintenance_app/img/speed_dial.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                BoxLayout:
                    size_hint_x: 1.5
                    padding: dp(5)

                    TextInput:
                        id: spindle_cooldown_speed
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

            BoxLayout:
                orientation: 'horizontal'

                BoxLayout:
                    padding: dp(5)

                    Image:
                        id: countdown_image
                        source: "./asmcnc/apps/maintenance_app/img/countdown_small.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                BoxLayout:
                    padding: dp(5)

                    TextInput:
                        id: spindle_cooldown_time
                        font_size: dp(30)
                        valign: "bottom"
                        markup: True
                        halign: "left"
                        input_filter: 'int'
                        multiline: False

                Label:
                    id: seconds_label
                    size_hint_x: 1.5
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
            orientation: 'horizontal'
            padding: dp(5)

            canvas:
                Color:
                    rgba: 1,1,1,1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos

            BoxLayout:
                size_hint_x: 0.3

                Image:
                    id: stylus_image
                    source: "./asmcnc/apps/maintenance_app/img/stylus_mini_logo.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            Label:
                id: stylus_label
                color: 0,0,0,1
                font_size: dp(30)
                markup: True
                halign: "left"
                valign: "middle"
                text_size: self.size

            BoxLayout:
                size_hint_x: 0.5

                Switch:
                    id: stylus_switch
                    background_color: [0,0,0,0]
                    center_x: self.parent.center_x
                    y: self.parent.y
                    pos: self.parent.pos

        # ROW 4

        BoxLayout:
            orientation: 'horizontal'
            padding: dp(5)

            canvas:
                Color:
                    rgba: 1,1,1,1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
        



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
        self.stylus_label.text = self.l.get_str("CNC Stylus")

