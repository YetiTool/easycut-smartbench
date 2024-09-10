from kivy.app import App
from kivy.lang import Builder

kv = """
#:import color_provider ui.utils.color_provider

BoxLayout:
    Label:
        text: "Hello, World!"
        color: color_provider.get_rgba("green")
        font_size: 20
"""


class TestApp(App):
    def build(self):
        return Builder.load_string(kv)


if __name__ == "__main__":
    TestApp().run()
