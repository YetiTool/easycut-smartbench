'''
Created on 19 Aug 2017

@author: Ed
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

import sys, os
from os.path import expanduser
from shutil import copy
from asmcnc.comms import usb_storage


Builder.load_string("""

<USBFileChooser>:

    on_enter: root.refresh_filechooser()

    filechooser_usb:filechooser_usb
    load_button:load_button
    image_select:image_select
    usb_status_label:usb_status_label


    BoxLayout:
        padding: 0
        spacing: 0
        size: root.size
        pos: root.pos
        orientation: "vertical"

        Label:
            canvas.before:
                Color:
                    rgba: hex('#333333FF')
                Rectangle:
                    size: self.size
                    pos: self.pos
            id: usb_status_label
            size_hint_y: 0.7
            markup: True
            font_size: '18sp'   
            valign: 'middle'
            halign: 'left'
            text_size: self.size
            padding: [10, 0]

        Label:
            canvas.before:
                Color:
                    rgba: hex('#333333FF')
                Rectangle:
                    size: self.size
                    pos: self.pos
            id: file_selected_label
            size_hint_y: 1
            text: root.filename_selected_label_text
            markup: True
            font_size: '20sp'   
            valign: 'middle'
            halign: 'center'                


        FileChooserIconView:
            padding: [0,10]
            size_hint_y: 5
            id: filechooser_usb
            show_hidden: False
            filters: ['*.nc','*.NC','*.gcode','*.GCODE','*.GCode','*.Gcode','*.gCode']
            on_selection: 
                root.refresh_filechooser()



               
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
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    root.quit_to_local()
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


    filename_selected_label_text = StringProperty()
    usb_stick = ObjectProperty()


    def __init__(self, **kwargs):
 
        super(USBFileChooser, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']


    def set_USB_path(self, usb_path):

        self.usb_path = usb_path
        self.filechooser_usb.rootpath = usb_path # Filechooser path reset to root on each re-entry, so user doesn't start at bottom of previously selected folder
        if verbose: print 'Filechooser_usb path: ' + self.filechooser_usb.path

    
    def on_enter(self):

        self.filechooser_usb.path = self.usb_path
        self.refresh_filechooser()
        self.filename_selected_label_text = "Only .nc and .gcode files will be shown. Press the icon to display the full filename here."
        self.update_usb_status()
        
    def on_pre_leave(self):
        if self.sm.current != 'local_filechooser': self.usb_stick.disable()

    def update_usb_status(self):
        try: 
            if self.usb_stick.is_available():
                self.usb_status_label.text = "USB connected: Please do not remove USB until file is loaded."
                self.usb_status_label.canvas.before.clear()
                with self.usb_status_label.canvas.before:
                    Color(76 / 255., 175 / 255., 80 / 255., 1.)
                    Rectangle(pos=self.usb_status_label.pos,size=self.usb_status_label.size)
            else:
                self.usb_status_label.text = "USB removed! Files will not load properly."
                self.usb_status_label.opacity = 1
                self.usb_status_label.canvas.before.clear()
                with self.usb_status_label.canvas.before:
                    Color(230 / 255., 74 / 255., 25 / 255., 1.)
                    Rectangle(pos=self.usb_status_label.pos,size=self.usb_status_label.size)

        except: 
            self.usb_status_label.opacity = 0

    def refresh_filechooser(self):

        if verbose: print 'Refreshing filechooser'
        try:
            if self.filechooser_usb.selection[0] != 'C':
                
                # display file selected in the filename display label
                if sys.platform == 'win32':
                    self.filename_selected_label_text = self.filechooser_usb.selection[0].split("\\")[-1]
                else:
                    self.filename_selected_label_text = self.filechooser_usb.selection[0].split("/")[-1]

                
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
            file_name = os.path.basename(file_selection)
            new_file_path = job_cache_dir + file_name
            print new_file_path
            
            self.go_to_loading_screen(new_file_path)
        

    def quit_to_local(self):

        self.manager.current = 'local_filechooser'

          
    def quit_to_home(self):

        self.manager.current = 'home'

        
    def go_to_loading_screen(self, file_selection):
        self.manager.get_screen('loading').loading_file_name = file_selection
        self.manager.current = 'loading'