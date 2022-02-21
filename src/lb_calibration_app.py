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

touch /home/pi/YETI_LBCAL_PROD_JIG.txt

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
from asmcnc.comms import smartbench_flurry_database_connection

from asmcnc.production.lowerbeam_calibration_jig.lowerbeam_calibration_1 import LBCalibration1
from asmcnc.production.lowerbeam_calibration_jig.lowerbeam_calibration_2 import LBCalibration2
from asmcnc.production.lowerbeam_calibration_jig.lowerbeam_calibration_3 import LBCalibration3
from asmcnc.production.lowerbeam_calibration_jig.lowerbeam_calibration_4 import LBCalibration4
from asmcnc.production.lowerbeam_calibration_jig.lowerbeam_calibration_success import LBCalibrationSuccess
from asmcnc.production.lowerbeam_calibration_jig.lowerbeam_calibration_fail import LBCalibrationFail
from asmcnc.skavaUI import screen_door
from asmcnc.skavaUI import screen_error

from asmcnc.production.database.calibration_database import CalibrationDatabase


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

        db = smartbench_flurry_database_connection.DatabaseEventManager(sm, m, sett)

        calibration_db = CalibrationDatabase()

        if m.s.is_connected():
            Clock.schedule_once(m.s.start_services, 4)

        error_screen = screen_error.ErrorScreenClass(name='errorScreen', screen_manager = sm, machine = m, job = jd, database = db, localization = l)
        sm.add_widget(error_screen)

        door_screen = screen_door.DoorScreen(name = 'door', screen_manager = sm, machine =m, job = jd, database = db, localization = l)
        sm.add_widget(door_screen)

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