from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string(
    """

<XYMoveRecovery>

    jogModeButtonImage:jogModeButtonImage

    BoxLayout:

        size: self.parent.size
        pos: self.parent.pos
        orientation: 'vertical'
        padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
        spacing:0.0208333333333*app.height

        GridLayout:
            cols: 3
            orientation: 'horizontal'
            spacing: 0
            size_hint_y: None
            height: self.width


            BoxLayout:
                padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                size: self.parent.size
                pos: self.parent.pos

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
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
                padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                size: self.parent.size
                pos: self.parent.pos

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
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
                font_size: str(0.01875 * app.width) + 'sp'
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

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
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
                padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                size: self.parent.size
                pos: self.parent.pos

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
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
                padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                size: self.parent.size
                pos: self.parent.pos
"""
)


class XYMoveRecovery(Widget):

    def __init__(self, **kwargs):
        super(XYMoveRecovery, self).__init__(**kwargs)
        self.m = kwargs['machine']
        self.sm = kwargs['screen_manager']

    jogMode = 'free'
    jog_mode_button_press_counter = 0

    def buttonJogXY(self, case):
        x_feed_speed = self.sm.get_screen('nudge'
                                          ).nudge_speed_widget.feedSpeedJogX
        y_feed_speed = self.sm.get_screen('nudge'
                                          ).nudge_speed_widget.feedSpeedJogY
        if self.jogMode == 'free':
            if case == 'X-':
                self.m.jog_absolute_single_axis('X', self.m.
                                                x_min_jog_abs_limit, x_feed_speed)
            if case == 'X+':
                self.m.jog_absolute_single_axis('X', self.m.
                                                x_max_jog_abs_limit, x_feed_speed)
            if case == 'Y-':
                self.m.jog_absolute_single_axis('Y', self.m.
                                                y_min_jog_abs_limit, y_feed_speed)
            if case == 'Y+':
                self.m.jog_absolute_single_axis('Y', self.m.
                                                y_max_jog_abs_limit, y_feed_speed)
        elif self.jogMode == 'plus_0-01':
            if case == 'X+':
                self.m.jog_relative('X', 0.01, x_feed_speed)
            if case == 'X-':
                self.m.jog_relative('X', -0.01, x_feed_speed)
            if case == 'Y+':
                self.m.jog_relative('Y', 0.01, y_feed_speed)
            if case == 'Y-':
                self.m.jog_relative('Y', -0.01, y_feed_speed)
        elif self.jogMode == 'plus_0-1':
            if case == 'X+':
                self.m.jog_relative('X', 0.1, x_feed_speed)
            if case == 'X-':
                self.m.jog_relative('X', -0.1, x_feed_speed)
            if case == 'Y+':
                self.m.jog_relative('Y', 0.1, y_feed_speed)
            if case == 'Y-':
                self.m.jog_relative('Y', -0.1, y_feed_speed)
        elif self.jogMode == 'plus_1':
            if case == 'X+':
                self.m.jog_relative('X', 1, x_feed_speed)
            if case == 'X-':
                self.m.jog_relative('X', -1, x_feed_speed)
            if case == 'Y+':
                self.m.jog_relative('Y', 1, y_feed_speed)
            if case == 'Y-':
                self.m.jog_relative('Y', -1, y_feed_speed)
        elif self.jogMode == 'plus_10':
            if case == 'X+':
                self.m.jog_relative('X', 10, x_feed_speed)
            if case == 'X-':
                self.m.jog_relative('X', -10, x_feed_speed)
            if case == 'Y+':
                self.m.jog_relative('Y', 10, y_feed_speed)
            if case == 'Y-':
                self.m.jog_relative('Y', -10, y_feed_speed)

    def jogModeCycled(self):
        self.jog_mode_button_press_counter += 1
        if self.jog_mode_button_press_counter % 5 == 0:
            self.jogMode = 'free'
            self.jogModeButtonImage.source = (
                './asmcnc/skavaUI/img/jog_mode_infinity.png')
        if self.jog_mode_button_press_counter % 5 == 1:
            self.jogMode = 'plus_10'
            self.jogModeButtonImage.source = (
                './asmcnc/skavaUI/img/jog_mode_10.png')
        if self.jog_mode_button_press_counter % 5 == 2:
            self.jogMode = 'plus_1'
            self.jogModeButtonImage.source = (
                './asmcnc/skavaUI/img/jog_mode_1.png')
        if self.jog_mode_button_press_counter % 5 == 3:
            self.jogMode = 'plus_0-1'
            self.jogModeButtonImage.source = (
                './asmcnc/skavaUI/img/jog_mode_0-1.png')
        if self.jog_mode_button_press_counter % 5 == 4:
            self.jogMode = 'plus_0-01'
            self.jogModeButtonImage.source = (
                './asmcnc/skavaUI/img/jog_mode_0-01.png')

    def cancelXYJog(self):
        if self.jogMode == 'free':
            self.m.quit_jog()
