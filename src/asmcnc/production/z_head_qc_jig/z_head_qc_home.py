from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.lang import Builder


Builder.load_string("""
<ZHeadQCHome>:
    BoxLayout:
        orientation: 'vertical'

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 1
            rows: 3

            Label: 
                text: 'Have you just updated the FW on this Z Head?'
                color: 1,1,1,1
                text_size: self.size
                markup: 'True'
                halign: 'center'
                valign: 'middle'
                font_size: dp(30)

            GridLayout: 
                cols: 2

                Button:
                    text: 'YES - Take me to QC!'
                    font_size: dp(20)
                    on_press: root.enter_qc()

                Button:
                    text: 'NO - Update FW now!'
                    font_size: dp(20)

            Button: 
                text: 'Secret option C - take me to WARRANTY QC!'
                font_size: dp(20)
                on_press: root.secret_option_c()
""")


class ZHeadQCHome(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQCHome, self).__init__(**kwargs)

        self.sm = kwargs['sm']

        self.start_calibration_timer(0.5)

    def start_calibration_timer(self, minutes):
        self.sm.get_screen('qc3').update_time(minutes*30)

    def enter_qc(self):
        self.sm.current = 'qc1'

    def secret_option_c(self):
        self.sm.current = 'qcWC'


