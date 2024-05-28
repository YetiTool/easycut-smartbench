from asmcnc.comms.logging import log_exporter
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string(
    """
<LBCalibrationFail>:
    success_label:success_label

    canvas:
        Color:
            rgba: [1,0,0,1]
        Rectangle:
            pos:self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1.00

        Button:
            text: '<<< Back'
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
            rows: 2

            Label:
                id: success_label
                text: 'Database update failed'
                font_size: dp(50)
            
            Button:
                on_press: root.retry_send()
                text: 'RETRY DATA SEND'
                font_size: dp(30)
                size_hint_y: 0.2
                size_hint_x: 0.3

"""
)


class LBCalibrationFail(Screen):

    def __init__(self, **kwargs):
        self.sm = kwargs.pop("sm")
        self.m = kwargs.pop("m")
        super(LBCalibrationFail, self).__init__(**kwargs)

    def enter_prev_screen(self):
        self.sm.current = "lbc4"

    def retry_send(self):
        self.sm.current = "lbc4"

    def on_enter(self):
        log_exporter.create_trim_and_send_logs(self.serial, 1000)

    def set_serial_no(self, serial_no):
        self.serial = serial_no
        self.success_label.text = "Database update failed: " + serial_no
