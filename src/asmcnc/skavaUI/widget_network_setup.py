'''
Created on 1 Feb 2018
@author: Ed
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
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
    countryTextEntry:countryTextEntry

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
            id: countryTextEntry
            size_hint_y: None
            height: '32dp'
            text: 'GB'
            focus: False
            multiline: False
        TextInput:
            id: networkTextEntry
            size_hint_y: None
            height: '32dp'
            text: 'Network name...'
            focus: False
            multiline: False
        TextInput:
            id: passwordTextEntry
            size_hint_y: None
            height: '32dp'
            text: 'Network password...'
            focus: False
            multiline: False
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

    def connectWifi(self):

        # get network name and password from text entered (widget)
        self.netname = self.networkTextEntry.text
        self.password = self.passwordTextEntry.text
        self.country = self.countryTextEntry.text 

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
    

        
