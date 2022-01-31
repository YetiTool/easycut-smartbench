'''
Created on 28 Jan 2022
@author: Archie
YetiTool's UI for SmartBench
www.yetitool.com


This app needs following platform changes to run: 

sudo systemctl disable ansible.service

touch /home/pi/ZHEADTESTJIG.txt

sudo nano /boot/config.txt

# Copy and paste to end of file: 

        dtoverlay=pi3-disable-bt

# Exit and save file

sudo reboot
'''

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from asmcnc.comms.router_machine import RouterMachine 
from asmcnc.comms import server_connection
from asmcnc.apps.app_manager import AppManagerClass
from settings.settings_manager import Settings
from asmcnc.job.job_data import JobData
from asmcnc.comms.localization import Localization

from asmcnc.skavaUI.screen_home import HomeScreen
from asmcnc.tests.z_head_qc_home import ZHeadQCHome
from asmcnc.tests.z_head_qc_1 import ZHeadQC1
from asmcnc.tests.z_head_qc_2 import ZHeadQC2

from datetime import datetime

Cmport = 'COM3'


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

class Diagnostics(App):
    def build(self):
        log('Starting diagnostics')

        sm = ScreenManager(transition=NoTransition())

        sett = Settings(sm)

        l = Localization()

        jd = JobData(localization = l, settings_manager = sett)

        m = RouterMachine(Cmport, sm, sett, l, jd)

        home_screen = HomeScreen(name='home', screen_manager = sm, machine = m, job = jd, settings = sett, localization = l)
        sm.add_widget(home_screen)

        z_head_qc_home = ZHeadQCHome(name='qchome', sm = sm)
        sm.add_widget(z_head_qc_home)

        z_head_qc_2 = ZHeadQC2(name='qc2', sm = sm, m = m)
        sm.add_widget(z_head_qc_2)
        
        z_head_qc_1 = ZHeadQC1(name='qc1', sm = sm, m = m)
        sm.add_widget(z_head_qc_1)

        sm.current = 'qchome'
        return sm

if __name__ == '__main__':
    Diagnostics().run()

