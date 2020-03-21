'''
Created on 19 March 2020
Wifi screen

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
import socket, sys, os

Builder.load_string("""

<WifiScreen>:
    
    network_name: network_name
    password: password
    country: country
    ip_status_label: ip_status_label
    wifi_image: wifi_image
    
    BoxLayout:
        size_hint: (None, None)
        height: dp(480)
        width: dp(800)
        orientation: 'vertical'
        canvas:
            Color:
                rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
            Rectangle:
                pos: self.pos
                size: self.size
        
        BoxLayout:
            size_hint: (None, None)
            height: dp(190)
            width: dp(800)
            padding: [30, 30, 30, 20]
            spacing: 30
            orientation: 'horizontal'
            
            # Status indicator            
            BoxLayout: 
                size_hint: (None, None)
                height: dp(140)
                width: dp(150)
                orientation: 'vertical'
                padding: [0,35,0,10]
                spacing: 10
                canvas:
                    Color:
                        rgba: root.status_color
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(25)
                    width: dp(150)
                    Image:
                        id: wifi_image
                        source: "./asmcnc/skavaUI/img/wifi_on.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True                    

                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(60)
                    width: dp(150)
                    orientation: 'vertical'
                    Label:
                        color: 1,1,1,1
                        font_size: 18
                        markup: True
                        halign: "center"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                        text: "IP address:"
                    Label:
                        id: ip_status_label
                        color: 1,1,1,1
                        font_size: 18
                        markup: True
                        halign: "center"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                        text: ''
            # Text Entry Area
            BoxLayout: 
                size_hint: (None, None)
                height: dp(140)
                width: dp(560)
                padding: [10,20,10,20]
                spacing: 10
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                # SSID
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(100)
                    width: dp(220)
                    orientation: "vertical"
                    padding: [10,0,0,20]   
                              
                    Label:
                        color: 0,0,0,1
                        font_size: 20
                        markup: True
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                        text: "Network Name"

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(40)
                        width: dp(210)
                        padding: (0,0,0,0)
                                    
                        TextInput: 
                            id: network_name
                            valign: 'middle'
                            halign: 'center'
                            text_size: self.size
                            font_size: '20sp'
                            markup: True
                            multiline: False
                            text: ''

                #Password
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(100)
                    width: dp(210)
                    orientation: "vertical"
                    padding: [0,0,0,20]   
                              
                    Label:
                        color: 0,0,0,1
                        font_size: 20
                        markup: True
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                        text: "Password"

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(40)
                        width: dp(210)
                        padding: (0,0,0,0)
                                    
                        TextInput: 
                            id: password
                            valign: 'middle'
                            halign: 'center'
                            text_size: self.size
                            font_size: '20sp'
                            markup: True
                            multiline: False
                            text: ''                                           
                #Country Code
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(100)
                    width: dp(90)
                    orientation: 'vertical'
                    padding: [0,0,10,20]   
                              
                    Label:
                        color: 0,0,0,1
                        font_size: 20
                        markup: True
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                        text: "Country"

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(40)
                        width: dp(80)
                        padding: (0,0,0,0)
                        canvas:
                            Color:
                                rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
                            Rectangle:
                                pos: self.pos
                                size: self.size
                        Spinner:
                            id: country
                            size_hint: (None, None)
                            size: 80, 40
                            text: 'GB'
                            font_size: '20sp'
                            color: 0,0,0,1
                            values: root.values
                            background_normal: ''

#                         TextInput: 
#                             id: country
#                             valign: 'middle'
#                             halign: 'center'
#                             text_size: self.size
#                             font_size: '20sp'
#                             markup: True
#                             input_filter: 'float'
#                             multiline: False
#                             text: '' 
        BoxLayout:
            size_hint: (None, None)
            height: dp(290)
            width: dp(800)
            padding: [30,0,30,30]
            spacing: 10
            
            # Doc viewer
            BoxLayout: 
                size_hint: (None, None)
                height: dp(260)
                width: dp(570)
                padding: 20
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        
                ScrollView:
                    size: self.size
                    pos: self.pos
                    do_scroll_x: True
                    do_scroll_y: True
                    scroll_type: ['content']
                    RstDocument:
                        source: './asmcnc/apps/wifi_app/wifi_documentation.rst'
                        background_color: hex('#FFFFFF')
                        base_font_size: 26
                        underline_color: '000000'
                                                                                   
            BoxLayout: 
                size_hint: (None, None)
                height: dp(260)
                width: dp(160)
                orientation: 'vertical'
                spacing: 30
                canvas:
                    Color:
                        rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(115)
                    width: dp(160)
                    padding: [2,0,0,0]                   
                    Button:
                        size_hint: (None,None)
                        height: dp(115)
                        width: dp(158)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.connect_wifi()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/wifi_app/img/connect.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(112)
                    width: dp(160)
                    padding: [28,0,20,0]   
                    Button:
                        size_hint: (None,None)
                        height: dp(112)
                        width: dp(112)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.quit_to_lobby()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/wifi_app/img/quit.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
""")

class WifiScreen(Screen):
    
    IP_REPORT_INTERVAL = 2
    status_color = [76 / 255., 175 / 255., 80 / 255., 1.]
    
    def __init__(self, **kwargs):
        super(WifiScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        Clock.schedule_interval(self.refresh_ip_label_value, self.IP_REPORT_INTERVAL)
 
    def on_pre_enter(self):
        if sys.platform != 'win32':
            print (str(os.system('grep "ssid" /etc/wpa_supplicant/wpa_supplicant.conf'))).split('=')
            
#             self.network_name.text = (str(os.system('grep "ssid" /etc/wpa_supplicant/wpa_supplicant.conf'))).split('=')[1]
#             self.country.text = (str(os.system('grep "country" /etc/wpa_supplicant/wpa_supplicant.conf'))).split('=')[1]
#         
    def on_enter(self):
        self.refresh_ip_label_value(1)
                    
    def connect_wifi(self):

        # get network name and password from text entered (widget)
        self.netname = self.network_name.text
        self.password = self.password.text
        self.country = self.country.text 

        # pass credentials to wpa_supplicant file
        self.wpanetpass = 'wpa_passphrase "' + self.netname + '" "' + self.password + '" 2>/dev/null | sudo tee /etc/wpa_supplicant/wpa_supplicant.conf'
        self.wpanetpasswlan0 = 'wpa_passphrase "' + self.netname + '" "' + self.password + '" 2>/dev/null | sudo tee /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
        
        #if wpanetpass.startswith('network={'):       

        # put the credentials and the necessary appendages into the wpa file
        os.system(self.wpanetpass)
        os.system('echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf')
        os.system('echo "country="' + self.country + '| sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf')
        os.system('echo "update_config=1" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf')
   
        os.system(self.wpanetpasswlan0)
        os.system('echo "ctrl_interface=run/wpa_supplicant" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf')
        os.system('echo "update_config=1" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf')
        os.system('echo "country="' + self.country + '| sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf')

        self.sm.current = 'rebooting'        

    def refresh_ip_label_value(self, dt):

        ip_address = ''
        self.wifi_image.source = "./asmcnc/skavaUI/img/wifi_off.png"
        self.status_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        if sys.platform == "win32":
            try:
                hostname=socket.gethostname()
                IPAddr=socket.gethostbyname(hostname)
                ip_address = str(IPAddr)
                self.wifi_image.source = "./asmcnc/skavaUI/img/wifi_on.png"
                self.status_color = [76 / 255., 175 / 255., 80 / 255., 1.]
            except:
                ip_address = ''
                self.wifi_image.source = "./asmcnc/skavaUI/img/wifi_off.png"
                self.status_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        else:
            try:
                f = os.popen('hostname -I')
                first_info = f.read().strip().split(' ')[0]
                if len(first_info.split('.')) == 4:
                    ip_address = first_info
                    self.wifi_image.source = "./asmcnc/skavaUI/img/wifi_on.png"
                    self.status_color = [76 / 255., 175 / 255., 80 / 255., 1.]
                else:
                    ip_address = ''
                    self.wifi_image.source = "./asmcnc/skavaUI/img/wifi_off.png"
                    self.status_color = [230 / 255., 74 / 255., 25 / 255., 1.]
            except:
                ip_address = ''
                self.wifi_image.source = "./asmcnc/skavaUI/img/wifi_off.png"
                self.status_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        self.ip_status_label.text = ip_address

    def quit_to_lobby(self):
        self.sm.current = 'lobby'
        
    
    values = ['GB' , 'US' , 'AF' , 'AX' , 'AL' , 'DZ' , 'AS' , 'AD' , 'AO' , 'AI' , 'AQ' , 'AG' , 'AR' , 'AM' , 'AW' , 'AU' , 'AT' , 'AZ' , 'BH' , 'BS' , 'BD' , 'BB' , 'BY' , 'BE' , 'BZ' , 'BJ' , 'BM' , 'BT' , 'BO' , 'BQ' , 'BA' , 'BW' , 'BV' , 'BR' , 'IO' , 'BN' , 'BG' , 'BF' , 'BI' , 'KH' , 'CM' , 'CA' , 'CV' , 'KY' , 'CF' , 'TD' , 'CL' , 'CN' , 'CX' , 'CC' , 'CO' , 'KM' , 'CG' , 'CD' , 'CK' , 'CR' , 'CI' , 'HR' , 'CU' , 'CW' , 'CY' , 'CZ' , 'DK' , 'DJ' , 'DM' , 'DO' , 'EC' , 'EG' , 'SV' , 'GQ' , 'ER' , 'EE' , 'ET' , 'FK' , 'FO' , 'FJ' , 'FI' , 'FR' , 'GF' , 'PF' , 'TF' , 'GA' , 'GM' , 'GE' , 'DE' , 'GH' , 'GI' , 'GR' , 'GL' , 'GD' , 'GP' , 'GU' , 'GT' , 'GG' , 'GN' , 'GW' , 'GY' , 'HT' , 'HM' , 'VA' , 'HN' , 'HK' , 'HU' , 'IS' , 'IN' , 'ID' , 'IR' , 'IQ' , 'IE' , 'IM' , 'IL' , 'IT' , 'JM' , 'JP' , 'JE' , 'JO' , 'KZ' , 'KE' , 'KI' , 'KP' , 'KR' , 'KW' , 'KG' , 'LA' , 'LV' , 'LB' , 'LS' , 'LR' , 'LY' , 'LI' , 'LT' , 'LU' , 'MO' , 'MK' , 'MG' , 'MW' , 'MY' , 'MV' , 'ML' , 'MT' , 'MH' , 'MQ' , 'MR' , 'MU' , 'YT' , 'MX' , 'FM' , 'MD' , 'MC' , 'MN' , 'ME' , 'MS' , 'MA' , 'MZ' , 'MM' , 'NA' , 'NR' , 'NP' , 'NL' , 'NC' , 'NZ' , 'NI' , 'NE' , 'NG' , 'NU' , 'NF' , 'MP' , 'NO' , 'OM' , 'PK' , 'PW' , 'PS' , 'PA' , 'PG' , 'PY' , 'PE' , 'PH' , 'PN' , 'PL' , 'PT' , 'PR' , 'QA' , 'RE' , 'RO' , 'RU' , 'RW' , 'BL' , 'SH' , 'KN' , 'LC' , 'MF' , 'PM' , 'VC' , 'WS' , 'SM' , 'ST' , 'SA' , 'SN' , 'RS' , 'SC' , 'SL' , 'SG' , 'SX' , 'SK' , 'SI' , 'SB' , 'SO' , 'ZA' , 'GS' , 'SS' , 'ES' , 'LK' , 'SD' , 'SR' , 'SJ' , 'SZ' , 'SE' , 'CH' , 'SY' , 'TW' , 'TJ' , 'TZ' , 'TH' , 'TL' , 'TG' , 'TK' , 'TO' , 'TT' , 'TN' , 'TR' , 'TM' , 'TC' , 'TV' , 'UG' , 'UA' , 'AE' , 'UM' , 'UY' , 'UZ' , 'VU' , 'VE' , 'VN' , 'VG' , 'VI' , 'WF' , 'EH' , 'YE' , 'ZM' , 'ZW']