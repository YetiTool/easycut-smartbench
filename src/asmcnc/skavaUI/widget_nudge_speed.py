from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string("""

<NudgeSpeed>

    speed_toggle:speed_toggle
    speed_image:speed_image
    jogModeButtonImage:jogModeButtonImage

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos
        orientation: 'vertical'
        spacing: 10
        padding: 10

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
                    source: "./asmcnc/skavaUI/img/set_jobstart.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

""")
    

class NudgeSpeed(Widget):

    def __init__(self, **kwargs):
        super(NudgeSpeed, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']

        self.set_jog_speeds()

    fast_x_speed = 6000
    fast_y_speed = 6000
    fast_z_speed = 750
            
    jogMode = 'free'
    jog_mode_button_press_counter = 0

    def set_jog_speeds(self):
        if self.speed_toggle.state == 'normal': 
            self.speed_image.source = "./asmcnc/skavaUI/img/slow.png"
            self.feedSpeedJogX = self.fast_x_speed / 5
            self.feedSpeedJogY = self.fast_y_speed / 5
            self.feedSpeedJogZ = self.fast_z_speed / 5
        else: 
            self.speed_image.source = "./asmcnc/skavaUI/img/fast.png"
            self.feedSpeedJogX = self.fast_x_speed
            self.feedSpeedJogY = self.fast_y_speed
            self.feedSpeedJogZ = self.fast_z_speed

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

    def set_datum(self):
        self.sm.get_screen('nudge').set_datum_popup()
