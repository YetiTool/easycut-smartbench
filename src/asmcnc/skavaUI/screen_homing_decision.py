# -*- coding: utf-8 -*-
"""
Created July 2022

@author: Dennis

Ask if user wants to rehome, for job recovery
"""

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from asmcnc.skavaUI import popup_info

Builder.load_string(
    """

<HomingDecisionScreen>:

    header_label: header_label
    subtitle_label: subtitle_label
    no_button: no_button
    yes_button: yes_button

    canvas:
        Color:
            rgba: hex('#E5E5E5FF')
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        spacing: 0
        padding: 40
        orientation: 'vertical'

        # Cancel button
        BoxLayout:
            size_hint: (None,None)
            height: dp(20)
            padding: (20,0,20,0)
            spacing: 680
            orientation: 'horizontal'
            pos: self.parent.pos

            Label:
                text: ""

            Button:
                size_hint: (None,None)
                height: dp(50)
                width: dp(50)
                background_color: hex('#FFFFFF00')
                opacity: 1
                on_press: root.cancel()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/cancel_btn_decision_context.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

        Label:
            size_hint_y: 0.1

        BoxLayout:
            orientation: 'vertical'
            spacing: 10
            padding: (0,20,0,20)
            size_hint_y: 3


            Label:
                id: header_label
                size_hint_y: 2
                markup: True
                font_size: '30px'
                valign: 'bottom'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')

            Label:
                id: subtitle_label
                size_hint_y: 1
                markup: True
                font_size: '18px'
                valign: 'top'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')

        BoxLayout:
            orientation: 'horizontal'
            spacing: 30
            size_hint_y: 3

            Button:
                id: yes_button
                size_hint_x: 1
                on_press: root.rehome()
                valign: "middle"
                halign: "center"
                markup: True
                font_size: root.default_font_size
                text_size: self.size
                background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                border: [dp(30)]*4
                padding: [20, 20]

            Button:
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
                id: no_button
                size_hint_x: 1
                on_press: root.already_homed()
                valign: "middle"
                halign: "center"
                markup: True
                font_size: root.default_font_size
                text_size: self.size
                background_normal: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                background_down: "./asmcnc/skavaUI/img/blank_blue_btn_2-1_rectangle.png"
                border: [dp(30)]*4
                padding: [20, 20]

        Label:
            size_hint_y: .5

"""
)


class HomingDecisionScreen(Screen):
    cancel_to_screen = "lobby"
    return_to_screen = "lobby"

    default_font_size = 30

    def __init__(self, **kwargs):
        super(HomingDecisionScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]

        self.update_strings()

    def already_homed(self):
        self.sm.current = self.return_to_screen

    def rehome(self):
        self.m.request_homing_procedure(self.return_to_screen, self.cancel_to_screen)

    def popup_help(self):
        info = (
            self.l.get_bold("Re-homing")
            + "\n"
            + self.l.get_str(
                "Homing is used by the machine to understand its position in 3D space."
            )
            + " "
            + self.l.get_str(
                "In the event of a mechanical stall (where the machine audibly clicks), SmartBench will have an incorrect understanding of its position."
            )
            + " "
            + self.l.get_str("In this case we recommend rehoming.")
            + " "
            + self.l.get_str(
                "If SmartBench did not stall, we recommend that you do not re-home."
            )
            .replace(
                " " + self.l.get_str("not") + " ", " " + self.l.get_bold("not") + " "
            )
            .replace(
                " " + self.l.get_str("not") + ",", " " + self.l.get_bold("not") + ","
            )
            + "\n\n"
            + self.l.get_str(
                "If you choose to rehome, use the nudge screen to properly realign your tool over the already cut toolpath."
            )
            + " "
            + self.l.get_str(
                "This accounts for inconsistencies in the homing process and will move your datum accordingly."
            )
        )

        popup_info.PopupInfo(self.sm, self.l, 760, info)

    def update_strings(self):
        self.header_label.text = self.l.get_str("Would you like to rehome?")
        self.yes_button.text = self.l.get_str("Yes, rehome")
        self.no_button.text = self.l.get_str("No, do not rehome")

    def cancel(self):
        self.sm.current = self.cancel_to_screen
