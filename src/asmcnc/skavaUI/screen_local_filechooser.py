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
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

import sys, os
from os.path import expanduser
from shutil import copy

from asmcnc.comms import usb_storage
from asmcnc.skavaUI import screen_file_loading
from asmcnc.skavaUI import popup_info


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex

<LocalFileChooser>:

    on_enter: root.refresh_filechooser()

    filechooser:filechooser
    toggle_view_button : toggle_view_button
    toggle_sort_button: toggle_sort_button
    button_usb:button_usb
    load_button:load_button
    delete_selected_button:delete_selected_button
    delete_all_button:delete_all_button
    image_view : image_view
    image_sort: image_sort
    image_usb:image_usb
    image_delete:image_delete
    image_delete_all:image_delete_all
    image_select:image_select
    file_selected_label:file_selected_label
    usb_status_label:usb_status_label

    BoxLayout:
        padding: 0
        spacing: 10
        size: root.size
        pos: root.pos
        orientation: "vertical"

        BoxLayout:
            orientation: 'vertical'
            size: self.parent.size
            pos: self.parent.pos
            spacing: 0

            Label:
                id: usb_status_label
                canvas.before:
                    Color:
                        rgba: hex('#333333FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos
                size_hint_y: 0.7
                markup: True
                font_size: '18sp'   
                valign: 'middle'
                halign: 'left'
                text_size: self.size
                padding: [10, 0]
                text: "USB connected: Please do not remove USB until file is loaded."

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

            FileChooser:
                id: filechooser
                size_hint_y: 5
                rootpath: './jobCache/'
                show_hidden: False
                on_touch_move: root.scrolling_start()
                on_touch_up: root.scrolling_stop()
                filters: ['*.nc','*.NC','*.gcode','*.GCODE','*.GCode','*.Gcode','*.gCode']
                on_selection: root.refresh_filechooser()
                sort_func: root.sort_by_date_reverse
                FileChooserIconLayout
                FileChooserListLayout
               

        BoxLayout:
            size_hint_y: None
            height: 100

            ToggleButton:
                id: toggle_view_button
                size_hint_x: 1
                on_press: root.switch_view()
                background_color: hex('#FFFFFF00')
                BoxLayout:
                    padding: 25
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_view
                        source: "./asmcnc/skavaUI/img/file_select_list_icon.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 

            ToggleButton:
                id: toggle_sort_button
                size_hint_x: 1
                on_press: root.switch_sort()
                background_color: hex('#FFFFFF00')
                BoxLayout:
                    padding: 25
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_sort
                        source: "./asmcnc/skavaUI/img/file_select_sort_down.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

            Button:
                id: button_usb
                disabled: True
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    root.open_USB()
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
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    root.get_FTP_files()
                    root.refresh_filechooser() 
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
                    root.delete_popup(file_selection = filechooser.selection[0])
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
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    root.delete_popup(file_selection = 'all')
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
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    root.go_to_loading_screen(filechooser.selection[0])
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
ftp_file_dir = '../../router_ftp/'   # Linux location where incoming files are FTP'd to

def date_order_sort(files, filesystem):
    return (sorted(f for f in files if filesystem.is_dir(f)) +
        sorted((f for f in files if not filesystem.is_dir(f)), key=lambda fi: os.stat(fi).st_mtime, reverse = False))

def date_order_sort_reverse(files, filesystem):
    return (sorted(f for f in files if filesystem.is_dir(f)) +
        sorted((f for f in files if not filesystem.is_dir(f)), key=lambda fi: os.stat(fi).st_mtime, reverse = True))

class LocalFileChooser(Screen):

    filename_selected_label_text = StringProperty()
    
    sort_by_date = ObjectProperty(date_order_sort)
    sort_by_date_reverse = ObjectProperty(date_order_sort_reverse)
    is_filechooser_scrolling = False

    def __init__(self, **kwargs):

        super(LocalFileChooser, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.usb_stick = usb_storage.USB_storage(self.sm) # object to manage presence of USB stick (fun in Linux)
        self.check_for_job_cache_dir()

    def check_for_job_cache_dir(self):
        if not os.path.exists(job_cache_dir):
            os.mkdir(job_cache_dir)
            
            if not path.exists(job_cache_dir + '.gitignore'):
                file = open(job_cache_dir + '.gitignore', "w+")
                file.write('*.nc')
                file.close()

    def on_enter(self):
        
        self.filechooser.path = job_cache_dir  # Filechooser path reset to root on each re-entry, so user doesn't start at bottom of previously selected folder
        self.usb_stick.enable() # start the object scanning for USB stick
        self.refresh_filechooser()
        self.check_USB_status(1)
        self.poll_USB = Clock.schedule_interval(self.check_USB_status, 0.25) # poll status to update button           
        self.filename_selected_label_text = "Only .nc and .gcode files will be shown. Press the icon to display the full filename here."
        self.switch_view()
    
    
    def on_pre_leave(self):
        
        Clock.unschedule(self.poll_USB)
        if self.sm.current != 'usb_filechooser': self.usb_stick.disable()

    def on_leave(self):
        self.usb_status_label.size_hint_y = 0

    def check_USB_status(self, dt):

        if not self.is_filechooser_scrolling:
            if self.usb_stick.is_available():
                self.button_usb.disabled = False
                self.image_usb.source = './asmcnc/skavaUI/img/file_select_usb.png'
                self.sm.get_screen('loading').usb_status_label.opacity = 1
                self.usb_status_label.size_hint_y = 0.7
                self.usb_status_label.canvas.before.clear()
                with self.usb_status_label.canvas.before:
                    Color(76 / 255., 175 / 255., 80 / 255., 1.)
                    Rectangle(pos=self.usb_status_label.pos,size=self.usb_status_label.size)
            else:
                self.button_usb.disabled = True
                self.image_usb.source = './asmcnc/skavaUI/img/file_select_usb_disabled.png'
                self.usb_status_label.size_hint_y = 0
                self.sm.get_screen('loading').usb_status = None
                self.sm.get_screen('loading').usb_status_label.opacity = 0

    def switch_view(self):

        if self.toggle_view_button.state == "normal":
            self.filechooser.view_mode = 'icon'
            self.image_view.source = "./asmcnc/skavaUI/img/file_select_list_view.png"

        elif self.toggle_view_button.state == "down":
            self.filechooser.view_mode = 'list'
            self.image_view.source = "./asmcnc/skavaUI/img/file_select_list_icon.png"

    def switch_sort(self):

        if self.toggle_sort_button.state == "normal":
            self.filechooser.sort_func = self.sort_by_date_reverse
            self.image_sort.source = "./asmcnc/skavaUI/img/file_select_sort_down.png"

        elif self.toggle_sort_button.state == "down":
            self.filechooser.sort_func = self.sort_by_date
            self.image_sort.source = "./asmcnc/skavaUI/img/file_select_sort_up.png"

        self.filechooser._update_files()

    def open_USB(self):

        self.sm.get_screen('usb_filechooser').set_USB_path(self.usb_stick.get_path())
        self.sm.get_screen('usb_filechooser').usb_stick = self.usb_stick
        self.manager.current = 'usb_filechooser'

    def refresh_filechooser(self):

        self.filechooser._update_item_selection()

        try:
            if self.filechooser.selection[0] != 'C':

                # display file selected in the filename display label
                if sys.platform == 'win32':
                    self.filename_selected_label_text = self.filechooser.selection[0].split("\\")[-1]
                else:
                    self.filename_selected_label_text = self.filechooser.selection[0].split("/")[-1]

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
            self.filename_selected_label_text = "Only .nc and .gcode files will be shown. Press the icon to display the full filename here."
            
            self.delete_selected_button.disabled = True
            self.image_delete.source = './asmcnc/skavaUI/img/file_select_delete_disabled.png'
            self.filename_selected_label_text = "Only .nc and .gcode files will be shown. Press the icon to display the full filename here."

        self.filechooser._update_files()

    
    def get_FTP_files(self):

        if sys.platform != "win32":
            ftp_files = os.listdir(ftp_file_dir)
            if ftp_files:
                for file in ftp_files:
                    copy(ftp_file_dir + file, job_cache_dir) # "copy" overwrites same-name file at destination
                    os.remove(ftp_file_dir + file) # clean original space


    def go_to_loading_screen(self, file_selection):

        if os.path.isfile(file_selection):
            self.manager.get_screen('loading').loading_file_name = file_selection
            self.manager.current = 'loading'

        else: 
            error_message = 'File selected does not exist!'
            popup_info.PopupError(self.sm, error_message)

    def delete_popup(self, **kwargs):

        if kwargs['file_selection'] == 'all':
            popup_info.PopupDeleteFile(screen_manager = self.sm, function = self.delete_all, file_selection = 'all')
        else: 
            popup_info.PopupDeleteFile(screen_manager = self.sm, function = self.delete_selected, file_selection = kwargs['file_selection'])

    def delete_selected(self, filename):        
        self.refresh_filechooser()

        if os.path.isfile(filename):
            try: 
                os.remove(filename)
                self.filechooser.selection = []
                
            except: 
                print "attempt to delete folder, or undeletable file"

            self.refresh_filechooser()    

    def delete_all(self):
        files_in_cache = os.listdir(job_cache_dir) # clean cache
        self.refresh_filechooser()

        def delete_files_loop():
            self.refresh_filechooser()

            try: 
                os.remove(job_cache_dir + files_in_cache[0])
                files_in_cache.pop(0)
                if files_in_cache:
                    Clock.schedule_once(lambda self: delete_files_loop(), 0.1)
                else:
                    self.refresh_filechooser()

            except:
                print "attempt to delete folder, or undeletable file"

        if files_in_cache:
            Clock.schedule_once(lambda self: delete_files_loop(), 0.1)

        self.filechooser.selection = []
        self.refresh_filechooser()


    def quit_to_home(self):

        self.manager.current = 'home'
        #self.manager.transition.direction = 'up'   


    def scrolling_start(self):
        self.is_filechooser_scrolling = True

    def scrolling_stop(self):
        self.is_filechooser_scrolling = False
