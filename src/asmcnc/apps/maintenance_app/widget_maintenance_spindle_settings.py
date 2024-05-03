from kivy.core.window import Window

from asmcnc.core_UI.custom_popups import PopupDisplaySpindleData
from asmcnc.core_UI.new_popups.spindle_health_check_popup import SpindleHealthCheckPopup
from asmcnc.core_UI.popups import ErrorPopup, InfoPopup

"""
Created on 19 August 2020
@author: Letty
widget to spindle settings
"""
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.clock import Clock
from asmcnc.apps.maintenance_app import (
    widget_maintenance_spindle_save,
)

Builder.load_string("""
#:import LabelBase asmcnc.core_UI.components.labels.base_label

<SpindleSpinner@SpinnerOption>

    background_normal: ''
    background_color: [1,1,1,1]
    height: dp(0.0833333333333*app.height)
    color: color_provider.get_rgba("black")
    halign: 'left'
    font_size: str(15.0/800.0*app.width) + 'sp'
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
        spacing:dp(0.03125)*app.height

        BoxLayout:
            size_hint_y: 0.3
            orientation: 'horizontal'
            padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]

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
                padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]

                Spinner:
                    id: spindle_brand
                    halign: 'left'
                    valign: 'middle'
                    markup: True
                    text: 'spinner'
                    font_size: str(0.0375*app.width) + 'sp'
                    text_size: self.size
                    multiline: False
                    color: color_provider.get_rgba("black")
                    values: root.brand_list_sc1
                    option_cls: Factory.get("SpindleSpinner")
                    background_normal: './asmcnc/apps/maintenance_app/img/brand_dropdown.png'
                    on_text: root.autofill_rpm_time()
                    # background_color: [1,1,1,0]

        BoxLayout:
            orientation: 'horizontal'
            pos: self.parent.pos
            size: self.parent.size
            spacing:dp(0.0416666666667)*app.height

            BoxLayout:
                orientation: 'vertical'
                spacing:dp(0.03125)*app.height

                BoxLayout:
                    size_hint_y: 2
                    orientation: 'vertical'
                    padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]

                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos

                    LabelBase:
                        id: cooldown_settings_label
                        size_hint_y: 0.5
                        color: color_provider.get_rgba("black")
                        font_size: dp(0.03*app.width)
                        halign: "left"
                        valign: "middle"
                        markup: True
                        text_size: self.size

                    BoxLayout:
                        orientation: 'horizontal'

                        BoxLayout:
                            padding:[dp(0.01625)*app.width, dp(0.0270833333333)*app.height]

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

                        LabelBase:
                            id: rpm_label
                            size_hint_x: 1.5
                            color: color_provider.get_rgba("black")
                            font_size: dp(0.0275*app.width)
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
                            padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]

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
                            size_hint_y: None
                            height: app.get_scaled_height(60)

                        LabelBase:
                            id: seconds_label
                            size_hint_x: 1.5
                            color: color_provider.get_rgba("black")
                            font_size: dp(0.0275*app.width)
                            markup: True
                            halign: "center"
                            valign: "middle"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos

                BoxLayout:
                    orientation: 'horizontal'
                    spacing:dp(0.01875)*app.width

                    BoxLayout:
                        orientation: 'horizontal'
                        padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]

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
                            padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height, 0, dp(0.0270833333333)*app.height]

                            BoxLayout:
                                size_hint: (None,None)
                                height: dp(0.075*app.height)
                                width: dp(0.1875*app.width)

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
                        padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]

                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                        LabelBase:
                            id: get_data_label
                            color: color_provider.get_rgba("black")
                            font_size: dp(0.03625*app.width)
                            halign: "center"
                            valign: "middle"
                            text_size: self.size
                            markup: True

                        BoxLayout:
                            size_hint_x: 0.5

                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                id: get_data_button
                                on_press: root.show_spindle_data_popup()
                                background_normal: ''
                                background_down: ''

                                Image:
                                    source: "./asmcnc/apps/maintenance_app/img/spindle_info_button.png"
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

    FloatLayout:
        LabelBase:
            id: min_speed_label
            x: cooldown_speed_slider.pos[0]
            y: cooldown_speed_slider.pos[1] - cooldown_speed_slider.size[1] * 0.1
            size_hint: None, None
            height: dp(0.0625*app.height)
            width: dp(0.0375*app.width)
            color: hex('#888888ff')
            font_size: dp(0.01625*app.width)

        LabelBase:
            id: max_speed_label
            x: cooldown_speed_slider.pos[0] + cooldown_speed_slider.size[0] * 0.9
            y: cooldown_speed_slider.pos[1] - cooldown_speed_slider.size[1] * 0.1
            size_hint: None, None
            height: dp(0.0625*app.height)
            width: dp(0.0375*app.width)
            color: hex('#888888ff')
            font_size: dp(0.01625*app.width)

        LabelBase:
            id: min_time_label
            x: cooldown_time_slider.pos[0]
            y: cooldown_time_slider.pos[1] - cooldown_time_slider.size[1] * 0.1
            size_hint: None, None
            height: dp(0.0625*app.height)
            width: dp(0.0375*app.width)
            color: hex('#888888ff')
            font_size: dp(0.01625*app.width)

        LabelBase:
            id: max_time_label
            x: cooldown_time_slider.pos[0] + cooldown_time_slider.size[0] * 0.9
            y: cooldown_time_slider.pos[1] - cooldown_time_slider.size[1] * 0.1
            size_hint: None, None
            height: dp(0.0625*app.height)
            width: dp(0.0375*app.width)
            color: hex('#888888ff')
            font_size: dp(0.01625*app.width)



"""
)


