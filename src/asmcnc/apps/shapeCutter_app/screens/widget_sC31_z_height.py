'''
Created on 10 March 2020
@author: Letty
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


<VirtualZ31>

    z_range:z_range
    z_cut:z_cut
    z_clear:z_clear
    z_bit:z_bit

    Image:
        id: z_range
        source: './asmcnc/skavaUI/img/zRange.png'
        allow_stretch: True
        keep_ratio: False
        size: self.parent.size
        pos: self.parent.pos
    Image:
        id:z_cut
        source: './asmcnc/skavaUI/img/zCut.png'
        allow_stretch: True
        keep_ratio: False
        size: self.parent.width, 0
        pos: self.parent.pos
        opacity: 1
    Image:
        id:z_clear
        source: './asmcnc/skavaUI/img/zClear.png'
        allow_stretch: True
        keep_ratio: False
        size: self.parent.width, 0
        pos: self.parent.pos
        opacity: 1
    Image:
        id: z_bit
        source: './asmcnc/skavaUI/img/zBit.png'
        allow_stretch: True
        keep_ratio: False
        size: self.parent.width/2, self.parent.height
        x: self.parent.x+(self.parent.width/4)
        y: self.parent.y
     
        
""")
    

class VirtualZ31(Widget):

    WIDGET_REFRESH_INTERVAL = 0.1

    def __init__(self, **kwargs):
    
        super(VirtualZ31, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.j=kwargs['job_parameters']
        
    def refresh_widget(self, dt):

        self.setZones()
        self.setBitPos()
    
    def setZones(self):
 
        z_max = self.j.range_z[1]
        z_min = self.j.range_z[0]
        z0_machine_coords = self.m.z_wco()
                  
        self.z_clear.y = self.z_clear.parent.y + self.z_clear.parent.size[1] - ((-z0_machine_coords/(self.m.grbl_z_max_travel))  * self.z_clear.parent.size[1])
        self.z_clear.size[1] = ( z_max/(self.m.grbl_z_max_travel) * self.z_clear.parent.size[1]) 
        self.z_cut.size[1] = ( (-z_min)/(self.m.grbl_z_max_travel) * self.z_clear.parent.size[1])
        self.z_cut.y = self.z_clear.y - self.z_cut.height
        
    def setBitPos(self):

        self.z_bit.y = (self.z_bit.parent.y + self.z_bit.parent.size[1] 
                        - (-(self.m.mpos_z()/(self.m.grbl_z_max_travel))  * self.z_clear.parent.size[1]))

    