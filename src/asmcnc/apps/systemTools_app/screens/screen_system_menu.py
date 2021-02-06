# -*- coding: utf-8 -*-
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

    button_system_info: button_system_info 
    button_download_logs: button_download_logs
    button_reboot: button_reboot
    button_exit_software: button_exit_software
    button_beta_testing: button_beta_testing
    button_grbl_settings: button_grbl_settings
    button_factory: button_factory
    button_update_testing: button_update_testing
    button_developer: button_developer
    button_go_back: button_go_back

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
            id: button_system_info
			text: 'System Info'
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
			on_press: root.go_to_build_info()
            background_normal: "./asmcnc/apps/systemTools_app/img/system_info.png"
            background_down: "./asmcnc/apps/systemTools_app/img/system_info.png"
            border: [dp(25)]*4
            padding_y: 5

		Button:
            id: button_download_logs
			text: 'Download Logs'
			on_press: root.download_logs()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/download_logs.png"
            background_down: "./asmcnc/apps/systemTools_app/img/download_logs.png"
            border: [dp(25)]*4
            padding_y: 5

		Button:
            id: button_reboot
			text: 'Reboot'
			on_press: root.reboot()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/reboot_console.png"
            background_down: "./asmcnc/apps/systemTools_app/img/reboot_console.png"
            border: [dp(25)]*4
            padding_y: 5

        Button:
            id: button_exit_software
            text: 'Exit Software'
            on_press: root.quit_to_console()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/quit_to_console.png"
            background_down: "./asmcnc/apps/systemTools_app/img/quit_to_console.png"
            border: [dp(25)]*4
            padding_y: 5

		Button:
            id: button_beta_testing
			text: 'Beta Testing'
			on_press: root.beta_testing()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/beta_testing.png"
            background_down: "./asmcnc/apps/systemTools_app/img/beta_testing.png"
            border: [dp(25)]*4
            padding_y: 5

		Button:
            id: button_grbl_settings
			text: 'GRBL Settings'
			on_press: root.grbl_settings()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/grbl_settings.png"
            background_down: "./asmcnc/apps/systemTools_app/img/grbl_settings.png"
            border: [dp(25)]*4
            padding_y: 5

		Button:
            id: button_factory
			text: 'Factory'
			on_press: root.factory_settings()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/factory.png"
            background_down: "./asmcnc/apps/systemTools_app/img/factory.png"
            border: [dp(25)]*4
            padding_y: 5

        Button:
            id: button_update_testing
            text: 'Update Testing'
            on_press: root.update_testing()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/update_developer.png"
            background_down: "./asmcnc/apps/systemTools_app/img/update_developer.png"
            border: [dp(25)]*4
            padding_y: 5

		Button:
            id: button_developer
			text: 'Developer'
			on_press: root.developer()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/developer.png"
            background_down: "./asmcnc/apps/systemTools_app/img/developer.png"
            border: [dp(25)]*4
            padding_y: 5

        Button:
            id: button_go_back
            text: 'Go Back'
            on_press: root.go_back()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/exit_system_tools.png"
            background_down: "./asmcnc/apps/systemTools_app/img/exit_system_tools.png"
            border: [dp(25)]*4
            padding_y: 5

""")

class SystemMenuScreen(Screen):

    default_font_size = 16


    def __init__(self, **kwargs):
        super(SystemMenuScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.l = kwargs['localization']

        self.id_list = [
        self.button_system_info,
        self.button_download_logs,
        self.button_reboot,
        self.button_exit_software,
        self.button_beta_testing,
        self.button_grbl_settings,
        self.button_factory,
        self.button_update_testing,
        self.button_developer,
        self.button_go_back
        ]

    def on_pre_enter(self):
        # check if language is up to date, if it isn't update all screen strings
        if self.button_download_logs.text != str(self.l.dictionary['Download Logs']):
            self.update_strings()

    def go_back(self):
    	self.systemtools_sm.exit_app()

    def go_to_build_info(self):
    	self.systemtools_sm.open_build_info_screen()

    def download_logs(self):
        popup_system.PopupDownloadLogs(self.systemtools_sm, self.l)

    def reboot(self):
        popup_system.RebootConsole(self.systemtools_sm, self.l)

    def quit_to_console(self):
        popup_system.QuitToConsole(self.systemtools_sm, self.l)

    def beta_testing(self):
        popup_system.PopupBetaTesting(self.systemtools_sm, self.l)

    def grbl_settings(self):
    	popup_system.PopupGRBLSettingsPassword(self.systemtools_sm, self.l)

    def factory_settings(self):
    	popup_system.PopupFactorySettingsPassword(self.systemtools_sm, self.l)

    def update_testing(self):
        popup_system.PopupUpdateTestingPassword(self.systemtools_sm, self.l)

    def developer(self):
    	popup_system.PopupDeveloperPassword(self.systemtools_sm, self.l)

    def update_strings(self):
        self.button_system_info.text = self.l.get_str('System Info')
        self.button_download_logs.text = self.l.get_str('Download Logs')
        self.button_reboot.text = self.l.get_str('Reboot')
        self.button_exit_software.text = self.l.get_str('Exit Software')
        self.button_beta_testing.text = self.l.get_str('Beta Testing')
        self.button_grbl_settings.text = self.l.get_str('GRBL Settings')
        self.button_factory.text = self.l.get_str('Factory')
        self.button_update_testing.text = self.l.get_str('Update Testing')
        self.button_developer.text = self.l.get_str('Developer')
        self.button_go_back.text = self.l.get_str('Go Back')

        for id_object in self.id_list:
            self.update_font_size(id_object)

    def update_font_size(self, value):
        if len(value.text) < 16:
            value.font_size = self.default_font_size
        elif len(value.text) > 15: 
            value.font_size = self.default_font_size - 2
        if len(value.text) > 20: 
            value.font_size = self.default_font_size - 4
        if len(value.text) > 22: 
            value.font_size = self.default_font_size - 5






