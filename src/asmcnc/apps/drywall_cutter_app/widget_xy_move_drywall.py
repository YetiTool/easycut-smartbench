import sys, textwrap

from kivy.lang import Builder
from kivy.uix.widget import Widget

from asmcnc.core_UI.components.buttons import probe_button
from asmcnc.core_UI.custom_popups import PopupDatum
from asmcnc.skavaUI import popup_info

Builder.load_string("""
<XYMoveDrywall>
    jogModeButtonImage:jogModeButtonImage
    speed_toggle:speed_toggle
    speed_image:speed_image
    go_to_datum_button_image:go_to_datum_button_image
    go_to_datum_button_overlay:go_to_datum_button_overlay
    
    canvas.before:
        Color:
            rgba: hex('#f9f9f9ff')
        Rectangle:
            pos: self.pos
            size: self.size
    
    BoxLayout:
    
        size: self.parent.size
        pos: self.parent.pos      
        orientation: 'vertical'
        spacing: 10
        
        GridLayout:
            cols: 3
            orientation: 'horizontal'
            spacing: 0
            size_hint_y: None
            height: self.width
    
            BoxLayout:
                padding:dp(10)
                size: self.parent.size
                pos: self.parent.pos
                Button:
                    background_color: hex('#F4433600')
                    on_release:
                        self.background_color = hex('#F4433600')
                    on_press:
                        root.go_to_datum()
                        self.background_color = hex('#F44336FF')
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: go_to_datum_button_image
                            source: "./asmcnc/apps/drywall_cutter_app/img/go_to_datum.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
            
            Button:
                background_color: hex('#F4433600')
                always_release: True
                on_release: 
                    root.cancelXYJog()
                    self.background_color = hex('#F4433600')
                on_press: 
                    root.buttonJogXY('X+')
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding:dp(0)
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/xy_arrow_up.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
    
            BoxLayout:
                padding:dp(10)
                size: self.parent.size
                pos: self.parent.pos
                Button:
                    background_color: hex('#F4433600')
                    on_release:
                        self.background_color = hex('#F4433600')
                    on_press:
                        root.set_datum()
                        self.background_color = hex('#F44336FF')
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/drywall_cutter_app/img/set_datum.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
                            
            Button:
                background_color: hex('#F4433600')
                always_release: True
                on_release: 
                    root.cancelXYJog()
                    self.background_color = hex('#F4433600')
                on_press: 
                    root.buttonJogXY('Y+')
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding:dp(0)
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/xy_arrow_left.png"
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
                    padding:dp(0)
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: jogModeButtonImage
                        source: "./asmcnc/skavaUI/img/jog_mode_infinity.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True  
            Button:
                background_color: hex('#F4433600')
                always_release: True
                on_release: 
                    root.cancelXYJog()
                    self.background_color = hex('#F4433600')
                on_press: 
                    root.buttonJogXY('Y-')
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding:dp(0)
                    size: self.parent.size
                    pos: self.parent.pos  
                    Image:
                        source: "./asmcnc/skavaUI/img/xy_arrow_right.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True                                    
            BoxLayout:
                padding: 15
                size: self.parent.size
                pos: self.parent.pos                 
                id: probe_button_container
            Button:
                background_color: hex('#F4433600')
                always_release: True
                on_release:
                    root.cancelXYJog()
                    self.background_color = hex('#F4433600')
                on_press:
                    root.buttonJogXY('X-')
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding:dp(0)
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/xy_arrow_down.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            BoxLayout:
                padding:dp(10)
                size: self.parent.size
                pos: self.parent.pos
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

    FloatLayout:
        Image:
            id: go_to_datum_button_overlay
            source: "./asmcnc/apps/drywall_cutter_app/img/go_to_datum_pulse.png"
            pos: go_to_datum_button_image.pos
            size: go_to_datum_button_image.size
            allow_stretch: True
            size_hint: (None, None)
            opacity: 0

""")


