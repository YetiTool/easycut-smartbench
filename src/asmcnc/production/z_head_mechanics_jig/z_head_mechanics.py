from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string("""
<ZHeadMechanics>:

    begin_test_button:begin_test_button

    test_progress_label:test_progress_label

    BoxLayout:
        orientation: 'vertical'
        padding: dp(5)
        spacing: dp(5)

        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(5)

            Button:
                id: begin_test_button
                size_hint_x: 2
                text: 'Begin Test'
                bold: True
                font_size: dp(25)
                background_color: hex('#00C300FF')
                background_normal: ''
                on_press: root.begin_test()

            Button:
                text: 'STOP'
                bold: True
                font_size: dp(25)
                background_color: [1,0,0,1]
                background_normal: ''
                on_press: root.stop()

        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(5)

            Label:
                size_hint_x: 4
                text: 'info'

            Button:
                text: 'GCODE Monitor'
                bold: True
                font_size: dp(25)
                text_size: self.size
                valign: 'middle'
                halign: 'center'
                on_press: root.go_to_monitor()

        Label:
            size_hint_y: 2
            id: test_progress_label
            text: 'Waiting...'
            font_size: dp(30)
            markup: True
            bold: True
            text_size: self.size
            valign: 'middle'
            halign: 'center'

""")


class ZHeadMechanics(Screen):
    def __init__(self, **kwargs):
        super(ZHeadMechanics, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    def begin_test(self):
        self.begin_test_button.disabled = True
        self.test_progress_label.text = 'Test running...\n[color=ff0000]WATCH FOR STALL THROUGHOUT ENTIRE TEST[/color]'

    def stop(self):
        self.begin_test_button.disabled = False
        self.test_progress_label.text = 'Waiting...'

    def go_to_monitor(self):
        self.sm.current = 'monitor'
