# -*- coding: utf-8 -*-
"""
Created July 2022

@author: Dennis

Ask if user wants to rehome, for job recovery
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from asmcnc.core_UI import scaling_utils as utils
from asmcnc.core_UI.popups import InfoPopup

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
        padding: app.get_scaled_tuple([40.0, 40.0])
        orientation: 'vertical'

        # Cancel button
        BoxLayout:
            size_hint: (None,None)
            height: app.get_scaled_height(20.0)
            padding: app.get_scaled_tuple([20.0, 0.0, 20.0, 0.0])
            spacing: app.get_scaled_width(680.0)
            orientation: 'horizontal'
            pos: self.parent.pos

            Label:
                font_size: app.get_scaled_sp('15.0sp')
                text: ""

            Button:
                font_size: app.get_scaled_sp('15.0sp')
                size_hint: (None,None)
                height: app.get_scaled_height(50.0000000002)
                width: app.get_scaled_width(50.0)
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
            font_size: app.get_scaled_sp('15.0sp')
            size_hint_y: 0.1

        BoxLayout:
            orientation: 'vertical'
            spacing: app.get_scaled_width(9.99999999998)
            padding: app.get_scaled_tuple([0.0, 20.0, 0.0, 20.0])
            size_hint_y: 3


            Label:
                id: header_label
                size_hint_y: 2
                markup: True
                font_size: str(0.0375*app.width) + 'px'
                valign: 'bottom'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')

            Label:
                id: subtitle_label
                size_hint_y: 1
                markup: True
                font_size: str(0.0225*app.width) + 'px'
                valign: 'top'
                halign: 'center'
                size:self.texture_size
                text_size: self.size
                color: hex('#333333ff')

        BoxLayout:
            orientation: 'horizontal'
            spacing: app.get_scaled_width(30.0)
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
                border: app.get_scaled_tuple([30.0, 30.0, 30.0, 30.0])
                padding: app.get_scaled_tuple([20.0, 20.0])

            Button:
                font_size: app.get_scaled_sp('15.0sp')
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
                border: app.get_scaled_tuple([30.0, 30.0, 30.0, 30.0])
                padding: app.get_scaled_tuple([20.0, 20.0])

        Label:
            font_size: app.get_scaled_sp('15.0sp')
            size_hint_y: .5

"""
)


class HomingDecisionScreen(Screen):
    cancel_to_screen = "lobby"
    return_to_screen = "lobby"
    default_font_size = utils.get_scaled_width(30)

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

        info_popup = InfoPopup(
            sm=self.sm, m=self.m, l=self.l,
            title='Information',
            main_string=info,
            popup_width=760,
            popup_height=440,
            )
        info_popup.open()

    def update_strings(self):
        self.header_label.text = self.l.get_str("Would you like to rehome?")
        self.yes_button.text = self.l.get_str("Yes, rehome")
        self.no_button.text = self.l.get_str("No, do not rehome")

    def cancel(self):
        self.sm.current = self.cancel_to_screen
