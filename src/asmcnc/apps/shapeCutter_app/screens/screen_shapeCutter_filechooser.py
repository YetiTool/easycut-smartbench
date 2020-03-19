'''
Created on 19 Aug 2017

@author: Ed

Screen allows user to select their job for loading into easycut, either from JobCache or from a memory stick.
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

<SCFileChooser>:

    on_enter: root.refresh_filechooser()

    filechooser:filechooser
    load_button:load_button
    delete_selected_button:delete_selected_button
    delete_all_button:delete_all_button
    image_delete:image_delete
    image_delete_all:image_delete_all
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
            spacing: 10
            FileChooserListView:
                size_hint_x: 5
                id: filechooser
                rootpath: './asmcnc/apps/shapeCutter_app/parameter_cache/'
                filter_dirs: True
                filters: ['*.csv', '*.CSV']
                on_selection: 
                    root.refresh_filechooser()
                    root.detect_preview_image(filechooser.selection[0])
       

                
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
                id: delete_selected_button
                disabled: True
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    root.delete_selected(filechooser.selection[0])
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    self.background_color = hex('#FFFFFFFF')
                BoxLayout:
                    padding: 25
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_delete
                        source: "./asmcnc/skavaUI/img/file_select_delete_disabled.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
            Button:
                id: delete_all_button
                disabled: False
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    root.delete_all()
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    self.background_color = hex('#FFFFFFFF')
                BoxLayout:
                    padding: 25
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_delete_all
                        source: "./asmcnc/skavaUI/img/file_select_delete_all.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
            Button:
                disabled: False
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    root.quit_to_home()
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
                on_release: 
                    root.return_to_SC17(filechooser.selection[0])
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

parameter_file_dir = './asmcnc/apps/shapeCutter_app/parameter_cache/'


class SCFileChooser(Screen):

    
    def __init__(self, **kwargs):

        super(SCFileChooser, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs['shapecutter']
        self.j = kwargs['job_parameters']
#         self.usb_stick = usb_storage.USB_storage() # object to manage presence of USB stick (fun in Linux)
#         self.usb_stick.enable() # start the object scanning for USB stick
        
    def on_enter(self):
        self.refresh_filechooser()

    def refresh_filechooser(self):

        try:
            if self.filechooser.selection[0] != 'C':

                self.load_button.disabled = False
                self.image_select.source = './asmcnc/skavaUI/img/file_select_select.png'
                
                self.delete_selected_button.disabled = False
                self.image_delete.source = './asmcnc/skavaUI/img/file_select_delete.png'

            else:
                
                self.load_button.disabled = True
                self.image_select.source = './asmcnc/skavaUI/img/file_select_select_disabled.png'
                
                self.delete_selected_button.disabled = True
                self.image_delete.source = './asmcnc/skavaUI/img/file_select_delete_disabled.png'

        except:
            self.load_button.disabled = True
            self.image_select.source = './asmcnc/skavaUI/img/file_select_select_disabled.png'
            
            self.delete_selected_button.disabled = True
            self.image_delete.source = './asmcnc/skavaUI/img/file_select_delete_disabled.png'

        self.filechooser._update_files()


    def return_to_SC17(self, file_selection):
        self.j.load_parameters(file_selection)
        self.shapecutter_sm.next_screen()


    def delete_selected(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)
            self.refresh_filechooser()    
          
        
    def delete_all(self):

        files_in_cache = os.listdir(job_cache_dir) # clean cache
        if files_in_cache:
            for file in files_in_cache:
                os.remove(job_cache_dir+file)
        self.refresh_filechooser()       


    def quit_to_home(self):
        self.shapecutter_sm.previous_screen()  
        
