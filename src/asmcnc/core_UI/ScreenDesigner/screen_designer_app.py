from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition

from asmcnc.comms.localization import Localization
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.core_UI.ScreenDesigner.designer_controller import DesignerController
import asmcnc.core_UI.path_utils as pu


class DesignerSplashScreen(Screen):
    """Splash screen for designer. Will be loaded on startup. Screen will switch, when main screen is loaded."""
    def __init__(self, **kwargs):
        super(DesignerSplashScreen, self).__init__(name='DesignerSplashScreen', **kwargs)

        self.sm = App.get_running_app().sm
        self.available_screens = {}
        self.main_layout = FloatLayout()
        self.add_widget(self.main_layout)
        # background image
        self.background_image = Image(source=pu.get_path('Inspector_Widget.png'), text='.')
        self.main_layout.add_widget(self.background_image)

    def on_enter(self, *args):
        Clock.schedule_once(lambda dt: App.get_running_app().controller.build_designer_screen(), 6.0)


class ScreenDesignerApp(App):
    """
    This app can be used to develop screens. You can either edit existing screens or create a new screen from scratch.
    """
    def __init__(self, **kwargs):
        super(ScreenDesignerApp, self).__init__(**kwargs)

        self.l = Localization()
        self.sm = ScreenManager(transition=WipeTransition())
        self.controller = DesignerController()
        self.icon = pu.get_path('inspection.png')

        self.width = 800
        self.height = 480

    def build(self):
        main_screen = DesignerSplashScreen()
        self.sm.add_widget(main_screen)
        self.title = "Inspector Widget"
        self.sm.current = main_screen.name
        return self.sm


if __name__ == '__main__':
    try:
        Config.set('graphics', 'width', '1200')
        Config.set('graphics', 'height', '720')
        Config.set('kivy', 'keyboard_mode', 'system')
        Config.write()

        ScreenDesignerApp().run()
    except Exception as e:
        Logger.exception(e)
