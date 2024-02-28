from kivy import Logger
from kivy.animation import Animation
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
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

YELLOW = [240. / 255, 1, 0, 1]
TRANSPARENT_YELLOW = [240.0 / 255, 1, 0, 0]


class BlinkingWidget(Widget):
    """
    A widget with a toggleable red blinking background.
    You can wrap any widget with this widget to make it blink.
    """

    blinking = BooleanProperty(False)
    bg_color = ObjectProperty(TRANSPARENT_YELLOW)

    def __init__(self, **kwargs):
        super(BlinkingWidget, self).__init__(**kwargs)

        self.animation = (
                Animation(bg_color=YELLOW, duration=0.5)
                + Animation(bg_color=TRANSPARENT_YELLOW, duration=0.5)
        )
        self.animation.repeat = True

        self.bind(blinking=self.on_blinking)

    def on_blinking(self, *args):
        if self.blinking:
            self.animation.start(self)
        else:
            self.animation.cancel(self)
            self.bg_color = TRANSPARENT_YELLOW


if __name__ == '__main__':
    box_layout = BoxLayout()


    def on_press(*args):
        setattr(blinking_widget, "blinking", not blinking_widget.blinking)


    button = Button(
        background_normal="/Users/archiejarvis/PycharmProjects/easycut/easycut-smartbench/src/asmcnc/skavaUI/img/spindle_off.png",
        background_down="/Users/archiejarvis/PycharmProjects/easycut/easycut-smartbench/src/asmcnc/skavaUI/img/spindle_off.png",
        on_press=on_press)

    blinking_widget = BlinkingWidget(size=button.size, size_hint=(None, None))
    blinking_widget.add_widget(button)

    box_layout.add_widget(blinking_widget)

    runTouchApp(box_layout)
