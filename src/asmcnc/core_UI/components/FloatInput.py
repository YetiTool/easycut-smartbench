from kivy.uix.textinput import TextInput
from kivy.clock import Clock


class FloatInput(TextInput):
    """TextInput field with automatic content selection when focused. Text is validated to float when unfocused."""

    def __init__(self, **kwargs):
        super(FloatInput, self).__init__(**kwargs)

        self.input_filter = 'float'

    def on_focus(self, instance, value):
        """Selects all text when focused. text validation is done when unfocused."""
        if value:
            Clock.schedule_once(lambda dt: instance.select_all())
        else:
            if self.text != '':
                try:
                    self.text = str(float(self.text))
                except:
                    pass
            else:
                self.text = str(float(0))

    def on_touch_down(self, touch):
        """If touch didn't hit, lose focus. Call to super for normal handling."""
        collision = self.collide_point(touch.x, touch.y)
        if not collision:
            self.focus = False
        return super(FloatInput, self).on_touch_down(touch)

