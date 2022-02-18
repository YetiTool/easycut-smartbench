from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string("""
<LBCalibration4>:
    serial_no_input:serial_no_input

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1.00

        Button:
            text: '<<< REPEAT CALIBRATION'
            on_press: root.enter_prev_screen()
            text_size: self.size
            markup: 'True'
            halign: 'left'
            valign: 'middle'
            padding: [dp(10),0]
            size_hint_y: 0.2
            size_hint_x: 0.5
            font_size: dp(20)

        GridLayout:
            cols: 1
            rows: 3

            spacing: 50

            Label:
                text: 'Enter LB serial number:'
                font_size: dp(50)
            
            GridLayout:
                cols: 1
                rows: 1

                padding: [200, 0]

                TextInput:
                    id: serial_no_input
                    font_size: dp(50)

            Button:
                on_press: root.enter_next_screen()
                text: 'OK'
                font_size: dp(30)
                size_hint_y: 0.6

""")

class LBCalibration4(Screen):
    def __init__(self, **kwargs):
        super(LBCalibration4, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    def enter_prev_screen(self):
        self.sm.current = 'lbc2'

    def enter_next_screen(self):
        self.sm.get_screen('lbc5').set_serial_no(self.serial_no_input.text)
        self.sm.current = 'lbc5'