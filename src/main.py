'''
Created on 16 Nov 2017
v2
@author: Ed
'''
# config
from kivy.config import Config
from asmcnc.comms.serial_connection import SerialConnection
from asmcnc.comms.router_machine import RouterMachine

Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty # @UnresolvedImport
from kivy.uix.popup import Popup

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *
from kivy.uix.scrollview import ScrollView
from kivy.properties import BooleanProperty, NumericProperty, ListProperty, ObjectProperty  # @UnresolvedImport

import time
import socket
import subprocess

import os, sys
import subprocess
import ntpath
from shutil import copyfile, rmtree
from kivy.lib.osc.OSC import null
import zipfile
from kivy.uix.video import Video
from os import listdir
from os.path import isfile, join
import pickle
import shutil
import math
import ntpath
from kivy.core.image import Image as CoreImage
import serial
import time
from threading import Thread

import time
from kivy.graphics import Line
from kivy.uix.slider import Slider
from kivy.cache import Cache
    
from kivy.graphics.vertex_instructions import (Rectangle, Ellipse, Line)
from kivy.graphics.context_instructions import Color  # @UnresolvedImport (for Eclipse users)
from asmcnc.comms import router_machine
from asmcnc.skavaUI import screen_inital, screen_help
from asmcnc.skavaUI import screen_home
from asmcnc.skavaUI import screen_local_filechooser
from asmcnc.skavaUI import screen_usb_filechooser
from asmcnc.skavaUI import screen_go
from asmcnc.skavaUI import screen_template
from asmcnc.skavaUI import screen_lobby



Builder.load_string("""

""")

class SkavaUI(App):

    def build(self):

        # Establish screens
        sm = ScreenManager(transition=NoTransition())
        
        # Initialise 'm'achine object
        # m = router_machine.RouterMachine('COM5', sm)
        m = router_machine.RouterMachine('COM4', sm)

#         initial_screen = screen_inital.InitialScreen(name='initial', screen_manager = sm, machine = m)
        lobby_screen = screen_lobby.LobbyScreen(name='lobby', screen_manager = sm, machine = m)
        home_screen = screen_home.HomeScreen(name='home', screen_manager = sm, machine = m)
        local_filechooser = screen_local_filechooser.LocalFileChooser(name='local_filechooser', screen_manager = sm)
        usb_filechooser = screen_usb_filechooser.USBFileChooser(name='usb_filechooser', screen_manager = sm)
        help_screen = screen_help.HelpScreen(name='help', screen_manager = sm)
        go_screen = screen_go.GoScreen(name='go', screen_manager = sm, machine = m)
        template_screen = screen_template.TemplateScreen(name='template', screen_manager = sm)

#         sm.add_widget(initial_screen)
        sm.add_widget(lobby_screen)
        sm.add_widget(home_screen)
        sm.add_widget(local_filechooser)
        sm.add_widget(usb_filechooser)
        sm.add_widget(help_screen)
        sm.add_widget(go_screen)
        sm.add_widget(template_screen)

#         sm.current = 'initial'
        sm.current = 'lobby'
 
        return sm


if __name__ == '__main__':
    
    SkavaUI().run()
