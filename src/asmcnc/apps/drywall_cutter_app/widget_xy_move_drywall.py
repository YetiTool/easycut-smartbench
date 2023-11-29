import sys, textwrap

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.clock import Clock

from asmcnc.skavaUI import popup_info

Builder.load_string("""
<XYMoveDrywall>
    jogModeButtonImage:jogModeButtonImage
    speed_toggle:speed_toggle
    speed_image:speed_image
    go_to_datum_button_image:go_to_datum_button_image
    go_to_datum_button_overlay:go_to_datum_button_overlay
    
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
                padding: 10
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
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/xy_arrow_up.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
    
            BoxLayout:
                padding: 10
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
                    padding: 0
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
                    padding: 0
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
                    padding: 0
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
                Button:
                    size_hint_y: 1
                    background_color: hex('#F4433600')
                    on_release: 
                        self.background_color = hex('#F4433600')
                    on_press: 
                        root.probe_z()
                        self.background_color = hex('#F44336FF')
                    BoxLayout:
                        padding: 0
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/skavaUI/img/z_probe.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
            Button:
                background_color: hex('#F4433600')
                always_release: True
                on_release:
                    print('release')
                    root.cancelXYJog()
                    self.background_color = hex('#F4433600')
                on_press:
                    print('press')
                    root.buttonJogXY('X-')
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/xy_arrow_down.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
            BoxLayout:
                padding: 10
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
        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']
        self.l = kwargs['localization']

        self.set_jog_speeds()

        Clock.schedule_interval(self.check_zh_at_datum, 0.04)

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

        elif self.jogMode == 'plus_0-01':
            if case == 'X+': self.m.jog_relative('X', 0.01, x_feed_speed)
            if case == 'X-': self.m.jog_relative('X', -0.01, x_feed_speed)
            if case == 'Y+': self.m.jog_relative('Y', 0.01, y_feed_speed)
            if case == 'Y-': self.m.jog_relative('Y', -0.01, y_feed_speed)

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

    def cancelXYJog(self):
        if self.jogMode == 'free':
            self.m.quit_jog()

    def probe_z(self):
        self.m.s.write_command('G0 G53 Z-60')
        self.m.probe_z(fast_probe=True)

    def go_to_datum(self):
        if not self.m.is_machine_homed and sys.platform != 'win32':
            popup_info.PopupHomingWarning(self.sm, self.m, self.l, 'drywall_cutter', 'drywall_cutter')
        else:
            if self.m.is_laser_enabled:
                self.m.jog_laser_to_datum('XY')
            else:
                self.m.go_xy_datum()

    def check_zh_at_datum(self, dt):
        # wpos == 0,0 when zh is at datum
        # Round to 1dp instead of 2dp to make up for grbl error
        if self.m.is_laser_enabled:
            if not (round(self.m.wpos_x() + self.m.laser_offset_x_value, 1) == 0 and round(self.m.wpos_y() + self.m.laser_offset_y_value, 1) == 0):
                # Pulse overlay by smoothly alternating between 0 and 1 opacity
                # Hacky way to track pulsing on or off without a variable by storing that information in the opacity value
                if self.go_to_datum_button_overlay.opacity <= 0:
                    self.go_to_datum_button_overlay.opacity = 0.01
                elif self.go_to_datum_button_overlay.opacity >= 1:
                    self.go_to_datum_button_overlay.opacity = 0.98
                # Check if second decimal place is even or odd
                elif int(("%.2f" % self.go_to_datum_button_overlay.opacity)[-1]) % 2 == 1:
                    self.go_to_datum_button_overlay.opacity += 0.1
                else:
                    self.go_to_datum_button_overlay.opacity -= 0.1
            else:
                self.go_to_datum_button_overlay.opacity = 0
        else:
            if not (round(self.m.wpos_x(), 1) == 0 and round(self.m.wpos_y(), 1) == 0):
                # Pulse overlay by smoothly alternating between 0 and 1 opacity
                # Hacky way to track pulsing on or off without a variable by storing that information in the opacity value
                if self.go_to_datum_button_overlay.opacity <= 0:
                    self.go_to_datum_button_overlay.opacity = 0.01
                elif self.go_to_datum_button_overlay.opacity >= 1:
                    self.go_to_datum_button_overlay.opacity = 0.98
                # Check if second decimal place is even or odd
                elif int(("%.2f" % self.go_to_datum_button_overlay.opacity)[-1]) % 2 == 1:
                    self.go_to_datum_button_overlay.opacity += 0.1
                else:
                    self.go_to_datum_button_overlay.opacity -= 0.1
            else:
                self.go_to_datum_button_overlay.opacity = 0

    def set_datum(self):
        warning = self.format_command(
            (self.l.get_str('Is this where you want to set your X-Y datum?'
                            ).replace('X-Y', '[b]X-Y[/b]')).replace(self.l.get_str('datum'), self.l.get_bold('datum'))
        )

        popup_info.PopupDatum(self.sm, self.m, self.l, 'XY', warning)

    def format_command(self, cmd):
        wrapped_cmd = textwrap.fill(cmd, width=35, break_long_words=False)
        return wrapped_cmd
