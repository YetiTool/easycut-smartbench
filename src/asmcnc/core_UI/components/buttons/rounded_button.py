from kivy.graphics import RoundedRectangle, Color

from asmcnc.core_UI.components.buttons.button_base import ButtonBase


class RoundedButton(ButtonBase):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)

        self.background_color = (0, 0, 0, 0)
        self.background_normal = ""
        self.background_down = ""

        self.bind(pos=self.update)
        self.bind(size=self.update)

    def update(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*[230 / 255., 74 / 255., 25 / 255., 1.]) if self.state == 'normal' else Color(*[208 / 255., 67 / 255., 23 / 255., 1.])
            RoundedRectangle(pos=self.pos, size=self.size, radius=[15, 15])
