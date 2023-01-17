from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.skavaUI import widget_gcode_monitor

Builder.load_string("""
<SpindleTestJigConsole>:
    gcode_monitor_container:gcode_monitor_container
    
    BoxLayout:
        orientation: 'vertical'
        
        Button:
            text: 'Back'
            on_press: root.back()
            size_hint_x: 1.0
            size_hint_y: 0.2
            
        BoxLayout:
            id: gcode_monitor_container
            size_hint_x: 1.0
            size_hint_y: 0.8

""")


class SpindleTestJigConsole(Screen):
    def __init__(self, **kwargs):
        super(SpindleTestJigConsole, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']

        self.gcode_monitor_container.add_widget(
            widget_gcode_monitor.GCodeMonitor(machine=self.m, screen_manager=self.sm,
                                              localization=self.l))

    def back(self):
        self.sm.current = 'spindle_test_1'