from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.clock import Clock

from asmcnc.comms.router_machine import RouterMachine
from settings.settings_manager import Settings
from asmcnc.job.job_data import JobData
from asmcnc.comms.localization import Localization
from asmcnc.comms import smartbench_flurry_database_connection

from asmcnc.skavaUI.screen_home import HomeScreen
from asmcnc.skavaUI import screen_door # @UnresolvedImport

from asmcnc.production.spindle_test_jig.spindle_test_jig_1 import SpindleTestJig1
from asmcnc.production.spindle_test_jig.spindle_test_jig_console import SpindleTestJigConsole


class SpindleTest(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())

        sett = Settings(sm)

        l = Localization()

        jd = JobData(localization=l, settings_manager=sett)

        m = RouterMachine('COM3', sm, sett, l, jd)

        db = smartbench_flurry_database_connection.DatabaseEventManager(sm, m, sett)

        if m.s.is_connected():
            Clock.schedule_once(m.s.start_services, 4)

        home_screen = HomeScreen(name='home', screen_manager=sm, machine=m, job=jd, settings=sett, localization=l)
        sm.add_widget(home_screen)

        screen_1 = SpindleTestJig1(name='spindle_test_1', screen_manager=sm, machine=m)
        sm.add_widget(screen_1)

        screen_console = SpindleTestJigConsole(name='spindle_test_console', screen_manager=sm, machine=m, localization=l)
        sm.add_widget(screen_console)

        door_screen = screen_door.DoorScreen(name = 'door', screen_manager = sm, machine =m, job = jd, database = db, localization = l)
        sm.add_widget(door_screen)

        sm.current = 'spindle_test_1'
        return sm


if __name__ == '__main__':
    SpindleTest().run()
