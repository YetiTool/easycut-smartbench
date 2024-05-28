"""
Created on 1 Feb 2018
@author: Ed
"""
from kivy.animation import Animation
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

        self.animation = None

        self.m.s.bind(m_z=self.on_m_z)

    def on_m_z(self, instance, value):
        self.animate_z(value)

    def animate_z(self, m_z):
        self.new_y = (
                self.z_bit.parent.y + self.z_bit.parent.height - -(
                m_z / self.m.grbl_z_max_travel) * self.z_clear.parent.height
        )

        # Calculate the distance to move per frame
        distance = self.new_y - self.z_bit.y
        self.speed = distance / 0.1

        # Schedule the update function to be called every frame
        Clock.schedule_interval(self.update, 0)

    def update(self, dt):
        # Update the y position based on the speed and the time delta
        self.z_bit.y += self.speed * dt

        # If the z_bit has reached or passed the target y position, unschedule the update function
        if (self.speed > 0 and self.z_bit.y >= self.new_y) or (self.speed < 0 and self.z_bit.y <= self.new_y):
            self.z_bit.y = self.new_y
            Clock.unschedule(self.update)
