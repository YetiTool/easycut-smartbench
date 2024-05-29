from kivy.animation import Animation
from kivy.clock import Clock
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
            
<FastBlinkingWidget>:
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
            Animation(bg_color=YELLOW, duration=0.5, s=1.0/30.0)
            + Animation(bg_color=TRANSPARENT_YELLOW, duration=0.5, s=1.0/30.0)
        )
        self.animation.repeat = True

        self.bind(blinking=self.on_blinking)

    def on_blinking(self, *args):
        if self.blinking:
            self.animation.start(self)
        else:
            self.animation.cancel(self)
            self.bg_color = TRANSPARENT_YELLOW


class FastBlinkingWidget(Widget):
    """Temporary fix for BlinkingWidget. Animation class causes performance issues."""

    blinking = BooleanProperty(False)
    bg_color = ObjectProperty(TRANSPARENT_YELLOW)
    blink_event = None  # Clock event

    def __init__(self, **kwargs):
        super(FastBlinkingWidget, self).__init__(**kwargs)
        self.bind(blinking=self.on_blinking)

    def on_blinking(self, *args):
        if self.blinking:
            self.blink_event = Clock.schedule_interval(self.blink, 0.5)
        else:
            self.blink_event.cancel()
            self.bg_color = TRANSPARENT_YELLOW

    def blink(self, dt):
        self.bg_color = YELLOW if self.bg_color == TRANSPARENT_YELLOW else TRANSPARENT_YELLOW
