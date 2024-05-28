from kivy.graphics import RoundedRectangle, Color
from kivy.uix.button import Button


class RoundedButton(Button):

    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_color = 0, 0, 0, 0
        self.background_normal = ""
        self.background_down = ""
        self.bind(pos=self.update)
        self.bind(size=self.update)

    def update(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            (
                Color(*[230 / 255.0, 74 / 255.0, 25 / 255.0, 1.0])
                if self.state == "normal"
                else Color(*[208 / 255.0, 67 / 255.0, 23 / 255.0, 1.0])
            )
            RoundedRectangle(pos=self.pos, size=self.size, radius=[15, 15])
