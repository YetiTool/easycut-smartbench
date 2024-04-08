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

from asmcnc.core_UI.components.widgets.coordinate_labels import MachineXCoordinateLabel, MachineYCoordinateLabel, \
    MachineZCoordinateLabel

Builder.load_string(
    """

#:import hex kivy.utils.get_color_from_hex

<StatusBar>

    grbl_status_label:grbl_status_label
    grbl_xw_label:grbl_xw_label
    grbl_yw_label:grbl_yw_label
    grbl_zw_label:grbl_zw_label
    serial_image:serial_image
    wifi_image:wifi_image
    ip_status_label:ip_status_label
    m_x_container:m_x_container
    m_y_container:m_y_container
    m_z_container:m_z_container

    cheeky_color: '#4CAF50FF'

    canvas:
        Color:
            rgba: hex(self.cheeky_color)
        Rectangle:
            pos:self.pos
            size: self.size

    BoxLayout:
        padding:[dp(0.00125)*app.width, dp(0.00208333333333)*app.height]
        spacing:0.0075*app.width
        orientation: "horizontal"
        size: self.parent.size
        pos: self.parent.pos
        padding: [5, 0, 5, 0]

        Image:
            id: serial_image
            size_hint_y: 0.9
            allow_stretch: True
            source: "./asmcnc/skavaUI/img/serial_on.png"
        Image:
            id: wifi_image
            size_hint_y: 0.9
            allow_stretch: True
            source: "./asmcnc/skavaUI/img/wifi_on.png"
        Label:
            font_size: str(0.0225 * app.width) + 'sp'
            id: ip_status_label
            text_size: self.size
            halign: 'left'
            valign: 'middle'
            text: 'IP 255.255.255.255'

#         Label:
#             size_hint_x: 0.1

        BoxLayout:
            id: m_x_container
            
        BoxLayout:
            id: m_y_container
            
        BoxLayout:
            id: m_z_container

        BoxLayout:
            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                id: grbl_xw_label
                text: 'wX:\\n-9999.99'
                text_size: self.size
                halign: 'left'
                valign: 'middle'
        BoxLayout:
            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                id: grbl_yw_label
                text: 'wY:\\n-9999.99'
                text_size: self.size
                halign: 'left'
                valign: 'middle'
        BoxLayout:
            Label:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_x: 0.1
                id: grbl_zw_label
                text: 'wZ:\\n-9999.99'
                text_size: self.size
                halign: 'left'
                valign: 'middle'

        Label:
            font_size: str((0.0225) * app.width) + 'sp'
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

        self.m_x_container.add_widget(MachineXCoordinateLabel(self.m.s))
        self.m_y_container.add_widget(MachineYCoordinateLabel(self.m.s))
        self.m_z_container.add_widget(MachineZCoordinateLabel(self.m.s))

        Clock.schedule_interval(
            self.refresh_grbl_label_values, self.GRBL_REPORT_INTERVAL
        )
        Clock.schedule_interval(self.refresh_ip_label_value, self.IP_REPORT_INTERVAL)

    def on_enter(self):
        self.refresh_ip_label_value()

    def check_limit_switch(self):
        pass

    def refresh_grbl_label_values(self, dt):
        if self.m.is_connected():
            self.serial_image.source = "./asmcnc/skavaUI/img/serial_on.png"
            self.grbl_status_label.text = self.m.state()
            self.check_limit_switch()
            self.grbl_xw_label.text = "wX: " + str(round(self.m.wpos_x(), 2))
            self.grbl_yw_label.text = "wY: " + str(round(self.m.wpos_y(), 2))
            self.grbl_zw_label.text = "wZ: " + str(round(self.m.wpos_z(), 2))
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
