from kivy.uix.widget import Widget
from kivy.lang import Builder


Builder.load_string("""
<YetiPilotWidget>:
    BoxLayout:
        orientation: 'horizontal'
        size: self.parent.size
        pos: self.parent.pos
        padding: 10
        
        BoxLayout:
            size_hint_x: 0.6
            spacing: 5
            Label:
                text: '[b]YetiPilot[/b]'
                color: 0, 0, 0, 1
                markup: True
                
            Switch:
                on_touch_down: root.toggle_yeti_pilot()
            
        BoxLayout:
            spacing: 0
            Label:
                text: '0'
                color: 0,0,0,1
                size_hint_x: 0.2
                
            Slider:
                min: 0
                max: 100
                step: 1
            
            Label:
                text: '100'
                color: 0,0,0,1
                size_hint_x: 0.2

""")

from asmcnc.job.yetipilot.screens.screen_yeti_pilot_cancel import YetiPilotCancelScreen


class YetiPilotWidget(Widget):
    def __init__(self, **kwargs):
        super(YetiPilotWidget, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']

    def toggle_yeti_pilot(self):
        if not self.sm.has_screen('yeti_pilot_cancel'):
            yeti_pilot_cancel = YetiPilotCancelScreen(name='yeti_pilot_cancel', screen_manager=self.sm)
            self.sm.add_widget(yeti_pilot_cancel)

        self.sm.current = 'yeti_pilot_cancel'


