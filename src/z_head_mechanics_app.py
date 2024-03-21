from asmcnc.comms.logging_system.logging_system import Logger
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.clock import Clock

from settings.settings_manager import Settings
from asmcnc.job.job_data import JobData
from asmcnc.comms.router_machine import RouterMachine
from asmcnc.comms.localization import Localization
from asmcnc.keyboard.custom_keyboard import Keyboard
from asmcnc.comms import smartbench_flurry_database_connection

from asmcnc.skavaUI.screen_home import HomeScreen
from asmcnc.skavaUI.screen_squaring_manual_vs_square import SquaringScreenDecisionManualVsSquare
from asmcnc.skavaUI.screen_homing_prepare import HomingScreenPrepare
from asmcnc.skavaUI.screen_homing_active import HomingScreenActive
from asmcnc.skavaUI.screen_squaring_active import SquaringScreenActive
from asmcnc.skavaUI import screen_door
from asmcnc.skavaUI import screen_error
from asmcnc.production.z_head_mechanics_jig.z_head_mechanics import ZHeadMechanics
from asmcnc.production.z_head_mechanics_jig.z_head_mechanics_monitor import ZHeadMechanicsMonitor
from asmcnc.production.z_head_mechanics_jig.z_head_mechanics_booting import ZHeadMechanicsBooting
from asmcnc.production.z_head_mechanics_jig.z_head_mechanics_manual_move import ZHeadMechanicsManualMove

from datetime import datetime


Cmport = 'COM3'


class ZHeadMechanicsApp(App):
    def build(self):
        Logger.info('Starting diagnostics')

        sm = ScreenManager(transition=NoTransition())

        sett = Settings(sm)

        l = Localization()

        kb = Keyboard(localization=l)

        jd = JobData(localization = l, settings_manager = sett)

        m = RouterMachine(Cmport, sm, sett, l, jd)

        db = smartbench_flurry_database_connection.DatabaseEventManager(sm, m, sett)

        if m.s.is_connected():
            Clock.schedule_once(m.s.start_services, 4)

        home_screen = HomeScreen(name='home', screen_manager = sm, machine = m, job = jd, settings = sett, localization = l, keyboard = kb)
        sm.add_widget(home_screen)

        squaring_decision_screen = SquaringScreenDecisionManualVsSquare(name = 'squaring_decision', screen_manager = sm, machine =m, localization = l)
        sm.add_widget(squaring_decision_screen)

        prepare_to_home_screen = HomingScreenPrepare(name = 'prepare_to_home', screen_manager = sm, machine =m, localization = l)
        sm.add_widget(prepare_to_home_screen)

        homing_active_screen = HomingScreenActive(name = 'homing_active', screen_manager = sm, machine =m, localization = l)
        sm.add_widget(homing_active_screen)

        squaring_active_screen = SquaringScreenActive(name = 'squaring_active', screen_manager = sm, machine =m, localization = l)
        sm.add_widget(squaring_active_screen)

        error_screen = screen_error.ErrorScreenClass(name = 'errorScreen', screen_manager = sm, machine = m, job = jd, database = db, localization = l)
        sm.add_widget(error_screen)

        door_screen = screen_door.DoorScreen(name = 'door', screen_manager = sm, machine =m, job = jd, database = db, localization = l)
        sm.add_widget(door_screen)

        z_head_mechanics = ZHeadMechanics(name = 'mechanics', sm = sm, m = m, l = l)
        sm.add_widget(z_head_mechanics)

        z_head_mechanics_monitor = ZHeadMechanicsMonitor(name = 'monitor', sm = sm, m = m, l = l)
        sm.add_widget(z_head_mechanics_monitor)

        z_head_mechanics_booting = ZHeadMechanicsBooting(name = 'booting', sm = sm, m = m)
        sm.add_widget(z_head_mechanics_booting)

        z_head_mechanics_manual_move = ZHeadMechanicsManualMove(name = 'manual_move', sm = sm, m = m)
        sm.add_widget(z_head_mechanics_manual_move)

        sm.current = 'booting'
        return sm

if __name__ == '__main__':
    ZHeadMechanicsApp().run()
