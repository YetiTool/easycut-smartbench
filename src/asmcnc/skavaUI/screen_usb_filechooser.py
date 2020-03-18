'''
Created on 19 Aug 2017

@author: Ed
'''
# config

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.clock import Clock

import sys, os
from os.path import expanduser
from shutil import copy
from asmcnc.comms import usb_storage


Builder.load_string("""

<USBFileChooser>:

    on_enter: root.refresh_filechooser()

    filechooser_usb:filechooser_usb
    cut_usb_files_switch:cut_usb_files_switch
    load_button:load_button
    image_select:image_select


    BoxLayout:
        padding: 0
        spacing: 10
        size: root.size
        pos: root.pos
        orientation: "vertical"

    
        BoxLayout:
            orientation: 'horizontal'
            size: self.parent.size
            pos: self.parent.pos
            BoxLayout:
                size_hint_x: 5
                orientation: 'vertical'
                spacing: 10
                FileChooserListView:
                    size_hint_y: 5
                    id: filechooser_usb
                    path: './jobCache/'
                    filter_dirs: True
                    dirselect: False
                    filters: ['*.nc','*.NC','*.gcode','*.GCODE','*.GCode','*.Gcode','*.gCode']
                    on_selection: 
                        root.refresh_filechooser()
                        print filechooser_usb.selection[0]
                BoxLayout:
                    size_hint_y: 1
                    orientation: 'horizontal'
                    spacing: 10
                    Switch:
                        size_hint_x: 2
                        active: False
                        id: cut_usb_files_switch
                    Label:
                        size_hint_x: 6
                        halign: 'left'
                        text: 'Remove files from USB after import'
               
        BoxLayout:
            size_hint_y: None
            height: 100

            Button:
                disabled: False
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    root.refresh_filechooser() 
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    self.background_color = hex('#FFFFFFFF')
                BoxLayout:
                    padding: 25
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_refresh
                        source: "./asmcnc/skavaUI/img/file_select_refresh.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 

            Button:
                disabled: False
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    root.quit_to_local()
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    self.background_color = hex('#FFFFFFFF')
                BoxLayout:
                    padding: 25
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_cancel
                        source: "./asmcnc/skavaUI/img/file_select_cancel.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
            Button:
                id: load_button
                disabled: True
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    root.import_usb_file(filechooser_usb.selection[0])
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    self.background_color = hex('#FFFFFFFF')
                BoxLayout:
                    padding: 25
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_select
                        source: "./asmcnc/skavaUI/img/file_select_select_disabled.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
                
""")


job_cache_dir = './jobCache/'    # where job files are cached for selection (for last used history/easy access)
job_q_dir = './jobQ/'            # where file is copied if to be used next in job
verbose = True

class USBFileChooser(Screen):


    def __init__(self, **kwargs):
        super(USBFileChooser, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.usb_stick = usb_storage.USB_storage()

    
    def on_enter(self):
        self.refresh_filechooser()
    
    
    def set_USB_path(self, usb_path):      
        self.filechooser_usb.path = usb_path
        if verbose: print 'Filechooser_usb path: ' + self.filechooser_usb.path


    def refresh_filechooser(self):

        if verbose: print 'Refreshing filechooser'
        try:
            if self.filechooser_usb.selection[0] != 'C':
                self.load_button.disabled = False
                self.image_select.source = './asmcnc/skavaUI/img/file_select_select.png'
            
            else:
                self.loadButton.disabled = True
                self.image_select.source = './asmcnc/skavaUI/img/file_select_select_disabled.png'

        except:
            self.load_button.disabled = True
            self.image_select.source = './asmcnc/skavaUI/img/file_select_select_disabled.png'

        self.filechooser_usb._update_files()

        
    def import_usb_file(self, file_selection):
        
        # Move over the nc file
        if os.path.isfile(file_selection):
            
            # ... to cache
            copy(file_selection, job_cache_dir) # "copy" overwrites same-name file at destination
            
            # Clean USB
            if self.cut_usb_files_switch.active:
                os.remove(file_selection) # clean original space       
        

        self.go_to_loading_screen(file_selection)
        

    def quit_to_local(self):
        self.manager.current = 'local_filechooser'
          
    def quit_to_home(self):
        self.manager.current = 'home'
        
    def go_to_loading_screen(self, file_selection):

        self.manager.get_screen('loading').loading_file_name = file_selection
        self.manager.current = 'loading'
