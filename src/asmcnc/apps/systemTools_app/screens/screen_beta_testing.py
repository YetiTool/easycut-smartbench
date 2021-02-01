'''
Created on 18 November 2020
Beta testers screen for system tools app

@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from asmcnc.comms import usb_storage

import os, sys

Builder.load_string("""

<BetaTestingScreen>

    user_branch: user_branch
    beta_version: beta_version
    usb_toggle: usb_toggle
    wifi_toggle: wifi_toggle

    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas.before:
            Color: 
                rgba: hex('#f9f9f9ff')
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

    def __init__(self, **kwargs):
        super(BetaTestingScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.set = kwargs['settings']

        self.user_branch.text = (self.set.sw_branch).strip('*')
        self.beta_version.text = self.set.latest_sw_beta

        self.usb_stick = usb_storage.USB_storage(self.systemtools_sm.sm)

    def go_back(self):
        self.systemtools_sm.open_system_tools()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    def on_enter(self):
        self.usb_stick.enable()

    def checkout_branch(self):
        if sys.platform != 'win32' and sys.platform != 'darwin':       
            os.system("cd /home/pi/easycut-smartbench/ && git fetch origin && git checkout " + str(self.user_branch.text))
            os.system("git pull")
            self.systemtools_sm.sm.current = 'rebooting'

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
