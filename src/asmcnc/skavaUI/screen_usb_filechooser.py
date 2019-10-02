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
    modelPreviewImage:modelPreviewImage
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
                    filters: ['*.nc','*.NC','*.gcode','*.GCODE','*.GCode','*.Gcode']
                    on_selection: 
                        root.refresh_filechooser()
#                         root.detect_preview_image(filechooser_usb.selection[0])
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
                size: self.parent.size
                pos: self.parent.pos
                padding: 10
                size_hint_x: 5
                canvas:
                    Color: 
                        rgba: 1,1,1,.1
                    Rectangle: 
                        size: self.size
                        pos: self.pos
                Image:
                    id:modelPreviewImage
                    source: root.no_preview_found_img_path
                    size: self.parent.size
                    allow_stretch: True                

                
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


    no_preview_found_img_path = './asmcnc/skavaUI/img/image_preview_inverted_large.png'


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

    
    preview_image_path = None
    
    def detect_preview_image(self, nc_file_path):
        
        if verbose: print "Detecting image for: " + nc_file_path
        
        # Assume there is no image preview to be found, so set image to default preview
        self.preview_image_path = None
        self.modelPreviewImage.source = self.no_preview_found_img_path

        # Scan file for image identifier in gcode e.g. (preview_img=123.png)
        try:
            original_file = open(nc_file_path, 'r')
            for line in original_file:
                if line.find('(preview_img') >= 0:
                    image_name = line.strip().split(':')[1][:-1]
                    image_dir_path = os.path.dirname(nc_file_path)
                    self.preview_image_path = image_dir_path + '/' + image_name
                    if os.path.isfile(self.preview_image_path):
                        self.modelPreviewImage.source = self.preview_image_path
                    break
            original_file.close()  
        except:
            print 'Handled error: Failed to open USB file preview image... selection too quick?'

    
    def import_usb_file(self, file_selection):
        
        # Move over the nc file
        if os.path.isfile(file_selection):
            
            # ... to cache
            copy(file_selection, job_cache_dir) # "copy" overwrites same-name file at destination
            
            # Clean USB
            if self.cut_usb_files_switch.active:
                os.remove(file_selection) # clean original space       
        
        # Move over the preview image
        if self.preview_image_path:
            if os.path.isfile(self.preview_image_path):
                
                # ... to cache
                copy(self.preview_image_path, job_cache_dir) # "copy" overwrites same-name file at destination
                
                # Clean USB
                if self.cut_usb_files_switch.active:
                    os.remove(self.preview_image_path) # clean original space
            
        self.go_to_loading_screen(file_selection)
        

    def quit_to_local(self):
        self.manager.current = 'local_filechooser'
        #self.manager.transition.direction = 'up' 
  
        
    def quit_to_home(self):
        self.manager.current = 'home'
        #self.manager.transition.direction = 'up'
        
    def go_to_loading_screen(self, file_selection):

        self.manager.get_screen('loading').loading_file_name = file_selection
        self.manager.current = 'loading'
