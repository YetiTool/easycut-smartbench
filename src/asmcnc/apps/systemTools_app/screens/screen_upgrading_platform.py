"""
@author archiejarvis on 07/06/2023
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

import subprocess
import threading
import time

Builder.load_string("""
<ScreenUpgradingPlatform>:
    upgrade_status_label:upgrade_status_label
    
    BoxLayout:
        orientation: "vertical"
        
        canvas:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                size: self.size
                pos: self.pos
        
        Label:
            text: "Upgrading Console Platform"
            font_size: 30
            color: 0, 0, 0, 1
            bold: True
            
        Label:
            text: "Once the upgrade is complete, your console will automatically restart."
            color: 0, 0, 0, 1
            
        Label:
            text: "DO NOT POWER OFF YOUR CONSOLE"
            color: 1, 0, 0, 1
            font_size: 30
            bold: True
            
        Label:
            id: upgrade_status_label
            font_size: 16
            color: 0, 0, 0, 1
""")


# WiFi will be checked before entering screen


class ScreenUpgradingPlatform(Screen):
    upgrade_in_progress = False
    reboot_required = True

    def __init__(self, **kwargs):
        super(ScreenUpgradingPlatform, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.l = kwargs['localization']

    def on_enter(self):
        Clock.schedule_once(lambda dt: self.start_upgrade(), 3)

    def set_upgrade_status_text(self, value):
        self.upgrade_status_label.text = self.upgrade_status_text

    def get_upgrade_status_text_thread(self, process):
        while self.upgrade_in_progress:
            line = process.stdout.readline().decode().strip()

            if line:
                if line == '0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.':
                    self.reboot_required = False
                Clock.schedule_once(lambda dt: self.set_upgrade_status_text(line), 0.1)
            time.sleep(0.1)

    def clean_up(self):
        subprocess.call('sudo rm -rf /var/lib/apt/lists/*', shell=True)
        subprocess.call('sudo apt-get clean', shell=True)

    def set_upgrade_in_progress(self, value):
        self.upgrade_in_progress = value

    def reboot(self):
        subprocess.call('sudo reboot', shell=True)

    def start_upgrade(self):
        self.set_upgrade_in_progress(True)
        self.clean_up()

        cmd = 'stdbuf -oL sudo apt-get update -y && stdbuf -oL sudo apt-get upgrade -y --show-progress'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        upgrade_status_thread = threading.Thread(target=self.get_upgrade_status_text_thread, args=(process,))
        upgrade_status_thread.start()

        process.wait()

        if process.returncode == 0:
            self.set_upgrade_status_text('Platform upgrade success')
            if self.reboot_required:
                Clock.schedule_once(lambda dt: self.reboot(), 5)
        else:
            self.set_upgrade_status_text('Platform upgrade failed')
            # TODO: Implement

        self.set_upgrade_in_progress(False)


