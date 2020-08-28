'''
Created on 1 Feb 2018
@author: Ed
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.clock import Clock

Builder.load_string("""


<FeedOverride>

    feed_rate_label:feed_rate_label
    feed_absolute:feed_absolute
    up_5: up_5
    down_5: down_5

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos      

        spacing: 00
        
        orientation: "vertical"
        
        Button:
            id: up_5
            on_press: root.feed_up()
            background_color: 1, 1, 1, 0 
            BoxLayout:
                padding: 2
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
                id: feed_rate_label
                pos_hint: {'center_x':0.5, 'center_y': .5}
                size: self.parent.size
                text: "100%"           
        
        Button:
            id: down_5
            on_press: root.feed_down()
            background_color: 1, 1, 1, 0 
            BoxLayout:
                padding: 2
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
            font_size: '16px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            color: [0,0,0,0.5]
        Label:
            size_hint_y: 0.15
            text: 'mm/min'
            font_size: '12px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            color: [0,0,0,0.5]      
""")
    

class FeedOverride(Widget):

    feed_override_percentage = NumericProperty()
    feed_rate_label = ObjectProperty()

    enable_button_time = 0.3
    push = 0

    def __init__(self, **kwargs):
        super(FeedOverride, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']

    def update_feed_rate_label(self):
        self.feed_absolute.text = str(self.m.feed_rate())

    def feed_up(self):
        self.push =+ 1
        if self.feed_override_percentage < 200 and self.push < 2:
            self.disable_buttons()
            self.feed_override_percentage += 5
            self.feed_rate_label.text = str(self.feed_override_percentage) + '%'
            Clock.schedule_once(lambda dt: self.m.feed_override_up_1(final_percentage=self.feed_override_percentage), 0.05) 
            Clock.schedule_once(lambda dt: self.m.feed_override_up_1(final_percentage=self.feed_override_percentage), 0.1) 
            Clock.schedule_once(lambda dt: self.m.feed_override_up_1(final_percentage=self.feed_override_percentage), 0.15) 
            Clock.schedule_once(lambda dt: self.m.feed_override_up_1(final_percentage=self.feed_override_percentage), 0.2)
            Clock.schedule_once(lambda dt: self.m.feed_override_up_1(final_percentage=self.feed_override_percentage), 0.25)
            Clock.schedule_once(self.enable_buttons, self.enable_button_time)
                
    def feed_norm(self):
        self.feed_override_percentage = 100
        self.feed_rate_label.text = str(self.feed_override_percentage) + '%'
        self.m.feed_override_reset()
                
    def feed_down(self):
        self.push =+ 1 
        if self.feed_override_percentage > 10 and self.push < 2:
            self.disable_buttons()
            self.feed_override_percentage -= 5
            self.feed_rate_label.text = str(self.feed_override_percentage) + '%'
            Clock.schedule_once(lambda dt: self.m.feed_override_down_1(final_percentage=self.feed_override_percentage), 0.05) 
            Clock.schedule_once(lambda dt: self.m.feed_override_down_1(final_percentage=self.feed_override_percentage), 0.1) 
            Clock.schedule_once(lambda dt: self.m.feed_override_down_1(final_percentage=self.feed_override_percentage), 0.15) 
            Clock.schedule_once(lambda dt: self.m.feed_override_down_1(final_percentage=self.feed_override_percentage), 0.2)
            Clock.schedule_once(lambda dt: self.m.feed_override_down_1(final_percentage=self.feed_override_percentage), 0.25)
            Clock.schedule_once(self.enable_buttons, self.enable_button_time)

    def disable_buttons(self):
        self.down_5.disabled = True
        self.up_5.disabled = True
        self.sm.get_screen('go').speedOverride.disable_buttons()

    def enable_buttons(self, dt):
        self.down_5.disabled = False
        self.up_5.disabled = False
        self.sm.get_screen('go').speedOverride.enable_buttons()
        self.push = 0