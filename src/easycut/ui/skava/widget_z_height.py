"""
Created on 1 Feb 2018
@author: Ed
"""
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
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
    WIDGET_REFRESH_INTERVAL = 0.1

    def __init__(self, **kwargs):
        super(VirtualZ, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.jd = kwargs["job"]
        Clock.schedule_interval(self.refresh_widget, self.WIDGET_REFRESH_INTERVAL)

    def refresh_widget(self, dt):
        self.setZones()
        self.setBitPos()

    def setZones(self):
        if self.sm.has_screen("home"):
            z_max = self.sm.get_screen("home").job_box.range_z[1]
            z_min = self.sm.get_screen("home").job_box.range_z[0]
            z0_machine_coords = self.m.z_wco()
            self.z_clear.y = (
                self.z_clear.parent.y
                + self.z_clear.parent.size[1]
                - -z0_machine_coords
                / self.m.grbl_z_max_travel
                * self.z_clear.parent.size[1]
            )
            if self.jd.filename == "":
                if self.z_clear.size[1] == 0:
                    self.z_clear.size[1] = 4.0/800.0 * Window.width
                if self.z_cut.size[1] == 0:
                    self.z_cut.size[1] = 4.0/800.0 * Window.width
            else:
                self.z_clear.size[1] = (
                    z_max / self.m.grbl_z_max_travel * self.z_clear.parent.size[1]
                )
                self.z_cut.size[1] = (
                    -z_min / self.m.grbl_z_max_travel * self.z_clear.parent.size[1]
                )
            self.z_cut.y = self.z_clear.y - self.z_cut.height

    def setBitPos(self):
        self.z_bit.y = (
            self.z_bit.parent.y
            + self.z_bit.parent.size[1]
            - -(self.m.mpos_z() / self.m.grbl_z_max_travel)
            * self.z_clear.parent.size[1]
        )
