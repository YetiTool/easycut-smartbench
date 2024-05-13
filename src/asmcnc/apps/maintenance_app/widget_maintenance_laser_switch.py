"""
Created on 10 June 2020
@author: Letty
widget to hold laser datum on_off 
"""
from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string(
    """

<LaserOnOffWidget>
    
    laser_image: laser_image
    laser_switch: laser_switch

    BoxLayout:
    
        size_hint: (None,None)
        height: dp(0.145833333333*app.height)
        width: dp(0.1875*app.width)
        pos: self.parent.pos
        padding:[0, 0, 0, 0]
        
        GridLayout:
            cols: 2
            rows: 1
            spacing:0.0125*app.width
            size_hint: (None,None)
            height: dp(0.145833333333*app.height)
            width: dp(0.21875*app.width)

            BoxLayout: 
                size_hint: (None, None)
                pos: self.parent.pos
                height: dp(0.145833333333*app.height)
                width: dp(0.10625*app.width)
                Switch:
                    id: laser_switch
                    background_color: color_provider.get_rgba("transparent")
                    center_x: self.parent.center_x
                    y: self.parent.y
                    pos: self.parent.pos
                    on_active: root.toggle_laser()
            BoxLayout: 
                size_hint: (None, None)
                pos: self.parent.pos
                height: dp(0.145833333333*app.height)
                width: dp(0.06875*app.width)
                padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]
                Image:
                    id: laser_image
                    source: "./asmcnc/apps/maintenance_app/img/laser_on.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True  


"""
)


class LaserOnOffWidget(Widget):
    def __init__(self, **kwargs):
        super(LaserOnOffWidget, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]

    def toggle_laser(self):
        if self.laser_switch.active:
            self.laser_image.source = "./asmcnc/apps/maintenance_app/img/laser_on.png"
            self.m.is_laser_enabled = True
            self.m.laser_on()
        else:
            self.laser_image.source = "./asmcnc/apps/maintenance_app/img/laser_off.png"
            self.m.laser_off()
            self.m.is_laser_enabled = False
