from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen


class StartingSmartBenchScreen(Screen):
    """The loading screen of the Easycut application."""

    def __init__(self, **kwargs):
        """Initialize the loading screen."""
        super(StartingSmartBenchScreen, self).__init__(**kwargs)
        self.register_event_type("on_loading_screen_open")

        self.name = "load_screen"

        background = Image(source="asmcnc/skavaUI/img/loading_screen.png")
        self.add_widget(background)

    def on_enter(self, *args):
        """When the screen is entered."""
        Clock.schedule_once(lambda dt: self.dispatch("on_loading_screen_open"), 3)

    def on_loading_screen_open(self, *args):
        """Event handler for when the loading is complete."""
        pass


if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager


    class TestApp(App):
        def build(self):
            sm = ScreenManager()
            sm.add_widget(StartingSmartBenchScreen())
            return sm


    TestApp().run()