from kivy.lang import Builder
from kivy.uix.widget import Widget

from asmcnc.skavaUI import widget_z_height

Builder.load_string("""

<ZMoveNudge>

    up_button:up_button
    virtual_z_container:virtual_z_container

    BoxLayout:

        size: self.parent.size
        pos: self.parent.pos
        padding: dp(10)
        spacing: dp(10)
        orientation: 'horizontal'

        BoxLayout:
            id: virtual_z_container
            padding: dp(10), dp(0)

        BoxLayout:
            spacing: dp(10)
            orientation: "vertical"

            Button:
                id: up_button
                size_hint_y: 1
                background_color: color_provider.get_rgba("transparent")
                on_release:
                    root.quit_jog_z()
                    self.background_color = color_provider.get_rgba("transparent")
                on_press:
                    root.jog_z('Z+')
                    self.background_color = color_provider.get_rgba("button_press_background")
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/xy_arrow_up.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

            Button:
                size_hint_y: 1
                background_color: color_provider.get_rgba("transparent")
                on_release:
                    root.quit_jog_z()
                    self.background_color = color_provider.get_rgba("transparent")
                on_press:
                    root.jog_z('Z-')
                    self.background_color = color_provider.get_rgba("button_press_background")
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/z_jog_down.png"
                        source: "./asmcnc/skavaUI/img/xy_arrow_down.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

    FloatLayout:
        Label:
            x: up_button.pos[0] + up_button.size[0] * 0.75
            y: up_button.pos[1] + up_button.size[1] * 0.75
            size_hint: None, None
            height: dp(30)
            width: dp(30)
            text: 'Z'
            markup: True
            bold: True
            color: color_provider.get_rgba("dark_grey")
            font_size: dp(20)

""")
    

class ZMoveNudge(Widget):

    def __init__(self, **kwargs):
        super(ZMoveNudge, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.jd = kwargs['job']

        self.virtual_z_container.add_widget(widget_z_height.VirtualZ(machine=self.m, screen_manager=self.sm, job=self.jd))

    jogMode = 'free'

    def jog_z(self, case):

        self.m.set_led_colour('WHITE')

        feed_speed = self.sm.get_screen('nudge').nudge_speed_widget.feedSpeedJogZ
        self.jogMode = self.sm.get_screen('nudge').xy_move_widget.jogMode
        
        if self.jogMode == 'free':
            if case == 'Z-': self.m.jog_absolute_single_axis('Z', 
                                                             self.m.z_min_jog_abs_limit,
                                                             feed_speed)
            if case == 'Z+': self.m.jog_absolute_single_axis('Z', 
                                                             self.m.z_max_jog_abs_limit,
                                                             feed_speed)

        elif self.jogMode == 'plus_0-01':
            if case == 'Z+': self.m.jog_relative('Z', 0.01, feed_speed)
            if case == 'Z-': self.m.jog_relative('Z', -0.01, feed_speed)
        
        elif self.jogMode == 'plus_0-1':
            if case == 'Z+': self.m.jog_relative('Z', 0.1, feed_speed)
            if case == 'Z-': self.m.jog_relative('Z', -0.1, feed_speed)
        
        elif self.jogMode == 'plus_1':
            if case == 'Z+': self.m.jog_relative('Z', 1, feed_speed)
            if case == 'Z-': self.m.jog_relative('Z', -1, feed_speed)
        
        elif self.jogMode == 'plus_10':
            if case == 'Z+': self.m.jog_relative('Z', 10, feed_speed)
            if case == 'Z-': self.m.jog_relative('Z', -10, feed_speed)

    def quit_jog_z(self):
        if self.jogMode == 'free': self.m.quit_jog()
        elif self.jogMode == 'job': self.m.quit_jog()
