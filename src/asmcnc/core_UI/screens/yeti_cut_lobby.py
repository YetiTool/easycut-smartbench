from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from asmcnc import paths
from asmcnc.core_UI.utils import color_provider


class YetiCutLobbyScreen(Screen):
    def __init__(self, **kwargs):
        super(YetiCutLobbyScreen, self).__init__(**kwargs)

        root = GridLayout(rows=3)
        self.add_widget(root)

        with root.canvas.before:
            Color(*color_provider.Colors["primary"])
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        header_layout = FloatLayout(orientation="horizontal", pos_hint={"top": 1})
        root.add_widget(header_layout)

        back_button = Image(source=paths.get_resource("back_yc.png"))
        header_layout.add_widget(back_button)

        header_label = Label(text="YetiCut", font_size=40, color=color_provider.Colors["white"])
        header_layout.add_widget(header_label)

        apps_grid_layout = GridLayout(cols=3, spacing=10, size_hint_y=0.4, pos_hint={"center_y": 0.5})
        self.add_widget(apps_grid_layout)

        shapes_app = BoxLayout(orientation="vertical")
        shapes_app_icon = Image(source=paths.get_resource("shapes.png"))
        shapes_app.add_widget(shapes_app_icon)
        apps_grid_layout.add_widget(shapes_app)

        worktop_app = BoxLayout(orientation="vertical")
        worktop_app_icon = Image(source=paths.get_resource("worktop.png"))
        worktop_app.add_widget(worktop_app_icon)
        apps_grid_layout.add_widget(worktop_app)

        trace_app = BoxLayout(orientation="vertical")
        trace_app_icon = Image(source=paths.get_resource("trace.png"))
        trace_app.add_widget(trace_app_icon)
        apps_grid_layout.add_widget(trace_app)



    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == "__main__":
    from kivy.app import App

    class YetiCutLobbyApp(App):
        def build(self):
            return YetiCutLobbyScreen()

    YetiCutLobbyApp().run()