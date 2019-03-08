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
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.clock import Clock

import sys, os
from os.path import expanduser
from shutil import copy

from asmcnc.comms import usb_storage
from asmcnc.skavaUI import screen_file_loading


Builder.load_string("""

<LocalFileChooser>:

    on_enter: root.refresh_filechooser()

    filechooser:filechooser
    button_usb:button_usb
    modelPreviewImage:modelPreviewImage
    load_button:load_button
    delete_selected_button:delete_selected_button
    delete_all_button:delete_all_button
    image_usb:image_usb
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
                rootpath: './jobCache/'
                filter_dirs: True
                filters: ['*.nc','*.NC','*.gcode','*.GCODE']
                on_selection: 
                    root.refresh_filechooser()
                    root.detect_preview_image(filechooser.selection[0])
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
                id: button_usb
                disabled: True
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    root.open_USB()
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    self.background_color = hex('#FFFFFFFF')
                BoxLayout:
                    padding: 25
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_usb
                        source: "./asmcnc/skavaUI/img/file_select_usb_disabled.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 
            Button:
                disabled: False
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    root.get_FTP_files()
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
                    root.go_to_loading_screen(filechooser.selection[0])
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
ftp_file_dir = '/home/sysop/router_ftp'   # Linux location where incoming files are FTP'd to

class LocalFileChooser(Screen):

    no_preview_found_img_path = './asmcnc/skavaUI/img/image_preview_inverted_large.png'    
    
    def __init__(self, **kwargs):

        super(LocalFileChooser, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.usb_stick = usb_storage.USB_storage() # object to manage presence of USB stick (fun in Linux)
        self.usb_stick.enable() # start the object scanning for USB stick


        
    def on_enter(self):

        self.refresh_filechooser()
        self.poll_USB = Clock.schedule_interval(self.check_USB_status, 0.25) # poll status to update button        
    
    
    def on_leave(self):
        
        self.poll_USB.cancel()
#         self.usb_stick.disable()

    
    def check_USB_status(self, dt):
        
        if self.usb_stick.is_available():
            self.button_usb.disabled = False
            self.image_usb.source = './asmcnc/skavaUI/img/file_select_usb.png'

        else:
            self.button_usb.disabled = True
            self.image_usb.source = './asmcnc/skavaUI/img/file_select_usb_disabled.png'
        

    def open_USB(self):

        self.sm.get_screen('usb_filechooser').set_USB_path(self.usb_stick.get_path())
        #self.manager.transition.direction = 'down'
        self.manager.current = 'usb_filechooser'
        

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

    
    def get_FTP_files(self):

        if sys.platform != "win32":
            ftp_files = os.listdir(ftp_file_dir)
            if ftp_files:
                for file in ftp_files:
                    copy(ftp_file_dir + file, job_cache_dir) # "copy" overwrites same-name file at destination
                    os.remove(ftp_file_dir + file) # clean original space

    
    preview_image_path = None
    
    def detect_preview_image(self, nc_file_path):
        
        # Assume there is no image preview to be found, so set image to default preview
        self.preview_image_path = None
        self.modelPreviewImage.source = self.no_preview_found_img_path
        
        # Scan file for image identifier in gcode e.g. (preview_img=123.png)
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


    def go_to_loading_screen(self, file_selection):
        
# NEW ------------------------------------------------------ DONE
        # Pass the selected file to the new screen
        self.manager.get_screen('loading').loading_file_name = file_selection
        self.manager.current = 'loading'
        
# ---------------------------------------------------------- DONE
        
        # Replace this with move to the file_loading screen
# --------------------------------------------------------------- OLD       
#         # Move over the nc file
#         if os.path.isfile(file_selection):
#             
#             # ... to Q
#             files_in_q = os.listdir(job_q_dir) # clean Q
#             if files_in_q:
#                 for file in files_in_q:
#                     os.remove(job_q_dir+file)
#             copy(file_selection, job_q_dir) # "copy" overwrites same-name file at destination
# 
#         # Move over the preview image
#         if self.preview_image_path:
#             if os.path.isfile(self.preview_image_path):
#                 
#                 # ... to Q
#                 copy(self.preview_image_path, job_q_dir) # "copy" overwrites same-name file at destination
#-------------------------------------------------------------------


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

        self.manager.current = 'home'
        #self.manager.transition.direction = 'up'   
        
