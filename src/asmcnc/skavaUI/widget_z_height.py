"""
Created on 1 Feb 2018
@author: Ed
"""
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.widget import Widget

Builder.load_string(
    """


<VirtualZ>

    z_range:z_range
    z_cut:z_cut
    z_clear:z_clear
    z_bit:z_bit

    StencilView:
        size: self.parent.size
        pos: self.parent.pos

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
     
        
"""
)


class VirtualZ(Widget):

    def __init__(self, **kwargs):
        super(VirtualZ, self).__init__(**kwargs)

        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.jd = kwargs["job"]

        self.event = None

        self.m.s.bind(z_change=self.on_z_change)

    def on_z_change(self, instance, value):
        if value and not self.event:
            self.event = Clock.schedule_interval(self.move_z, 0.1)
        elif not value and self.event:
            self.event.cancel()
            self.event = None

    def move_z(self, *args):
        self.z_bit.y = (
                self.z_bit.parent.y + self.z_bit.parent.height - -(
                self.m.mpos_z() / self.m.grbl_z_max_travel) * self.z_clear.parent.height
        )