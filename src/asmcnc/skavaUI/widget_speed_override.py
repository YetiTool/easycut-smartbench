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


Builder.load_string("""


<SpeedOverride>

    feed_rate_label:feed_rate_label

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos      

        spacing: 00
        
        orientation: "vertical"
        
        Button:
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
        # Label:
        #     id: spindle_rpm
        #     text: 'speed'
        #     font_size: '16px' 
        #     valign: 'middle'
        #     halign: 'center'
        #     size:self.texture_size
        #     text_size: self.size            
        
         
        
""")
    

class SpeedOverride(Widget):

    feed_override_percentage = NumericProperty()
    feed_rate_label = ObjectProperty()

    def __init__(self, **kwargs):
        super(SpeedOverride, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']     

    def feed_up(self):
        if self.feed_override_percentage < 200: self.feed_override_percentage += 10
        self.feed_rate_label.text = str(self.feed_override_percentage) + "%"
        self.m.speed_override_up_10(final_percentage=self.feed_override_percentage)
        
    def feed_norm(self):
        self.feed_override_percentage = 100
        self.feed_rate_label.text = str(self.feed_override_percentage) + "%"
        self.m.speed_override_reset()
                
    def feed_down(self):
        if self.feed_override_percentage > 10: self.feed_override_percentage -= 10
        self.feed_rate_label.text = str(self.feed_override_percentage) + "%"
        self.m.speed_override_down_10(final_percentage=self.feed_override_percentage)        


