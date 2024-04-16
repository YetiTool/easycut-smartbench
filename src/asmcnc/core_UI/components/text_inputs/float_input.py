from asmcnc.core_UI.components.text_inputs.max_length_input import MaxLengthInput


class FloatInput(MaxLengthInput):
    """TextInput field with automatic content selection when focused. Text is validated to float when unfocused."""

    def __init__(self, positive_only=True, **kwargs):
        super(FloatInput, self).__init__(max_length=6, **kwargs)
        self.input_filter = 'float'
        self.positive_only = positive_only

    def on_text(self, instance, value):
        """Prevents '-' to be written to avoid negative numbers"""
        if self.positive_only:
            self.text = value.replace("-", "")
        super(FloatInput, self).on_text(instance, self.text)


if __name__ == "__main__":
    from kivy.base import runTouchApp
    from kivy.uix.boxlayout import BoxLayout

    box_layout = BoxLayout(orientation="vertical")
    box_layout.add_widget(FloatInput())

    runTouchApp(box_layout)
