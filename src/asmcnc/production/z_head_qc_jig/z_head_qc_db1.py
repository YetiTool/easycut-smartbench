from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import re

Builder.load_string(
    """
<ZHeadQCDB1>:
    serial_no_input:serial_no_input
    error_label:error_label

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1.00

        Label:
            font_size: str(0.01875 * app.width) + 'sp'
            size_hint_y: 0.2

        GridLayout:
            cols: 1
            rows: 4

            spacing:0.0625*app.width

            GridLayout:
                cols: 1
                rows: 1

                padding:[dp(0.25)*app.width, 0]

                TextInput:
                    id: serial_no_input
                    font_size: dp(0.0625*app.width)
                    multiline: False

            Label:
                text: '^ Enter ZH Serial number: ^'
                font_size: dp(0.0625*app.width)

            Label:
                id: error_label
                font_size: dp(0.0375*app.width)

            Button:
                on_press: root.enter_next_screen()
                text: 'OK'
                font_size: dp(0.0375*app.width)
                size_hint_y: 0.6

"""
)


class ZHeadQCDB1(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQCDB1, self).__init__(**kwargs)
        self.sm = kwargs["sm"]
        self.m = kwargs["m"]

    def validate_serial_number(self, serial):
        expression = "(zh)\\d{4}"
        pattern = re.compile(expression)
        match = bool(pattern.match(serial))
        return match

    def enter_next_screen(self):
        serial_number = self.serial_no_input.text.lower().replace(" ", "")
        validated = self.validate_serial_number(serial_number)
        if not validated:
            self.error_label.text = "Serial number invalid"
            return
        self.sm.get_screen("qcDB3").set_serial_no(serial_number)
        self.sm.get_screen("qcDB4").set_serial_no(serial_number)
        self.sm.get_screen("qcDB2").set_serial_no(serial_number)
        self.sm.current = "qcDB2"
