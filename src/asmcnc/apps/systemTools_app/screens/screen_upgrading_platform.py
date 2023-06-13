"""
@author archiejarvis on 07/06/2023
"""

import threading
import subprocess

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<ScreenUpgradingPlatform>:
    status_label: status_label

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
            
        Label:
            id: status_label
""")


# WiFi will be checked before entering screen


class ScreenUpgradingPlatform(Screen):
    upgrade_in_progress = False
    override_fail = False

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
                if output.strip() == '0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.':
                    self.override_fail = True

    def start_upgrade(self):
        self.set_upgrade_in_progress(True)
        self.clean_up()

        cmd = 'stdbuf -oL sudo apt-get update -y && stdbuf -oL sudo apt-get upgrade -y --show-progress'

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        t = threading.Thread(target=self.read_output, args=(process,))
        t.start()

        process.wait()

        process.returncode = self.override_fail

        UpgradePlatformPopup(return_code=process.returncode, system_tools=self.systemtools_sm, localization=self.l)


from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class UpgradePlatformPopup(Popup):
    return_code = None

    def __init__(self, return_code, **kwargs):
        super(UpgradePlatformPopup, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.l = kwargs['localization']
        self.return_code = return_code

        description = self.l.get_str(
            "The platform upgrade has completed successfully installed. Your console will automatically reboot in 30 "
            "seconds.") \
            if self.return_code == 1 else self.l.get_str(
            "The platform upgrade has failed. Please check your WiFi connection and try again later.")
        title_string = self.l.get_str('Platform Upgrade')
        ok_string = self.l.get_bold('Reboot Now') if self.return_code == 1 else self.l.get_bold('Ok')

        label = Label(size_hint_y=2, text_size=(320, None), halign='center', valign='middle', text=description,
                      color=[0, 0, 0, 1], padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 5, 0, 0])
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[30, 20, 30, 0])
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font='Roboto-Bold',
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(360, 360),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        if self.return_code == 1:
            ok_button.bind(on_press=self.reboot)
        else:
            ok_button.bind(on_press=lambda dt: self.dismiss())

        if self.return_code == 1:
            Clock.schedule_once(lambda dt: self.reboot(), 30)

        popup.open()

    def reboot(self):
        subprocess.call('sudo reboot', shell=True)

    def on_open(self):
        if self.return_code == 1:
            Clock.schedule_once(lambda dt: self.reboot(), 30)

    def dismiss(self):
        self.systemtools_sm.current = 'screen_system_tools'
        super(UpgradePlatformPopup, self).dismiss()
