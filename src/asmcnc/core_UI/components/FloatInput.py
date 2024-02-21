from kivy.uix.textinput import TextInput
from kivy.clock import Clock


class FloatInput(TextInput):

    def __init__(self, **kwargs):
        super(FloatInput, self).__init__(**kwargs)
        self.bind(focus=self.text_on_focus)

    def text_on_focus(self, instance, value):
        if value:
            Clock.schedule_once(lambda dt: instance.select_all())
