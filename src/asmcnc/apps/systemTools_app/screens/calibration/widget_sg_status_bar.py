'''
Created on 1 Feb 2018
@author: Ed
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty 
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.clock import Clock
from asmcnc.core_UI.utils import color_provider

import os, sys
import socket


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex

<SGStatusBar>

    grbl_status_label:grbl_status_label
    grbl_xm_label:grbl_xm_label
    grbl_ym_label:grbl_ym_label
    grbl_zm_label:grbl_zm_label
    # grbl_xw_label:grbl_xw_label
    # grbl_yw_label:grbl_yw_label
    # grbl_zw_label:grbl_zw_label

    grbl_X_ld_label : grbl_X_ld_label
    grbl_X1_ld_label : grbl_X1_ld_label
    grbl_X2_ld_label : grbl_X2_ld_label
    grbl_Y_ld_label : grbl_Y_ld_label
    grbl_Y1_ld_label : grbl_Y1_ld_label
    grbl_Y2_ld_label : grbl_Y2_ld_label
    grbl_Z_ld_label : grbl_Z_ld_label

    wifi_image:wifi_image
    ip_status_label:ip_status_label

    cheeky_color: color_provider.get_rgba("green")

    canvas:
        Color:
            rgba: self.cheeky_color
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
            id: grbl_X_ld_label
            text: 'sgX:\\n0'
            text_size: self.size
            halign: 'left'
            valign: 'middle'

        Label:
            size_hint_x: 0.1
            id: grbl_X1_ld_label
            text: 'sgX:\\n0'
            text_size: self.size
            halign: 'left'
            valign: 'middle'

        Label:
            size_hint_x: 0.1
            id: grbl_X2_ld_label
            text: 'sgX:\\n0'
            text_size: self.size
            halign: 'left'
            valign: 'middle'

        Label:
            size_hint_x: 0.1
            id: grbl_Y_ld_label
            text: 'sgY:\\n0'
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 0.1
            id: grbl_Y1_ld_label
            text: 'sgY1:\\n0'
            text_size: self.size
            halign: 'left'
            valign: 'middle'

        Label:
            size_hint_x: 0.1
            id: grbl_Y2_ld_label
            text: 'sgY2:\\n0'
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            size_hint_x: 0.1
            id: grbl_Z_ld_label
            text: 'sgZ:\\n0'
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



class SGStatusBar(Widget):

    GRBL_REPORT_INTERVAL = 0.1
    IP_REPORT_INTERVAL = 2
    
    cheeky_color = color_provider.get_rgba("green")

    wifi_on = "./asmcnc/skavaUI/img/wifi_on.png"
    wifi_off = "./asmcnc/skavaUI/img/wifi_off.png"
    wifi_warning = "./asmcnc/skavaUI/img/wifi_warning.png"

    def __init__(self, **kwargs):

        super(SGStatusBar, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        Clock.schedule_interval(self.refresh_grbl_label_values, self.GRBL_REPORT_INTERVAL)      # Poll for status
        Clock.schedule_interval(self.refresh_ip_label_value, self.IP_REPORT_INTERVAL)      # Poll for status

    def on_enter(self):
        self.refresh_ip_label_value()


    def refresh_grbl_label_values(self, dt):
        if self.m.is_connected():

            self.grbl_status_label.text = self.m.state()
            self.grbl_xm_label.text = 'mX:\n' + str(round(self.m.mpos_x(), 2))
            self.grbl_ym_label.text = 'mY:\n' + str(round(self.m.mpos_y(), 2))
            self.grbl_zm_label.text = 'mZ:\n' + str(round(self.m.mpos_z(), 2))

            self.grbl_X_ld_label.text = 'sgX:\n' + str(self.m.x_sg())
            self.grbl_X1_ld_label.text = 'sgX1:\n' + str(self.m.x1_sg())
            self.grbl_X2_ld_label.text = 'sgX2:\n' + str(self.m.x2_sg())
            self.grbl_Y_ld_label.text = 'sgY:\n' + str(self.m.y_sg())
            self.grbl_Y1_ld_label.text = 'sgY1:\n' + str(self.m.y1_sg())
            self.grbl_Y2_ld_label.text = 'sgY2:\n' + str(self.m.y2_sg())
            self.grbl_Z_ld_label.text = 'sgZ:\n' + str(self.m.z_sg())


    def refresh_ip_label_value(self, dt):

        self.ip_status_label.text = self.m.sett.ip_address

        if self.m.sett.wifi_available: 
            self.wifi_image.source = self.wifi_on

        elif not self.m.sett.ip_address: 
            self.wifi_image.source = self.wifi_off

        else: 
            self.wifi_image.source = self.wifi_warning

