"""
@author archiejarvis on 07/06/2023
"""

import threading
import subprocess

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from datetime import datetime


def log(message):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " " + message)


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
            font_size: dp(30)
            color: 0, 0, 0, 1
            bold: True
            
        Label:
            text: "DO NOT POWER OFF YOUR CONSOLE"
            color: 1, 0, 0, 1
            font_size: dp(30)
            bold: True
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

    def set_status_text(self, text):
        self.status_label.text = text

    def read_output(self, process):
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                log(output.strip())
                if output.strip().startswith('0 upgraded, 0 newly installed'):
                    self.reboot_required = False

    def start_upgrade(self):
        self.set_upgrade_in_progress(True)
        self.clean_up()

        cmd = 'stdbuf -oL sudo apt-get update -y && stdbuf -oL sudo apt-get upgrade -y --show-progress'

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        t = threading.Thread(target=self.read_output, args=(process,))
        t.start()

        process.wait()

        success = process.returncode == 0

        UpgradePlatformPopup(reboot_required=self.reboot_required and success, success=success,
                             system_tools=self.systemtools_sm, localization=self.l)


from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

labels = {
    'title': {
        True: {
            0: 'Platform Upgrade - Failed, Reboot Required',
            1: 'Platform Upgrade - Success, Reboot Required'
        },
        False: {
            0: 'Platform Upgrade - Failed',
            1: 'Platform Upgrade - Up to Date'
        }
    },
    'description': {
        True: {
            0: 'Something went wrong while upgrading the console platform. Check your Wi-Fi connection and try again '
               'later. Your console will automatically reboot in 30 seconds, or you can press reboot now.',
            1: 'The platform upgrade has completed successfully installed. Your console will automatically reboot in '
               '30 seconds, or you can press reboot now.'
        },
        False: {
            0: 'Something went wrong while upgrading the console platform. Check your Wi-Fi connection and try again '
               'later.',
            1: "Your console's platform is already up to date. Press the button below to return to System Tools."
        }
    },
    'ok_string': {
        True: {
            0: 'Reboot Now',
            1: 'Reboot Now'  # dupe
        },
        False: {
            0: 'Ok',
            1: 'Ok'  # dupe
        }
    }
}


class UpgradePlatformPopup(Popup):
    def __init__(self, success, reboot_required, **kwargs):
        super(UpgradePlatformPopup, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.l = kwargs['localization']
        self.success = success
        self.reboot_required = reboot_required

        description = labels['description'][reboot_required][success]
        title_string = labels['title'][reboot_required][success]
        ok_string = labels['ok_string'][reboot_required][success]

        label = Label(size_hint_y=2, text_size=(320, None), halign='center', valign='middle', text=description,
                      color=[0, 0, 0, 1], padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, dp(5), 0, 0])
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[dp(30), dp(20), dp(30), 0])
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font='Roboto-Bold',
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(dp(360), dp(360)),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        if self.success:  #and self.reboot_required:
            # ok_button.bind(on_release=self.reboot)
            Clock.schedule_once(self.reboot, 30)
        else:
            ok_button.bind(on_press=lambda x: self.dismiss(popup))

        popup.open()

    def reboot(self, dt=None, *args):
        log('rebooting')
        subprocess.call('sudo reboot', shell=True)

    def dismiss(self, popup):
        popup.dismiss()
        self.systemtools_sm.sm.current = 'system_menu'

