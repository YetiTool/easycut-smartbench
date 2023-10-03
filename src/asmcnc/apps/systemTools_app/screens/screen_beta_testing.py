'''
Created on 18 November 2020
Beta testers screen for system tools app

@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from asmcnc.comms import usb_storage
from asmcnc.apps.systemTools_app.screens import popup_system
from asmcnc.skavaUI import popup_info
from kivy.clock import Clock

import os, sys

Builder.load_string("""

#:import Factory kivy.factory.Factory


<BetaLanguageSpinner@SpinnerOption>

    background_normal: ''
    background_color: [1,1,1,1]
    height: dp(40)
    color: 0,0,0,1
    halign: 'left'
    markup: 'True'
    font_size: 18

<BetaTestingScreen>

    user_branch: user_branch
    beta_version: beta_version
    language_button : language_button
    usb_toggle: usb_toggle
    wifi_toggle: wifi_toggle

    on_touch_down: root.on_touch()

    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas.before:
            Color: 
                rgba: hex('#e5e5e5ff')
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding: 0
            spacing: 10
            orientation: "vertical"
            BoxLayout:
                padding: 0
                spacing: 0
                canvas:
                    Color:
                        rgba: hex('#1976d2ff')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    size_hint: (None,None)
                    height: dp(60)
                    width: dp(800)
                    text: "Beta Testing"
                    color: hex('#f9f9f9ff')
                    font_size: 30
                    halign: "center"
                    valign: "bottom"
                    markup: True
                   
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(320)
                padding: 0
                spacing: 10
                orientation: 'horizontal'

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(600)
                    height: dp(320)
                    padding: [40,20]
                    spacing: 20
                    orientation: 'vertical'

                    GridLayout:
                        pos: self.parent.pos
                        cols: 2
                        rows: 0
                        padding: 0
                        size_hint_y: 0.6

                        Label
                            text: 'Run developer branch:'
                            color: [0,0,0,1]
                            font_size: 20
                            halign: "left"
                            markup: True
                            text_size: self.size

                        TextInput:
                            id: user_branch
                            text: 'branch'
                            multiline: False
                            font_size: 20

                    Button:
                        text: 'Checkout and pull (uses wifi)'
                        on_press: root.checkout_branch()

                    GridLayout:
                        size_hint_y: 0.4
                        pos: self.parent.pos
                        cols: 2
                        rows: 0
                        padding: 0

                        Label:
                            text: 'Latest beta version:'
                            color: [0,0,0,1]
                            font_size: 20
                            markup: True
                            halign: "left"

                        Label:
                            id: beta_version
                            text: 'beta_version_no'
                            color: [0,0,0,1]
                            font_size: 20
                            markup: True
                            halign: "left"

                    Button:
                        text: 'Update to beta'
                        on_press: root.update_to_latest_beta()


                BoxLayout:
                    size_hint: (None,None)
                    width: dp(190)
                    height: dp(320)
                    padding: 0
                    spacing: 0
                    orientation: 'vertical'

                    Spinner:
                        id: language_button
                        size_hint: (None,None)
                        height: dp(35)
                        width: dp(180)
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
                        width: dp(192.5)
                        height: dp(120)
                        orientation: 'horizontal'
                        padding: [20, 30]
                        ToggleButton:
                            id: usb_toggle
                            text: 'USB'
                            group: 'wifi-usb'
                        ToggleButton:
                            id: wifi_toggle
                            text: 'WIFI'
                            group: 'wifi-usb'
                            state: 'down'
                    BoxLayout:
                        size_hint: (None,None)
                        width: dp(192.5)
                        height: dp(120)
                        padding: [81.75, 45]
                        spacing: 0

                        Button:
                            size_hint: (None,None)
                            height: dp(30)
                            width: dp(29)
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.refresh_latest_software_version()
                            BoxLayout:
                                padding: 0
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
                width: dp(800)
                height: dp(80)
                padding: 0
                spacing: 10
                orientation: 'horizontal'

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(80)
                    height: dp(80)
                    padding: 0
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(80)
                        width: dp(80)
                        padding: [10, 10, 10, 10]
                        Button:
                            size_hint: (None,None)
                            height: dp(52)
                            width: dp(60)
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.go_back()
                            BoxLayout:
                                padding: 0
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
                    width: dp(620)
                    height: dp(80)
                    padding: 10
                    spacing: 0
                    orientation: 'vertical'

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(80)
                    height: dp(80)
                    padding: 0
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(80)
                        width: dp(80)
                        padding: [19, 10, 10, 10]
                        Button:
                            size_hint: (None,None)
                            height: dp(60)
                            width: dp(51)
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.exit_app()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/systemTools_app/img/back_to_lobby.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True


""")

class BetaTestingScreen(Screen):

    reset_language = False

    def __init__(self, **kwargs):
        super(BetaTestingScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.set = kwargs['settings']
        self.l = kwargs['localization']
        self.kb = kwargs['keyboard']

        self.user_branch.text = (self.set.sw_branch).strip('* ')
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
        if sys.platform != 'win32' and sys.platform != 'darwin':

            message = (
                self.l.get_str('Please wait') + \
                '...\n' + \
                self.l.get_str('Console will reboot to finish update.')
                )
            wait_popup = popup_info.PopupWait(self.systemtools_sm.sm, self.l, description = message)


            def nested_branch_update(dt):

                # Update config as for any other SW release
                self.set.update_config() 
                
                # Strip whitespace
                branch_name_formatted = str(self.user_branch.text).translate(None, ' ')

                checkout_exit_code = os.system(
                    "cd /home/pi/easycut-smartbench/ && git fetch origin && git checkout " + branch_name_formatted)
                pull_exit_code = os.system("git pull")
                
                # exit code 0 means success, anything else is error
                if checkout_exit_code == 0 and pull_exit_code == 0:
                    self.set.ansible_service_run_without_reboot()
                    wait_popup.popup.dismiss()
                    self.systemtools_sm.sm.current = 'rebooting'
                else:
                    wait_popup.popup.dismiss()
                    message = (self.l.get_str("Failed to checkout and pull branch.") + \
                        '\n' + \
                        self.l.get_str("Please check the spelling of your branch and your internet connection."))
                    error_popup = popup_info.PopupError(self.systemtools_sm.sm, self.l, message)

            Clock.schedule_once(nested_branch_update, 0.5)

    def update_to_latest_beta(self):
        if self.wifi_toggle.state == 'down':
            self.set.get_sw_update_via_wifi(beta=True)
        elif self.usb_toggle.state == 'down':
            self.set.get_sw_update_via_usb(beta=True)
        self.usb_stick.disable()
        self.systemtools_sm.sm.current = 'rebooting'

    def refresh_latest_software_version(self):
        self.set.refresh_latest_sw_version()
        self.user_branch.text = (self.set.sw_branch).strip('*')
        self.beta_version.text = self.set.latest_sw_beta

    ## LOCALIZATION TESTING

    def choose_language(self):
        chosen_lang = self.language_button.text
        self.l.load_in_new_language(chosen_lang)
        self.restart_app()
        self.reset_language = True

    def restart_app(self):
        if self.reset_language == True: 
            popup_system.RebootAfterLanguageChange(self.systemtools_sm, self.l)
