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

import os, sys
import socket


Builder.load_string("""

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
        padding: 1
        spacing: 6
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
            font_size: 13
        Label:
            size_hint_x: 0.1
            id: grbl_ym_label
            text: 'mY:\\n-9999.99'
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            markup: True
            font_size: 13
        Label:
            size_hint_x: 0.1
            id: grbl_zm_label
            text: 'mZ:\\n-9999.99'
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            markup: True
            font_size: 13

        Label:
            size_hint_x: 0.1
            id: grbl_xw_label
            text: 'wX:\\n-9999.99'
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            markup: True
            font_size: 13
        Label:
            size_hint_x: 0.1
            id: grbl_yw_label
            text: 'wY:\\n-9999.99'
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            markup: True
            font_size: 13
        Label:
            size_hint_x: 0.1
            id: grbl_zw_label
            text: 'wZ:\\n-9999.99'
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            markup: True
            font_size: 13
""")



class WorkCoordinates(Widget):

    GRBL_REPORT_INTERVAL = 0.1
#     IP_REPORT_INTERVAL = 2
    
    cheeky_color = StringProperty('#2498f4ff')

    def __init__(self, **kwargs):

        super(WorkCoordinates, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm = kwargs['screen_manager']
        Clock.schedule_interval(self.refresh_grbl_label_values, self.GRBL_REPORT_INTERVAL)      # Poll for status
#         Clock.schedule_interval(self.refresh_ip_label_value, self.IP_REPORT_INTERVAL)      # Poll for status

#     def on_enter(self):
#         self.refresh_ip_label_value()


    def refresh_grbl_label_values(self, dt):
        if self.m.is_connected():
#             self.serial_image.source = "./asmcnc/skavaUI/img/serial_on.png"
#             self.grbl_status_label.text = self.m.state()
            self.grbl_xm_label.text = 'mX:\n' + str(round(self.m.mpos_x(), 2))
            self.grbl_ym_label.text = 'mY:\n' + str(round(self.m.mpos_y(), 2))
            self.grbl_zm_label.text = 'mZ:\n' + str(round(self.m.mpos_z(), 2))
            self.grbl_xw_label.text = 'wX:\n' + str(round(self.m.wpos_x(), 2))
            self.grbl_yw_label.text = 'wY:\n' + str(round(self.m.wpos_y(), 2))
            self.grbl_zw_label.text = 'wZ:\n' + str(round(self.m.wpos_z(), 2))

#         else:
#             self.serial_image.source = "./asmcnc/skavaUI/img/serial_off.png"

#     def refresh_ip_label_value(self, dt):
# 
#         ip_address = ''
#         self.wifi_image.source = "./asmcnc/skavaUI/img/wifi_off.png"
# 
# 
#         if sys.platform == "win32":
#             try:
#                 hostname=socket.gethostname()
#                 IPAddr=socket.gethostbyname(hostname)
#                 ip_address = str(IPAddr)
#                 self.wifi_image.source = "./asmcnc/skavaUI/img/wifi_on.png"
#             except:
#                 ip_address = ''
#                 self.wifi_image.source = "./asmcnc/skavaUI/img/wifi_off.png"
#         else:
#             try:
#                 f = os.popen('hostname -I')
#                 first_info = f.read().strip().split(' ')[0]
#                 if len(first_info.split('.')) == 4:
#                     ip_address = first_info
#                     self.wifi_image.source = "./asmcnc/skavaUI/img/wifi_on.png"
#                 else:
#                     ip_address = ''
#                     self.wifi_image.source = "./asmcnc/skavaUI/img/wifi_off.png"
#             except:
#                 ip_address = ''
#                 self.wifi_image.source = "./asmcnc/skavaUI/img/wifi_off.png"
# 
#         self.ip_status_label.text = ip_address
