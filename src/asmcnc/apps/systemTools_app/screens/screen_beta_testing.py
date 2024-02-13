"""
Created on 18 November 2020
Beta testers screen for system tools app

@author: Letty
"""
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from asmcnc.comms import usb_storage
from asmcnc.apps.systemTools_app.screens import popup_system
from asmcnc.skavaUI import popup_info
from kivy.clock import Clock
import os, sys

Builder.load_string(
    """

#:import Factory kivy.factory.Factory


<BetaLanguageSpinner@SpinnerOption>

    background_normal: ''
    background_color: [1,1,1,1]
    height: dp(app.get_scaled_height(40))
    color: 0,0,0,1
    halign: 'left'
    markup: 'True'
    font_size:dp(0.0225*app.width)
    font_name: 'KRFont'

<BetaTestingScreen>

    user_branch: user_branch
    beta_version: beta_version
    language_button : language_button
    usb_toggle: usb_toggle
    wifi_toggle: wifi_toggle

    on_touch_down: root.on_touch()

    BoxLayout:
        height: dp(app.get_scaled_height(800))
        width: dp(app.get_scaled_width(480))
        canvas.before:
            Color: 
                rgba: hex('#e5e5e5ff')
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding:dp(0)
            spacing:0.0208333333333*app.height
            orientation: "vertical"
            BoxLayout:
                padding:dp(0)
                spacing: 0
                canvas:
                    Color:
                        rgba: hex('#1976d2ff')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    size_hint: (None,None)
                    height: dp(app.get_scaled_height(60))
                    width: dp(app.get_scaled_width(800))
                    text: "Beta Testing"
                    color: hex('#f9f9f9ff')
                    font_size:dp(0.0375*app.width)
                    halign: "center"
                    valign: "bottom"
                    markup: True
                   
            BoxLayout:
                size_hint: (None,None)
                width: dp(app.get_scaled_width(800))
                height: dp(app.get_scaled_height(320))
                padding:dp(0)
                spacing:0.0125*app.width
                orientation: 'horizontal'

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(app.get_scaled_width(600))
                    height: dp(app.get_scaled_height(320))
                    padding:(dp(app.get_scaled_width(40)),dp(app.get_scaled_height(20)))
                    spacing:0.0416666666667*app.height
                    orientation: 'vertical'

                    GridLayout:
                        pos: self.parent.pos
                        cols: 2
                        rows: 0
                        padding:dp(0)
                        size_hint_y: 0.6

                        Label
                            text: 'Run developer branch:'
                            color: [0,0,0,1]
                            font_size:dp(0.025*app.width)
                            halign: "left"
                            markup: True
                            text_size: self.size

                        TextInput:
                            id: user_branch
                            text: 'branch'
                            multiline: False
                            font_size:dp(0.025*app.width)

                    Button:
                        font_size: str(get_scaled_width(15)) + 'sp'
                        text: 'Checkout and pull (uses wifi)'
                        on_press: root.checkout_branch()

                    GridLayout:
                        size_hint_y: 0.4
                        pos: self.parent.pos
                        cols: 2
                        rows: 0
                        padding:dp(0)

                        Label:
                            text: 'Latest beta version:'
                            color: [0,0,0,1]
                            font_size:dp(0.025*app.width)
                            markup: True
                            halign: "left"

                        Label:
                            id: beta_version
                            text: 'beta_version_no'
                            color: [0,0,0,1]
                            font_size:dp(0.025*app.width)
                            markup: True
                            halign: "left"

                    Button:
                        font_size: str(get_scaled_width(15)) + 'sp'
                        text: 'Update to beta'
                        on_press: root.update_to_latest_beta()


                BoxLayout:
                    size_hint: (None,None)
                    width: dp(app.get_scaled_width(190))
                    height: dp(app.get_scaled_height(320))
                    padding:dp(0)
                    spacing: 0
                    orientation: 'vertical'

                    Spinner:
                        font_size: str(get_scaled_width(15)) + 'sp'
                        id: language_button
                        size_hint: (None,None)
                        height: dp(app.get_scaled_height(35))
                        width: dp(app.get_scaled_width(180))
                        background_normal: "./asmcnc/apps/systemTools_app/img/word_button.png"
                        background_down: ""
                        border: [dp(7.5)]*4
                        center: self.parent.center
                        pos: self.parent.pos
                        text: 'Choose language...'
                        color: hex('#f9f9f9ff')
                        markup: True
                        option_cls: Factory.get("BetaLanguageSpinner")
                        on_text: root.choose_language()

                    BoxLayout:
                        size_hint: (None,None)
                        width: dp(app.get_scaled_width(192.5))
                        height: dp(app.get_scaled_height(120))
                        orientation: 'horizontal'
                        padding:(dp(app.get_scaled_width(20)),dp(app.get_scaled_height(30)))
                        ToggleButton:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            id: usb_toggle
                            text: 'USB'
                            group: 'wifi-usb'
                        ToggleButton:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            id: wifi_toggle
                            text: 'WIFI'
                            group: 'wifi-usb'
                            state: 'down'
                    BoxLayout:
                        size_hint: (None,None)
                        width: dp(app.get_scaled_width(192.5))
                        height: dp(app.get_scaled_height(120))
                        padding:(dp(app.get_scaled_width(81.75)),dp(app.get_scaled_height(45)))
                        spacing: 0

                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(30))
                            width: dp(app.get_scaled_width(29))
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.refresh_latest_software_version()
                            BoxLayout:
                                padding:dp(0)
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/wifi_app/img/mini_refresh.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True

            BoxLayout:
                size_hint: (None,None)
                width: dp(app.get_scaled_width(800))
                height: dp(app.get_scaled_height(80))
                padding:dp(0)
                spacing:0.0125*app.width
                orientation: 'horizontal'

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(app.get_scaled_width(80))
                    height: dp(app.get_scaled_height(80))
                    padding:dp(0)
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(app.get_scaled_height(80))
                        width: dp(app.get_scaled_width(80))
                        padding:(dp(app.get_scaled_width(10)),dp(app.get_scaled_height(10)),dp(app.get_scaled_width(10)),dp(app.get_scaled_height(10)))
                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(52))
                            width: dp(app.get_scaled_width(60))
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.go_back()
                            BoxLayout:
                                padding:dp(0)
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/systemTools_app/img/back_to_menu.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(app.get_scaled_width(620))
                    height: dp(app.get_scaled_height(80))
                    padding:(dp(app.get_scaled_width(10)),dp(app.get_scaled_height(10)))
                    spacing: 0
                    orientation: 'vertical'

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(app.get_scaled_width(80))
                    height: dp(app.get_scaled_height(80))
                    padding:dp(0)
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(app.get_scaled_height(80))
                        width: dp(app.get_scaled_width(80))
                        padding:(dp(app.get_scaled_width(19)),dp(app.get_scaled_height(10)),dp(app.get_scaled_width(19)),dp(app.get_scaled_height(10)))
                        Button:
                            font_size: str(get_scaled_width(15)) + 'sp'
                            size_hint: (None,None)
                            height: dp(app.get_scaled_height(60))
                            width: dp(app.get_scaled_width(51))
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.exit_app()
                            BoxLayout:
                                padding:dp(0)
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/systemTools_app/img/back_to_lobby.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True


"""
)


