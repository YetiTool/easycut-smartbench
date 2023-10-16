from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string("""

<ZMoveMechanics>

    speed_toggle:speed_toggle
    speed_image:speed_image
    jogModeButtonImage:jogModeButtonImage
    up_button:up_button

    BoxLayout:

        size: self.parent.size
        pos: self.parent.pos
        padding: 10
        spacing: 10
        orientation: 'horizontal'

        BoxLayout:
            spacing: 10
            orientation: "vertical"

            ToggleButton:
                id: speed_toggle
                on_press: root.set_jog_speeds()
                background_color: 1, 1, 1, 0
                BoxLayout:
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
                background_color: hex('#F4433600')
                on_release:
                    self.background_color = hex('#F4433600')
                on_press:
                    root.jogModeCycled()
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: jogModeButtonImage
                        source: "./asmcnc/skavaUI/img/jog_mode_infinity.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

        BoxLayout:
            spacing: 10
            orientation: "vertical"

            Button:
                id: up_button
                size_hint_y: 1
                background_color: hex('#F4433600')
                on_release:
                    root.quit_jog_z()
                    self.background_color = hex('#F4433600')
                on_press:
                    root.jog_z('Z+')
                    self.background_color = hex('#F44336FF')
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
                background_color: hex('#F4433600')
                on_release:
                    root.quit_jog_z()
                    self.background_color = hex('#F4433600')
                on_press:
                    root.jog_z('Z-')
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
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
            color: hex('#333333ff')
            font_size: dp(20)

""")
    

class ZMoveMechanics(Widget):

    def __init__(self, **kwargs):
        super(ZMoveMechanics, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']

        self.set_jog_speeds()

    fast_z_speed = 750
    feedSpeedJogZ = 750

    def set_jog_speeds(self):
        if self.speed_toggle.state == 'normal': 
            self.speed_image.source = "./asmcnc/skavaUI/img/slow.png"
            self.feedSpeedJogZ = self.fast_z_speed / 5
        else: 
            self.speed_image.source = "./asmcnc/skavaUI/img/fast.png"
            self.feedSpeedJogZ = self.fast_z_speed

    jogMode = 'free'
    jog_mode_button_press_counter = 0
    
    def jogModeCycled(self):

        self.jog_mode_button_press_counter += 1
        if self.jog_mode_button_press_counter % 5 == 0:
            self.jogMode = 'free'
            self.jogModeButtonImage.source = './asmcnc/skavaUI/img/jog_mode_infinity.png'
        if self.jog_mode_button_press_counter % 5 == 1:
            self.jogMode = 'plus_10'
            self.jogModeButtonImage.source = './asmcnc/skavaUI/img/jog_mode_10.png'
        if self.jog_mode_button_press_counter % 5 == 2:
            self.jogMode = 'plus_1'
            self.jogModeButtonImage.source = './asmcnc/skavaUI/img/jog_mode_1.png'
        if self.jog_mode_button_press_counter % 5 == 3:
            self.jogMode = 'plus_0-1'
            self.jogModeButtonImage.source = './asmcnc/skavaUI/img/jog_mode_0-1.png'
        if self.jog_mode_button_press_counter % 5 == 4:
            self.jogMode = 'plus_0-01'
            self.jogModeButtonImage.source = './asmcnc/skavaUI/img/jog_mode_0-01.png'

    def jog_z(self, case):

        self.m.set_led_colour('WHITE')

        feed_speed = self.feedSpeedJogZ
        
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
