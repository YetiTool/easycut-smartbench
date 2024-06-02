# -*- coding: utf-8 -*-
"""
Created March 2019

@author: Ed

Squaring decision: manual or auto?
"""

from datetime import datetime

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from asmcnc.skavaUI import popup_info

from asmcnc.core_UI.scaling_utils import get_scaled_sp

Builder.load_string(
    """

<LiftZOnPauseDecisionScreen>:

    header_label: header_label
    yes_button: yes_button
    no_button: no_button

    canvas:
        Color: 
            rgba: hex('#E5E5E5FF')
        Rectangle: 
            size: self.size
            pos: self.pos         

    BoxLayout: 
        spacing: 0
        padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
        orientation: 'vertical'

        Label:
            id: header_label
            size_hint_y: 3
            markup: True
            font_size: str(0.0375*app.width) + 'px' 
            valign: 'center'
            halign: 'center'
            size:self.texture_size
            text_size: self.size
            color: hex('#333333ff')
    
        BoxLayout:
            orientation: 'horizontal'
            padding:[dp(0.025)*app.width, 0, dp(0.025)*app.width, 0]
            spacing:0.05*app.width
            size_hint_y: 3

            Button:
                id: no_button
                size_hint_x: 1
                on_press: root.decision_no()
                valign: "middle"
                halign: "center"
                markup: True
                font_size: root.default_font_size
                text_size: self.size
                background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                border: [dp(30)]*4
                padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                        
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_x: 0.3
                background_color: hex('#FFFFFF00')
                on_press: root.popup_help()
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/help_btn_orange_round.png"
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                        
            Button:
                id: yes_button
                size_hint_x: 1
                on_press: root.decision_yes()
                valign: "middle"
                halign: "center"
                markup: True
                font_size: root.default_font_size
                text_size: self.size
                background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                border: [dp(30)]*4
                padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                        
        Label:
            font_size: str(0.01875 * app.width) + 'sp'
            size_hint_y: .5                

"""
)


class LiftZOnPauseDecisionScreen(Screen):
    default_font_size = get_scaled_sp("36sp")

    def __init__(self, **kwargs):
        super(LiftZOnPauseDecisionScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def popup_help(self):
        info = (
            self.l.get_bold(
                "Automatic lifting during a pause (recommended for most tools)"
            )
            + ":"
            + "\n"
            + self.l.get_str(
                "When paused, SmartBench can automatically lift the Z axis and move the tool away from the job."
            )
            + "\n\n"
            + " - "
            + self.l.get_str("This can be used to inspect the work or clear blockages.")
            + "\n"
            + " - "
            + self.l.get_str(
                "It allows the spindle to decelerate away from the job, avoiding burn marks."
            )
            + "\n\n"
            + self.l.get_str(
                "SmartBench automatically returns the tool to the correct position before resuming."
            )
            + "\n\n"
            + self.l.get_bold(
                "Do not allow this feature if the tool has any inverted horizontal features which would rip through the job if the tool were to be lifted (e.g. a biscuit cutter tool profile)."
            )
        )
        popup_info.PopupInfo(self.sm, self.l, 760, info)

    def decision_no(self):
        if self.m.fw_can_operate_zUp_on_pause():  # precaution (this screen shouldn't appear if fw not capable)
            self.sm.get_screen("go").lift_z_on_job_pause = False
        self.sm.current = "jobstart_warning"

    def decision_yes(self):
        if self.m.fw_can_operate_zUp_on_pause():  # precaution (this screen shouldn't appear if fw not capable)
            self.sm.get_screen("go").lift_z_on_job_pause = True
        self.sm.current = "jobstart_warning"

    def update_strings(self):
        self.yes_button.text = self.l.get_str("Yes")
        self.no_button.text = self.l.get_str("No")
        self.header_label.text = self.l.get_str(
            "If the job pauses, should SmartBench automatically lift the Z axis away from the job?"
        )