class BetaTestingScreen(Screen):
    reset_language = False

    def __init__(self, **kwargs):
        super(BetaTestingScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs["system_tools"]
        self.set = kwargs["settings"]
        self.l = kwargs["localization"]
        self.kb = kwargs["keyboard"]
        self.user_branch.text = self.set.sw_branch.strip("* ")
        self.beta_version.text = self.set.latest_sw_beta
        self.usb_stick = usb_storage.USB_storage(self.systemtools_sm.sm, self.l)
        self.language_button.values = self.l.supported_languages
        self.language_button.text = self.l.lang
        self.text_inputs = [self.user_branch]

    def go_back(self):
        self.systemtools_sm.open_system_tools()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    def on_enter(self):
        self.language_button.text = self.l.lang
        self.usb_stick.enable()
        self.kb.setup_text_inputs(self.text_inputs)

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def checkout_branch(self):
        if sys.platform != "win32" and sys.platform != "darwin":
            message = (
                self.l.get_str("Please wait")
                + "...\n"
                + self.l.get_str("Console will reboot to finish update.")
            )
            wait_popup = popup_info.PopupWait(
                self.systemtools_sm.sm, self.l, description=message
            )

            def nested_branch_update(dt):
                self.set.update_config()
                branch_name_formatted = str(self.user_branch.text).translate(None, " ")
                checkout_exit_code = os.system(
                    "cd /home/pi/easycut-smartbench/ && git fetch origin && git checkout "
                    + branch_name_formatted
                )
                pull_exit_code = os.system("git pull")
                if checkout_exit_code == 0 and pull_exit_code == 0:
                    self.set.ansible_service_run_without_reboot()
                    wait_popup.popup.dismiss()
                    self.systemtools_sm.sm.current = "rebooting"
                else:
                    wait_popup.popup.dismiss()
                    message = (
                        self.l.get_str("Failed to checkout and pull branch.")
                        + "\n"
                        + self.l.get_str(
                            "Please check the spelling of your branch and your internet connection."
                        )
                    )
                    error_popup = popup_info.PopupError(
                        self.systemtools_sm.sm, self.l, message
                    )

            Clock.schedule_once(nested_branch_update, 0.5)

    def update_to_latest_beta(self):
        if self.wifi_toggle.state == "down":
            self.set.get_sw_update_via_wifi(beta=True)
        elif self.usb_toggle.state == "down":
            self.set.get_sw_update_via_usb(beta=True)
        self.usb_stick.disable()
        self.systemtools_sm.sm.current = "rebooting"

    def refresh_latest_software_version(self):
        self.set.refresh_latest_sw_version()
        self.user_branch.text = self.set.sw_branch.strip("*")
        self.beta_version.text = self.set.latest_sw_beta

    def choose_language(self):
        chosen_lang = self.language_button.text
        self.l.load_in_new_language(chosen_lang)
        self.restart_app()
        self.reset_language = True

    def restart_app(self):
        if self.reset_language == True:
            popup_system.RebootAfterLanguageChange(self.systemtools_sm, self.l)
