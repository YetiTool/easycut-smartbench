'''
Created on 1 Feb 2018
@author: Ed
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.properties import ObjectProperty

import os, sys
import socket


Builder.load_string("""

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
        padding: 1
        spacing: 6
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
            size_hint_x: 0.2
            id: ip_status_label
            text_size: self.size
            halign: 'left'
            valign: 'middle'
            text: 'IP 255.255.255.255'

#         Label:
#             size_hint_x: 0.1

        Label:
            size_hint_x: 0.1
            id: grbl_xm_label
            text: 'mX:\\n-9999.99'
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 0.1
            id: grbl_ym_label
            text: 'mY:\\n-9999.99'
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 0.1
            id: grbl_zm_label
            text: 'mZ:\\n-9999.99'
            text_size: self.size
            halign: 'left'
            valign: 'middle'


        Label:
            size_hint_x: 0.1
            id: grbl_xw_label
            text: 'wX:\\n-9999.99'
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 0.1
            id: grbl_yw_label
            text: 'wY:\\n-9999.99'
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 0.1
            id: grbl_zw_label
            text: 'wZ:\\n-9999.99'
            text_size: self.size
            halign: 'left'
            valign: 'middle'

        Label:
            size_hint_x: 0.1
            id: grbl_status_label
            text: 'Status'
            text_size: self.size
            halign: 'right'
            valign: 'middle'

""")



class StatusBar(Widget):

    GRBL_REPORT_INTERVAL = 0.1
    IP_REPORT_INTERVAL = 2
    
    cheeky_color = StringProperty('#4CAF50FF')

    wifi_on = "./asmcnc/skavaUI/img/wifi_on.png"
    wifi_off = "./asmcnc/skavaUI/img/wifi_off.png"
    wifi_warning = "./asmcnc/skavaUI/img/wifi_warning.png"

    machine = ObjectProperty()
    screen_manager = ObjectProperty()

    def __init__(self, **kwargs):
        super(StatusBar, self).__init__(**kwargs)
        Clock.schedule_interval(self.refresh_grbl_label_values, self.GRBL_REPORT_INTERVAL)      # Poll for status
        Clock.schedule_interval(self.refresh_ip_label_value, self.IP_REPORT_INTERVAL)      # Poll for status

    def on_enter(self):
        self.refresh_ip_label_value()


    def refresh_grbl_label_values(self, dt):
        if self.machine.is_connected():
            self.serial_image.source = "./asmcnc/skavaUI/img/serial_on.png"
            self.grbl_status_label.text = str(self.machine.state().decode('UTF-8','ignore'))
            self.grbl_xm_label.text = 'mX:\n' + str(round(self.machine.mpos_x(), 2))
            self.grbl_ym_label.text = 'mY:\n' + str(round(self.machine.mpos_y(), 2))
            self.grbl_zm_label.text = 'mZ:\n' + str(round(self.machine.mpos_z(), 2))
            self.grbl_xw_label.text = 'wX:\n' + str(round(self.machine.wpos_x(), 2))
            self.grbl_yw_label.text = 'wY:\n' + str(round(self.machine.wpos_y(), 2))
            self.grbl_zw_label.text = 'wZ:\n' + str(round(self.machine.wpos_z(), 2))

        else:
            self.serial_image.source = "./asmcnc/skavaUI/img/serial_off.png"

    def refresh_ip_label_value(self, dt):

        self.ip_status_label.text = self.machine.sett.ip_address

        if self.machine.sett.wifi_available: 
            self.wifi_image.source = self.wifi_on

        elif not self.machine.sett.ip_address: 
            self.wifi_image.source = self.wifi_off

        else: 
            self.wifi_image.source = self.wifi_warning

