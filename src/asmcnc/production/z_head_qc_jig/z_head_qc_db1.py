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
            size_hint_y: 0.2

        GridLayout:
            cols: 1
            rows: 4

            spacing: 50

            GridLayout:
                cols: 1
                rows: 1

                padding: [200, 0]

                TextInput:
                    id: serial_no_input
                    font_size: dp(50)
                    multiline: False

            Label:
                text: '^ Enter ZH Serial number: ^'
                font_size: dp(50)

            Label:
                id: error_label
                font_size: dp(30)

            Button:
                on_press: root.enter_next_screen()
                text: 'OK'
                font_size: dp(30)
                size_hint_y: 0.6

"""
)


class ZHeadQCDB1(Screen):

    def __init__(self, **kwargs):
        self.sm = kwargs.pop("sm")
        self.m = kwargs.pop("m")
        super(ZHeadQCDB1, self).__init__(**kwargs)

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
