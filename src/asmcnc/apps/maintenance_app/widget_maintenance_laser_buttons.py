'''
Created on 10 June 2020
@author: Letty
widget to hold laser datum setting buttons
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

Builder.load_string("""

<LaserDatumButtons>
    
    vacuum_toggle: vacuum_toggle
    spindle_toggle: spindle_toggle
    vacuum_image: vacuum_image
    spindle_image: spindle_image
    
    BoxLayout:
    
        size: self.parent.size
        pos: self.parent.pos
        orientation: 'vertical'
        padding: 10
        spacing: 10
        
        GridLayout:
            cols: 2
            rows: 2
            spacing: 0
            size_hint_y: None
            height: self.width

            BoxLayout: 
                size: self.parent.size
                pos: self.parent.pos 
                ToggleButton:
                    id: vacuum_toggle
                    on_press: root.set_vacuum()
                    size_hint: (None,None)
                    height: dp(120)
                    width: dp(120)
                    background_color: [0,0,0,0]
                    center: self.parent.center
                    pos: self.parent.pos
                    BoxLayout:
                        padding: 10
                        size: self.parent.size
                        pos: self.parent.pos      
                        Image:
                            id: vacuum_image
                            source: "./asmcnc/apps/maintenance_app/img/extractor_off_120.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True  

            BoxLayout: 
                size: self.parent.size
                pos: self.parent.pos 
                ToggleButton:
                    id: spindle_toggle
                    on_press: root.set_spindle()
                    size_hint: (None,None)
                    height: dp(120)
                    width: dp(120)
                    background_color: [0,0,0,0]
                    center: self.parent.center
                    pos: self.parent.pos
                    BoxLayout:
                        padding: 10
                        size: self.parent.size
                        pos: self.parent.pos      
                        Image:
                            id: spindle_image
                            source: "./asmcnc/apps/maintenance_app/img/spindle_off_120.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True 

            BoxLayout: 
                size: self.parent.size
                pos: self.parent.pos 
                Button:
                    size_hint: (None,None)
                    height: dp(120)
                    width: dp(120)
                    background_color: [0,0,0,0]
                    center: self.parent.center
                    pos: self.parent.pos
                    on_press: root.reset_laser_offset()
                    BoxLayout:
                        padding: 0
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/maintenance_app/img/reset_button_120.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

            BoxLayout: 
				size: self.parent.size
                pos: self.parent.pos 
                Button:
                    size_hint: (None,None)
                    height: dp(120)
                    width: dp(120)
                    background_color: [0,0,0,0]
                    center: self.parent.center
                    pos: self.parent.pos
                    on_press: root.save_laser_offset()
                    BoxLayout:
                        padding: 0
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/maintenance_app/img/save_button_120.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True


""")


class LaserDatumButtons(Widget):


    def __init__(self, **kwargs):
    
        super(LaserDatumButtons, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']

    def reset_laser_offset(self):
        self.sm.get_screen('maintenance').laser_datum_reset_coordinate_x = self.m.mpos_x()
        self.sm.get_screen('maintenance').laser_datum_reset_coordinate_y = self.m.mpos_y()

    def save_laser_offset(self):
        # need to cleverly calculate from movements & saving calibration from maintenance screen
        z_head_laser_offset_x = self.sm.get_screen('maintenance').laser_datum_reset_coordinate_x - self.m.mpos_x()
        z_head_laser_offset_y = self.sm.get_screen('maintenance').laser_datum_reset_coordinate_y - self.m.mpos_y()

        self.sm.get_screen('maintenance').laser_datum_offset_x = z_head_laser_offset_x
        self.sm.get_screen('maintenance').laser_datum_offset_y = z_head_laser_offset_y

        self.m.write_z_head_laser_offset_values(z_head_laser_offset_x, z_head_laser_offset_y) #placeholder
        self.m.read_z_head_laser_offset_values()
        
    def set_vacuum(self):
        if self.vacuum_toggle.state == 'normal': 
            self.vacuum_image.source = "./asmcnc/apps/maintenance_app/img/extractor_off_120.png"
            self.m.vac_off()
        else: 
            self.vacuum_image.source = "./asmcnc/apps/maintenance_app/img/extractor_on_120.png"
            self.m.vac_on()
    
    def set_spindle(self):
        if self.spindle_toggle.state == 'normal': 
            self.spindle_image.source = "./asmcnc/apps/maintenance_app/img/spindle_off_120.png"
            self.m.spindle_off()
        else: 
            self.spindle_image.source = "./asmcnc/apps/maintenance_app/img/spindle_on_120.png"
            self.m.spindle_on()
