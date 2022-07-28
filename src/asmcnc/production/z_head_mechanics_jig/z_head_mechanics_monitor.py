from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string("""
<ZHeadMechanicsMonitor>:

    gcode_monitor_container:gcode_monitor_container

    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)

        Button:
            text: 'Back'
            bold: True
            font_size: dp(25)
            on_press: root.back()

        BoxLayout:
            id: gcode_monitor_container
            size_hint_y: 5

""")


class ZHeadMechanicsMonitor(Screen):
    def __init__(self, **kwargs):
        super(ZHeadMechanicsMonitor, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    def back(self):
        self.sm.current = 'mechanics'
