# -*- coding: utf-8 -*-
"""
Created Feb 2024

@author: Benji
"""
import sys
from datetime import datetime

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


Builder.load_string("""
<ProbingScreen>:
    
    probing_label: probing_label

    canvas:
        Color: 
            rgba: hex('#E5E5E5FF')
        Rectangle: 
            size: self.size
            pos: self.pos         

    BoxLayout: 
        spacing: 0
        padding:[dp(0.05)*app.width, dp(0.0833333333333)*app.height]
        orientation: 'vertical'

        Label:
            font_size: str(0.01875 * app.width) + 'sp'
            size_hint_y: 1

        BoxLayout:
            orientation: 'horizontal'
            spacing:0.025*app.width
            size_hint_y: 1.5

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.windows_cheat_to_procede()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/z_probe_big.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
            Label:
                id: probing_label
                size_hint_x: 1.1
                markup: True
                font_size: str(0.0375*app.width) + 'px' 
                valign: 'middle'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')
                        
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_press: root.stop_button_press()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/stop_big.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
        Label:
            font_size: str(0.01875 * app.width) + 'sp'
            size_hint_y: 1                

"""
) # Based on src/asmcnc/skavaUI/screen_homing_active.py

def log(message):
    timestamp = datetime.now()
    print(timestamp.strftime("%H:%M:%S.%f")[:12] + " " + str(message))


class ProbingScreen(Screen):
    button_reference = None

    def __init__(self, **kwargs):
        super(ProbingScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        
        self.update_strings()

    def update_strings(self):
        self.probing_label.text = self.l.get_str("Probing") + "..."

    def on_enter(self):
        self.m.probe_z()
        Clock.schedule_once(lambda dt: self.probing_clock(), 0.5) # Wait before checking if probing
    
    def probing_clock(self):
        self.confirm_probing_event = Clock.schedule_interval(lambda dt: self.confirm_probing(), 0.5)

    def confirm_probing(self):
        machine_state = self.m.state()
        if machine_state.lower() != "run":
            # Machine is no longer probing
            self.sm.remove_widget(self)

    def stop_button_press(self):
        log("Probing cancelled by user")
        self.cancel_probing()
        self.exit()

    def cancel_probing(self):
        self.m._grbl_feed_hold()
        Clock.schedule_once(lambda dt: self.m._grbl_soft_reset(), 0.5) # Wait before reseting to avoid alarm

    def exit(self):
        Clock.unschedule(self.confirm_probing_event)
        self.sm.current = self.sm.return_to_screen
