'''
Created on 3 Mar 2022
@author: Dennis
'''

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from asmcnc.comms.router_machine import RouterMachine
from settings.settings_manager import Settings
from asmcnc.job.job_data import JobData
from asmcnc.comms.localization import Localization
from kivy.clock import Clock
from asmcnc.comms import smartbench_flurry_database_connection

from asmcnc.skavaUI.screen_home import HomeScreen
from asmcnc.skavaUI.screen_squaring_manual_vs_square import SquaringScreenDecisionManualVsSquare
from asmcnc.skavaUI.screen_homing_prepare import HomingScreenPrepare
from asmcnc.skavaUI.screen_homing_active import HomingScreenActive
from asmcnc.skavaUI.screen_squaring_active import SquaringScreenActive
from asmcnc.skavaUI import screen_door
from asmcnc.skavaUI import screen_error
from asmcnc.production.z_head_cycle_jig.z_head_cycle import ZHeadCycle

from datetime import datetime

Cmport = 'COM3'


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

class ZHeadCycleApp(App):
    def build(self):
        log('Starting diagnostics')

        sm = ScreenManager(transition=NoTransition())

        sett = Settings(sm)

        l = Localization()

        jd = JobData(localization = l, settings_manager = sett)

        m = RouterMachine(Cmport, sm, sett, l, jd)

        db = smartbench_flurry_database_connection.DatabaseEventManager(sm, m, sett)

        if m.s.is_connected():
            Clock.schedule_once(m.s.start_services, 4)

        error_screen = screen_error.ErrorScreenClass(name='errorScreen', screen_manager = sm, machine = m, job = jd, database = db, localization = l)
        sm.add_widget(error_screen)

        door_screen = screen_door.DoorScreen(name = 'door', screen_manager = sm, machine =m, job = jd, database = db, localization = l)
        sm.add_widget(door_screen)

        home_screen = HomeScreen(name='home', screen_manager = sm, machine = m, job = jd, settings = sett, localization = l)
        sm.add_widget(home_screen)

        squaring_decision_screen = SquaringScreenDecisionManualVsSquare(name = 'squaring_decision', screen_manager = sm, machine =m, localization = l)
        sm.add_widget(squaring_decision_screen)

        prepare_to_home_screen = HomingScreenPrepare(name = 'prepare_to_home', screen_manager = sm, machine =m, localization = l)
        sm.add_widget(prepare_to_home_screen)

        homing_active_screen = HomingScreenActive(name = 'homing_active', screen_manager = sm, machine =m, localization = l)
        sm.add_widget(homing_active_screen)

        squaring_active_screen = SquaringScreenActive(name = 'squaring_active', screen_manager = sm, machine =m, localization = l)
        sm.add_widget(squaring_active_screen)

        z_head_cycle = ZHeadCycle(name='cycle', sm = sm, m = m, l=l, sett=sett, jd=jd)
        sm.add_widget(z_head_cycle)

        sm.current = 'cycle'
        return sm

if __name__ == '__main__':
    ZHeadCycleApp().run()
