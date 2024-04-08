from kivy.base import runTouchApp
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout

from asmcnc.core_UI.utils import color_provider


class StatusBar(BoxLayout):
    """Status bar for the app."""

    bg_color = ListProperty(color_provider.get_rgba("green"))

    def __init__(self, **kwargs):
        super(StatusBar, self).__init__(**kwargs)

        self.bind(bg_color=self.__update_bg)
        self.bind(size=self.__update_bg)

    def set_bg_color(self, color):
        """
        Set the background color of the status bar.
        Example usage: status_bar.set_bg_color(color_provider.get_rgba("red"))
        :param color: The color to set the background to.
        :return: None
        """
        self.bg_color = color

    def __update_bg(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*color_provider.get_rgba("green"))
            Rectangle(pos=self.pos, size=self.size)


if __name__ == "__main__":
    box = BoxLayout(orientation="vertical")
    filler = BoxLayout(size_hint_y=0.9)
    status_bar = StatusBar(size_hint_y=0.1)
    box.add_widget(filler)
    box.add_widget(status_bar)
    runTouchApp(box)
