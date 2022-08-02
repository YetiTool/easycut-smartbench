from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen

from asmcnc.comms.localization import Localization
from asmcnc.comms.router_machine import RouterMachine
from asmcnc.gauges.go_screen_gauge import GoScreenGauge
from asmcnc.job.job_data import JobData
from settings.settings_manager import Settings

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


class GaugeTestScreen(Screen):
    def __init__(self, **kwargs):
        super(GaugeTestScreen, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

        self.gauge = GoScreenGauge(
            title='Gauge Test',
            key='TEST',
            max_value=100,
            lower_boundary=15,
            upper_boundary=15,
            inverse=False,
            unit='',
            factor=1,
            sm=self.sm,
            m=self.m
        )

        self.add_widget(self.gauge)


if __name__ == '__main__':
    GaugeTestApp().run()