class XYMoveDrywall(Widget):

    def __init__(self, **kwargs):

        super(XYMoveDrywall, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.l=kwargs['localization']
        self.cs = kwargs['coordinate_system']

        self.set_jog_speeds()
        self.ids.probe_button_container.add_widget(probe_button.ProbeButton(self.m, self.sm, self.l, fast_probe=True))

    jogMode = 'free'
    jog_mode_button_press_counter = 0

    fast_x_speed = 6000
    fast_y_speed = 6000

    def set_jog_speeds(self):
        if self.speed_toggle.state == 'normal': 
            self.speed_image.source = "./asmcnc/skavaUI/img/slow.png"
            self.feedSpeedJogX = self.fast_x_speed / 5
            self.feedSpeedJogY = self.fast_y_speed / 5
        else: 
            self.speed_image.source = "./asmcnc/skavaUI/img/fast.png"
            self.feedSpeedJogX = self.fast_x_speed
            self.feedSpeedJogY = self.fast_y_speed

    def buttonJogXY(self, case):

        x_feed_speed = self.feedSpeedJogX
        y_feed_speed = self.feedSpeedJogY

        if self.jogMode == 'free':
            if case == 'X-': self.m.jog_absolute_single_axis('X',
                                                             self.m.x_min_jog_abs_limit,
                                                             x_feed_speed)
            if case == 'X+': self.m.jog_absolute_single_axis('X',
                                                             self.m.x_max_jog_abs_limit,
                                                             x_feed_speed)
            if case == 'Y-': self.m.jog_absolute_single_axis('Y',
                                                             self.m.y_min_jog_abs_limit,
                                                             y_feed_speed)
            if case == 'Y+': self.m.jog_absolute_single_axis('Y',
                                                             self.m.y_max_jog_abs_limit,
                                                             y_feed_speed)

        elif self.jogMode == 'plus_0-1':
            if case == 'X+': self.m.jog_relative('X', 0.1, x_feed_speed)
            if case == 'X-': self.m.jog_relative('X', -0.1, x_feed_speed)
            if case == 'Y+': self.m.jog_relative('Y', 0.1, y_feed_speed)
            if case == 'Y-': self.m.jog_relative('Y', -0.1, y_feed_speed)

        elif self.jogMode == 'plus_1':
            if case == 'X+': self.m.jog_relative('X', 1, x_feed_speed)
            if case == 'X-': self.m.jog_relative('X', -1, x_feed_speed)
            if case == 'Y+': self.m.jog_relative('Y', 1, y_feed_speed)
            if case == 'Y-': self.m.jog_relative('Y', -1, y_feed_speed)

        elif self.jogMode == 'plus_10':
            if case == 'X+': self.m.jog_relative('X', 10, x_feed_speed)
            if case == 'X-': self.m.jog_relative('X', -10, x_feed_speed)
            if case == 'Y+': self.m.jog_relative('Y', 10, y_feed_speed)
            if case == 'Y-': self.m.jog_relative('Y', -10, y_feed_speed)

    def jogModeCycled(self):

        self.jog_mode_button_press_counter += 1
        if self.jog_mode_button_press_counter % 4 == 0:
            self.jogMode = 'free'
            self.jogModeButtonImage.source = './asmcnc/skavaUI/img/jog_mode_infinity.png'
        if self.jog_mode_button_press_counter % 4 == 1:
            self.jogMode = 'plus_10'
            self.jogModeButtonImage.source = './asmcnc/skavaUI/img/jog_mode_10.png'
        if self.jog_mode_button_press_counter % 4 == 2:
            self.jogMode = 'plus_1'
            self.jogModeButtonImage.source = './asmcnc/skavaUI/img/jog_mode_1.png'
        if self.jog_mode_button_press_counter % 4 == 3:
            self.jogMode = 'plus_0-1'
            self.jogModeButtonImage.source = './asmcnc/skavaUI/img/jog_mode_0-1.png'

    def cancelXYJog(self):
        if self.jogMode == 'free':
            self.m.quit_jog()

    def probe_z(self):
        self.m.probe_z(fast_probe=True)

    def go_to_datum(self):
        if self.m.is_machine_homed == False and sys.platform != 'win32':
            popup_info.PopupHomingWarning(self.sm, self.m, self.l, 'drywall_cutter', 'drywall_cutter')
        else:
            self.m.go_xy_datum_with_laser()

    def check_zh_at_datum(self, opacity):
        x_delta = self.m.wpos_x() + self.m.laser_offset_x_value
        y_delta = self.m.wpos_y() + self.m.laser_offset_y_value
        # allow a deviation of 0.01 due to machine precision
        if abs(x_delta) > 0.01 or abs(y_delta) > 0.01:
            self.go_to_datum_button_overlay.opacity = opacity
        else:
            self.go_to_datum_button_overlay.opacity = 0

    def set_datum(self):
        warning = self.format_command(
            (self.l.get_str('Is this where you want to set your X-Y datum?'
                ).replace('X-Y', '[b]X-Y[/b]')).replace(self.l.get_str('datum'), self.l.get_bold('datum'))
            )

        PopupDatum(self.sm, self.m, self.l, 'XY', warning, jog_after_laser_datum_set=False)

    def format_command(self, cmd):
        wrapped_cmd = textwrap.fill(cmd, width=35, break_long_words=False)
        return wrapped_cmd
