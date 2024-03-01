"""
Created on 1 Feb 2018
@author: Ed
"""
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.components.images.blinking_image import BlinkingWidget

Builder.load_string(
    """
<CommonMove>

    speed_image:speed_image
    speed_toggle:speed_toggle
    vacuum_image:vacuum_image
    vacuum_toggle:vacuum_toggle
    vacuum_spindle_container:vacuum_spindle_container

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos      

        spacing:0.0416666666667*app.height
        
        orientation: "vertical"
        
        BoxLayout:
            spacing: 0
            padding:dp(0)
            size_hint_y: 1
            orientation: 'vertical'
            canvas:
                Color: 
                    rgba: 1,1,1,1
                RoundedRectangle: 
                    size: self.size
                    pos: self.pos 

            ToggleButton:
                font_size: str(0.01875 * app.width) + 'sp'
                id: speed_toggle
                on_press: root.set_jog_speeds()
                background_color: 1, 1, 1, 0 
                BoxLayout:
                    padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                    size: self.parent.size
                    pos: self.parent.pos      
                    Image:
                        id: speed_image
                        source: "./asmcnc/skavaUI/img/slow.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True  
            
        BoxLayout:
            spacing: 0
            padding:dp(0)
            size_hint_y: 2
            orientation: 'vertical'
            id: vacuum_spindle_container
            canvas:
                Color: 
                    rgba: 1,1,1,1
                RoundedRectangle: 
                    size: self.size
                    pos: self.pos 

            ToggleButton:
                font_size: str(0.01875 * app.width) + 'sp'
                id: vacuum_toggle
                on_press: root.set_vacuum()
                background_color: 1, 1, 1, 0 
                BoxLayout:
                    padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                    size: self.parent.size
                    pos: self.parent.pos      
                    Image:
                        id: vacuum_image
                        source: "./asmcnc/skavaUI/img/vac_off.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True  
"""
)


class CommonMove(Widget):
    def __init__(self, **kwargs):
        super(CommonMove, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.set_jog_speeds()
        self.add_spindle_button()

    def add_spindle_button(self):
        self.spindle_button_padding_container = BoxLayout(padding=[dp(10)])
        self.spindle_button = Button(
            background_normal="./asmcnc/skavaUI/img/spindle_off.png",
            background_down="./asmcnc/skavaUI/img/spindle_off.png",
            on_press=self.set_spindle,
            allow_stretch=True,
        )
        self.spindle_blinker = BlinkingWidget()
        self.spindle_blinker.bind(pos=self.update_spindle_button, size=self.update_spindle_button)
        self.spindle_blinker.add_widget(self.spindle_button)
        self.spindle_button_padding_container.add_widget(self.spindle_blinker)
        self.vacuum_spindle_container.add_widget(self.spindle_button_padding_container)

    def update_spindle_button(self, *args):
        self.spindle_button.center = self.spindle_blinker.center

    fast_x_speed = 6000
    fast_y_speed = 6000
    fast_z_speed = 750

    def set_jog_speeds(self):
        if self.speed_toggle.state == "normal":
            self.speed_image.source = "./asmcnc/skavaUI/img/slow.png"
            self.feedSpeedJogX = self.fast_x_speed / 5
            self.feedSpeedJogY = self.fast_y_speed / 5
            self.feedSpeedJogZ = self.fast_z_speed / 5
        else:
            self.speed_image.source = "./asmcnc/skavaUI/img/fast.png"
            self.feedSpeedJogX = self.fast_x_speed
            self.feedSpeedJogY = self.fast_y_speed
            self.feedSpeedJogZ = self.fast_z_speed

    def set_vacuum(self):
        if self.vacuum_toggle.state == "normal":
            self.vacuum_image.source = "./asmcnc/skavaUI/img/vac_off.png"
            self.m.vac_off()
        else:
            self.vacuum_image.source = "./asmcnc/skavaUI/img/vac_on.png"
            self.m.vac_on()

    def set_spindle(self, *args):
        def button_two_callback():
            self.spindle_button.background_normal = "./asmcnc/skavaUI/img/spindle_on.png"
            self.m.spindle_on()
            self.spindle_blinker.blinking = True

        if self.spindle_blinker.blinking:
            self.spindle_button.background_normal = "./asmcnc/skavaUI/img/spindle_off.png"
            self.m.spindle_off()
            self.spindle_blinker.blinking = False
        else:
            self.sm.pm.show_spindle_safety_popup(None, button_two_callback)
