from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.widget import Widget


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
            Animation(bg_color=YELLOW, duration=0.5, step=1/30)
            + Animation(bg_color=TRANSPARENT_YELLOW, duration=0.5, step=1/30)
        )
        self.animation.repeat = True

        self.bind(blinking=self.on_blinking)

    def on_blinking(self, *args):
        if self.blinking:
            self.animation.start(self)
        else:
            self.animation.cancel(self)
            self.bg_color = TRANSPARENT_YELLOW
