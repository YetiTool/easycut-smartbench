from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string("""
<ZHeadMechanics>:

    test_progress_label:test_progress_label

    BoxLayout:
        orientation: 'vertical'
        padding: dp(5)
        spacing: dp(5)

        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(5)

            Button:
                size_hint_x: 2
                text: 'Begin Test'
                font_size: dp(20)
                background_color: [0,1,0,1]
                background_normal: ''

            Button:
                text: 'STOP'
                font_size: dp(20)
                background_color: [1,0,0,1]
                background_normal: ''

        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(5)

            Label:
                size_hint_x: 4
                text: 'info'

            Button:
                text: 'GCODE monitor'
                font_size: dp(20)

        Label:
            size_hint_y: 2
            id: test_progress_label
            text: 'Waiting...'
            font_size: dp(30)
            markup: True

""")


class ZHeadMechanics(Screen):
    def __init__(self, **kwargs):
        super(ZHeadMechanics, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
