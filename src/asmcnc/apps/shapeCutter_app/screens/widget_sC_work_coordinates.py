"""
Created on 1 Feb 2018
@author: Ed
"""

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    ObjectProperty,
    ListProperty,
    NumericProperty,
    StringProperty,
)
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.clock import Clock
import os, sys
import socket

Builder.load_string(
    """

#:import hex kivy.utils.get_color_from_hex

<WorkCoordinates>

#     grbl_status_label:grbl_status_label
    grbl_xm_label:grbl_xm_label
    grbl_ym_label:grbl_ym_label
    grbl_zm_label:grbl_zm_label
    grbl_xw_label:grbl_xw_label
    grbl_yw_label:grbl_yw_label
    grbl_zw_label:grbl_zw_label
#     serial_image:serial_image
#     wifi_image:wifi_image
#     ip_status_label:ip_status_label

    cheeky_color: '#2498f4ff'

    canvas:
        Color:
            rgba: hex(self.cheeky_color)
        RoundedRectangle:
            pos:self.pos
            size: self.size

    BoxLayout:
        padding:[dp(0.00125)*app.width, dp(0.00208333333333)*app.height]
        spacing:0.0075*app.width
        orientation: "horizontal"
        size: self.parent.size
        pos: self.parent.pos

        Label:
            size_hint_x: 0.1
            id: grbl_xm_label
            text: 'mX:\\n-9999.99'
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            markup: True
            font_size: 0.01625*app.width
        Label:
            size_hint_x: 0.1
            id: grbl_ym_label
            text: 'mY:\\n-9999.99'
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            markup: True
            font_size: 0.01625*app.width
        Label:
            size_hint_x: 0.1
            id: grbl_zm_label
            text: 'mZ:\\n-9999.99'
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            markup: True
            font_size: 0.01625*app.width

        Label:
            size_hint_x: 0.1
            id: grbl_xw_label
            text: 'wX:\\n-9999.99'
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            markup: True
            font_size: 0.01625*app.width
        Label:
            size_hint_x: 0.1
            id: grbl_yw_label
            text: 'wY:\\n-9999.99'
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            markup: True
            font_size: 0.01625*app.width
        Label:
            size_hint_x: 0.1
            id: grbl_zw_label
            text: 'wZ:\\n-9999.99'
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            markup: True
            font_size: 0.01625*app.width
"""
)


class WorkCoordinates(Widget):
    GRBL_REPORT_INTERVAL = 0.1
    cheeky_color = StringProperty("#2498f4ff")

    def __init__(self, **kwargs):
        self.m = kwargs.pop("machine")
        self.sm = kwargs.pop("screen_manager")
        super(WorkCoordinates, self).__init__(**kwargs)
        Clock.schedule_interval(
            self.refresh_grbl_label_values, self.GRBL_REPORT_INTERVAL
        )

    def refresh_grbl_label_values(self, dt):
        if self.m.is_connected():
            self.grbl_xm_label.text = "mX:\n" + str(round(self.m.mpos_x(), 2))
            self.grbl_ym_label.text = "mY:\n" + str(round(self.m.mpos_y(), 2))
            self.grbl_zm_label.text = "mZ:\n" + str(round(self.m.mpos_z(), 2))
            self.grbl_xw_label.text = "wX:\n" + str(round(self.m.wpos_x(), 2))
            self.grbl_yw_label.text = "wY:\n" + str(round(self.m.wpos_y(), 2))
            self.grbl_zw_label.text = "wZ:\n" + str(round(self.m.wpos_z(), 2))
