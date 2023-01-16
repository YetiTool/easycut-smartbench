from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from asmcnc.comms.router_machine import RouterMachine
from settings.settings_manager import Settings
from asmcnc.job.job_data import JobData
from asmcnc.comms.localization import Localization

from asmcnc.production.spindle_test_jig.spindle_test_rig_1 import SpindleTestRig1


class SpindleTest(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())

        sett = Settings(sm)

        l = Localization()

        jd = JobData(localization=l, settings_manager=sett)

        m = RouterMachine('COM3', sm, sett, l, jd)

        screen_1 = SpindleTestRig1(name='screen_1', screen_manager=sm, machine=m)
        sm.add_widget(screen_1)

        sm.current = 'screen_1'

        return sm


if __name__ == '__main__':
    SpindleTest().run()