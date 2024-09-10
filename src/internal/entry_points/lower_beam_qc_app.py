'''
Created on 8 Feb 2022
@author: Dennis
YetiTool's UI for SmartBench
www.yetitool.com

#######################################################
LOWER BEAM QC APPLICATION

Used in production to carry out quality control checks. 
#######################################################

#######################################################
PLATFORM

This app needs following platform changes to run
as default application at startup: 

touch /home/pi/YETI_LBQC_PROD_JIG.txt

#######################################################
'''
from core.logging.logging_system import Logger
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from core.serial.router_machine import RouterMachine
from core.managers.settings_manager import Settings
from core.job.job_data import JobData
from core.utils.localization import Localization
from ui.keyboard.custom_keyboard import Keyboard
from kivy.clock import Clock
from core.services import smartbench_flurry_database_connection

from ui.screens.screen_home import HomeScreen
from ui.screens import screen_door
from ui.screens import screen_error
from internal.production.lower_beam_qc_jig.lower_beam_qc import LowerBeamQC
from internal.production.lower_beam_qc_jig.lower_beam_qc_warranty import LowerBeamQCWarranty

Cmport = 'COM3'


class LowerBeamQCApp(App):
    def build(self):
        Logger.info('Starting diagnostics')

        sm = ScreenManager(transition=NoTransition())

        sett = Settings(sm)

        l = Localization()

        kb = Keyboard(localization=l)

        jd = JobData(localization=l, settings_manager=sett)

        m = RouterMachine(Cmport, sm, sett, l, jd)

        db = smartbench_flurry_database_connection.DatabaseEventManager(sm, m, sett)

        if m.s.is_connected():
            Clock.schedule_once(m.s.start_services, 4)

        home_screen = HomeScreen(name='home', screen_manager=sm, machine=m, job=jd, settings=sett, localization=l,
                                 keyboard=kb)
        sm.add_widget(home_screen)

        error_screen = screen_error.ErrorScreenClass(name='errorScreen', screen_manager=sm, machine=m, job=jd,
                                                     database=db, localization=l)
        sm.add_widget(error_screen)

        door_screen = screen_door.DoorScreen(name='door', screen_manager=sm, machine=m, job=jd, database=db,
                                             localization=l)
        sm.add_widget(door_screen)

        lower_beam_qc = LowerBeamQC(name='qc', sm=sm, m=m, l=l)
        sm.add_widget(lower_beam_qc)

        lower_beam_qc_warranty = LowerBeamQCWarranty(name='qcWarranty', sm=sm, m=m, l=l)
        sm.add_widget(lower_beam_qc_warranty)

        sm.current = 'qc'
        return sm


if __name__ == '__main__':
    LowerBeamQCApp().run()
