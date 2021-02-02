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

    system_info : system_info 
    download_logs: download_logs
    reboot: reboot
    exit_software: exit_software
    beta_testing: beta_testing
    grbl_settings: grbl_settings
    factory: factory
    update_testing: update_testing
    developer: developer
    go_back: go_back

    canvas.before:
        Color: 
            rgba: hex('#e5e5e5ff')
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
            id: system_info
			text: 'System Info'
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: '16sp'
            text_size: self.size
			on_press: root.go_to_build_info()
            background_normal: "./asmcnc/apps/systemTools_app/img/system_info.png"
            background_down: "./asmcnc/apps/systemTools_app/img/system_info.png"
            border: [dp(25)]*4
            padding_y: 5

		Button:
            id: download_logs
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
            padding_y: 5

		Button:
            id: reboot
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
            padding_y: 5

        Button:
            id: exit_software
            text: 'Exit Software'
            on_press: root.quit_to_console()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: '16sp'
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/quit_to_console.png"
            background_down: "./asmcnc/apps/systemTools_app/img/quit_to_console.png"
            border: [dp(25)]*4
            padding_y: 5

		Button:
            id: beta_testing
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
            padding_y: 5

		Button:
            id: grbl_settings
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
            padding_y: 5

		Button:
            id: factory
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
            padding_y: 5

        Button:
            id: update_testing
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
            padding_y: 5

		Button:
            id: developer
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
            padding_y: 5

        Button:
            id: go_back
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
            padding_y: 5

""")

class SystemMenuScreen(Screen):

    def __init__(self, **kwargs):
        super(SystemMenuScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.l = kwargs['localization']

    def on_pre_enter(self):
        # check if language is up to date, if it isn't update all screen strings
        if self.download_logs.text != str(self.l.dictionary['Download Logs']):
            self.update_strings()

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


    def update_strings(self):
        self.system_info.text = str(self.l.dictionary['System Info'])
        self.download_logs.text = str(self.l.dictionary['Download Logs'])
        self.reboot.text = str(self.l.dictionary['Reboot'])
        self.exit_software.text = str(self.l.dictionary['Exit Software'])
        self.beta_testing.text = str(self.l.dictionary['Beta Testing'])
        self.grbl_settings.text = str(self.l.dictionary['GRBL Settings'])
        self.factory.text = str(self.l.dictionary['Factory'])
        self.update_testing.text = str(self.l.dictionary['Update Testing'])
        self.developer.text = str(self.l.dictionary['Developer'])
        self.go_back.text = str(self.l.dictionary['Go Back'])







