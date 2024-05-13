from asmcnc.comms.logging_system.logging_system import Logger
from kivy.core.window import Window
from datetime import datetime
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from asmcnc.core_UI.popups import ErrorPopup


Builder.load_string("""
#:import LabelBase asmcnc.core_UI.components.labels.base_label

<UpgradeScreen>:

    title_label:title_label
    instruction_label:instruction_label
    support_label:support_label
    spindle_label:spindle_label
    error_label:error_label

    upgrade_code_input:upgrade_code_input

    qr_image:qr_image

    exit_button:exit_button
    
    on_touch_down: root.on_touch()

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'

            canvas:
                Color:
                    rgba: color_provider.get_rgba("blue")
                Rectangle:
                    size: self.size
                    pos: self.pos

            BoxLayout:
                padding:[dp(0.075)*app.width, 0, 0, 0]

                LabelBase:
                    id: title_label
                    text: 'Upgrade SB V1.3 to PrecisionPro +'
                    halign: 'center'
                    valign: 'middle'
                    font_size: dp(0.0375*app.width)
                    text_size: self.size

            BoxLayout:
                size_hint_x: 0.08
                padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]

                Button:
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: exit_button
                    size_hint: (None,None)
                    height: dp(0.104166666667*app.height)
                    width: dp(0.0625*app.width)
                    background_color: color_provider.get_rgba("transparent")
                    opacity: 1
                    on_press: root.quit_to_lobby()
                    BoxLayout:
                        padding: 0
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/shapeCutter_app/img/exit_icon.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 7
            padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]

            canvas: 
                Color:
                    rgba: color_provider.get_rgba("light_grey")
                Rectangle:
                    size: self.size
                    pos: self.pos

            BoxLayout:
                orientation: 'vertical'

                LabelBase:
                    id: instruction_label
                    size_hint_y: 2
                    font_size: dp(0.03*app.width)
                    color: color_provider.get_rgba("black")
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size

                BoxLayout:
                    padding:[dp(0.25)*app.width, 0, dp(0.25)*app.width, dp(0.0416666666667)*app.height]

                    TextInput:
                        id: upgrade_code_input
                        font_size: dp(0.0375*app.width)
                        multiline: False
                        valign: 'middle'
                        halign: 'center'
                        on_text_validate: root.code_entered()

            BoxLayout:
                orientation: 'vertical'
                size_hint_y: 1.15

                BoxLayout:
                    orientation:'vertical'

                    LabelBase:
                        id: error_label
                        size_hint_y: 0
                        height: 0
                        font_size: dp(0.02875*app.width)
                        color: color_provider.get_rgba("monochrome_red")
                        halign: 'center'
                        valign: 'middle'
                        text_size: self.size

                    BoxLayout:
                        orientation: 'vertical'

                        LabelBase:
                            id: support_label
                            size_hint_y: 1.5
                            font_size: dp(0.03*app.width)
                            color: color_provider.get_rgba("black")
                            halign: 'center'
                            valign: 'middle'
                            text_size: self.size

                        Image:
                            id: qr_image
                            size_hint_y: 2
                            source: "./asmcnc/apps/upgrade_app/img/qr_upgrade.png"

                        LabelBase:
                            id: spindle_label
                            font_size: dp(0.025*app.width)
                            color: color_provider.get_rgba("black")
                            halign: 'center'
                            valign: 'middle'
                            text_size: self.size

                BoxLayout:
                    size_hint_y: 0
                    height: 0

"""
)


