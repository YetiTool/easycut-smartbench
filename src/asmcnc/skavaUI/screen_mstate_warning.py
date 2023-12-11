"""
Created on 8 April 2019

Screen to tell user that machine is not Idle (before running a job). 

@author: Letty
"""
from kivy.lang import Builder
from kivy.properties import (
    StringProperty,
)
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex

Builder.load_string(
    """

<WarningMState>:

    title_label : title_label
    cannot_start_job : cannot_start_job
    getout_button : getout_button
    return_label : return_label

    canvas:
        Color: 
            rgba: hex('#fb8c00')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding:[dp(0.075)*app.width, dp(0.125)*app.height]
        spacing:0.0625*app.height
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 1
            spacing:0.0208333333333*app.height
             
            Label:
                id: title_label
                size_hint_y: 1
                text_size: self.size
                font_size: str(0.03625*app.width) + 'sp'
                markup: True
                halign: 'left'
                vallign: 'top'
 
            Label:
                id: cannot_start_job
                size_hint_y: 1
                text_size: self.size
                font_size: str(0.0275*app.width) + 'sp'
                halign: 'left'
                valign: 'middle'
                text: 'Cannot start job.'
                markup: True
                
            Label:
                size_hint_y: 1
                font_size: str(0.0275*app.width) + 'sp'
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                text: root.user_instruction
                markup: True
                
            BoxLayout:
                orientation: 'horizontal'
                padding:[dp(0.1625)*app.width, 0]
            
                Button:
                    font_size: str(0.01875 * app.width) + 'sp'
                    size_hint_y:0.9
                    id: getout_button
                    size: self.texture_size
                    valign: 'top'
                    halign: 'center'
                    disabled: False
                    background_normal: ''
                    background_down: ''
                    background_color: hex('#e65100')
                    on_press:
                        root.button_press()
                    on_release:
                        root.button_release()
                        
                    BoxLayout:
                        padding:[dp(0.00625)*app.width, dp(0.0104166666667)*app.height]
                        size: self.parent.size
                        pos: self.parent.pos
                        
                        Label:
                            id: return_label
                            font_size: str(0.025*app.width) + 'sp'
                        
  
            
"""
)


class WarningMState(Screen):
    button_text = StringProperty()
    user_instruction = StringProperty()

    def __init__(self, **kwargs):
        super(WarningMState, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def on_enter(self):
        if self.m.state().startswith("Alarm"):
            self.user_instruction = self.l.get_str(
                "SmartBench is in an Alarm state. Please clear the machine, and then reset it."
            )
        elif self.m.state().startswith("Check"):
            self.user_instruction = (
                self.l.get_str(
                    "SmartBench is in Check state. Please disable by pressing the Check $C button in the G-code console."
                )
                .replace(self.l.get_str("Check"), self.l.get_bold("Check"))
                .replace("$C", "[b]$C[/b]")
            )
        elif self.m.state().startswith("Door") or self.m.state().startswith("Hold"):
            self.user_instruction = self.l.get_str(
                "SmartBench is paused. Please resume by entering ~ into the G-code console."
            ).replace("~", "[b]~[/b]")
        else:
            self.user_instruction = (
                self.l.get_str("SmartBench is still carrying out a command.")
                + " "
                + self.l.get_str(
                    "Please wait for SmartBench to finish before attempting to start a job."
                )
            )
        self.update_strings()

    def button_press(self):
        self.getout_button.background_color = get_color_from_hex("#c43c00")

    def button_release(self):
        self.sm.current = "home"

    def update_strings(self):
        self.title_label.text = (
            self.l.get_bold("WARNING")
            + "\n"
            + self.l.get_str("SmartBench is not in an idle state.")
        )
        self.cannot_start_job.text = self.l.get_str("Cannot start job.")
        self.return_label.text = self.l.get_str("Return")
