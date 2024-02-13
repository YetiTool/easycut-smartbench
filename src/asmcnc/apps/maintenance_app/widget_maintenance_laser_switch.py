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
        height: dp(app.get_scaled_height(70))
        width: dp(app.get_scaled_width(150))
        pos: self.parent.pos
        padding:(dp(0),dp(0),dp(0),dp(0))
        
        GridLayout:
            cols: 2
            rows: 1
            spacing:0.0125*app.width
            size_hint: (None,None)
            height: dp(app.get_scaled_height(70))
            width: dp(app.get_scaled_width(175))

            BoxLayout: 
                size_hint: (None, None)
                pos: self.parent.pos
                height: dp(app.get_scaled_height(70))
                width: dp(app.get_scaled_width(85))
                Switch:
                    id: laser_switch
                    background_color: [0,0,0,0]
                    center_x: self.parent.center_x
                    y: self.parent.y
                    pos: self.parent.pos
                    on_active: root.toggle_laser()
            BoxLayout: 
                size_hint: (None, None)
                pos: self.parent.pos
                height: dp(app.get_scaled_height(70))
                width: dp(app.get_scaled_width(55))
                padding:(dp(app.get_scaled_width(5)),dp(app.get_scaled_height(5)))
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
