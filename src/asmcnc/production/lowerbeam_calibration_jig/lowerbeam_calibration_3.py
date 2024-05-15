from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string("""
<LBCalibration3>:
    canvas:
        Color:
            rgba: hex('#4CAF50FF')
        Rectangle:
            pos:self.pos
            size: self.size

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
            padding: app.get_scaled_tuple([10, 0])
            size_hint_y: 0.2
            size_hint_x: 0.5
            font_size: app.get_scaled_width(20)

        GridLayout:
            cols: 1
            rows: 2

            Label:
                text: 'Calibration complete!'
                font_size: app.get_scaled_width(50)
            
            Button:
                on_press: root.enter_next_screen()
                text: 'OK'
                font_size: app.get_scaled_width(30)
                size_hint_y: 0.2
                size_hint_x: 0.3

""")

class LBCalibration3(Screen):
    def __init__(self, **kwargs):
        super(LBCalibration3, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    def enter_prev_screen(self):
        self.sm.current = 'lbc2'

    def enter_next_screen(self):
        self.sm.current = 'lbc4'