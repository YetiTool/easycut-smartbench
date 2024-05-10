from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from asmcnc.comms.flurry.flurry import Flurry
from asmcnc.comms.localization import Localization
from asmcnc.comms.router_machine import RouterMachine
from asmcnc.job.job_data import JobData
from settings.settings_manager import Settings


class TestApp(App):
    width = 800
    height = 480

    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.screen_manager = ScreenManager()
        self.settings_manager = Settings(self.screen_manager)
        self.localisation = Localization()
        self.job = JobData(settings_manager=self.settings_manager, localization=self.localisation)
        self.machine = RouterMachine("COM3", self.screen_manager, self.settings_manager, self.localisation, self.job)

    def build(self):
        self.flurry = Flurry()
        return self.screen_manager


if __name__ == "__main__":
    TestApp().run()