class UpgradeScreen(Screen):
    def __init__(self, **kwargs):
        super(UpgradeScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.kb = kwargs["keyboard"]
        # Add the IDs of ALL the TextInputs on this screen
        self.text_inputs = [self.upgrade_code_input]

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def on_pre_enter(self):
        # Reset app
        self.update_strings()
        self.hide_error_message()
        self.m.write_dollar_setting(51, 1)

    def on_enter(self):
        self.kb.setup_text_inputs(self.text_inputs)

    def quit_to_lobby(self):
        self.sm.current = "lobby"
        self.m.write_dollar_setting(51, 0)

    def get_correct_unlock_code(self, serial):
        try:
            return str(hex((serial + 42) * 10000))[2:]
        except TypeError:
            return 1

    def code_entered(self):
        self.hide_error_message()
        self.show_verifying()
        self.m.turn_on_spindle_for_data_read()
        Clock.schedule_once(self.get_restore_info, 0.3)

    def get_restore_info(self, dt):
        self.m.s.write_protocol(
            self.m.p.GetDigitalSpindleInfo(), "GET DIGITAL SPINDLE INFO"
        )
        self.check_info_count = 0
        Clock.schedule_once(self.check_restore_info, 0.3)

    def check_restore_info(self, dt):
        self.check_info_count += 1
        # Value of -999 represents disconnected spindle - if detected then stop waiting
        if (
            self.m.s.digital_spindle_ld_qdA != -999
            and self.m.s.spindle_serial_number not in [None, -999, 999]
            or self.check_info_count > 10
        ):
            self.read_restore_info()
        else: # Keep trying for a few seconds
            Clock.schedule_once(self.check_restore_info, 0.3)

    def read_restore_info(self):
        self.m.turn_off_spindle()
        self.hide_verifying()
        # Value of -999 for ld_qdA represents disconnected spindle
        if (
            # Get info was successful, show serial and check code
            self.m.s.digital_spindle_ld_qdA != -999
            and self.m.s.spindle_serial_number not in [None, -999, 999]
        ):
            self.spindle_label.text = (
                self.l.get_str("Need support?")
                + " "
                + self.l.get_str("Quote Spindle motor number: NN").replace(
                    "NN", str(self.m.s.spindle_serial_number)
                )
            )
            self.check_unlock_code()
        else:
            # Otherwise, spindle is probably disconnected
            self.show_error_message(
                self.l.get_str("No SC2 Spindle motor detected.")
                + " "
                + self.l.get_str("Please check your connections.")
            )
            self.spindle_label.text = (
                self.l.get_str("Need support?") + " " + self.l.get_str('Quote "No SC2"')
            )

    def check_unlock_code(self):
        correct_unlock_code = self.get_correct_unlock_code(
            self.m.s.spindle_serial_number
        )
        entered_unlock_code = self.upgrade_code_input.text.lower().replace("o", "0")
        if correct_unlock_code == entered_unlock_code:
            self.upgrade_and_proceed()
        else:
            self.show_error_message(
                self.l.get_str("Upgrade code incorrect, please check it and try again.")
            )

    def upgrade_and_proceed(self):
        try:
            self.update_spindle_cooldown_settings()
            self.m.enable_theateam()
            self.sm.current = "upgrade_successful"
        except:
            ErrorPopup(sm=self.sm, l=self.l, main_string=self.l.get_str("Error!")).open()
            Logger.info("Failed to create SC2 compatibility file!")

    def update_spindle_cooldown_settings(self):
        # Write default SC2 settings, and set voltage to whatever is already selected
        if not (
            self.m.write_spindle_cooldown_rpm_override_settings(False)
            and self.m.write_spindle_cooldown_settings(
                brand="YETI SC2",
                voltage=self.m.spindle_voltage,
                digital=True,
                time_seconds=10,
                rpm=self.m.yeti_cooldown_rpm_default,
            )
        ):
            ErrorPopup(
                sm=self.sm,
                l=self.l,
                main_string=self.l.get_str("There was a problem saving your settings."),
            ).open()

    def show_error_message(self, error_message):
        self.error_label.text = error_message
        self.error_label.size_hint_y = 0.15
        self.support_label.parent.padding = [0, 5, 0, 0]

    def hide_error_message(self):
        self.error_label.text = ""
        self.error_label.size_hint_y = 0
        self.support_label.parent.padding = [0, 0, 0, 0]

    def show_verifying(self):
        # Spindle label text is updated separately
        self.support_label.text = self.l.get_str("Verifying upgrade code...")
        self.support_label.font_size = 0.04 * Window.width
        self.spindle_label.text = ""
        self.qr_image.opacity = 0
        self.upgrade_code_input.disabled = True
        self.exit_button.disabled = True
        self.exit_button.opacity = 0

    def hide_verifying(self):
        self.support_label.text = self.l.get_str(
            "For more information about upgrades, please contact your place of purchase or visit www.yetitool.com"
        )
        self.support_label.font_size = 0.03 * Window.width
        self.qr_image.opacity = 1
        self.upgrade_code_input.disabled = False
        self.exit_button.disabled = False
        self.exit_button.opacity = 1

    def update_strings(self):
        self.title_label.text = self.l.get_str("Upgrade SB V1.3 to PrecisionPro +")
        self.instruction_label.text = (
            "1. "
            + self.l.get_str(
                "Plug in your SC2 Spindle motor (both power and data cable)"
            )
            + "\n"
            + "2. "
            + self.l.get_str("Type in your upgrade code below")
            + "\n"
            + "3. "
            + self.l.get_str('Press "Enter" on the keyboard')
        )
        self.support_label.text = self.l.get_str(
            "For more information about upgrades, please contact your place of purchase or visit www.yetitool.com"
        )
        self.spindle_label.text = self.l.get_str("Looking for Spindle motor...")
