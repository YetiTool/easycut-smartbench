"""
@author archiejarvis on 31/05/2023
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

Builder.load_string("""
<SplashScreen>:
    Image:
        source: 'asmcnc/skavaUI/img/splash.png'
        allow_stretch: True
""")


class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)


class SplashScreenApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(SplashScreen(name='splash_screen'))

        return sm


if __name__ == '__main__':
    app = SplashScreenApp()
    app.run()