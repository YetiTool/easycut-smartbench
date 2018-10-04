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
            print network, '  ', password
            
            sudoPassword = 'posys'
            command = 'sudo pipaos-setwifi '+ network + ' ' + password
            p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))


