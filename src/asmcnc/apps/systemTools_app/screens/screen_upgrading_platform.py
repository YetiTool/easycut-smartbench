"""
@author archiejarvis on 07/06/2023
"""

import subprocess

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<ScreenUpgradingPlatform>:
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
            text: "DO NOT POWER OFF YOUR CONSOLE"
            color: 1, 0, 0, 1
            font_size: 30
            bold: True
            
        Label:
            text: "Once the upgrade is complete, your console will automatically restart."
            color: 0, 0, 0, 1
            
        Image:
            source: "./asmcnc/apps/systemTools_app/img/spinner.gif"
            anim_delay: 0
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
        Clock.schedule_once(lambda dt: self.start_upgrade(), 1)

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

        process.wait()

        if process.returncode == 0:
            if self.reboot_required:
                Clock.schedule_once(lambda dt: self.reboot(), 5)
        else:
            pass
            # TODO: Implement error handling

