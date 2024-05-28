from enum import Enum
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from asmcnc.core_UI.job_go.screens.screen_spindle_health_check import (
    SpindleHealthCheckActiveScreen,
)

Builder.load_string(
    """

<DisabledYetiPilotWidget>:
    
    text_container:text_container
    body_label:body_label

    button_container:button_container
    health_check_button:health_check_button
    health_check_button_img:health_check_button_img

    BoxLayout:
        orientation: 'horizontal'
        size: self.parent.size
        pos: self.parent.pos
        padding:[dp(0.0125)*app.width, dp(0.0166666666667)*app.height, dp(0.0125)*app.width, dp(0.0166666666667)*app.height]

        BoxLayout:
            id: text_container
            size_hint_x: 0.85
            orientation: 'vertical'
            padding:[dp(0.0025)*app.width, 0, dp(0.00625)*app.width, 0]
            spacing: 0

            ScrollView:
                do_scroll_x: False
                do_scroll_y: True
                scroll_y: 1
                bar_width: 0.005*app.width
                bar_inactive_color: [.7, .7, .7, .7]

                Label:
                    id: body_label
                    size_hint_y: None
                    color: hex('#333333ff')
                    markup: True
                    halign: 'left'
                    height: self.texture_size[1]
                    text_size: self.width - dp(3.0/800.0)*app.width, None
                    font_size: str(0.01875*app.width) + 'sp'
                    valign: "middle"
                    max_lines: 60

        BoxLayout: 
            id: button_container
            size_hint_x: 0.15

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                id: health_check_button
                size_hint_x: 1
                disabled: False
                background_color: hex('#F4433600')

                on_press:
                    root.run_spindle_health_check()

                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: health_check_button_img
                        # source: "./asmcnc/core_UI/job_go/img/spindle_check_silver.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: False
                
"""
)


class DisabledYPCase(Enum):
    DISABLED = 0
    FAILED_AND_CAN_RUN_AGAIN = 1
    FAILED = 2


class DisabledYetiPilotWidget(Widget):
    health_check_enabled_img = "./asmcnc/core_UI/job_go/img/spindle_check_silver.png"
    health_check_disabled_img = "./asmcnc/core_UI/job_go/img/spindle_check_disabled.png"
    font_str = "[size=%dsp]"
    bigger_font_str = font_str % float(17.0 / 800.0 * Window.width)
    smaller_font_str = font_str % float(15.0 / 800.0 * Window.width)

    def __init__(self, **kwargs):
        self.sm = kwargs.pop("screen_manager")
        self.l = kwargs.pop("localization")
        self.m = kwargs.pop("machine")
        self.db = kwargs.pop("database")
        self.yp = kwargs.pop("yetipilot")
        super(DisabledYetiPilotWidget, self).__init__(**kwargs)
        self.yp.disable()
        self.update_strings()

    def set_version(self, case):
        self.update_strings(case=case)
        if case != DisabledYPCase.DISABLED:
            self.text_container.size_hint_x = 0.85
            self.button_container.opacity = 1
            self.button_container.size_hint_x = 0.15
        else:
            self.text_container.size_hint_x = 1
            self.button_container.opacity = 0
            self.button_container.size_hint_x = 0
        if case == DisabledYPCase.FAILED_AND_CAN_RUN_AGAIN:
            self.health_check_button.disabled = False
            self.health_check_button_img.source = self.health_check_enabled_img
        else:
            self.health_check_button.disabled = True
            self.health_check_button_img.source = self.health_check_disabled_img

    def get_translated_text_based_on_case(self, case):
        translated_text = ""
        if case == DisabledYPCase.DISABLED:
            translated_text += self.l.get_str(
                "Enable Spindle motor health check in the Maintenance app to change this."
            )
        else:
            translated_text += self.l.get_str("Spindle motor health check failed.")
            if case == DisabledYPCase.FAILED_AND_CAN_RUN_AGAIN:
                translated_text += "\n"
                translated_text += self.l.get_str(
                    "Re-run before job start to enable YetiPilot."
                )
        return translated_text

    def update_strings(self, case="disabled"):
        translated_text = self.get_translated_text_based_on_case(case)
        self.body_label.text = (
            self.bigger_font_str + self.l.get_bold("YetiPilot is disabled") + "[/size]"
        )
        self.body_label.text += "\n"
        self.body_label.text += self.smaller_font_str
        self.body_label.text += translated_text
        self.body_label.text += "[/size]"

    def run_spindle_health_check(self):
        if not self.sm.has_screen("spindle_health_check_active"):
            shc_screen = SpindleHealthCheckActiveScreen(
                name="spindle_health_check_active",
                screen_manager=self.sm,
                machine=self.m,
                localization=self.l,
            )
            self.sm.add_widget(shc_screen)
        self.sm.get_screen("spindle_health_check_active").start_after_pass = False
        self.sm.current = "spindle_health_check_active"
