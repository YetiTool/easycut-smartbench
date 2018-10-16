'''
Created on 1 Feb 2018
@author: Ed
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, NumericProperty, StringProperty # @UnresolvedImport


Builder.load_string("""

<NetworkSetup>:

    networkTextEntry:networkTextEntry
    passwordTextEntry:passwordTextEntry
    ipLabel:ipLabel
    netNameLabel:netNameLabel

    BoxLayout:
    
        size: self.parent.size
        pos: self.parent.pos      
        padding: 10
        spacing: 10
        orientation: "vertical" 
        canvas:
            Color:
                rgba: 0,0,0,0.2
            Rectangle:
                size: self.size
                pos: self.pos

        Button:
            text: 'Refresh status...'
            on_release: root.detectIP()
        TextInput:
            id: networkTextEntry
            size_hint_y: None
            height: '32dp'
            text: 'Network name...'
            focus: False
        TextInput:
            id: passwordTextEntry
            size_hint_y: None
            height: '32dp'
            text: 'Network password...'
            focus: False
        Label:
            id: ipLabel
            text: 'IP address info here'
        Label:
            id: netNameLabel
            text: 'IP address info here'
        Button:
            text: 'Connect...'
            on_release: root.connectWifi()

          
         
""")

import socket, sys, os


class NetworkSetup(Widget):

    def __init__(self, **kwargs):
    
        super(NetworkSetup, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']

    def detectIP(self):
        
        if sys.platform == "win32": 
            try:
                hostname=socket.gethostname()   
                IPAddr=socket.gethostbyname(hostname)
                self.ipLabel.text = 'This device IP is: ' + IPAddr
                self.netNameLabel.text = 'It is known on the network as: ' + hostname
            except:
                self.ipLabel.text = 'Network not found'
                self.netNameLabel.text = ''
        else:
            try: 
                f = os.popen('hostname -I')
                self.ipLabel.text = 'This device IP is: ' + f.read().strip().split(' ')[0]
                self.netNameLabel.text = ''
            except:
                self.ipLabel.text = 'Network not found'
                self.netNameLabel.text = ''
                

    def connectWifi(self):
        if sys.platform != "win32": 
            network = self.networkTextEntry.text
            password = self.passwordTextEntry.text
            
            print 'Changing wireless credentials...'
            success=self.set_wireless_auth(network, password)
            if success:
                print 'done!'
            else:
                print 'failed :('
        


    
    # Wireless credential files in pipaOS stretch and jessie
    file_wpa='/boot/wpa_supplicant.txt'
    file_interfaces='/boot/interfaces.txt'
    
    
    def set_wireless_auth(self, essid, psk):
        '''
        Adapted code from  https://github.com/pipaos/pipaos-tools/blob/master/src/pipaos-setwifi - thanks!
        Sets the wireless credentials on the interfaces file (debian jessie)
        Or the wpa supplicant file (debian stretch)
        This wrapper is provided to support legacy pipaOS jessie.
        '''
        changed=False
    
        if os.path.isfile(self.file_wpa):
            changed = set_credentials(essid, psk, self.file_wpa)
    
        if os.path.isfile(self.file_interfaces):
            changed = set_credentials(essid, psk, self.file_interfaces)
    
        return changed
    
    
    def set_credentials(self, essid, psk, conffile):
        '''
        Parses Debian interfaces configuration to replace ssid and psk
        '''
        changed=False
        ssid=None
        passphrase=None
    
        # open settings file
        with open(conffile, 'r') as f:
            settings=f.readlines()
    
        # replace connection details
        for j,line in enumerate(settings):
            idx=line.find('wpa-ssid')
            if idx != -1:
                settings[j]='  wpa-ssid: {}\n'.format(essid)
                changed=True
                continue
    
            idx=line.find('wpa-psk')
            if idx != -1:
                settings[j]='  wpa-psk: {}\n'.format(psk)
                changed=True
                continue
    
            idx=line.find('ssid=')
            if idx != -1:
                settings[j]='  ssid="{}"\n'.format(essid)
                changed=True
                continue
    
            idx=line.find('psk=')
            if idx != -1:
                settings[j]='  psk="{}"\n'.format(psk)
                changed=True
                continue
    
    
        with open(conffile, 'w') as f:
            f.writelines(settings)
    
        return changed
    
