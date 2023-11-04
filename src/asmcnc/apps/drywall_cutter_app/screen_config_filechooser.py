# -*- coding: utf-8 -*-
'''
Created on 19 Aug 2017

@author: Ed

Screen allows user to select their job for loading into easycut, either from JobCache or from a memory stick.
'''
# config

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty  # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

import sys, os
from os.path import expanduser
from shutil import copy
from itertools import takewhile
from chardet import detect

from asmcnc.comms import usb_storage
from asmcnc.skavaUI import screen_file_loading
from asmcnc.skavaUI import popup_info

Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex

<ConfigFileChooser>:

    on_enter: root.refresh_filechooser()

    filechooser : filechooser
    icon_layout_fc : icon_layout_fc
    list_layout_fc : list_layout_fc
    metadata_preview : metadata_preview
    toggle_view_button : toggle_view_button
    sort_button : sort_button
    load_button : load_button
    delete_selected_button : delete_selected_button
    delete_all_button : delete_all_button
    image_view : image_view
    image_sort: image_sort
    image_delete : image_delete
    image_delete_all : image_delete_all
    image_select : image_select
    file_selected_label : file_selected_label
    usb_status_label : usb_status_label

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
                font_size: '18sp'   
                valign: 'middle'
                halign: 'center'
                bold: True

            BoxLayout: 
                orientation: 'horizontal'
                size_hint_y: 5

                FileChooser:
                    id: filechooser
                    rootpath: './asmcnc/apps/drywall_cutter_app/config/configurations/'
                    show_hidden: False
                    filters: ['*.json']
                    on_selection: root.refresh_filechooser()
                    sort_func: root.sort_by_date_reverse
                    FileChooserIconLayout
                        id: icon_layout_fc
                    FileChooserListLayout
                        id: list_layout_fc

                ScrollView:
                    size_hint: 1, 1
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    do_scroll_x: True
                    do_scroll_y: True
                    scroll_type: ['bars', 'content']

                    Label:
                        id: metadata_preview
                        size_hint_y: None
                        height: self.texture_size[1]
                        text_size: self.width, None
                        padding: 10, 10
                        markup: True


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

            Button:
                id: sort_button
                size_hint_x: 1
                on_press: root.switch_sort()
                background_color: hex('#FFFFFF00')
                BoxLayout:
                    padding: 25
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_sort
                        source: "./asmcnc/skavaUI/img/file_select_sort_down_date.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

            Button:
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
                    
            Button:
                disabled: True
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
                    root.load_config_and_return_to_dwt()
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

configs_dir = './asmcnc/apps/drywall_cutter_app/config/configurations/'  # where job files are cached for selection (for last used history/easy access)


def date_order_sort(files, filesystem):
    return (sorted(f for f in files if filesystem.is_dir(f)) +
            sorted((f for f in files if not filesystem.is_dir(f)), key=lambda fi: os.stat(fi).st_mtime, reverse=False))


def date_order_sort_reverse(files, filesystem):
    return (sorted(f for f in files if filesystem.is_dir(f)) +
            sorted((f for f in files if not filesystem.is_dir(f)), key=lambda fi: os.stat(fi).st_mtime, reverse=True))


def name_order_sort(files, filesystem):
    return (sorted(f for f in files if filesystem.is_dir(f)) +
            sorted(f for f in files if not filesystem.is_dir(f)))


def name_order_sort_reverse(files, filesystem):
    return (sorted(f for f in files if filesystem.is_dir(f)) +
            sorted((f for f in files if not filesystem.is_dir(f)), reverse=True))


decode_and_encode = lambda x: (unicode(x, detect(x)['encoding'] or 'utf-8').encode('utf-8'))


