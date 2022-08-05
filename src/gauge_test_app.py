from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from asmcnc.comms.localization import Localization
from asmcnc.comms.router_machine import RouterMachine
from asmcnc.job.job_data import JobData
from settings.settings_manager import Settings

from asmcnc.gauges.gauge_test_screen import GaugeTestScreen

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

        gauge_test_screen = GaugeTestScreen(name='gauge_test', sm=sm, m=m, jd=jd, l=l)
        sm.add_widget(gauge_test_screen)

        sm.current = 'gauge_test'

        return sm


if __name__ == '__main__':
    GaugeTestApp().run()
