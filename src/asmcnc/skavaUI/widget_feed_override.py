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


<FeedOverride>

    feed_rate_label:feed_rate_label
    feed_absolute:feed_absolute
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
            on_press: root.feed_up()
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
                on_press: root.feed_norm()
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
                id: feed_rate_label
                pos_hint: {'center_x':0.5, 'center_y': .5}
                size: self.parent.size
                text: "100%"           
        
        Button:
            font_size: str(0.01875 * app.width) + 'sp'
            id: down_5
            on_press: root.feed_down()
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
            id: feed_absolute
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
            text: 'mm/min'
            font_size: str(0.015*app.width) + 'px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            color: [0,0,0,0.5]      
"""
)


class FeedOverride(Widget):
    feed_override_percentage = NumericProperty()
    feed_rate_label = ObjectProperty()
    enable_button_time = 0.36

    def __init__(self, **kwargs):
        super(FeedOverride, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.db = kwargs["database"]

    def update_feed_rate_label(self):
        self.feed_absolute.text = str(self.m.feed_rate())

    def update_feed_percentage_override_label(self):
        self.feed_rate_label.text = str(self.m.s.feed_override_percentage) + "%"

    def feed_up(self):
        if self.m.s.feed_override_percentage >= 200:
            return
        self.disable_buttons()
        for i in range(5):
            Clock.schedule_once(lambda dt: self.m.feed_override_up_1(), 0.06 * i)
        Clock.schedule_once(lambda dt: self.db.send_feed_rate_info(), 1)
        Clock.schedule_once(self.enable_buttons, self.enable_button_time)

    def feed_norm(self):
        self.m.feed_override_reset()
        self.update_feed_percentage_override_label()
        Clock.schedule_once(lambda dt: self.db.send_feed_rate_info(), 1)

    def feed_down(self):
        if self.m.s.feed_override_percentage <= 10:
            return
        self.disable_buttons()
        for i in range(5):
            Clock.schedule_once(lambda dt: self.m.feed_override_down_1(), 0.06 * i)
        Clock.schedule_once(lambda dt: self.db.send_feed_rate_info(), 1)
        Clock.schedule_once(self.enable_buttons, self.enable_button_time)

    def disable_buttons(self):
        self.down_5.disabled = True
        self.up_5.disabled = True
        self.sm.get_screen("go").speedOverride.down_5.disabled = True
        self.sm.get_screen("go").speedOverride.up_5.disabled = True
        return True

    def enable_buttons(self, dt):
        self.down_5.disabled = False
        self.up_5.disabled = False
        self.sm.get_screen("go").speedOverride.down_5.disabled = False
        self.sm.get_screen("go").speedOverride.up_5.disabled = False

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
