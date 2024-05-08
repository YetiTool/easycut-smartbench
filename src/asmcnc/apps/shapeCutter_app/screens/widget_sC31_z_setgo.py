"""
Created on 5 March 2020
@author: Letty
"""
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.base import runTouchApp

Builder.load_string(
    """


<SC31ZSetGo>

    speed_image:speed_image
    speed_toggle:speed_toggle

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos      

        spacing: app.get_scaled_width(20.0)
        
        orientation: "vertical"
        
        BoxLayout:
            spacing: 0
            padding: 0
            size_hint_y: 1
            orientation: 'vertical'
            canvas:
                Color: 
                    rgba: 1,1,1,1
                RoundedRectangle: 
                    size: self.size
                    pos: self.pos 

            ToggleButton:
                font_size: app.get_scaled_sp('15.0sp')
                id: speed_toggle
                on_press: root.set_jog_speeds()
                background_color: 1, 1, 1, 0 
                BoxLayout:
                    padding: app.get_scaled_tuple([10.0, 10.0])
                    size: self.parent.size
                    pos: self.parent.pos      
                    Image:
                        id: speed_image
                        source: "./asmcnc/skavaUI/img/slow.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True  

            Button:
                font_size: app.get_scaled_sp('15.0sp')
                size_hint_y: 1
                background_color: hex('#F4433600')
                on_release: 
                    self.background_color = hex('#F4433600')
                on_press:
                    root.set_jobstart_z()
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/z_set_0.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

            Button:
                font_size: app.get_scaled_sp('15.0sp')
                size_hint_y: 1
                background_color: hex('#F4433600')
                on_release: 
                    self.background_color = hex('#F4433600')
                on_press:
                    root.go_to_jobstart_z()
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/z_goto_0.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
        
         
        
"""
)


class SC31ZSetGo(Widget):
    def __init__(self, **kwargs):
        super(SC31ZSetGo, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.set_jog_speeds()

    fast_x_speed = 6000
    fast_y_speed = 6000
    fast_z_speed = 750

    def set_jog_speeds(self):
        if self.speed_toggle.state == "normal":
            self.speed_image.source = "./asmcnc/skavaUI/img/slow.png"
            self.feedSpeedJogX = self.fast_x_speed / 5
            self.feedSpeedJogY = self.fast_y_speed / 5
            self.feedSpeedJogZ = self.fast_z_speed / 5
        else:
            self.speed_image.source = "./asmcnc/skavaUI/img/fast.png"
            self.feedSpeedJogX = self.fast_x_speed
            self.feedSpeedJogY = self.fast_y_speed
            self.feedSpeedJogZ = self.fast_z_speed

    def set_jobstart_z(self):
        self.m.set_jobstart_z()

    def go_to_jobstart_z(self):
        self.m.go_to_jobstart_z()
