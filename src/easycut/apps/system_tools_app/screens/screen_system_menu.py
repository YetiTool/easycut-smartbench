# -*- coding: utf-8 -*-
from kivy.core.window import Window

"""
Created on 18 November 2020
Menu screen for system tools app

@author: Letty
"""
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
import sys
from kivy.clock import Clock
from asmcnc.skavaUI import popup_info
from asmcnc.apps.systemTools_app.screens import popup_system
from asmcnc.core_UI import scaling_utils

Builder.load_string(
"""

<SystemMenuScreen>

    button_system_info: button_system_info 
    button_support_menu: button_support_menu
    button_reboot: button_reboot
    button_exit_software: button_exit_software
    button_usb_first_aid: button_usb_first_aid
    button_beta_testing: button_beta_testing
    button_grbl_settings: button_grbl_settings
    button_factory: button_factory
    # button_update_testing: button_update_testing
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
        padding:[dp(0.0104125)*app.width, dp(0.125)*app.height]
        spacing:[dp(0.0104125)*app.width, dp(0.125)*app.height]
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
            padding_y: 5.0/800.0*app.width
            border: (0,0,0,0)

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
            padding_y: 5.0/800.0*app.width
            border: (0,0,0,0)

        Button:
            id: button_support_menu
            text: 'Support'
            on_press: root.go_to_support()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/support.png"
            background_down: "./asmcnc/apps/systemTools_app/img/support.png"
            padding_y: 5.0/800.0*app.width
            border: (0,0,0,0)

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
            padding_y: 5.0/800.0*app.width
            border: (0,0,0,0)

        Button:
            id: button_usb_first_aid
            text: 'USB First Aid'
            on_press: root.usb_first_aid()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/usb_first_aid.png"
            background_down: "./asmcnc/apps/systemTools_app/img/usb_first_aid.png"
            padding_y: 5.0/800.0*app.width
            border: (0,0,0,0)

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
            padding_y: 5.0/800.0*app.width
            border: (0,0,0,0)

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
            padding_y: 5.0/800.0*app.width
            border: (0,0,0,0)

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
            padding_y: 5.0/800.0*app.width
            border: (0,0,0,0)

        # Button:
        #     id: button_update_testing
        #     text: 'Update Testing'
        #     on_press: root.update_testing()
        #     valign: "bottom"
        #     halign: "center"
        #     markup: True
        #     font_size: root.default_font_size
        #     text_size: self.size
        #     background_normal: "./asmcnc/apps/systemTools_app/img/update_developer.png"
        #     background_down: "./asmcnc/apps/systemTools_app/img/update_developer.png"
        #     padding_y: 5.0/800.0*app.width
        #     border: (0,0,0,0)


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
            padding_y: 5.0/800.0*app.width
            border: (0,0,0,0)

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
            padding_y: 5.0/800.0*app.width
            border: (0,0,0,0)

"""
)


class SystemMenuScreen(Screen):
    default_font_size = scaling_utils.get_scaled_width(16)

    def __init__(self, **kwargs):
        super(SystemMenuScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs["system_tools"]
        self.l = kwargs["localization"]
        self.kb = kwargs["keyboard"]
        self.id_list = [
            self.button_system_info,
            self.button_support_menu,
            self.button_reboot,
            self.button_exit_software,
            self.button_usb_first_aid,
            self.button_beta_testing,
            self.button_grbl_settings,
            self.button_factory,
            self.button_developer,
            self.button_go_back,
        ]
        self.update_strings()

    def go_back(self):
        self.systemtools_sm.exit_app()

    def go_to_build_info(self):
        self.systemtools_sm.open_build_info_screen()

    def go_to_support(self):
        self.systemtools_sm.open_support_menu_screen()

    def reboot(self):
        popup_system.RebootConsole(self.systemtools_sm, self.l)

    def quit_to_console(self):
        popup_system.QuitToConsole(self.systemtools_sm, self.l)

    def usb_first_aid(self):
        self.systemtools_sm.do_usb_first_aid()

    def beta_testing(self):
        popup_system.PopupBetaTesting(self.systemtools_sm, self.l)

    def grbl_settings(self):
        popup_system.PopupGRBLSettingsPassword(self.systemtools_sm, self.l, self.kb)

    def factory_settings(self):
        popup_system.PopupFactorySettingsPassword(self.systemtools_sm, self.l, self.kb)

    def developer(self):
        popup_system.PopupDeveloperPassword(self.systemtools_sm, self.l, self.kb)

    def update_strings(self):
        self.button_system_info.text = self.l.get_str("System Info")
        self.button_support_menu.text = self.l.get_str("Support")
        self.button_reboot.text = self.l.get_str("Reboot")
        self.button_exit_software.text = self.l.get_str("Exit Software")
        self.button_usb_first_aid.text = self.l.get_str("USB First Aid")
        self.button_beta_testing.text = self.l.get_str("Beta Testing")
        self.button_grbl_settings.text = self.l.get_str("GRBL Settings")
        self.button_factory.text = self.l.get_str("Factory")
        self.button_developer.text = self.l.get_str("Developer")
        self.button_go_back.text = self.l.get_str("Go Back")
        for id_object in self.id_list:
            self.update_font_size(id_object)

    def update_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length < 16:
            value.font_size = self.default_font_size
        elif text_length > 15:
            value.font_size = self.default_font_size - 0.0025 * Window.width
        if text_length > 19:
            value.font_size = self.default_font_size - 0.005 * Window.width
        if text_length > 22:
            value.font_size = self.default_font_size - 0.00625 * Window.width
        if text_length > 25:
            value.font_size = self.default_font_size - 0.0075 * Window.width
