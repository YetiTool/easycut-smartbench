from kivy.uix.textinput import TextInput


class MaxLengthInput(TextInput):
    """TextInput field with a maximum length. Text is truncated when the length exceeds the maximum."""

    def __init__(self, max_length, **kwargs):
        super(MaxLengthInput, self).__init__(**kwargs)

        self.max_length = max_length
        self.bind(text=self.on_text)

    def on_text(self, instance, value):
        """Truncate text if it exceeds the maximum length."""
        if len(value) > self.max_length:
            self.text = value[:self.max_length]


if __name__ == "__main__":
    from kivy.base import runTouchApp
    from kivy.uix.boxlayout import BoxLayout

    box_layout = BoxLayout(orientation="vertical")
    box_layout.add_widget(MaxLengthInput(max_length=6))

    runTouchApp(box_layout)
