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


class BlinkEventManager:
    """Event manager for blinking widgets. Used so that all blinking widgets blink at the same time, and only
    one event is scheduled at a time."""
    blink_event = None


class FastBlinkingWidget(Widget):
    """Temporary fix for BlinkingWidget. Animation class causes performance issues."""

    # Class variables
    instances = []
    blink_color = TRANSPARENT_YELLOW

    # Instance variables
    blinking = BooleanProperty(False)
    bg_color = ObjectProperty(TRANSPARENT_YELLOW)

    def __init__(self, **kwargs):
        super(FastBlinkingWidget, self).__init__(**kwargs)
        self.__class__.instances.append(self)
        self.bind(blinking=self.on_blinking)

    def on_blinking(self, *args):
        if self.blinking:
            if BlinkEventManager.blink_event is None:
                BlinkEventManager.blink_event = Clock.schedule_interval(self.__class__.blink_all, 0.5)
        else:
            if not any(instance.blinking for instance in self.__class__.instances):
                BlinkEventManager.blink_event.cancel()
                BlinkEventManager.blink_event = None
            self.bg_color = TRANSPARENT_YELLOW

    @classmethod
    def blink_all(cls, dt):
        cls.blink_color = YELLOW if cls.blink_color == TRANSPARENT_YELLOW else TRANSPARENT_YELLOW
        for instance in cls.instances:
            if instance.blinking:
                instance.bg_color = cls.blink_color
