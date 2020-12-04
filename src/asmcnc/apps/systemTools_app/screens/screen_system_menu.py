'''
Created on 18 November 2020
Menu screen for system tools app

@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
import sys

from asmcnc.skavaUI import popup_info
from asmcnc.apps.systemTools_app.screens import popup_system

Builder.load_string("""

<SystemMenuScreen>

    canvas.before:
        Color: 
            rgba: hex('#f9f9f9ff')
        Rectangle: 
            size: self.size
            pos: self.pos

    GridLayout:
        size: self.parent.size
        pos: self.parent.pos
        padding: [dp(8.33), dp(60)]
        spacing: [dp(8.33), dp(60)]
        cols: 5
        rows: 2

		Button:
			text: 'System Info'
			on_press: root.go_to_build_info()
            background_normal: ''
            background_color: hex('#f9f9f9ff')
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/apps/systemTools_app/img/system_info.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

		Button:
			text: 'Download Logs'
			on_press: root.download_logs()
            background_normal: ''
            background_color: hex('#f9f9f9ff')
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/apps/systemTools_app/img/system_info.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

		Button:
			text: 'Reboot'
			on_press: root.reboot()
            background_normal: ''
            background_color: hex('#f9f9f9ff')
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/apps/systemTools_app/img/system_info.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

        Button:
            text: 'Quit to Console'
            on_press: root.quit_to_console()
            background_normal: ''
            background_color: hex('#f9f9f9ff')
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/apps/systemTools_app/img/system_info.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

		Button:
			text: 'Beta Testing'
			on_press: root.beta_testing()
            background_normal: ''
            background_color: hex('#f9f9f9ff')
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/apps/systemTools_app/img/system_info.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

		Button:
			text: 'GRBL Settings'
			on_press: root.grbl_settings()
            background_normal: ''
            background_color: hex('#f9f9f9ff')
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/apps/systemTools_app/img/system_info.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

		Button:
			text: 'Factory Settings'
			on_press: root.factory_settings()
            background_normal: ''
            background_color: hex('#f9f9f9ff')
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/apps/systemTools_app/img/system_info.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

        Button:
            text: 'Update testing'
            on_press: root.update_testing()
            background_normal: ''
            background_color: hex('#f9f9f9ff')
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/apps/systemTools_app/img/system_info.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

		Button:
			text: 'Developer'
			on_press: root.developer()
            background_normal: ''
            background_color: hex('#f9f9f9ff')
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/apps/systemTools_app/img/system_info.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

        Button:
            text: 'Go Back'
            on_press: root.go_back()
            background_normal: ''
            background_color: hex('#f9f9f9ff')
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/apps/systemTools_app/img/system_info.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

""")

class SystemMenuScreen(Screen):

    def __init__(self, **kwargs):
        super(SystemMenuScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']

    def go_back(self):
    	self.systemtools_sm.exit_app()

    def go_to_build_info(self):
    	self.systemtools_sm.open_build_info_screen()

    def download_logs(self):
        self.systemtools_sm.download_logs_to_usb()

    def reboot(self):
        self.systemtools_sm.sm.current = 'rebooting'

    def quit_to_console(self):
        print 'Bye!'
        sys.exit()

    def beta_testing(self):
        popup_system.PopupBetaTesting(self.systemtools_sm)

    def grbl_settings(self):
    	popup_system.PopupGRBLSettingsPassword(self.systemtools_sm)

    def factory_settings(self):
    	popup_system.PopupFactorySettingsPassword(self.systemtools_sm)

    def update_testing(self):
        popup_system.PopupUpdateTestingPassword(self.systemtools_sm)

    def developer(self):
    	popup_system.PopupDeveloperPassword(self.systemtools_sm)









