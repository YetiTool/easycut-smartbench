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

<StatusBar>

    grbl_status_label:grbl_status_label
    grbl_xm_label:grbl_xm_label
    grbl_ym_label:grbl_ym_label
    grbl_zm_label:grbl_zm_label
    grbl_xw_label:grbl_xw_label
    grbl_yw_label:grbl_yw_label
    grbl_zw_label:grbl_zw_label
    serial_image:serial_image
    wifi_image:wifi_image
    ip_status_label:ip_status_label

    cheeky_color: '#4CAF50FF'

    canvas:
        Color:
            rgba: hex(self.cheeky_color)
        Rectangle:
            pos:self.pos
            size: self.size

    BoxLayout:
        padding: app.get_scaled_tuple([1.0, 1.0])
        spacing: app.get_scaled_width(6.0)
        orientation: "horizontal"
        size: self.parent.size
        pos: self.parent.pos

        Image:
            id: serial_image
            size_hint_x: 0.05
            source: "./asmcnc/skavaUI/img/serial_on.png"
            center_x: self.parent.center_x
            y: self.parent.y
            size: self.parent.width, self.parent.height
            allow_stretch: True
        Image:
            id: wifi_image
            size_hint_x: 0.05
            source: "./asmcnc/skavaUI/img/wifi_on.png"
            center_x: self.parent.center_x
            y: self.parent.y
            size: self.parent.width, self.parent.height
            allow_stretch: True
        Label:
            font_size: app.get_scaled_sp('15.0sp')
            size_hint_x: 0.2
            id: ip_status_label
            text_size: self.size
            halign: 'left'
            valign: 'middle'
            text: 'IP 255.255.255.255'

#         Label:
#             size_hint_x: 0.1

        Label:
            font_size: app.get_scaled_sp('15.0sp')
            size_hint_x: 0.1
            id: grbl_xm_label
            text: 'mX:\\n-9999.99'
            text_size: self.size
            halign: 'left'
            valign: 'middle'
            markup: True
        Label:
            font_size: app.get_scaled_sp('15.0sp')
            size_hint_x: 0.1
            id: grbl_ym_label
            text: 'mY:\\n-9999.99'
            text_size: self.size
            halign: 'left'
            valign: 'middle'
            markup: True
        Label:
            font_size: app.get_scaled_sp('15.0sp')
            size_hint_x: 0.1
            id: grbl_zm_label
            text: 'mZ:\\n-9999.99'
            text_size: self.size
            halign: 'left'
            valign: 'middle'
            markup: True


        Label:
            font_size: app.get_scaled_sp('15.0sp')
            size_hint_x: 0.1
            id: grbl_xw_label
            text: 'wX:\\n-9999.99'
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            font_size: app.get_scaled_sp('15.0sp')
            size_hint_x: 0.1
            id: grbl_yw_label
            text: 'wY:\\n-9999.99'
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            font_size: app.get_scaled_sp('15.0sp')
            size_hint_x: 0.1
            id: grbl_zw_label
            text: 'wZ:\\n-9999.99'
            text_size: self.size
            halign: 'left'
            valign: 'middle'

        Label:
            font_size: app.get_scaled_sp('15.0sp')
            size_hint_x: 0.1
            id: grbl_status_label
            text: 'Status'
            text_size: self.size
            halign: 'right'
            valign: 'middle'

"""
)


class StatusBar(Widget):
    GRBL_REPORT_INTERVAL = 0.1
    IP_REPORT_INTERVAL = 2
    cheeky_color = StringProperty("#4CAF50FF")
    wifi_on = "./asmcnc/skavaUI/img/wifi_on.png"
    wifi_off = "./asmcnc/skavaUI/img/wifi_off.png"
    wifi_warning = "./asmcnc/skavaUI/img/wifi_warning.png"

    def __init__(self, **kwargs):
        super(StatusBar, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        Clock.schedule_interval(
            self.refresh_grbl_label_values, self.GRBL_REPORT_INTERVAL
        )
        Clock.schedule_interval(self.refresh_ip_label_value, self.IP_REPORT_INTERVAL)

    def on_enter(self):
        self.refresh_ip_label_value()

    def check_limit_switch(self):
        if self.m.s.limit_x:
            self.grbl_xm_label.text = "m[b][color=ff0000]x[/color][/b]:\n" + str(
                round(self.m.mpos_x(), 2)
            )
        elif self.m.s.limit_X:
            self.grbl_xm_label.text = "m[b][color=ff0000]X[/color][/b]:\n" + str(
                round(self.m.mpos_x(), 2)
            )
        else:
            self.grbl_xm_label.text = "mX:\n" + str(round(self.m.mpos_x(), 2))
        if self.m.s.limit_Y_axis:
            self.grbl_ym_label.text = "m[b][color=ff0000]Y[/color][/b]:\n" + str(
                round(self.m.mpos_y(), 2)
            )
        elif self.m.s.limit_Y:
            self.grbl_ym_label.text = "m[b][color=ff0000]Y[/color][/b]:\n" + str(
                round(self.m.mpos_y(), 2)
            )
        elif self.m.s.limit_y:
            self.grbl_ym_label.text = "m[b][color=ff0000]y[/color][/b]:\n" + str(
                round(self.m.mpos_y(), 2)
            )
        else:
            self.grbl_ym_label.text = "mY:\n" + str(round(self.m.mpos_y(), 2))
        if self.m.s.limit_z:
            self.grbl_zm_label.text = "m[b][color=ff0000]Z[/color][/b]:\n" + str(
                round(self.m.mpos_z(), 2)
            )
        else:
            self.grbl_zm_label.text = "mZ:\n" + str(round(self.m.mpos_z(), 2))

    def refresh_grbl_label_values(self, dt):
        if self.m.is_connected():
            self.serial_image.source = "./asmcnc/skavaUI/img/serial_on.png"
            self.grbl_status_label.text = self.m.state()
            self.check_limit_switch()
            self.grbl_xw_label.text = "wX:\n" + str(round(self.m.wpos_x(), 2))
            self.grbl_yw_label.text = "wY:\n" + str(round(self.m.wpos_y(), 2))
            self.grbl_zw_label.text = "wZ:\n" + str(round(self.m.wpos_z(), 2))
        else:
            self.serial_image.source = "./asmcnc/skavaUI/img/serial_off.png"

    def refresh_ip_label_value(self, dt):
        self.ip_status_label.text = self.m.sett.ip_address
        if self.m.sett.wifi_available:
            self.wifi_image.source = self.wifi_on
        elif not self.m.sett.ip_address:
            self.wifi_image.source = self.wifi_off
        else:
            self.wifi_image.source = self.wifi_warning
