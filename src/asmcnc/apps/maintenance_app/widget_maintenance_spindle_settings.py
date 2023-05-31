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

    spindle_brand:spindle_brand
    cooldown_speed_slider:cooldown_speed_slider
    cooldown_time_slider:cooldown_time_slider
    rpm_label:rpm_label
    seconds_label:seconds_label
    cooldown_settings_label:cooldown_settings_label
    get_data_label:get_data_label
    stylus_switch:stylus_switch
    min_speed_label:min_speed_label
    max_speed_label:max_speed_label
    min_time_label:min_time_label
    max_time_label:max_time_label
    spindle_save_container:spindle_save_container
    spindle_data_container:spindle_data_container
    get_data_button:get_data_button


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

                BoxLayout:
                    size_hint_y: 2
                    orientation: 'vertical'
                    padding: dp(5)

                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos

                    Label:
                        id: cooldown_settings_label
                        size_hint_y: 0.5
                        color: 0,0,0,1
                        font_size: dp(24)
                        halign: "left"
                        valign: "middle"
                        bold: True
                        text_size: self.size

                    BoxLayout:
                        orientation: 'horizontal'

                        BoxLayout:
                            padding: dp(13)

                            Image:
                                id: spindle_image
                                source: "./asmcnc/apps/maintenance_app/img/speed_dial.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True

                        Slider:
                            id: cooldown_speed_slider
                            size_hint_x: 3
                            min: 10000
                            max: 20000
                            step: 500

                        Label:
                            id: rpm_label
                            size_hint_x: 1.5
                            color: 0,0,0,1
                            font_size: dp(25)
                            markup: True
                            halign: "center"
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

                        Slider:
                            id: cooldown_time_slider
                            size_hint_x: 3
                            min: 1
                            max: 60
                            step: 1

                        Label:
                            id: seconds_label
                            size_hint_x: 1.5
                            color: 0,0,0,1
                            font_size: dp(25)
                            markup: True
                            halign: "center"
                            valign: "middle"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos

                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(15)

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
                            source: "./asmcnc/apps/maintenance_app/img/stylus_mini_logo.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

                        BoxLayout:
                            padding: [dp(10), dp(10), dp(0), dp(13)]

                            BoxLayout:
                                size_hint: (None,None)
                                height: dp(36)
                                width: dp(150)

                                Image:
                                    source: "./asmcnc/apps/maintenance_app/img/stylus_text_logo.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True

                        BoxLayout:
                            size_hint_x: 0.5

                            Switch:
                                id: stylus_switch
                                background_color: [0,0,0,0]
                                center_x: self.parent.center_x
                                y: self.parent.y
                                pos: self.parent.pos

                    BoxLayout:
                        id: spindle_data_container
                        size_hint_x: 0.75
                        orientation: 'horizontal'
                        padding: dp(5)

                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                        Label:
                            id: get_data_label
                            color: 0,0,0,1
                            font_size: dp(30)
                            halign: "center"
                            valign: "middle"
                            text_size: self.size

                        BoxLayout:
                            size_hint_x: 0.5

                            Button:
                                id: get_data_button
                                on_press: root.get_spindle_data()
                                # background_normal: ''
                                # background_down: ''

                                # Image:
                                #     source: "./asmcnc/apps/maintenance_app/img/uptime_button.png"
                                #     center_x: self.parent.center_x
                                #     y: self.parent.y
                                #     size: self.parent.width, self.parent.height
                                #     allow_stretch: False

            BoxLayout:
                id: spindle_save_container
                size_hint_x: 0.3
                canvas:
                    Color:
                        rgba: 1,1,1,1
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos

    FloatLayout:
        Label:
            id: min_speed_label
            x: cooldown_speed_slider.pos[0]
            y: cooldown_speed_slider.pos[1] - cooldown_speed_slider.size[1] * 0.1
            size_hint: None, None
            height: dp(30)
            width: dp(30)
            color: hex('#888888ff')
            font_size: dp(13)

        Label:
            id: max_speed_label
            x: cooldown_speed_slider.pos[0] + cooldown_speed_slider.size[0] * 0.9
            y: cooldown_speed_slider.pos[1] - cooldown_speed_slider.size[1] * 0.1
            size_hint: None, None
            height: dp(30)
            width: dp(30)
            color: hex('#888888ff')
            font_size: dp(13)

        Label:
            id: min_time_label
            x: cooldown_time_slider.pos[0]
            y: cooldown_time_slider.pos[1] - cooldown_time_slider.size[1] * 0.1
            size_hint: None, None
            height: dp(30)
            width: dp(30)
            color: hex('#888888ff')
            font_size: dp(13)

        Label:
            id: max_time_label
            x: cooldown_time_slider.pos[0] + cooldown_time_slider.size[0] * 0.9
            y: cooldown_time_slider.pos[1] - cooldown_time_slider.size[1] * 0.1
            size_hint: None, None
            height: dp(30)
            width: dp(30)
            color: hex('#888888ff')
            font_size: dp(13)



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
        self.cooldown_speed_slider.bind(value=self.cooldown_speed_updated)
        self.cooldown_time_slider.bind(value=self.cooldown_time_updated)

        self.spindle_save_widget = widget_maintenance_spindle_save.SpindleSaveWidget(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.spindle_save_container.add_widget(self.spindle_save_widget)

        self.update_strings()

    def cooldown_speed_updated(self, instance, value):
        # Convert to int and display
        self.rpm_label.text = "%i " % value + self.l.get_str("RPM")
        self.rpm_override = True

    def cooldown_time_updated(self, instance, value):
        # Convert to int and display
        self.seconds_label.text = "%i " % value + self.l.get_str("seconds")

    def autofill_rpm_time(self):

        if 'AMB' in self.spindle_brand.text:
            self.cooldown_time_slider.value = 30
            self.cooldown_speed_slider.value = self.m.amb_cooldown_rpm_default

        if 'YETI' in self.spindle_brand.text:
            self.cooldown_time_slider.value = 10
            self.cooldown_speed_slider.value = self.m.yeti_cooldown_rpm_default

        if 'manual' in self.spindle_brand.text:
            self.cooldown_speed_slider.disabled = True

        if 'digital' in self.spindle_brand.text:
            self.cooldown_speed_slider.disabled = False

        self.rpm_override = False

    def hide_spindle_data_container(self):
        self.spindle_data_container.size_hint_x = 0
        self.spindle_data_container.opacity = 0
        self.spindle_data_container.parent.spacing = 0
        self.get_data_button.disabled = True

    def show_spindle_data_container(self):
        self.spindle_data_container.size_hint_x = 0.75
        self.spindle_data_container.opacity = 1
        self.spindle_data_container.parent.spacing = 15
        self.get_data_button.disabled = False

    def get_spindle_data(self):
        pass

    #     if self.m.theateam() and self.m.get_dollar_setting(51):
    #         if self.m.state().startswith('Idle'):
    #             self.wait_popup = popup_info.PopupWait(self.sm, self.l)
    #             self.m.s.write_command('M3 S0')
    #             Clock.schedule_once(self.get_spindle_info, 0.3)
    #         else:
    #             popup_info.PopupError(self.sm, self.l, self.l.get_str("Please ensure machine is idle before continuing."))
    #     else:
    #         self.uptime_label.text = "Uptime: " + str(int(self.m.spindle_brush_use_seconds/3600)) + " hours"

    # def get_spindle_info(self, dt):
    #     self.m.s.write_protocol(self.m.p.GetDigitalSpindleInfo(), "GET DIGITAL SPINDLE INFO")
    #     self.check_info_count = 0
    #     Clock.schedule_once(self.check_spindle_info, 0.3)

    # def check_spindle_info(self, dt):
    #     self.check_info_count += 1
    #     # Value of -999 represents disconnected spindle
    #     if (self.m.s.digital_spindle_ld_qdA != -999 and self.m.s.spindle_serial_number not in [None, -999, 999]) or (self.check_info_count > 10):
    #         self.read_restore_info()
    #     else: # Keep trying for a few seconds
    #         Clock.schedule_once(self.check_spindle_info, 0.3)

    # def read_restore_info(self):
    #     self.m.s.write_command('M5')
    #     self.wait_popup.popup.dismiss()
    #     # Value of -999 for ld_qdA represents disconnected spindle
    #     if self.m.s.digital_spindle_ld_qdA != -999 and self.m.s.spindle_serial_number not in [None, -999, 999]:
    #         # Get info was successful, show info
    #         self.uptime_label.text = "Uptime: " + str(int(self.m.s.spindle_brush_run_time_seconds/3600)) + " hours"
    #     else:
    #         # Otherwise, spindle is probably disconnected
    #         error_message = self.l.get_str("No SC2 Spindle motor detected.") + " " + self.l.get_str("Please check your connections.")
    #         popup_info.PopupError(self.sm, self.l, error_message)

    def update_strings(self):
        self.rpm_label.text = self.l.get_str("RPM")
        self.seconds_label.text = self.l.get_str("seconds")
        self.cooldown_settings_label.text = self.l.get_str("SPINDLE COOLDOWN SETTINGS")
        self.get_data_label.text = self.l.get_str("Get data")
        self.min_speed_label.text = "10k " + self.l.get_str("RPM")
        self.max_speed_label.text = "20k " + self.l.get_str("RPM")
        self.min_time_label.text = "1 " + self.l.get_str("seconds")
        self.max_time_label.text = "60 " + self.l.get_str("seconds")

