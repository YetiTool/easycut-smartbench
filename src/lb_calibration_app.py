'''
Created on 9 Feb 2022
@author: Archie
YetiTool's UI for SmartBench
www.yetitool.com

#######################################################
LOWER BEAM CALIBRATION APPLICATION

Used in production to carry out quality control checks. 
#######################################################

#######################################################
PLATFORM

This app needs following platform changes to run
as default application at startup: 

sudo systemctl disable ansible.service

touch /home/pi/YETI_LBCAL_PROD_JIG.txt

sudo nano /boot/config.txt

# Copy and paste to end of file: 

        dtoverlay=pi3-disable-bt

# Exit and save file

sudo reboot

#######################################################
'''

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.clock import Clock

from asmcnc.comms.router_machine import RouterMachine
from settings.settings_manager import Settings
from asmcnc.job.job_data import JobData
from asmcnc.comms.localization import Localization

from asmcnc.production.lowerbeam_calibration_jig.lowerbeam_calibration_1 import LBCalibration1
from asmcnc.production.lowerbeam_calibration_jig.lowerbeam_calibration_2 import LBCalibration2
from asmcnc.production.lowerbeam_calibration_jig.lowerbeam_calibration_3 import LBCalibration3
from asmcnc.production.lowerbeam_calibration_jig.lowerbeam_calibration_4 import LBCalibration4
from asmcnc.production.lowerbeam_calibration_jig.lowerbeam_calibration_success import LBCalibrationSuccess
from asmcnc.production.lowerbeam_calibration_jig.lowerbeam_calibration_fail import LBCalibrationFail

from datetime import datetime

Cmport = 'COM3'

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

class LBCalibration(App):
    def build(self):
        log('Starting LB Calibration')

        sm = ScreenManager(transition=NoTransition())

        sett = Settings(sm)

        l = Localization()

        jd = JobData(localization = l, settings_manager = sett)

        m = RouterMachine(Cmport, sm, sett, l, jd)

        if m.s.is_connected():
            Clock.schedule_once(m.s.start_services, 4)

        lb_calibration_1 = LBCalibration1(name = 'lbc1', sm = sm, m = m)
        sm.add_widget(lb_calibration_1)

        lb_calibration_2 = LBCalibration2(name = 'lbc2', sm = sm, m = m)
        sm.add_widget(lb_calibration_2)

        lb_calibration_3 = LBCalibration3(name = 'lbc3', sm = sm, m = m)
        sm.add_widget(lb_calibration_3)

        lb_calibration_4 = LBCalibration4(name = 'lbc4', sm = sm, m = m)
        sm.add_widget(lb_calibration_4)

        lb_calibration_5 = LBCalibrationSuccess(name = 'lbc5', sm = sm, m = m)
        sm.add_widget(lb_calibration_5)

        lb_calibration_6 = LBCalibrationFail(name = 'lbc6', sm = sm, m = m)
        sm.add_widget(lb_calibration_6)

        sm.current = 'lbc1'

        return sm

if __name__ == '__main__':
    LBCalibration().run()