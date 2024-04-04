from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.uix.button import Button


class HoldButton(Button):
    released = False

    background_down = ""
    background_normal = ""
    background_color = None
    held_background_color = None

    rect = None
    clock = None
    animation = None

    def __init__(self, hold_time, callback, background_color, held_background_color, **kwargs):
        super(HoldButton, self).__init__(**kwargs)
        self.hold_time = hold_time
        self.callback = callback
        self.background_color = background_color
        self.held_background_color = held_background_color

        self.bind(on_press=self.on_press)
        self.bind(on_release=self.on_release)

        self.canvas.add(Color(*self.held_background_color))

        self.rect = Rectangle(pos=self.pos, size=(0, self.height))
        self.canvas.add(self.rect)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def start_animation(self):
        self.animation = Animation(size=(self.width, self.height), duration=self.hold_time)
        self.animation.start(self.rect)

    def stop_animation(self):
        if self.animation:
            self.animation.stop(self.rect)
            self.rect.size = (0, self.height)
            self.clock.cancel()

    def on_press(self, *args):
        if self.animation:
            self.stop_animation()

        self.released = False
        self.clock = Clock.schedule_once(self.call_if_not_released, self.hold_time)
        self.start_animation()

    def call_if_not_released(self, *args):
        if not self.released:
            self.callback()

    def on_release(self, *args):
        self.released = True
        self.stop_animation()
        self.clock.cancel()


class WarningHoldButton(HoldButton):
    background_color = (255.0 / 255, 246.0 / 255, 143.0 / 255, 1)
    held_background_color = (255. / 255, 165.0 / 255, 0, 0.3)

    def __init__(self, hold_time, callback, **kwargs):
        super(WarningHoldButton, self).__init__(hold_time, callback,
                                                self.background_color, self.held_background_color, **kwargs)
