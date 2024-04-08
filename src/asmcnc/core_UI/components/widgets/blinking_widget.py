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
        self.blinking_event = None
        self.bind(blinking=self.on_blinking)

    def on_blinking(self, *args):
        if self.blinking:
            self.blinking_event = Clock.schedule_interval(self.update_color, 0.5)
        else:
            self.blinking_event.cancel()
            self.bg_color = TRANSPARENT_YELLOW

    def update_color(self, dt):
        if self.bg_color == YELLOW:
            self.bg_color = TRANSPARENT_YELLOW
        else:
            self.bg_color = YELLOW