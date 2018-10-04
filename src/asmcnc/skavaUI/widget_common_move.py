'''
Created on 1 Feb 2018
@author: Ed
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.base import runTouchApp


Builder.load_string("""


<CommonMove>

    speed_image:speed_image
    speed_toggle:speed_toggle
    vacuum_image:vacuum_image
    vacuum_toggle:vacuum_toggle
    spindle_image:spindle_image
    spindle_toggle:spindle_toggle

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos      

        spacing: 20
        
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
                id: speed_toggle
                on_release: root.set_jog_speeds()
                background_color: 1, 1, 1, 0 
                BoxLayout:
                    padding: 10
                    size: self.parent.size
                    pos: self.parent.pos      
                    Image:
                        id: speed_image
                        source: "./asmcnc/skavaUI/img/slow.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True  
            
        BoxLayout:
            spacing: 0
            padding: 0
            size_hint_y: 2
            orientation: 'vertical'
            canvas:
                Color: 
                    rgba: 1,1,1,1
                RoundedRectangle: 
                    size: self.size
                    pos: self.pos 

            ToggleButton:
                id: vacuum_toggle
                on_release: root.set_vacuum()
                background_color: 1, 1, 1, 0 
                BoxLayout:
                    padding: 10
                    size: self.parent.size
                    pos: self.parent.pos      
                    Image:
                        id: vacuum_image
                        source: "./asmcnc/skavaUI/img/vac_off.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True  


            ToggleButton:
                id: spindle_toggle
                on_release: root.set_spindle()
                background_color: 1, 1, 1, 0 
                BoxLayout:
                    padding: 10
                    size: self.parent.size
                    pos: self.parent.pos      
                    Image:
                        id: spindle_image
                        source: "./asmcnc/skavaUI/img/spindle_off.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True  
        
         
        
""")
    

class CommonMove(Widget):

    def __init__(self, **kwargs):
        super(CommonMove, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.set_jog_speeds()
        
    fast_x_speed = 6000
    fast_y_speed = 6000
    fast_z_speed = 750
            
    def set_jog_speeds(self):
        if self.speed_toggle.state == 'normal': 
            self.speed_image.source = "./asmcnc/skavaUI/img/slow.png"
            self.feedSpeedJogX = self.fast_x_speed / 5
            self.feedSpeedJogY = self.fast_y_speed / 5
            self.feedSpeedJogZ = self.fast_z_speed / 5
        else: 
            self.speed_image.source = "./asmcnc/skavaUI/img/fast.png"
            self.feedSpeedJogX = self.fast_x_speed
            self.feedSpeedJogY = self.fast_y_speed
            self.feedSpeedJogZ = self.fast_z_speed

    def set_vacuum(self):
        if self.vacuum_toggle.state == 'normal': 
            self.vacuum_image.source = "./asmcnc/skavaUI/img/vac_off.png"
            self.m.vac_off()
        else: 
            self.vacuum_image.source = "./asmcnc/skavaUI/img/vac_on.png"
            self.m.vac_on()
    
    def set_spindle(self):
        if self.spindle_toggle.state == 'normal': 
            self.spindle_image.source = "./asmcnc/skavaUI/img/spindle_off.png"
            self.m.spindle_off()
        else: 
            self.spindle_image.source = "./asmcnc/skavaUI/img/spindle_on.png"
            self.m.spindle_on()

