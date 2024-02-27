from kivy import Logger
from kivy.animation import Animation
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget

Logger.setLevel("DEBUG")

# Couldn't update the canvas instruction in code, as I need to use Color but also need to set it
# to my list property, so I needed to use builder string

Builder.load_string("""
<BlinkingWidget>:
    canvas.before:
        Color:
            rgba: self.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
""")


class BlinkingWidget(Widget):
    """
    A widget with a toggleable red blinking background.
    You can wrap any widget with this widget to make it blink.
    """

    blinking = BooleanProperty(False)
    bg_color = ObjectProperty([1, 0, 0, 0])

    def __init__(self, **kwargs):
        super(BlinkingWidget, self).__init__(**kwargs)

        self.animation = (
            Animation(bg_color=(1, 0, 0, 1), duration=0.5)
            + Animation(bg_color=(1, 0, 0, 0), duration=0.5)
        )
        self.animation.repeat = True

        self.bind(blinking=self.on_blinking)
        self.blinking = True

    def on_blinking(self, instance, value):
        if value:
            self.animation.start(self)
        else:
            self.animation.stop(self)


if __name__ == '__main__':
    box_layout = BoxLayout()
    image = Image(
        source="/Users/archiejarvis/PycharmProjects/easycut/easycut-smartbench/src/asmcnc/skavaUI/img/spindle_on.png",
        )
    blinking_widget = BlinkingWidget(size=image.texture_size, size_hint=(None, None))
    blinking_widget.add_widget(image)

    box_layout.add_widget(blinking_widget)

    runTouchApp(box_layout)
