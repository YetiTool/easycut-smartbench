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


<SpeedOverride>

    speed_rate_label:speed_rate_label
    spindle_rpm:spindle_rpm
    up_5: up_5
    down_5: down_5

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos      

        spacing: 00
        
        orientation: "vertical"
        
        Button:
            id: up_5
            on_press: root.speed_up()
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
                id: speed_rate_label
                pos_hint: {'center_x':0.5, 'center_y': .5}
                size: self.parent.size
                text: "100%"           
        
        Button:
            id: down_5
            on_press: root.speed_down()
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
            id: spindle_rpm
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
            text: 'RPM'
            font_size: '12px' 
            valign: 'middle'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            color: [0,0,0,0.5]  
""")
    

class SpeedOverride(Widget):

    speed_override_percentage = NumericProperty()
    speed_rate_label = ObjectProperty()

    enable_button_time = 0.3
    push = 0

    def __init__(self, **kwargs):
        super(SpeedOverride, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.db=kwargs['database']   

    def update_spindle_speed_label(self):
        self.spindle_rpm.text = str(self.m.spindle_speed())

    def update_speed_percentage_override_label(self):
        self.speed_override_percentage = self.m.s.speed_override_percentage
        self.speed_rate_label.text = str(self.m.s.speed_override_percentage) + '%'

    def speed_up(self):
        self.push =+ 1 
        if self.speed_override_percentage < 200 and self.push < 2:
            if self.disable_buttons():
                self.speed_override_percentage += 5
                self.speed_rate_label.text = str(self.speed_override_percentage) + "%"
                Clock.schedule_once(lambda dt: self.m.speed_override_up_1(final_percentage=self.speed_override_percentage), 0.05) 
                Clock.schedule_once(lambda dt: self.m.speed_override_up_1(final_percentage=self.speed_override_percentage), 0.1) 
                Clock.schedule_once(lambda dt: self.m.speed_override_up_1(final_percentage=self.speed_override_percentage), 0.15) 
                Clock.schedule_once(lambda dt: self.m.speed_override_up_1(final_percentage=self.speed_override_percentage), 0.2)
                Clock.schedule_once(lambda dt: self.m.speed_override_up_1(final_percentage=self.speed_override_percentage), 0.25)
                Clock.schedule_once(lambda dt: self.db.send_spindle_speed_info(), 1)
                Clock.schedule_once(self.enable_buttons, self.enable_button_time)
        
    def speed_norm(self):
        self.m.speed_override_reset()
        self.update_speed_percentage_override_label()
        Clock.schedule_once(lambda dt: self.db.send_spindle_speed_info(), 1)
                
    def speed_down(self):
        self.push =+ 1 
        if self.speed_override_percentage > 10 and self.push < 2:          
            if self.disable_buttons():
                self.speed_override_percentage -= 5
                self.speed_rate_label.text = str(self.speed_override_percentage) + "%"
                Clock.schedule_once(lambda dt: self.m.speed_override_down_1(final_percentage=self.speed_override_percentage), 0.05) 
                Clock.schedule_once(lambda dt: self.m.speed_override_down_1(final_percentage=self.speed_override_percentage), 0.1) 
                Clock.schedule_once(lambda dt: self.m.speed_override_down_1(final_percentage=self.speed_override_percentage), 0.15) 
                Clock.schedule_once(lambda dt: self.m.speed_override_down_1(final_percentage=self.speed_override_percentage), 0.2)
                Clock.schedule_once(lambda dt: self.m.speed_override_down_1(final_percentage=self.speed_override_percentage), 0.25)
                Clock.schedule_once(lambda dt: self.db.send_spindle_speed_info(), 1)
                Clock.schedule_once(self.enable_buttons, self.enable_button_time)

    def disable_buttons(self):
        self.down_5.disabled = True
        self.up_5.disabled = True
        try: 
            self.sm.get_screen('go').feedOverride.down_5.disabled = True
            self.sm.get_screen('go').feedOverride.up_5.disabled = True
        except: 
            pass
        return True

    def enable_buttons(self, dt):
        self.down_5.disabled = False
        self.up_5.disabled = False
        try: 
            self.sm.get_screen('go').feedOverride.down_5.disabled = False
            self.sm.get_screen('go').feedOverride.up_5.disabled = False      
        except:
            pass
        self.push = 0