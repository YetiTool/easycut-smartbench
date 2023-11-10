from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.skavaUI import widget_gcode_monitor
Builder.load_string(
    """
<ZHeadMechanicsMonitor>:

    gcode_monitor_container:gcode_monitor_container

    BoxLayout:
        orientation: 'vertical'
        padding: [dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
        spacing: dp(0.0208333333333*app.height)

        Button:
            text: 'Back'
            bold: True
            font_size: dp(0.03125*app.width)
            on_press: root.back()

        BoxLayout:
            id: gcode_monitor_container
            size_hint_y: 8

            canvas:
                Color:
                    rgba: hex('#E5E5E5FF')
                Rectangle:
                    size: self.size
                    pos: self.pos

"""
    )


class ZHeadMechanicsMonitor(Screen):

    def __init__(self, **kwargs):
        super(ZHeadMechanicsMonitor, self).__init__(**kwargs)
        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.l = kwargs['l']
        self.gcode_monitor_container.add_widget(widget_gcode_monitor.
            GCodeMonitor(machine=self.m, screen_manager=self.sm,
            localization=self.l))

    def back(self):
        self.sm.current = 'mechanics'
