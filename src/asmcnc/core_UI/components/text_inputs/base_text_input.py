from kivy.clock import Clock
from kivy.uix.textinput import TextInput

from asmcnc.core_UI.hoverable import HoverBehavior


class TextInputBase(TextInput, HoverBehavior):
    """
    Description:
    This is the base class for all text inputs used in our apps. It offers base functionality, like selecting all content when focused.

    Base classes:
    kivy.uix.textinput.TextInput
    asmcnc.core_UI.hoverable.HoverBehavior
    """
    def __init__(self, **kwargs):
        super(TextInputBase, self).__init__(**kwargs)

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
        return super(TextInputBase, self).on_touch_down(touch)