class ConfigFileChooser(Screen):
    filename_selected_label_text = StringProperty()

    sort_by_date = ObjectProperty(date_order_sort)
    sort_by_date_reverse = ObjectProperty(date_order_sort_reverse)
    sort_by_name = ObjectProperty(name_order_sort)
    sort_by_name_reverse = ObjectProperty(name_order_sort_reverse)
    is_filechooser_scrolling = False

    def __init__(self, **kwargs):
        super(ConfigFileChooser, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.l = kwargs['localization']
        self.callback = kwargs['callback']
        self.usb_stick = usb_storage.USB_storage(self.sm,
                                                 self.l)  # object to manage presence of USB stick (fun in Linux)

        self.check_for_job_cache_dir()

        self.usb_status_label.text = self.l.get_str("USB connected: Please do not remove USB until file is loaded.")

        # MANAGING KIVY SCROLL BUG

        self.list_layout_fc.ids.scrollview.bind(on_scroll_stop=self.scrolling_stop)
        self.list_layout_fc.ids.scrollview.bind(on_scroll_start=self.scrolling_start)
        self.icon_layout_fc.ids.scrollview.bind(on_scroll_stop=self.scrolling_stop)
        self.icon_layout_fc.ids.scrollview.bind(on_scroll_start=self.scrolling_start)

        self.list_layout_fc.ids.scrollview.effect_cls = kivy.effects.scroll.ScrollEffect
        self.icon_layout_fc.ids.scrollview.effect_cls = kivy.effects.scroll.ScrollEffect

        self.icon_layout_fc.ids.scrollview.funbind('scroll_y', self.icon_layout_fc.ids.scrollview._update_effect_bounds)
        self.list_layout_fc.ids.scrollview.funbind('scroll_y', self.list_layout_fc.ids.scrollview._update_effect_bounds)
        self.icon_layout_fc.ids.scrollview.fbind('scroll_y', self.alternate_update_effect_bounds_icon)
        self.list_layout_fc.ids.scrollview.fbind('scroll_y', self.alternate_update_effect_bounds_list)

    def alternate_update_effect_bounds_icon(self, *args):
        self.update_y_bounds_try_except(self.icon_layout_fc.ids.scrollview)

    def alternate_update_effect_bounds_list(self, *args):
        self.update_y_bounds_try_except(self.list_layout_fc.ids.scrollview)

    def update_y_bounds_try_except(sefl, scrollview_object):

        try:
            if not scrollview_object._viewport or not scrollview_object.effect_y:
                return
            scrollable_height = scrollview_object.height - scrollview_object.viewport_size[1]
            scrollview_object.effect_y.min = 0 if scrollable_height < 0 else scrollable_height
            scrollview_object.effect_y.max = scrollable_height
            scrollview_object.effect_y.value = scrollview_object.effect_y.max * scrollview_object.scroll_y

        except:
            pass

    def scrolling_start(self, *args):
        self.is_filechooser_scrolling = True

    def scrolling_stop(self, *args):
        self.is_filechooser_scrolling = False

    # SCREEN FUNCTIONS

    def check_for_job_cache_dir(self):
        if not os.path.exists(configs_dir):
            os.mkdir(configs_dir)

            if not os.path.exists(configs_dir + '.gitignore'):
                file = open(configs_dir + '.gitignore', "w+")
                file.write('*.json')
                file.close()

    def on_enter(self):

        self.filechooser.path = configs_dir  # Filechooser path reset to root on each re-entry, so user doesn't start at bottom of previously selected folder
        # self.usb_stick.enable()  # start the object scanning for USB stick
        self.refresh_filechooser()
        # self.check_USB_status(1)
        # self.poll_USB = Clock.schedule_interval(self.check_USB_status, 0.25)  # poll status to update button
        self.switch_view()

    def switch_view(self):

        if self.toggle_view_button.state == "normal":
            self.filechooser.view_mode = 'icon'
            self.image_view.source = "./asmcnc/skavaUI/img/file_select_list_view.png"

        elif self.toggle_view_button.state == "down":
            self.filechooser.view_mode = 'list'
            self.image_view.source = "./asmcnc/skavaUI/img/file_select_list_icon.png"

    def switch_sort(self):

        if self.filechooser.sort_func == self.sort_by_date_reverse:
            self.filechooser.sort_func = self.sort_by_date
            self.image_sort.source = "./asmcnc/skavaUI/img/file_select_sort_up_name.png"

        elif self.filechooser.sort_func == self.sort_by_date:
            self.filechooser.sort_func = self.sort_by_name
            self.image_sort.source = "./asmcnc/skavaUI/img/file_select_sort_down_name.png"

        elif self.filechooser.sort_func == self.sort_by_name:
            self.filechooser.sort_func = self.sort_by_name_reverse
            self.image_sort.source = "./asmcnc/skavaUI/img/file_select_sort_up_date.png"

        elif self.filechooser.sort_func == self.sort_by_name_reverse:
            self.filechooser.sort_func = self.sort_by_date_reverse
            self.image_sort.source = "./asmcnc/skavaUI/img/file_select_sort_down_date.png"

        self.filechooser._update_files()

    def open_USB(self):
        if not self.is_filechooser_scrolling:
            self.sm.get_screen('usb_filechooser').set_USB_path(self.usb_stick.get_path())
            self.sm.get_screen('usb_filechooser').usb_stick = self.usb_stick
            self.sm.current = 'usb_filechooser'

    def refresh_filechooser(self):

        self.filechooser._update_item_selection()

        try:
            if self.filechooser.selection[0] != 'C':
                self.display_selected_file()

            else:

                self.load_button.disabled = True
                self.image_select.source = './asmcnc/skavaUI/img/file_select_select_disabled.png'

                self.delete_selected_button.disabled = True
                self.image_delete.source = './asmcnc/skavaUI/img/file_select_delete_disabled.png'

                self.file_selected_label.text = self.l.get_str("Press the icon to display the full filename here.")
                self.metadata_preview.text = self.l.get_str("Select a file to see metadata or gcode preview.")

        except:
            self.load_button.disabled = True
            self.image_select.source = './asmcnc/skavaUI/img/file_select_select_disabled.png'
            self.file_selected_label.text = self.l.get_str("Press the icon to display the full filename here.")
            self.metadata_preview.text = self.l.get_str("Select a file to see metadata or gcode preview.")

            self.delete_selected_button.disabled = True
            self.image_delete.source = './asmcnc/skavaUI/img/file_select_delete_disabled.png'
            self.file_selected_label.text = self.l.get_str("Press the icon to display the full filename here.")
            self.metadata_preview.text = self.l.get_str("Select a file to see metadata or gcode preview.")

        self.filechooser._update_files()

    def display_selected_file(self):

        # display file selected in the filename display label
        if sys.platform == 'win32':
            self.file_selected_label.text = self.filechooser.selection[0].split("\\")[-1]
        else:
            self.file_selected_label.text = self.filechooser.selection[0].split("/")[-1]

        self.get_metadata()

        self.load_button.disabled = False
        self.image_select.source = './asmcnc/skavaUI/img/file_select_select.png'

        self.delete_selected_button.disabled = False
        self.image_delete.source = './asmcnc/skavaUI/img/file_select_delete.png'

    def get_metadata(self):

        def not_end_of_metadata(x):
            if "(End of YetiTool SmartBench MES-Data)" in x:
                return False
            else:
                return True

        def format_metadata(y):
            mini_list = y.split(': ')
            return str(self.l.get_bold(mini_list[0]) + '[b]: [/b]' + mini_list[1])

        try:

            # with codecs.open(self.filechooser.selection[0], encoding='utf-8') as previewed_file:
            with open(self.filechooser.selection[0]) as previewed_file:

                try:

                    if '(YetiTool SmartBench MES-Data)' in previewed_file.readline():
                        metadata_or_gcode_preview = map(format_metadata, [decode_and_encode(i).strip('\n\r()') for i in
                                                                          takewhile(not_end_of_metadata, previewed_file)
                                                                          if
                                                                          (decode_and_encode(i).split(':', 1)[1]).strip(
                                                                              '\n\r() ')])

                    else:
                        # just get GCode preview if no metadata
                        previewed_file.seek(0)
                        metadata_or_gcode_preview = [self.l.get_bold("G-Code Preview (first 20 lines)"), ""] + [
                            (decode_and_encode(next(previewed_file, "")).strip('\n\r')) for x in xrange(20)]

                    self.metadata_preview.text = '\n'.join(metadata_or_gcode_preview)

                except:
                    self.metadata_preview.text = self.l.get_bold("Could not preview file.")

        except:
            self.metadata_preview.text = self.l.get_bold("Could not open file.")

    def load_config_and_return_to_dwt(self):
        self.callback(self.filechooser.selection[0])

        self.sm.current = 'drywall_cutter'

    def delete_popup(self, **kwargs):

        if kwargs['file_selection'] == 'all':
            popup_info.PopupDeleteFile(screen_manager=self.sm, localization=self.l, function=self.delete_all,
                                       file_selection='all')
        else:
            popup_info.PopupDeleteFile(screen_manager=self.sm, localization=self.l, function=self.delete_selected,
                                       file_selection=kwargs['file_selection'])

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
        files_in_cache = os.listdir(configs_dir)  # clean cache
        self.refresh_filechooser()

        if files_in_cache:
            for file in files_in_cache:
                try:
                    os.remove(configs_dir + file)
                    if files_in_cache.index(file) + 2 >= len(files_in_cache):
                        self.refresh_filechooser()

                except:
                    print "attempt to delete folder, or undeletable file"

        self.filechooser.selection = []
        self.refresh_filechooser()

    def quit_to_home(self):
        if not self.is_filechooser_scrolling:
            self.sm.current = 'home'
