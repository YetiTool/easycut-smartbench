from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.lang import Builder

from asmcnc.comms.router_machine import RouterMachine
from asmcnc.comms import server_connection
from asmcnc.apps.app_manager import AppManagerClass
from settings.settings_manager import Settings
from asmcnc.job.job_data import JobData
from asmcnc.comms.localization import Localization
from kivy.clock import Clock
from asmcnc.comms import smartbench_flurry_database_connection

from asmcnc.gauges.go_screen_gauge import GoScreenGauge

Cmport = 'COM3'


class GaugeTestApp(App):
    def build(self):
        sm = ScreenManager(
            transition=NoTransition()
        )

        sett = Settings(sm)

        l = Localization()

        jd = JobData(localization=l, settings_manager=sett)

        m = RouterMachine(Cmport, sm, sett, l, jd)

        if m.s.is_connected():
            Clock.schedule_once(m.s.start_services, 4)

        gauge_test_screen = GaugeTestScreen(sm=sm, m=m, jd=jd, l=l)
        sm.add_widget(gauge_test_screen)

        return sm


class GaugeTestScreen(Screen):
    def __init__(self, **kwargs):
        super(GaugeTestScreen, self).__init__(**kwargs)
        self.gauge = GoScreenGauge(sm=kwargs['sm'], m=kwargs['m'])
        self.add_widget(self.gauge)


if __name__ == '__main__':
    go_screen_app = GaugeTestApp()
