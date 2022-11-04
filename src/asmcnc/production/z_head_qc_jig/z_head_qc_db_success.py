from asmcnc.comms.logging import log_exporter
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<ZHeadQCDBSuccess>:
    success_label:success_label

    canvas:
        Color:
            rgba: hex('#4CAF50FF')
        Rectangle:
            pos:self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1.00

        GridLayout:
            cols: 1
            rows: 2

            Label:
                id: success_label
                text: 'Database updated for '
                font_size: dp(50)
                text_size: self.size
                halign: 'center'
                valign: 'center'
            
            Button:
                on_press: root.enter_next_screen()
                text: 'OK'
                font_size: dp(30)
                size_hint_y: 0.2
                size_hint_x: 0.3

""")

class ZHeadQCDBSuccess(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQCDBSuccess, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    def enter_next_screen(self):
        self.sm.current = 'qc6'

    def set_serial_no(self, serial_no):
        self.success_label.text = 'Database updated for:\n' + serial_no
