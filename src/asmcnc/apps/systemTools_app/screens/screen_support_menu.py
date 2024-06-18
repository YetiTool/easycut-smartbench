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
import sys, os
from kivy.clock import Clock
import traceback
from asmcnc.apps.systemTools_app.screens import popup_system

Builder.load_string(
"""

<SupportMenuScreen>

    button_download_logs: button_download_logs
    button_reinstall_pika : button_reinstall_pika
    button_git_fsck : button_git_fsck
    button_download_settings_to_usb : button_download_settings_to_usb
    button_upload_settings_from_usb : button_upload_settings_from_usb
    button_overwrite_serial_number : button_overwrite_serial_number
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

        BoxLayout:
            padding: 0


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
            padding_y: 5.0/800.0*app.width
            border: (0,0,0,0)

        Button:
            id: button_reinstall_pika
            text: 'Get pika'
            on_press: root.get_pika()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/pika_reinstall.png"
            background_down: "./asmcnc/apps/systemTools_app/img/pika_reinstall.png"
            padding_y: 5.0/800.0*app.width
            border: (0,0,0,0)

        Button:
            id: button_git_fsck
            text: 'Git FSCK'
            on_press: root.check_easycut_repo()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/git_fsck_button.png"
            background_down: "./asmcnc/apps/systemTools_app/img/git_fsck_button.png"
            padding_y: 5.0/800.0*app.width
            border: (0,0,0,0)

        BoxLayout:
            padding: 0


        BoxLayout:
            padding: 0
            
        Button:
            id: button_download_settings_to_usb
            text: 'Save Settings'
            on_press: root.download_settings_to_usb()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/download_to_usb.png"
            background_down: "./asmcnc/apps/systemTools_app/img/download_to_usb.png"
            padding_y: 5.0/800.0*app.width
            border: (0,0,0,0)

        Button:
            id: button_upload_settings_from_usb
            text: 'Restore Settings'
            on_press: root.upload_settings_from_usb()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/upload_from_usb.png"
            background_down: "./asmcnc/apps/systemTools_app/img/upload_from_usb.png"
            padding_y: 5.0/800.0*app.width
            border: (0,0,0,0)

        Button:
            id: button_overwrite_serial_number
            text: 'Overwrite Serial Number'
            on_press: root.overwrite_serial_number()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/upload_from_usb.png"
            background_down: "./asmcnc/apps/systemTools_app/img/upload_from_usb.png"
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


class SupportMenuScreen(Screen):
    default_font_size = 16.0 / 800.0 * Window.width

    def __init__(self, **kwargs):
        super(SupportMenuScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs["system_tools"]
        self.l = kwargs["localization"]
        self.id_list = [
            self.button_download_logs,
            self.button_reinstall_pika,
            self.button_git_fsck,
            self.button_download_settings_to_usb,
            self.button_upload_settings_from_usb,
            self.button_go_back,
        ]
        self.update_strings()

    def go_back(self):
        self.systemtools_sm.exit_app()

    def download_settings_to_usb(self):
        self.systemtools_sm.show_popup_before_download_settings_to_usb()

    def upload_settings_from_usb(self):
        self.systemtools_sm.show_popup_before_upload_settings_from_usb()

    def overwrite_serial_number(self):
        self.systemtools_sm.show_popup_before_overwrite_serial_number()

    def download_logs(self):
        popup_system.PopupDownloadLogs(self.systemtools_sm, self.l)

    def get_pika(self):
        self.systemtools_sm.reinstall_pika()

    def check_easycut_repo(self):
        self.systemtools_sm.check_git_repository()

    def quit_to_console(self):
        popup_system.QuitToConsole(self.systemtools_sm, self.l)

    def usb_first_aid(self):
        self.systemtools_sm.do_usb_first_aid()

    def update_strings(self):
        self.button_download_logs.text = self.l.get_str("Download Logs")
        self.button_reinstall_pika.text = self.l.get_str("Get Pika")
        self.button_git_fsck.txt = self.l.get_str("Git FSCK")
        self.button_download_settings_to_usb.text = self.l.get_str("Save settings")
        self.button_upload_settings_from_usb.text = self.l.get_str("Restore settings")
        self.button_overwrite_serial_number.text = self.l.get_str("Overwrite Serial Number")
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
            value.font_size = self.default_font_size - 0.00375 * Window.width
