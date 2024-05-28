"""
Created on 1 Feb 2018
@author: Ed
"""

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.widget import Widget

Builder.load_string(
    """


<SpeedOverride>

    speed_rate_label:speed_rate_label
    spindle_rpm:spindle_rpm
    up_5: up_5
    down_5: down_5
    norm_button:norm_button

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos      

        spacing:0.0*app.height
        
        orientation: "vertical"
        
        Button:
            font_size: str(0.01875 * app.width) + 'sp'
            id: up_5
            on_press: root.speed_up()
            background_color: 1, 1, 1, 0 
            BoxLayout:
                padding:[dp(0.0025)*app.width, dp(0.00416666666667)*app.height]
                size: self.parent.size
                pos: self.parent.pos      
                Image:
                    id: speed_image
                    source: "./asmcnc/skavaUI/img/feed_speed_up.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True  
       
        FloatLayout:
            size: self.parent.size
            pos: self.parent.pos  
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                id: norm_button
                on_press: root.speed_norm()
                background_color: 1, 1, 1, 0 
                pos_hint: {'center_x':0.5, 'center_y': .5}
                size: self.parent.size
            Image:
                source: "./asmcnc/skavaUI/img/feed_speed_norm.png"
                pos_hint: {'center_x':0.5, 'center_y': .5}
                size: self.parent.size
                allow_stretch: True  
            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                id: speed_rate_label
                pos_hint: {'center_x':0.5, 'center_y': .5}
                size: self.parent.size
                text: "100%"           
        
        Button:
            font_size: str(0.01875 * app.width) + 'sp'
            id: down_5
            on_press: root.speed_down()
            background_color: 1, 1, 1, 0 
            BoxLayout:
                padding:[dp(0.0025)*app.width, dp(0.00416666666667)*app.height]
                size: self.parent.size
                pos: self.parent.pos      
                Image:
                    id: speed_image
                    source: "./asmcnc/skavaUI/img/feed_speed_down.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True  
        Label:
            id: spindle_rpm
            size_hint_y: 0.22
            text: '0'
            font_size: str(0.02*app.width) + 'px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            color: [0,0,0,0.5]
        Label:
            size_hint_y: 0.15
            text: 'RPM'
            font_size: str(0.015*app.width) + 'px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            color: [0,0,0,0.5]  
"""
)


class SpeedOverride(Widget):
    speed_override_percentage = NumericProperty()
    speed_rate_label = ObjectProperty()
    enable_button_time = 0.36

    def __init__(self, **kwargs):
        self.m = kwargs.pop("machine")
        self.sm = kwargs.pop("screen_manager")
        self.db = kwargs.pop("database")
        super(SpeedOverride, self).__init__(**kwargs)
        self.m.s.bind(spindle_speed=self.update_spindle_speed_label)

    def update_spindle_speed_label(self, instance, value):
        self.spindle_rpm.text = str(value)

    def update_speed_percentage_override_label(self):
        self.speed_override_percentage = self.m.s.speed_override_percentage
        self.speed_rate_label.text = str(self.m.s.speed_override_percentage) + "%"

    def speed_up(self):
        if self.m.s.speed_override_percentage >= 200:
            return
        self.disable_buttons()
        for i in range(5):
            Clock.schedule_once(lambda dt: self.m.speed_override_up_1(), 0.06 * i)
        Clock.schedule_once(lambda dt: self.db.send_spindle_speed_info(), 1)
        Clock.schedule_once(self.enable_buttons, self.enable_button_time)

    def speed_norm(self):
        self.m.speed_override_reset()
        self.update_speed_percentage_override_label()
        Clock.schedule_once(lambda dt: self.db.send_spindle_speed_info(), 1)

    def speed_down(self):
        if self.m.s.speed_override_percentage <= 10:
            return
        self.disable_buttons()
        for i in range(5):
            Clock.schedule_once(lambda dt: self.m.speed_override_down_1(), 0.06 * i)
        Clock.schedule_once(lambda dt: self.db.send_spindle_speed_info(), 1)
        Clock.schedule_once(self.enable_buttons, self.enable_button_time)

    def disable_buttons(self):
        self.down_5.disabled = True
        self.up_5.disabled = True
        try:
            self.sm.get_screen("go").feedOverride.down_5.disabled = True
            self.sm.get_screen("go").feedOverride.up_5.disabled = True
        except:
            pass
        return True

    def enable_buttons(self, dt):
        self.down_5.disabled = False
        self.up_5.disabled = False
        try:
            if self.m.s.yp.use_yp:
                self.sm.get_screen("go").feedOverride.down_5.disabled = True
                self.sm.get_screen("go").feedOverride.up_5.disabled = True
            else:
                self.sm.get_screen("go").feedOverride.down_5.disabled = False
                self.sm.get_screen("go").feedOverride.up_5.disabled = False
        except:
            pass

    def set_widget_visibility(self, visible):
        self.up_5.disabled = not visible
        self.down_5.disabled = not visible
        self.norm_button.disabled = not visible
        if visible:
            self.up_5.opacity = 1
            self.down_5.opacity = 1
            self.norm_button.opacity = 1
        else:
            self.up_5.opacity = 0.5
            self.down_5.opacity = 0.5
            self.norm_button.opacity = 0.5
