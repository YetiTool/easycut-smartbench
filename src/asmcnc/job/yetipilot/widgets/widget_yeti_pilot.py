from kivy.uix.widget import Widget
from kivy.lang import Builder
from asmcnc.job.yetipilot.main.yetipilot import YetiPilot
from math import ceil


Builder.load_string("""
<YetiPilotWidget>:
    power_slider:power_slider
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
                on_active: root.toggle_yeti_pilot()
            
        BoxLayout:
            spacing: 0
            orientation: 'vertical'
            
            Label:
                text: str(int(root.power_slider.value * 20)) + 'W'
                color: 0,0,0,1
            
            BoxLayout:
                spacing: 0
                Label:
                    text: '0'
                    color: 0,0,0,1
                    size_hint_x: 0.2
                    
                Slider:
                    id: power_slider
                    min: 1
                    max: 100
                    step: 1
                    on_value: root.on_slider_value_change()
                
                Label:
                    text: '100'
                    color: 0,0,0,1
                    size_hint_x: 0.2
                

""")


def get_closest_multiple(n, x):
    return int(ceil(n / float(x))) * x


class YetiPilotWidget(Widget):
    def __init__(self, **kwargs):
        super(YetiPilotWidget, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.jd = kwargs['job_data']

        self.switch.active = True
        self.toggle_yeti_pilot()
        self.power_slider.value = get_closest_multiple(self.m.s.autopilot_instance.digital_spindle_target_watts, 20) / 20

    def toggle_yeti_pilot(self):
        if not self.m.s.autopilot_instance:
            self.m.s.autopilot_instance = YetiPilot(screen_manager=self.sm, machine=self.m, job_data=self.jd)
        self.m.s.autopilot_instance.set_enabled(self.switch.active)

    def on_slider_value_change(self):
        if self.m.s.autopilot_instance is not None:
            self.m.s.autopilot_instance.set_target_power(self.power_slider.value * 20)

