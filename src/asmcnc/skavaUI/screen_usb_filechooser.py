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
from os import path


Builder.load_string("""

<USBFileChooser>:

    on_enter: root.refresh_filechooser()

    filechooser_usb:filechooser_usb
    icon_layout_fc : icon_layout_fc
    list_layout_fc : list_layout_fc
    toggle_view_button : toggle_view_button
    toggle_sort_button: toggle_sort_button
    load_button:load_button
    image_view : image_view
    image_sort: image_sort
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


        FileChooser:
            padding: [0,10]
            size_hint_y: 5
            id: filechooser_usb
            show_hidden: False
            filters: ['*.nc','*.NC','*.gcode','*.GCODE','*.GCode','*.Gcode','*.gCode']
            on_selection: root.refresh_filechooser()
            sort_func: root.sort_by_date_reverse
            FileChooserIconLayout
                id: icon_layout_fc
            FileChooserListLayout
                id: list_layout_fc
               
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
                    root.screen_change_command(root.quit_to_local)
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
                    root.screen_change_command(root.import_usb_file)
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

def date_order_sort(files, filesystem):
    return (sorted(f for f in files if filesystem.is_dir(f)) +
        sorted((f for f in files if not filesystem.is_dir(f)), key=lambda fi: os.stat(fi).st_mtime, reverse = False))

def date_order_sort_reverse(files, filesystem):
    return (sorted(f for f in files if filesystem.is_dir(f)) +
        sorted((f for f in files if not filesystem.is_dir(f)), key=lambda fi: os.stat(fi).st_mtime, reverse = True))

class USBFileChooser(Screen):


    filename_selected_label_text = StringProperty()
    usb_stick = ObjectProperty()

    sort_by_date = ObjectProperty(date_order_sort)
    sort_by_date_reverse = ObjectProperty(date_order_sort_reverse)
    is_filechooser_scrolling = False

    def __init__(self, **kwargs):
 
        super(USBFileChooser, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']

        self.list_layout_fc.ids.scrollview.bind(on_scroll_stop = self.scrolling_stop)
        self.list_layout_fc.ids.scrollview.bind(on_scroll_start = self.scrolling_start)
        self.icon_layout_fc.ids.scrollview.bind(on_scroll_stop = self.scrolling_stop)
        self.icon_layout_fc.ids.scrollview.bind(on_scroll_start = self.scrolling_start)

        self.list_layout_fc.ids.scrollview.effect_cls = kivy.effects.scroll.ScrollEffect
        self.icon_layout_fc.ids.scrollview.effect_cls = kivy.effects.scroll.ScrollEffect

        self.fully_disable_scroll()

        self.enable_scroll_event = None

    def set_USB_path(self, usb_path):

        self.usb_path = usb_path
        self.filechooser_usb.rootpath = usb_path # Filechooser path reset to root on each re-entry, so user doesn't start at bottom of previously selected folder
        if verbose: print 'Filechooser_usb path: ' + self.filechooser_usb.path

    def on_pre_enter(self):
        self.sm.transition.bind(on_progress = self.fully_disable_scroll)
        # self.sm.transition.bind(on_complete = self.enable_scroll_on_enter)

    def on_enter(self):
        print("open usb filechooser")

        self.filechooser_usb.path = self.usb_path
        self.refresh_filechooser()
        self.filename_selected_label_text = "Only .nc and .gcode files will be shown. Press the icon to display the full filename here."
        self.update_usb_status()
        self.switch_view()

        self.enable_scroll_event = Clock.schedule_interval(self.enable_scroll_on_enter, 1)

    def on_pre_leave(self):
        if self.sm.current != 'local_filechooser': self.usb_stick.disable()
        self.sm.transition.unbind(on_complete = self.enable_scroll_on_enter)
        self.sm.transition.unbind(on_progress = self.fully_disable_scroll)

    def on_leave(self):
        print("close usb filechooser")
        # self.sm.get_screen('local_filechooser').enable_scroll_on_enter()


    def check_for_job_cache_dir(self):
        if not path.exists(job_cache_dir):
            os.mkdir(job_cache_dir)

            if not path.exists(job_cache_dir + '.gitignore'):
                file = open(job_cache_dir + '.gitignore', "w+")
                file.write('*.nc')
                file.close()

    def update_usb_status(self):
        try: 
            if self.usb_stick.is_available():
                self.usb_status_label.size_hint_y = 0.7
                self.usb_status_label.text = "USB connected: Please do not remove USB until file is loaded."
                self.usb_status_label.canvas.before.clear()
                with self.usb_status_label.canvas.before:
                    Color(76 / 255., 175 / 255., 80 / 255., 1.)
                    Rectangle(pos=self.usb_status_label.pos,size=self.usb_status_label.size)

            else:
                self.usb_status_label.text = "USB removed! Files will not load properly."
                self.usb_status_label.size_hint_y = 0.7
                self.usb_status_label.canvas.before.clear()
                with self.usb_status_label.canvas.before:
                    Color(230 / 255., 74 / 255., 25 / 255., 1.)
                    Rectangle(pos=self.usb_status_label.pos,size=self.usb_status_label.size)

        except: 
            pass

    def switch_view(self):

        if self.toggle_view_button.state == "normal":
            self.filechooser_usb.view_mode = 'icon'
            self.image_view.source = "./asmcnc/skavaUI/img/file_select_list_view.png"

        elif self.toggle_view_button.state == "down":
            self.filechooser_usb.view_mode = 'list'
            self.image_view.source = "./asmcnc/skavaUI/img/file_select_list_icon.png"

    def switch_sort(self):

        if self.toggle_sort_button.state == "normal":
            self.filechooser_usb.sort_func = self.sort_by_date_reverse
            self.image_sort.source = "./asmcnc/skavaUI/img/file_select_sort_down.png"

        elif self.toggle_sort_button.state == "down":
            self.filechooser_usb.sort_func = self.sort_by_date
            self.image_sort.source = "./asmcnc/skavaUI/img/file_select_sort_up.png"

        self.filechooser_usb._update_files()

    def refresh_filechooser(self):

        if verbose: print 'Refreshing usb filechooser'
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

     
    def import_usb_file(self, dt):

        file_selection = filechooser_usb.selection[0]

        self.check_for_job_cache_dir()
        
        # Move over the nc file
        if os.path.isfile(file_selection):
            
            # ... to cache
            copy(file_selection, job_cache_dir) # "copy" overwrites same-name file at destination          
            file_name = os.path.basename(file_selection)
            new_file_path = job_cache_dir + file_name
            print new_file_path
            
            self.go_to_loading_screen(new_file_path)
        

    def quit_to_local(self, dt):
        print("Stability test")
        self.manager.current = 'local_filechooser'

        
    def go_to_loading_screen(self, file_selection):
        print("Stability test")
        self.manager.get_screen('loading').loading_file_name = file_selection
        self.manager.current = 'loading'

    def screen_change_command(self, screen_function):

        if not self.is_filechooser_scrolling:
            self.fully_disable_scroll()
            Clock.schedule_once(screen_function, 1)

    def scrolling_start(self, *args):
        self.is_filechooser_scrolling = True

    def scrolling_stop(self, *args):
        self.is_filechooser_scrolling = False

    def fully_disable_scroll(self, *args):

        print("Disable scroll - USB")
        self.list_layout_fc.ids.scrollview.do_scroll_y = False
        self.icon_layout_fc.ids.scrollview.do_scroll_y = False

    def enable_scroll_on_enter(self, *args):

        print("Enable usb: screen: " + str(self.sm.current))
        print("Enable usb: transition: " + str(self.sm.transition.is_active))
        print("Enable usb: animation: " + str(self.sm.transition._anim))

        if self.sm.current == 'usb_filechooser' and (not self.sm.transition.is_active) and (self.sm.transition._anim == None):

            print('ENABLE SCROLL - USB')
            self.list_layout_fc.ids.scrollview.do_scroll_y = True
            self.icon_layout_fc.ids.scrollview.do_scroll_y = True

            if self.enable_scroll_event != None: Clock.unschedule(self.enable_scroll_event)
