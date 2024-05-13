"""
Created on 19 August 2020
@author: Letty
"""
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

Builder.load_string("""
#:import LabelBase asmcnc.core_UI.components.labels.base_label


<BrushMonitorWidget>

    empty_monitor: empty_monitor
    fuel_bar: fuel_bar
    percentage: percentage

    Image:
        id: empty_monitor
        source: "./asmcnc/apps/maintenance_app/img/empty_bar.png"
        allow_stretch: True
        keep_ratio: False
        size: self.parent.size
        pos: self.parent.pos
    Image:
        id: fuel_bar
        source: "./asmcnc/apps/maintenance_app/img/green_bar.png"
        allow_stretch: True
        keep_ratio: False
        size: [self.parent.width*root.monitor_percentage, self.parent.height*0.9]
        x: self.parent.x + (self.parent.width*root.x_pos_modifier)
        y: self.parent.y+(self.parent.height*0.05)

    LabelBase: 
        id: percentage
        color: color_provider.get_rgba("white")
        font_size: dp(0.0625*app.width)
        markup: True
        halign: "right"
        valign: "middle"
        text_size: self.size
        text: root.percentage_text
        size: dp(130), self.parent.height
        x: self.parent.x+(self.parent.width*0.75)
        y: self.parent.y

        
"""
)


class BrushMonitorWidget(Widget):
    monitor_percentage = NumericProperty()
    x_pos_modifier = NumericProperty()
    percentage_text = ""

    def __init__(self, **kwargs):
        super(BrushMonitorWidget, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.monitor_percentage = kwargs["input_percentage"]
        self.x_pos_modifier = 1 - self.monitor_percentage
        self.percentage_text = str(int(self.monitor_percentage * 100)) + "%"
        self.update_monitor()

    def set_percentage(self, value):
        self.monitor_percentage = float(value)
        self.x_pos_modifier = 1 - self.monitor_percentage
        self.update_monitor()

    def update_monitor(self):
        self.fuel_bar.size = [
            self.empty_monitor.width * self.monitor_percentage,
            self.empty_monitor.height * 0.9,
        ]
        self.fuel_bar.x = self.empty_monitor.x + self.empty_monitor.width * (
            1 - self.monitor_percentage
        )
        self.percentage.text = str(int(round(self.monitor_percentage * 100))) + "%"
        if self.monitor_percentage > 0.5:
            self.fuel_bar.source = "./asmcnc/apps/maintenance_app/img/green_bar.png"
        elif self.monitor_percentage <= 0.5 and self.monitor_percentage > 0.3:
            self.fuel_bar.source = "./asmcnc/apps/maintenance_app/img/yellow_bar.png"
        elif self.monitor_percentage < 0.3 and self.monitor_percentage > 0.1:
            self.fuel_bar.source = "./asmcnc/apps/maintenance_app/img/orange_bar.png"
        elif self.monitor_percentage <= 0.1:
            self.fuel_bar.source = "./asmcnc/apps/maintenance_app/img/red_bar.png"
