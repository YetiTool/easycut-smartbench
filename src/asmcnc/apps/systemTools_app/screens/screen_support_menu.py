# -*- coding: utf-8 -*-
'''
Created on 18 November 2020
Menu screen for system tools app

@author: Letty
'''

import os
import re
import subprocess
import threading
import time

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from asmcnc.apps.systemTools_app.screens import popup_system

Builder.load_string("""

<SupportMenuScreen>

    button_download_logs: button_download_logs
    button_reinstall_pika : button_reinstall_pika
    button_git_fsck : button_git_fsck
    button_upgrade_platform: button_upgrade_platform
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
            border: [dp(25)]*4
            padding_y: 5

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
            border: [dp(25)]*4
            padding_y: 5

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
            border: [dp(25)]*4
            padding_y: 5

        BoxLayout:
            padding: 0
        BoxLayout:
            padding: 0
            
        Button:
            id: button_upgrade_platform
            text: 'Upgrade Platform'
            on_press: root.try_upgrade_platform()
            valign: "bottom"
            halign: "center"
            markup: True
            font_size: root.default_font_size
            text_size: self.size
            background_normal: "./asmcnc/apps/systemTools_app/img/upgrade_platform.png"
            background_down: "./asmcnc/apps/systemTools_app/img/upgrade_platform.png"
            border: [dp(25)]*4
            padding_y: 5
            
        BoxLayout:
            padding: 0
        BoxLayout:
            padding: 0

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


class SupportMenuScreen(Screen):
    default_font_size = 16

    def __init__(self, **kwargs):
        super(SupportMenuScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.l = kwargs['localization']

        self.id_list = [
            self.button_download_logs,
            self.button_reinstall_pika,
            self.button_git_fsck,
            self.button_go_back
        ]

        self.update_strings()

    def go_back(self):
        self.systemtools_sm.exit_app()

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

    upgrade_in_progress = False
    upgrade_percentage = 0

    def get_upgrade_progress(self, process):
        while True:
            line = process.stdout.readline().decode().strip()
            print(line)

            if not line:
                break

            match = re.search(r"([0-9]+)%", line)

            if match:
                percentage = int(match.group(1))
                self.upgrade_percentage = percentage
                print(percentage)

            time.sleep(0.1)

    def try_upgrade_platform(self):
        if self.upgrade_in_progress:
            return

        self.upgrade_in_progress = True

        if not self.systemtools_sm.set.wifi_available:
            # TODO: Show popup with error
            print('No internet connection')
            return

        print('Platform upgrade started')

        cmd = 'stdbuf -oL sudo apt update -y && stdbuf -oL sudo apt upgrade -y --show-progress'

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        thread = threading.Thread(target=self.get_upgrade_progress, args=(process,))

        thread.start()
        process.wait()

        if process.returncode == 0:
            # TODO: Show popup and restart
            print('Platform upgrade success')
        else:
            # TODO: Show popup with error
            print('Platform upgrade failed')

        self.upgrade_in_progress = False

    def update_strings(self):
        self.button_download_logs.text = self.l.get_str('Download Logs')
        self.button_reinstall_pika.text = self.l.get_str('Get Pika')
        self.button_git_fsck.txt = self.l.get_str("Git FSCK")
        self.button_go_back.text = self.l.get_str('Go Back')

        for id_object in self.id_list:
            self.update_font_size(id_object)

    def update_font_size(self, value):
        if len(value.text) < 16:
            value.font_size = self.default_font_size
        elif len(value.text) > 15:
            value.font_size = self.default_font_size - 2
        if len(value.text) > 19:
            value.font_size = self.default_font_size - 3
