from kivy.app import App
from kivy.lang import Builder

kv = """
#:import color_provider asmcnc.core_UI.utils.color_provider

BoxLayout:
    Label:
        text: "Hello, World!"
        color: color_provider.get_rgba("green")
        font_size: app.get_scaled_width(20.0)
"""


class TestApp(App):
    def build(self):
        return Builder.load_string(kv)


if __name__ == "__main__":
    TestApp().run()
