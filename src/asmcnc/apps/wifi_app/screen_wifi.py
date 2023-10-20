"""
Created on 19 March 2020
Wifi screen

@author: Letty
"""
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.clock import Clock
import socket, sys, os
from kivy.properties import StringProperty, ObjectProperty
from asmcnc.skavaUI import popup_info
Builder.load_string(
    """

#:import Factory kivy.factory.Factory


<NetworkSpinner@SpinnerOption>

    background_normal: ''
    background_color: [1,1,1,1]
    height: dp(0.0833333333333*app.height)
    color: 0,0,0,1
    halign: 'left'
    markup: 'True'

<WifiScreen>:
    
    network_name: network_name
    _password: _password
    country: country
    ip_status_label: ip_status_label
    wifi_image: wifi_image

    ip_address_label : ip_address_label
    network_name_label : network_name_label
    password_label : password_label
    country_label : country_label
    connect_button : connect_button
    custom_ssid_button:custom_ssid_button
    network_name_input:network_name_input
    custom_network_name:custom_network_name
    custom_network_name_box:custom_network_name_box
    network_name_box:network_name_box

    connection_instructions_rst : connection_instructions_rst
    
    on_touch_down: root.on_touch()
    
    BoxLayout:
        size_hint: (None, None)
        height: dp(1.0*app.height)
        width: dp(1.0*app.width)
        orientation: 'vertical'
        canvas:
            Color:
                rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
            Rectangle:
                pos: self.pos
                size: self.size
        
        BoxLayout:
            size_hint: (None, None)
            height: dp(0.395833333333*app.height)
            width: dp(1.0*app.width)
            padding:[0.0375*app.width, 0.0625*app.height, 0.0375*app.width, 0.0416666666667*app.height]
            spacing: 0.0375*app.width
            orientation: 'horizontal'
            
            # Status indicator            
            BoxLayout: 
                size_hint: (None, None)
                height: dp(0.291666666667*app.height)
                width: dp(0.1875*app.width)
                orientation: 'vertical'
                padding:[0,0.0729166666667*app.height,0,0.0208333333333*app.height]
                spacing: 0.0208333333333*app.height
                canvas:
                    Color:
                        rgba: root.status_color
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(0.0520833333333*app.height)
                    width: dp(0.1875*app.width)
                    Image:
                        id: wifi_image
                        source: "./asmcnc/skavaUI/img/wifi_on.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True                    

                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(0.125*app.height)
                    width: dp(0.1875*app.width)
                    orientation: 'vertical'
                    Label:
                        id: ip_address_label
                        color: 1,1,1,1
                        font_size: 0.0225*app.width
                        markup: True
                        halign: "center"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos

                    Label:
                        id: ip_status_label
                        color: 1,1,1,1
                        font_size: 0.0225*app.width
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
                height: dp(0.291666666667*app.height)
                width: dp(0.7*app.width)
                padding:[0.0125*app.width,0.0416666666667*app.height,0.0125*app.width,0.0625*app.height]
                spacing: 0.0125*app.width
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                # SSID
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(0.208333333333*app.height)
                    width: dp(0.275*app.width)
                    orientation: "vertical"
                    padding:[0.0125*app.width,0,0.025*app.width,-0.0416666666667*app.height]
                    
                    BoxLayout: 
                        size_hint: (None, None) 
                        orientation: "horizontal"
                        width: dp(0.2625*app.width)
                        height: dp(0.0833333333333*app.height)
                        BoxLayout: 
                            size_hint: (None, None) 
                            orientation: "vertical"
                            width: dp(0.18875*app.width)
                            height: dp(0.0833333333333*app.height)
                            Label:
                                id: network_name_label
                                width: dp(0.18875*app.width)
                                color: 0,0,0,1
                                font_size: 0.025*app.width
                                markup: True
                                halign: "left"
                                valign: "middle"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos

                        BoxLayout: 
                            size_hint: (None, None) 
                            orientation: "vertical"
                            width: dp(0.04875*app.width)
                            height: dp(0.0833333333333*app.height)
                            padding:[0.00625*app.width,0.0104166666667*app.height,0.00625*app.width,0.0104166666667*app.height]
                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                size_hint: (None,None)
                                height: dp(0.0625*app.height)
                                width: dp(0.03625*app.width)
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
                        height: dp(0.0833333333333*app.height)
                        width: dp(0.2625*app.width)
                        padding:[0,0,0,0]
                        orientation: 'horizontal'
                        id: network_name_input
                        
                        # The Spinner with the background image, grouped together in this BoxLayout
                        BoxLayout:
                            size_hint: (None,None)
                            height: dp(0.0833333333333*app.height)
                            width: dp(0.2625*app.width)
                            padding:(0.00625*app.width,0.0104166666667*app.height,0.00625*app.width,0.0166666666667*app.height)
                            id: network_name_box
                            
                            canvas:
                                Rectangle:
                                    pos: self.pos
                                    size: self.size
                                    source: "./asmcnc/apps/wifi_app/img/network_spinner_bg.png"
    
                            Spinner:
                                id: network_name
                                halign: 'left'
                                valign: 'top'
                                markup: True
                                size_hint: (None, None)
                                size: 200, 24
                                text: ''
                                font_size: str(0.025*app.width) + 'sp'
                                text_size: self.size
                                multiline: False
                                color: 0,0,0,1
                                values: root.SSID_list
                                option_cls: Factory.get("NetworkSpinner")
                                background_normal: ''
                                background_color: [1,1,1,0]
                        
                        # The TextInput for the custom network name, very similar to the Password BoxLayout
                        BoxLayout:
                            size_hint: (None,None)
                            height: dp(0.0833333333333*app.height)
                            width: dp(0.2625*app.width)
                            padding:(0,0,0,0)
                            id: custom_network_name_box
                            
                            TextInput: 
                                id: custom_network_name
                                # valign: 'middle'
                                padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
                                halign: 'center'
                                text_size: self.size
                                font_size: str(0.025*app.width) + 'sp'
                                markup: True
                                multiline: False
                                text: ''
                                background_normal: "./asmcnc/apps/wifi_app/img/password_bg.png"
                    
                    # The button to toggle between the normal network name and the custom network name
                    BoxLayout: 
                        size_hint: (None, None) 
                        orientation: "horizontal"
                        width: dp(0.2625*app.width)
                        height: dp(0.0833333333333*app.height)
                        padding:[0,0.0104166666667*app.height,0,0.0104166666667*app.height]
                        ToggleButton:
                            id: custom_ssid_button
                            on_release: root.custom_ssid_input()
                            font_size: 0.025*app.width
                            color: hex('#f9f9f9ff')
                            markup: True
                            background_normal: "./asmcnc/apps/wifi_app/img/CustomSSID_blank.png"
                            background_down: "./asmcnc/apps/wifi_app/img/CustomSSID_blank.png"

                #Password
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(0.208333333333*app.height)
                    width: dp(0.2625*app.width)
                    orientation: "vertical"
                    padding:[0,0,0,0.0416666666667*app.height]
                              
                    Label:
                        id: password_label
                        color: 0,0,0,1
                        font_size: 0.025*app.width
                        markup: True
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(0.0833333333333*app.height)
                        width: dp(0.2625*app.width)
                        padding:(0,0,0,0)
                                    
                        TextInput: 
                            id: _password
                            valign: 'middle'
                            halign: 'center'
                            text_size: self.size
                            font_size: str(0.025*app.width) + 'sp'
                            markup: True
                            multiline: False
                            text: ''
                            background_normal: "./asmcnc/apps/wifi_app/img/password_bg.png"

                #Country Code
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(0.208333333333*app.height)
                    width: dp(0.1125*app.width)
                    orientation: 'vertical'
                    padding:[0,0,0.0125*app.width,0.0416666666667*app.height]
                              
                    Label:
                        id: country_label
                        color: 0,0,0,1
                        font_size: 0.025*app.width
                        markup: True
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(0.0833333333333*app.height)
                        width: dp(0.1*app.width)
                        padding:(0.025*app.width,0,0.00625*app.width,0)
                        orientation: 'horizontal'
                        canvas:
                            Rectangle:
                                pos: self.pos
                                size: self.size
                                source: "./asmcnc/apps/wifi_app/img/country_spinner_bg.png"
                        Spinner:
                            id: country
                            size_hint: (None, None)
                            halign: 'left'
                            valign: 'middle'
                            markup: True
                            size: 55, 40
                            text: 'GB'
                            font_size: str(0.025*app.width) + 'sp'
                            text_size: self.size
                            color: 0,0,0,1
                            values: root.values
                            background_color: [1,1,1,0]
                            option_cls: Factory.get("NetworkSpinner")

        BoxLayout:
            size_hint: (None, None)
            height: dp(0.604166666667*app.height)
            width: dp(1.0*app.width)
            padding:[0.0375*app.width,0,0.0375*app.width,0.0625*app.height]
            spacing: 0.0125*app.width
            
            # Doc viewer
            BoxLayout: 
                size_hint: (None, None)
                height: dp(0.541666666667*app.height)
                width: dp(0.7125*app.width)
                padding: [0.025*app.width, 0.0416666666667*app.height]
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
                        id: connection_instructions_rst
                        background_color: hex('#FFFFFF')
                        base_font_size: 26
                        underline_color: '000000'
                                                                                   
            BoxLayout: 
                size_hint: (None, None)
                height: dp(0.541666666667*app.height)
                width: dp(0.2*app.width)
                orientation: 'vertical'
                spacing: 0.0625*app.height
                canvas:
                    Color:
                        rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(0.239583333333*app.height)
                    width: dp(0.2*app.width)
                    padding:[0.0025*app.width,0,0,0]
                    canvas:
                        Color:
                            rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size

                    Button:
                        id: connect_button
                        background_normal: "./asmcnc/apps/wifi_app/img/connect_blank.png"
                        background_down: "./asmcnc/apps/wifi_app/img/connect_blank.png"
                        border: [dp(14.5)]*4
                        size_hint: (None,None)
                        height: dp(0.239583333333*app.height)
                        width: dp(0.1975*app.width)
                        on_press: root.check_credentials()
                        # text: 'Connect'
                        font_size: str(0.035*app.width) + 'sp'
                        color: hex('#f9f9f9ff')
                        markup: True
                        center: self.parent.center
                        pos: self.parent.pos
                        opacity: 1 if self.state == 'normal' else .5

                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(0.233333333333*app.height)
                    width: dp(0.2*app.width)
                    padding:[0.035*app.width,0,0.025*app.width,0]
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint: (None,None)
                        height: dp(0.233333333333*app.height)
                        width: dp(0.14*app.width)
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
"""
    )


