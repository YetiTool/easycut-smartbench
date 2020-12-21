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
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: '16sp'
            text_size: self.size
			on_press: root.go_to_build_info()
            # background_normal: ''
            background_color: hex('#f9f9f9ff')
            background_normal: "./asmcnc/apps/systemTools_app/img/system_info.png"
            background_down: "./asmcnc/apps/systemTools_app/img/system_info.png"
            border: [dp(25)]*4
            # BoxLayout:
            #     padding: 0
            #     size: self.parent.size
            #     pos: self.parent.pos
            #     Image:
            #         source: "./asmcnc/apps/systemTools_app/img/system_info.png"
            #         center_x: self.parent.center_x
            #         y: self.parent.y
            #         size: self.parent.width, self.parent.height
            #         allow_stretch: True

		Button:
			text: 'Download Logs'
			on_press: root.download_logs()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: '16sp'
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/download_logs.png"
            background_down: "./asmcnc/apps/systemTools_app/img/download_logs.png"
            border: [dp(25)]*4
            # BoxLayout:
            #     padding: 0
            #     size: self.parent.size
            #     pos: self.parent.pos
            #     Image:
            #         source: "./asmcnc/apps/systemTools_app/img/download_logs.png"
            #         center_x: self.parent.center_x
            #         y: self.parent.y
            #         size: self.parent.width, self.parent.height
            #         allow_stretch: True

		Button:
			text: 'Reboot'
			on_press: root.reboot()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: '16sp'
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/reboot_console.png"
            background_down: "./asmcnc/apps/systemTools_app/img/reboot_console.png"
            border: [dp(25)]*4
            # BoxLayout:
            #     padding: 0
            #     size: self.parent.size
            #     pos: self.parent.pos
            #     Image:
            #         source: "./asmcnc/apps/systemTools_app/img/reboot_console.png"
            #         center_x: self.parent.center_x
            #         y: self.parent.y
            #         size: self.parent.width, self.parent.height
            #         allow_stretch: True

        Button:
            text: 'Quit to Console'
            on_press: root.quit_to_console()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: '16sp'
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/quit_to_console.png"
            background_down: "./asmcnc/apps/systemTools_app/img/quit_to_console.png"
            border: [dp(25)]*4
            # BoxLayout:
            #     padding: 0
            #     size: self.parent.size
            #     pos: self.parent.pos
            #     Image:
            #         source: "./asmcnc/apps/systemTools_app/img/quit_to_console.png"
            #         center_x: self.parent.center_x
            #         y: self.parent.y
            #         size: self.parent.width, self.parent.height
            #         allow_stretch: True

		Button:
			text: 'Beta Testing'
			on_press: root.beta_testing()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: '16sp'
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/beta_testing.png"
            background_down: "./asmcnc/apps/systemTools_app/img/beta_testing.png"
            border: [dp(25)]*4
            # BoxLayout:
            #     padding: 0
            #     size: self.parent.size
            #     pos: self.parent.pos
            #     Image:
            #         source: "./asmcnc/apps/systemTools_app/img/beta_testing.png"
            #         center_x: self.parent.center_x
            #         y: self.parent.y
            #         size: self.parent.width, self.parent.height
            #         allow_stretch: True

		Button:
			text: 'GRBL Settings'
			on_press: root.grbl_settings()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: '16sp'
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/grbl_settings.png"
            background_down: "./asmcnc/apps/systemTools_app/img/grbl_settings.png"
            border: [dp(25)]*4
            # BoxLayout:
            #     padding: 0
            #     size: self.parent.size
            #     pos: self.parent.pos
            #     Image:
            #         source: "./asmcnc/apps/systemTools_app/img/grbl_settings.png"
            #         center_x: self.parent.center_x
            #         y: self.parent.y
            #         size: self.parent.width, self.parent.height
            #         allow_stretch: True

		Button:
			text: 'Factory'
			on_press: root.factory_settings()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: '16sp'
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/factory.png"
            background_down: "./asmcnc/apps/systemTools_app/img/factory.png"
            border: [dp(25)]*4
            # BoxLayout:
            #     padding: 0
            #     size: self.parent.size
            #     pos: self.parent.pos
            #     Image:
            #         source: "./asmcnc/apps/systemTools_app/img/factory.png"
            #         center_x: self.parent.center_x
            #         y: self.parent.y
            #         size: self.parent.width, self.parent.height
            #         allow_stretch: True

        Button:
            text: 'Update Testing'
            on_press: root.update_testing()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: '16sp'
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/update_developer.png"
            background_down: "./asmcnc/apps/systemTools_app/img/update_developer.png"
            border: [dp(25)]*4
            # background_normal: ''
            # background_color: hex('#f9f9f9ff')
            # BoxLayout:
            #     padding: 0
            #     size: self.parent.size
            #     pos: self.parent.pos
            #     Image:
            #         source: "./asmcnc/apps/systemTools_app/img/update_developer.png"
            #         center_x: self.parent.center_x
            #         y: self.parent.y
            #         size: self.parent.width, self.parent.height
            #         allow_stretch: True

		Button:
			text: 'Developer'
			on_press: root.developer()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: '16sp'
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/developer.png"
            background_down: "./asmcnc/apps/systemTools_app/img/developer.png"
            border: [dp(25)]*4
            # BoxLayout:
            #     padding: 0
            #     size: self.parent.size
            #     pos: self.parent.pos
            #     Image:
            #         source: "./asmcnc/apps/systemTools_app/img/developer.png"
            #         center_x: self.parent.center_x
            #         y: self.parent.y
            #         size: self.parent.width, self.parent.height
            #         allow_stretch: True

        Button:
            text: 'Go Back'
            on_press: root.go_back()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: '16sp'
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/exit_system_tools.png"
            background_down: "./asmcnc/apps/systemTools_app/img/exit_system_tools.png"
            border: [dp(25)]*4
            # BoxLayout:
            #     padding: 0
            #     size: self.parent.size
            #     pos: self.parent.pos
            #     Image:
            #         source: "./asmcnc/apps/systemTools_app/img/exit_system_tools.png"
            #         center_x: self.parent.center_x
            #         y: self.parent.y
            #         size: self.parent.width, self.parent.height
            #         allow_stretch: True

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
        popup_system.PopupDownloadLogs(self.systemtools_sm)

    def reboot(self):
        popup_system.RebootConsole(self.systemtools_sm)

    def quit_to_console(self):
        popup_system.QuitToConsole(self.systemtools_sm)

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









