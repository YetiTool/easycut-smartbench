"""
Created on 1 Feb 2018
@author: Ed
"""
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.properties import NumericProperty
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
        if self.animation:
            self.animation.cancel(self.z_bit)

        self.new_y = (
                self.z_bit.parent.y + self.z_bit.parent.height - -(
                m_z / self.m.grbl_z_max_travel) * self.z_clear.parent.height
        )

        self.animation = Animation(y=self.new_y, duration=0.2, s=1.0/60.0)
        self.animation.start(self.z_bit)


if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout

    class SerialTest(EventDispatcher):
        m_z = NumericProperty(0.0)

    class MachineTest(object):
        s = SerialTest()
        grbl_z_max_travel = 120.0

    class TestApp(App):
        def build(self):
            self.machine = MachineTest()

            root = BoxLayout()
            root.add_widget(VirtualZ(machine=self.machine))

            Clock.schedule_interval(self.change_m_z, 0.1)
            return root

        def change_m_z(self, dt):
            self.machine.s.m_z = self.machine.s.m_z - 1

    TestApp().run()