class WifiScreen(Screen):
    default_font_size = 20
    IP_REPORT_INTERVAL = 2
    status_color = [76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0]
    network_name = ObjectProperty()
    _password = ObjectProperty()
    country = ObjectProperty()
    SSID_list = []
    wifi_documentation_path = './asmcnc/apps/wifi_app/wifi_documentation/'
    wifi_on = './asmcnc/skavaUI/img/wifi_on.png'
    wifi_off = './asmcnc/skavaUI/img/wifi_off.png'
    wifi_warning = './asmcnc/skavaUI/img/wifi_warning.png'
    dismiss_wait_popup_event = None
    wifi_error_timeout_event = None
    refresh_ip_label_value_event = None

    def __init__(self, **kwargs):
        super(WifiScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.set = kwargs['settings_manager']
        self.l = kwargs['localization']
        self.kb = kwargs['keyboard']
        if sys.platform != 'win32' and sys.platform != 'darwin':
            self.network_name.values = self.get_available_networks()
        self.update_strings()
        self.get_rst_source()
        self.refs = [self.network_name.__self__, self.
            custom_network_name_box.__self__]
        self.network_name_input.remove_widget(self.custom_network_name_box)
        self.text_inputs = [self._password, self.custom_network_name]

    def custom_ssid_input(self):
        if self.custom_ssid_button.state == 'normal':
            try:
                self.network_name_input.remove_widget(self.
                    custom_network_name_box)
                self.network_name_input.add_widget(self.network_name_box)
            except:
                pass
            self.custom_ssid_button.text = self.l.get_str('Other network')
        else:
            try:
                self.network_name_input.remove_widget(self.network_name_box)
                self.network_name_input.add_widget(self.custom_network_name_box
                    )
                self.custom_network_name.focus = True
            except:
                pass
            self.custom_ssid_button.text = self.l.get_str('Select network')

    def on_enter(self):
        self.kb.setup_text_inputs(self.text_inputs)
        self.refresh_ip_label_value_event = Clock.schedule_interval(self.
            refresh_ip_label_value, self.IP_REPORT_INTERVAL)
        self.refresh_ip_label_value(1)
        if sys.platform != 'win32' and sys.platform != 'darwin':
            if self.is_wlan0_connected():
                try:
                    self.network_name.text = str(os.popen(
                        'grep "ssid" /etc/wpa_supplicant/wpa_supplicant.conf'
                        ).read()).split('=')[1].strip('\n').strip('"')
                except:
                    self.network_name.text = ''
            else:
                self.network_name.text = ''
                wifi_connected_before = os.popen(
                    'grep "wifi_connected_before" /home/pi/easycut-smartbench/src/config.txt'
                    ).read()
                if 'True' in wifi_connected_before:
                    message = self.l.get_str('No network connection.'
                        ) + '\n' + self.l.get_str(
                        'Please refresh the list and try again.')
                    popup_info.PopupWarning(self.sm, self.l, message)
            try:
                self.country.text = str(os.popen(
                    'grep "country" /etc/wpa_supplicant/wpa_supplicant.conf'
                    ).read()).split('=')[1].strip('\n').strip('"')
            except:
                self.country.text = 'GB'
        self._password.text = ''
        self.update_strings()

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def check_credentials(self):
        if self.custom_ssid_button.state == 'normal':
            self.netname = self.network_name.text
        else:
            self.netname = self.custom_network_name.text
        self.password = self._password.text
        if len(self.netname) < 1:
            message = self.l.get_str('Please enter a valid network name.')
            popup_info.PopupWarning(self.sm, self.l, message)
        elif len(self.password) < 8 or len(self.password) > 63:
            message = self.l.get_str(
                'Please enter a password between 8 and 63 characters.')
            popup_info.PopupWarning(self.sm, self.l, message)
        else:
            self.connect_wifi()

    def is_wlan0_connected(self):
        state_raw = os.popen(
            'ip addr show | grep "wlan0" | grep -oP "state\\s\\w+"').read()
        state = state_raw.split(' ')[1].strip('\n')
        return state == 'UP'

    def connect_wifi(self):
        self._password.text = ''
        wait_popup = popup_info.PopupWait(self.sm, self.l)
        self.wpanetpass = ('wpa_passphrase "' + self.netname + '" "' + self
            .password +
            '" 2>/dev/null | sudo tee /etc/wpa_supplicant/wpa_supplicant.conf')
        self.wpanetpasswlan0 = ('wpa_passphrase "' + self.netname + '" "' +
            self.password +
            '" 2>/dev/null | sudo tee /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
            )
        try:
            os.system(self.wpanetpass)
            os.system(
                'echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf'
                )
            os.system('echo "country="' + self.country.text +
                '| sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf')
            os.system(
                'echo "update_config=1" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf'
                )
            os.system(self.wpanetpasswlan0)
            os.system(
                'echo "ctrl_interface=run/wpa_supplicant" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
                )
            os.system(
                'echo "update_config=1" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
                )
            os.system('echo "country="' + self.country.text +
                '| sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
                )
        except:
            try:
                self.wpanetpass = ('wpa_passphrase "' + self.netname +
                    '" "invalidPassword" 2>/dev/null | sudo tee /etc/wpa_supplicant/wpa_supplicant.conf'
                    )
                os.system(self.wpanetpass)
                os.system(
                    'echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf'
                    )
                os.system('echo "country="' + self.country.text +
                    '| sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf'
                    )
                os.system(
                    'echo "update_config=1" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf'
                    )
                self.wpanetpasswlan0 = ('wpa_passphrase "' + self.netname +
                    '" "invalidPassword" 2>/dev/null | sudo tee /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
                    )
                os.system(self.wpanetpasswlan0)
                os.system(
                    'echo "ctrl_interface=run/wpa_supplicant" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
                    )
                os.system(
                    'echo "update_config=1" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
                    )
                os.system('echo "country="' + self.country.text +
                    '| sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
                    )
            except:
                self.wpanetpass = (
                    'wpa_passphrase "" "" 2>/dev/null | sudo tee /etc/wpa_supplicant/wpa_supplicant.conf'
                    )
                os.system(self.wpanetpass)
                os.system(
                    'echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf'
                    )
                os.system('echo "country="' + self.country.text +
                    '| sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf'
                    )
                os.system(
                    'echo "update_config=1" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant.conf'
                    )
                self.wpanetpasswlan0 = (
                    'wpa_passphrase "" "" 2>/dev/null | sudo tee /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
                    )
                os.system(self.wpanetpasswlan0)
                os.system(
                    'echo "ctrl_interface=run/wpa_supplicant" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
                    )
                os.system(
                    'echo "update_config=1" | sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
                    )
                os.system('echo "country="' + self.country.text +
                    '| sudo tee --append /etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
                    )
        os.system(
            'sudo sed -i "s/wifi_connected_before=False/wifi_connected_before=True/" config.txt'
            )
        os.system('sudo ip addr flush dev wlan0')
        os.system('sudo wpa_cli -i wlan0 reconfigure')
        os.system('sudo systemctl restart dhcpcd')

        def dismiss_wait_popup(dt):
            if self.set.wifi_available:
                if self.wifi_error_timeout_event:
                    Clock.unschedule(self.wifi_error_timeout_event)
                try:
                    wait_popup.popup.dismiss()
                except:
                    pass
                return
            self.dismiss_wait_popup_event = Clock.schedule_once(
                dismiss_wait_popup, 0.5)

        def wifi_error_timeout(dt):
            if not self.set.wifi_available:
                if self.dismiss_wait_popup_event:
                    Clock.unschedule(self.dismiss_wait_popup_event)
                try:
                    wait_popup.popup.dismiss()
                except:
                    pass
                message = self.l.get_str('No WiFi connection!')
                popup_info.PopupWarning(self.sm, self.l, message)
        self.dismiss_wait_popup_event = Clock.schedule_once(dismiss_wait_popup,
            5)
        self.wifi_error_timeout_event = Clock.schedule_once(wifi_error_timeout,
            30)

    def refresh_ip_label_value(self, dt):
        self.ip_status_label.text = self.set.ip_address
        if self.set.wifi_available:
            self.wifi_image.source = self.wifi_on
            self.status_color = [76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0]
        elif not self.set.ip_address:
            self.wifi_image.source = self.wifi_off
            self.status_color = [230 / 255.0, 74 / 255.0, 25 / 255.0, 1.0]
        else:
            self.wifi_image.source = self.wifi_warning
            self.status_color = [230 / 255.0, 74 / 255.0, 25 / 255.0, 1.0]

    def quit_to_lobby(self):
        self.sm.current = 'lobby'

    def get_available_networks(self):
        raw_SSID_list = os.popen(
            'sudo iwlist wlan0 scan | grep "ESSID:" | sed "s/ESSID://g" | sed "s/^[ \t]*//g"'
            ).read()
        SSID_list = raw_SSID_list.replace('"', '').strip().split('\n')
        if '' in SSID_list:
            SSID_list.remove('')
        SSID_list = {x for x in SSID_list if not set(x) <= set('\\x00')}
        return SSID_list

    def refresh_available_networks(self):
        wait_popup = popup_info.PopupWait(self.sm, self.l)
        Clock.schedule_once(lambda dt: wait_popup.popup.dismiss(), 0.5)

        def get_networks():
            self.network_name.values = self.get_available_networks()
        Clock.schedule_once(lambda dt: get_networks(), 0.2)

    def open_network_spinner(self):
        self.network_name.is_open = True
        self.network_name.focus = True
    values = ['GB', 'US', 'AF', 'AX', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI',
        'AQ', 'AG', 'AR', 'AM', 'AW', 'AU', 'AT', 'AZ', 'BH', 'BS', 'BD',
        'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT', 'BO', 'BQ', 'BA', 'BW',
        'BV', 'BR', 'IO', 'BN', 'BG', 'BF', 'BI', 'KH', 'CM', 'CA', 'CV',
        'KY', 'CF', 'TD', 'CL', 'CN', 'CX', 'CC', 'CO', 'KM', 'CG', 'CD',
        'CK', 'CR', 'CI', 'HR', 'CU', 'CW', 'CY', 'CZ', 'DK', 'DJ', 'DM',
        'DO', 'EC', 'EG', 'SV', 'GQ', 'ER', 'EE', 'ET', 'FK', 'FO', 'FJ',
        'FI', 'FR', 'GF', 'PF', 'TF', 'GA', 'GM', 'GE', 'DE', 'GH', 'GI',
        'GR', 'GL', 'GD', 'GP', 'GU', 'GT', 'GG', 'GN', 'GW', 'GY', 'HT',
        'HM', 'VA', 'HN', 'HK', 'HU', 'IS', 'IN', 'ID', 'IR', 'IQ', 'IE',
        'IM', 'IL', 'IT', 'JM', 'JP', 'JE', 'JO', 'KZ', 'KE', 'KI', 'KP',
        'KR', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY', 'LI', 'LT',
        'LU', 'MO', 'MK', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT', 'MH', 'MQ',
        'MR', 'MU', 'YT', 'MX', 'FM', 'MD', 'MC', 'MN', 'ME', 'MS', 'MA',
        'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'NC', 'NZ', 'NI', 'NE', 'NG',
        'NU', 'NF', 'MP', 'NO', 'OM', 'PK', 'PW', 'PS', 'PA', 'PG', 'PY',
        'PE', 'PH', 'PN', 'PL', 'PT', 'PR', 'QA', 'RE', 'RO', 'RU', 'RW',
        'BL', 'SH', 'KN', 'LC', 'MF', 'PM', 'VC', 'WS', 'SM', 'ST', 'SA',
        'SN', 'RS', 'SC', 'SL', 'SG', 'SX', 'SK', 'SI', 'SB', 'SO', 'ZA',
        'GS', 'SS', 'ES', 'LK', 'SD', 'SR', 'SJ', 'SZ', 'SE', 'CH', 'SY',
        'TW', 'TJ', 'TZ', 'TH', 'TL', 'TG', 'TK', 'TO', 'TT', 'TN', 'TR',
        'TM', 'TC', 'TV', 'UG', 'UA', 'AE', 'UM', 'UY', 'UZ', 'VU', 'VE',
        'VN', 'VG', 'VI', 'WF', 'EH', 'YE', 'ZM', 'ZW']

    def update_strings(self):
        self.ip_address_label.text = self.l.get_str('IP address:')
        self.network_name_label.text = self.l.get_bold('Network Name')
        self.password_label.text = self.l.get_bold('Password')
        self.country_label.text = self.l.get_bold('Country')
        self.connect_button.text = self.l.get_str('Connect')
        self.custom_ssid_input()
        self.custom_network_name.hint_text = self.l.get_str(
            'Enter network name')
        self.update_hint_font_size(self.custom_network_name)
        self.update_button_font_size(self.connect_button, 28, 10)
        self.update_button_font_size(self.custom_ssid_button, 20, 20)

    def update_hint_font_size(self, value):
        if value.hint_text:
            if len(value.hint_text) > 22:
                value.font_size = self.default_font_size - 3

    def update_button_font_size(self, value, default_size, max_length):
        value.font_size = default_size
        if len(value.text) > max_length:
            value.font_size = 19

    def get_rst_source(self):
        try:
            self.connection_instructions_rst.source = (self.
                wifi_documentation_path + self.l.lang + '.rst')
        except:
            self.connection_instructions_rst.source = (self.
                wifi_documentation_path + self.l.default_lang + '.rst')

    def on_leave(self):
        if self.wifi_error_timeout_event:
            self.wifi_error_timeout_event.cancel()
        if self.dismiss_wait_popup_event:
            self.dismiss_wait_popup_event.cancel()
        if self.refresh_ip_label_value_event:
            self.refresh_ip_label_value_event.cancel()
