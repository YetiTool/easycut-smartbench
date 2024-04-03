from kivy.base import runTouchApp
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label

from asmcnc.core_UI.utils import color_provider

layout = BoxLayout(
    orientation="vertical",
    size_hint=(1, 1),
)


def update_size(instance, value):
    instance.canvas.before.clear()
    with instance.canvas.before:
        Color(rgba=color_provider.get_rgba("primary"))
        Rectangle(size=instance.size, pos=instance.pos)


layout.bind(size=update_size)

carousel = Carousel(
    direction="right",
    loop=True,
    size_hint=(1, 1),
)

for color_name in color_provider.Colours:
    color = color_provider.get_rgba(color_name)
    color_hex = color_provider.get_color_hex(color_name)
    markup_color_string = color_provider.get_markup_color_string(color_name, color_name)

    print(color, color_hex, markup_color_string)

    carousel.add_widget(Label(
        text=markup_color_string,
        color=color,
        font_size=20,
        markup=True
    ))

layout.add_widget(carousel)

runTouchApp(layout)
