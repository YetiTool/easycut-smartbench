'''
Created on 19 August 2020
@author: Letty
widget to spindle settings
'''

import kivy
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.clock import Clock

from asmcnc.skavaUI import popup_info
from asmcnc.apps.maintenance_app import widget_maintenance_spindle_save

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
    uptime_label: uptime_label
    stylus_switch: stylus_switch
    spindle_save_container:spindle_save_container


    BoxLayout:
        orientation: 'vertical'
        pos: self.parent.pos
        size: self.parent.size
        spacing: dp(15)

        BoxLayout:
            size_hint_y: 0.3
            orientation: 'horizontal'
            padding: dp(5)

            canvas:
                Color:
                    rgba: 1,1,1,1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos

            Image:
                size_hint_x: 0.2
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

        BoxLayout:
            orientation: 'horizontal'
            pos: self.parent.pos
            size: self.parent.size
            spacing: dp(20)

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(15)

                # ROW 1



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

                    Image:
                        size_hint_x: 0.3
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

                    BoxLayout:
                        padding: dp(3)
                        size_hint_x: 0.3

                        Image:
                            source: "./asmcnc/apps/maintenance_app/img/uptime_hourglass.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

                    Label:
                        id: uptime_label
                        color: 0,0,0,1
                        font_size: dp(30)
                        markup: True
                        halign: "left"
                        valign: "middle"
                        text_size: self.size

                    BoxLayout:
                        size_hint_x: 0.5
                        padding: [dp(40), dp(0)]

                        Button:
                            on_press: root.get_uptime()
                            background_normal: ''
                            background_down: ''

                            Image:
                                source: "./asmcnc/apps/maintenance_app/img/uptime_button.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: False

            BoxLayout:
                id: spindle_save_container
                size_hint_x: 0.3
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

        self.spindle_save_widget = widget_maintenance_spindle_save.SpindleSaveWidget(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.spindle_save_container.add_widget(self.spindle_save_widget)

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

    def get_uptime(self):
        if self.m.theateam() and self.m.get_dollar_setting(51):
            if self.m.state().startswith('Idle'):
                self.wait_popup = popup_info.PopupWait(self.sm, self.l)
                self.m.s.write_command('M3 S0')
                Clock.schedule_once(self.get_spindle_info, 0.3)
            else:
                popup_info.PopupError(self.sm, self.l, self.l.get_str("Please ensure machine is idle before continuing."))
        else:
            self.uptime_label.text = "Uptime: " + str(int(self.m.spindle_brush_use_seconds/3600)) + " hours"

    def get_spindle_info(self, dt):
        self.m.s.write_protocol(self.m.p.GetDigitalSpindleInfo(), "GET DIGITAL SPINDLE INFO")
        self.check_info_count = 0
        Clock.schedule_once(self.check_spindle_info, 0.3)

    def check_spindle_info(self, dt):
        self.check_info_count += 1
        # Value of -999 represents disconnected spindle
        if (self.m.s.digital_spindle_ld_qdA != -999 and self.m.s.spindle_serial_number not in [None, -999, 999]) or (self.check_info_count > 10):
            self.read_restore_info()
        else: # Keep trying for a few seconds
            Clock.schedule_once(self.check_spindle_info, 0.3)

    def read_restore_info(self):
        self.m.s.write_command('M5')
        self.wait_popup.popup.dismiss()
        # Value of -999 for ld_qdA represents disconnected spindle
        if self.m.s.digital_spindle_ld_qdA != -999 and self.m.s.spindle_serial_number not in [None, -999, 999]:
            # Get info was successful, show info
            self.uptime_label.text = "Uptime: " + str(int(self.m.s.spindle_brush_run_time_seconds/3600)) + " hours"
        else:
            # Otherwise, spindle is probably disconnected
            error_message = self.l.get_str("No SC2 Spindle motor detected.") + " " + self.l.get_str("Please check your connections.")
            popup_info.PopupError(self.sm, self.l, error_message)

    def update_strings(self):
        self.rpm_label.text = self.l.get_str("RPM")
        self.seconds_label.text = self.l.get_str("seconds")
        self.stylus_label.text = self.l.get_str("CNC Stylus")
        self.uptime_label.text = self.l.get_str("Turn on spindle to read")

