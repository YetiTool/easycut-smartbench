from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_string("""
<YetiPilotWidget>:
    switch:switch
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
                id: switch
                on_active: root.toggle_yeti_pilot(self)
                
""")


class YetiPilotWidget(Widget):
    def __init__(self, **kwargs):
        super(YetiPilotWidget, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.yp = kwargs['yetipilot']

        self.disable_yeti_pilot()

    def switch_reflects_yp(self):
        self.switch.active = self.yp.use_yp

    def toggle_yeti_pilot(self, switch):
        if switch.active:
            self.yp.enable()
        else:
            self.yp.disable()

    def disable_yeti_pilot(self):
        self.switch.active = False
        self.toggle_yeti_pilot(self.switch)
