'''
Created on 19 March 2020
Wifi screen

@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.clock import Clock
import socket, sys, os
from kivy.properties import StringProperty, ObjectProperty

from asmcnc.skavaUI import popup_info

Builder.load_string("""

#:import Factory kivy.factory.Factory


<NetworkSpinner@SpinnerOption>

    background_normal: ''
    background_color: [1,1,1,1]
    height: dp(40)
    color: 0,0,0,1
    halign: 'left'
    markup: 'True'

<WifiScreen>:
    
    network_name: network_name
    _password: _password
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
                    padding: [10,0,20,20]   
                    
                    BoxLayout: 
                        size_hint: (None, None) 
                        orientation: "horizontal"
                        width: dp(210)
                        height: dp(40)
                        BoxLayout: 
                            size_hint: (None, None) 
                            orientation: "vertical"
                            width: dp(151)
                            height: dp(40)
                            Label:
                                width: dp(151)
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
                            size_hint: (None, None) 
                            orientation: "vertical"
                            width: dp(39)
                            height: dp(40)
                            Button:
                                size_hint: (None,None)
                                height: dp(40)
                                width: dp(39)
                                background_color: hex('#F4433600')
                                center: self.parent.center
                                pos: self.parent.pos
                                on_press: root.refresh_available_networks()
                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        source: "./asmcnc/apps/wifi_app/img/mini_refresh.png"
                                        center_x: self.parent.center_x
                                        y: self.parent.y
                                        size: self.parent.width, self.parent.height
                                        allow_stretch: True


                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(40)
                        width: dp(210)
                        padding: (0,0,0,0)
                        canvas:
                            Color:
                                rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
                            Rectangle:
                                pos: self.pos
                                size: self.size
                        Spinner:
                            id: network_name
                            halign: 'left'
                            size_hint: (None, None)
                            size: 210, 40
                            text: ''
                            font_size: '20sp'
                            color: 0,0,0,1
                            values: root.SSID_list
                            option_cls: Factory.get("NetworkSpinner")
                            background_normal: ''
                            background_color: [1,1,1,1]

                        # TextInput: 
                        #     id: network_name
                        #     valign: 'middle'
                        #     halign: 'center'
                        #     text_size: self.size
                        #     font_size: '20sp'
                        #     markup: True
                        #     multiline: False
                        #     text: ''

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
                            id: _password
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
                            background_color: [1,1,1,1]
                            option_cls: Factory.get("NetworkSpinner")

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
                        on_press: root.check_credentials()
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

    network_name = ObjectProperty()
    _password = ObjectProperty()
    country = ObjectProperty()
    SSID_list = []

    def __init__(self, **kwargs):
        super(WifiScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        Clock.schedule_interval(self.refresh_ip_label_value, self.IP_REPORT_INTERVAL)

        if sys.platform != 'win32' and sys.platform != 'darwin':
            self.network_name.values = self.get_available_networks()
 
    def on_enter(self):
        self.refresh_ip_label_value(1)
        # self.refresh_networks_event = Clock.schedule_interval(self.refresh_available_networks, 1)
        if sys.platform != 'win32' and sys.platform != 'darwin':
            try: self.network_name.text = ((str((os.popen('grep "ssid" /etc/wpa_supplicant/wpa_supplicant.conf').read())).split("=")[1]).strip('\n')).strip('"')
            except: self.network_name.text = ''
            try: self.country.text = ((str((os.popen('grep "country" /etc/wpa_supplicant/wpa_supplicant.conf').read())).split("=")[1]).strip('\n')).strip('"')
            except: self.country.text = 'GB'
        self._password.text = ''


    def check_credentials(self):

        # get network name and password from text entered (widget)
        self.netname = self.network_name.text
        self.password = self._password.text

        if len(self.netname) < 1: 

            message = "Please enter a valid network name."
            popup_info.PopupWarning(self.sm, message)

        elif (len(self.password) < 8 or len(self.password) > 63): 

            message = "Please enter a password between 8 and 63 characters."
            popup_info.PopupWarning(self.sm, message)

        else: 
            self.connect_wifi()

    def connect_wifi(self):
        popup_info.PopupWait(self.sm)

        # pass credentials to wpa_supplicant file
        self.wpanetpass = 'wpa_passphrase "' + self.netname + '" "' + self.password + '" 2>/dev/null | sudo tee /etc/wpa_supplicant/wpa_supplicant.conf'
        self.wpanetpasswlan0 = 'wpa_passphrase "' + self.netname + '" "' + self.password + '" 2>/dev/null | sudo tee /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'

        # put the credentials and the necessary appendages into the wpa file
        try: 
            os.system(self.wpanetpass)
            os.system('echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf')
            os.system('echo "country="' + self.country.text + '| sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf')
            os.system('echo "update_config=1" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf')


            os.system(self.wpanetpasswlan0)
            os.system('echo "ctrl_interface=run/wpa_supplicant" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf')
            os.system('echo "update_config=1" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf')
            os.system('echo "country="' + self.country.text + '| sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf')

        except: 
            try: 
                self.wpanetpass = 'wpa_passphrase "' + self.netname + '" "invalidPassword" 2>/dev/null | sudo tee /etc/wpa_supplicant/wpa_supplicant.conf'
                os.system(self.wpanetpass)
                os.system('echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf')
                os.system('echo "country="' + self.country.text + '| sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf')
                os.system('echo "update_config=1" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf')

                self.wpanetpasswlan0 = 'wpa_passphrase "' + self.netname + '" "invalidPassword" 2>/dev/null | sudo tee /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
                os.system(self.wpanetpasswlan0)
                os.system('echo "ctrl_interface=run/wpa_supplicant" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf')
                os.system('echo "update_config=1" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf')
                os.system('echo "country="' + self.country.text + '| sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf')

            except:
                self.wpanetpass = 'wpa_passphrase "" "" 2>/dev/null | sudo tee /etc/wpa_supplicant/wpa_supplicant.conf'
                os.system(self.wpanetpass)
                os.system('echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf')
                os.system('echo "country="' + self.country.text + '| sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf')
                os.system('echo "update_config=1" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf')

                self.wpanetpasswlan0 = 'wpa_passphrase "" "" 2>/dev/null | sudo tee /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
                os.system(self.wpanetpasswlan0)
                os.system('echo "ctrl_interface=run/wpa_supplicant" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf')
                os.system('echo "update_config=1" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf')
                os.system('echo "country="' + self.country.text + '| sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf')


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
    
    def get_available_networks(self):
        raw_SSID_list = os.popen('sudo iw dev wlan0 scan | grep SSID').read()
        SSID_list = raw_SSID_list.replace('\tSSID: ','').strip().split('\n')
        if '' in SSID_list: SSID_list.remove('')
        return SSID_list

    def refresh_available_networks(self):
        wait_popup = popup_info.PopupWait(self.sm)
        Clock.schedule_once(lambda dt: wait_popup.popup.dismiss(), 0.5)

        def get_networks():
            self.network_name.values = self.get_available_networks()

        Clock.schedule_once(lambda dt: get_networks(), 0.2)        
        

    values = ['GB' , 'US' , 'AF' , 'AX' , 'AL' , 'DZ' , 'AS' , 'AD' , 'AO' , 'AI' , 'AQ' , 'AG' , 'AR' , 'AM' , 'AW' , 'AU' , 'AT' , 'AZ' , 'BH' , 'BS' , 'BD' , 'BB' , 'BY' , 'BE' , 'BZ' , 'BJ' , 'BM' , 'BT' , 'BO' , 'BQ' , 'BA' , 'BW' , 'BV' , 'BR' , 'IO' , 'BN' , 'BG' , 'BF' , 'BI' , 'KH' , 'CM' , 'CA' , 'CV' , 'KY' , 'CF' , 'TD' , 'CL' , 'CN' , 'CX' , 'CC' , 'CO' , 'KM' , 'CG' , 'CD' , 'CK' , 'CR' , 'CI' , 'HR' , 'CU' , 'CW' , 'CY' , 'CZ' , 'DK' , 'DJ' , 'DM' , 'DO' , 'EC' , 'EG' , 'SV' , 'GQ' , 'ER' , 'EE' , 'ET' , 'FK' , 'FO' , 'FJ' , 'FI' , 'FR' , 'GF' , 'PF' , 'TF' , 'GA' , 'GM' , 'GE' , 'DE' , 'GH' , 'GI' , 'GR' , 'GL' , 'GD' , 'GP' , 'GU' , 'GT' , 'GG' , 'GN' , 'GW' , 'GY' , 'HT' , 'HM' , 'VA' , 'HN' , 'HK' , 'HU' , 'IS' , 'IN' , 'ID' , 'IR' , 'IQ' , 'IE' , 'IM' , 'IL' , 'IT' , 'JM' , 'JP' , 'JE' , 'JO' , 'KZ' , 'KE' , 'KI' , 'KP' , 'KR' , 'KW' , 'KG' , 'LA' , 'LV' , 'LB' , 'LS' , 'LR' , 'LY' , 'LI' , 'LT' , 'LU' , 'MO' , 'MK' , 'MG' , 'MW' , 'MY' , 'MV' , 'ML' , 'MT' , 'MH' , 'MQ' , 'MR' , 'MU' , 'YT' , 'MX' , 'FM' , 'MD' , 'MC' , 'MN' , 'ME' , 'MS' , 'MA' , 'MZ' , 'MM' , 'NA' , 'NR' , 'NP' , 'NL' , 'NC' , 'NZ' , 'NI' , 'NE' , 'NG' , 'NU' , 'NF' , 'MP' , 'NO' , 'OM' , 'PK' , 'PW' , 'PS' , 'PA' , 'PG' , 'PY' , 'PE' , 'PH' , 'PN' , 'PL' , 'PT' , 'PR' , 'QA' , 'RE' , 'RO' , 'RU' , 'RW' , 'BL' , 'SH' , 'KN' , 'LC' , 'MF' , 'PM' , 'VC' , 'WS' , 'SM' , 'ST' , 'SA' , 'SN' , 'RS' , 'SC' , 'SL' , 'SG' , 'SX' , 'SK' , 'SI' , 'SB' , 'SO' , 'ZA' , 'GS' , 'SS' , 'ES' , 'LK' , 'SD' , 'SR' , 'SJ' , 'SZ' , 'SE' , 'CH' , 'SY' , 'TW' , 'TJ' , 'TZ' , 'TH' , 'TL' , 'TG' , 'TK' , 'TO' , 'TT' , 'TN' , 'TR' , 'TM' , 'TC' , 'TV' , 'UG' , 'UA' , 'AE' , 'UM' , 'UY' , 'UZ' , 'VU' , 'VE' , 'VN' , 'VG' , 'VI' , 'WF' , 'EH' , 'YE' , 'ZM' , 'ZW']