class SpindleSettingsWidget(Widget):
    brand_list_sc1 = [
        " YETI SC1 digital 230V",
        " YETI SC1 digital 110V",
        " AMB digital 230V",
        " AMB manual 230V",
        " AMB manual 110V",
    ]
    brand_list_sc2 = [
         " YETI SC2 digital 230V",
         " YETI SC2 digital 110V",
    ] + brand_list_sc1

    def __init__(self, **kwargs):
        super(SpindleSettingsWidget, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.rpm_override = self.m.spindle_cooldown_rpm_override
        self.cooldown_speed_slider.bind(value=self.cooldown_speed_updated)
        self.cooldown_time_slider.bind(value=self.cooldown_time_updated)
        self.spindle_save_widget = widget_maintenance_spindle_save.SpindleSaveWidget(
            machine=self.m, screen_manager=self.sm, localization=self.l
        )
        self.spindle_save_container.add_widget(self.spindle_save_widget)
        self.update_strings()

        self.wait_popup = InfoPopup(sm=self.sm, m=self.m, l=self.l,
                                    main_string="SmartBench is raising the Z axis.",
                                    title=self.l.get_str("Please wait") + "...",
                                    main_layout_padding=(40, 20, 40, 20), main_layout_spacing=10,
                                    main_label_size_delta=140,
                                    popup_width=500, popup_height=200, button_one_text=None, auto_dismiss=True)

    def cooldown_speed_updated(self, instance, value):
        self.rpm_label.text = "%i " % value + self.l.get_str("RPM")
        self.rpm_override = True

    def cooldown_time_updated(self, instance, value):
        self.seconds_label.text = "%i " % value + self.l.get_str("seconds")

    def autofill_rpm_time(self):
        if "AMB" in self.spindle_brand.text:
            self.cooldown_time_slider.value = 30
            self.cooldown_speed_slider.value = self.m.amb_cooldown_rpm_default
        if "YETI" in self.spindle_brand.text:
            self.cooldown_time_slider.value = 10
            self.cooldown_speed_slider.value = self.m.yeti_cooldown_rpm_default
        if "manual" in self.spindle_brand.text:
            self.cooldown_speed_slider.disabled = True
        if "digital" in self.spindle_brand.text:
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

    def show_spindle_data_popup(self):
        self.shc_popup = SpindleHealthCheckPopup(self.m, size_hint=(0.8, 0.8), callback=self.raise_z_then_get_data)
        self.shc_popup.open()

    def raise_z_then_get_data(self, *args):
        self.shc_popup.dismiss()
        if self.m.state().startswith("Idle"):
            self.wait_popup.open()
            self.m.raise_z_axis_for_collet_access()
            Clock.schedule_once(self.get_spindle_data, 0.4)
        else:
            self.sm.pm.show_error_popup("Please ensure machine is idle before continuing.")

    def get_spindle_data(self, dt):
        if not self.m.smartbench_is_busy():
            self.wait_popup.dismiss()
            self.wait_popup.open()
            self.m.turn_on_spindle_for_data_read()
            Clock.schedule_once(self.get_spindle_info, 0.3)
        else:
            Clock.schedule_once(self.get_spindle_data, 0.4)

    def get_spindle_info(self, dt):
        self.m.s.write_protocol(
            self.m.p.GetDigitalSpindleInfo(), "GET DIGITAL SPINDLE INFO"
        )
        self.check_info_count = 0
        Clock.schedule_once(self.check_spindle_info, 0.3)

    def check_spindle_info(self, dt):
        self.check_info_count += 1
        if (
                self.m.s.digital_spindle_ld_qdA != -999
                and self.m.s.spindle_serial_number not in [None, -999, 999]
                or self.check_info_count > 10
        ):
            self.read_restore_info()
        else:
            Clock.schedule_once(self.check_spindle_info, 0.3)

    def read_restore_info(self):
        self.m.turn_off_spindle()
        self.wait_popup.dismiss()
        if (
                self.m.s.digital_spindle_ld_qdA != -999
                and self.m.s.spindle_serial_number not in [None, -999, 999]
        ):
            PopupDisplaySpindleData(self.sm, self.l, self.m.s)
        else:
            error_message = (
                    self.l.get_str("No SC2 Spindle motor detected.")
                    + " "
                    + self.l.get_str("Please check your connections.")
            )
            self.sm.pm.show_error_popup(error_message)

    def update_strings(self):
        self.rpm_label.text = self.l.get_str("RPM")
        self.seconds_label.text = self.l.get_str("seconds")
        self.cooldown_settings_label.text = self.l.get_bold("SPINDLE COOLDOWN SETTINGS")
        self.get_data_label.text = self.l.get_bold("Get data")
        self.min_speed_label.text = "10000 " + self.l.get_str("RPM")
        self.max_speed_label.text = "20000 " + self.l.get_str("RPM")
        self.min_time_label.text = "1 " + self.l.get_str("seconds")
        self.max_time_label.text = "60 " + self.l.get_str("seconds")
        self.update_font_size(self.cooldown_settings_label)

    def update_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length > 33:
            value.font_size = 0.0275 * Window.width
        else:
            value.font_size = 0.03 * Window.width
