# -*- coding: utf-8 -*-
"""
Created on 19 Aug 2017

@author: Ed

Screen allows user to select their job for loading into easycut, either from JobCache or from a memory stick.
"""
import os
import sys
from itertools import takewhile
from shutil import copy

import kivy
from chardet import detect
from asmcnc.comms.logging_system.logging_system import Logger
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.properties import (
    ObjectProperty,
    StringProperty,
)
from kivy.uix.screenmanager import Screen

from asmcnc.comms import usb_storage
from asmcnc.comms.model_manager import ModelManagerSingleton
from asmcnc.skavaUI import popup_info

Builder.load_string(
    """

#:import hex kivy.utils.get_color_from_hex

<LocalFileChooser>:

    on_enter: root.refresh_filechooser()

    filechooser : filechooser
    icon_layout_fc : icon_layout_fc
    list_layout_fc : list_layout_fc
    metadata_preview : metadata_preview
    toggle_view_button : toggle_view_button
    sort_button : sort_button
    button_usb : button_usb
    load_button : load_button
    delete_selected_button : delete_selected_button
    delete_all_button : delete_all_button
    image_view : image_view
    image_sort: image_sort
    image_usb : image_usb
    image_delete : image_delete
    image_delete_all : image_delete_all
    image_select : image_select
    file_selected_label : file_selected_label
    usb_status_label : usb_status_label

    BoxLayout:
        padding: 0
        spacing: app.get_scaled_width(9.99999999998)
        size: root.size
        pos: root.pos
        orientation: "vertical"

        BoxLayout:
            orientation: 'vertical'
            size: self.parent.size
            pos: self.parent.pos
            spacing: 0

            Label:
                font_size: app.get_scaled_sp('15.0sp')
                id: usb_status_label
                canvas.before:
                    Color:
                        rgba: hex('#333333FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos
                size_hint_y: 0.7
                markup: True
                font_size: app.get_scaled_sp('18.0sp')
                valign: 'middle'
                halign: 'left'
                text_size: self.size
                padding: app.get_scaled_tuple([10.0, 0.0])

            Label:
                font_size: app.get_scaled_sp('15.0sp')
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
                font_size: app.get_scaled_sp('18.0sp')
                valign: 'middle'
                halign: 'center'
                bold: True

            BoxLayout: 
                orientation: 'horizontal'
                size_hint_y: 5

                FileChooser:
                    id: filechooser
                    rootpath: './jobCache/'
                    show_hidden: False
                    filters: ['*.nc','*.NC','*.gcode','*.GCODE','*.GCode','*.Gcode','*.gCode']
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
                        font_size: app.get_scaled_sp('15.0sp')
                        id: metadata_preview
                        size_hint_y: None
                        height: self.texture_size[1]
                        text_size: self.width, None
                        padding: app.get_scaled_tuple([10.0, 10.0])
                        markup: True
               

        BoxLayout:
            size_hint_y: None
            height: app.get_scaled_height(100.0)

            ToggleButton:
                font_size: app.get_scaled_sp('15.0sp')
                id: toggle_view_button
                size_hint_x: 1
                on_press: root.switch_view()
                background_color: hex('#FFFFFF00')
                BoxLayout:
                    padding: app.get_scaled_tuple([25.0, 25.0])
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
                font_size: app.get_scaled_sp('15.0sp')
                id: sort_button
                size_hint_x: 1
                on_press: root.switch_sort()
                background_color: hex('#FFFFFF00')
                BoxLayout:
                    padding: app.get_scaled_tuple([25.0, 25.0])
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
                font_size: app.get_scaled_sp('15.0sp')
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
                    padding: app.get_scaled_tuple([25.0, 25.0])
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
                font_size: app.get_scaled_sp('15.0sp')
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
                    padding: app.get_scaled_tuple([25.0, 25.0])
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
                font_size: app.get_scaled_sp('15.0sp')
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
                    padding: app.get_scaled_tuple([25.0, 25.0])
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
                font_size: app.get_scaled_sp('15.0sp')
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
                    padding: app.get_scaled_tuple([25.0, 25.0])
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
                font_size: app.get_scaled_sp('15.0sp')
                disabled: False
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    root.quit_to_home()
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    self.background_color = hex('#FFFFFFFF')
                BoxLayout:
                    padding: app.get_scaled_tuple([25.0, 25.0])
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
                font_size: app.get_scaled_sp('15.0sp')
                id: load_button
                disabled: True
                size_hint_x: 1
                on_release: 
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    root.go_to_loading_screen()
                    self.background_color = hex('#FFFFFFFF')
                BoxLayout:
                    padding: app.get_scaled_tuple([25.0, 25.0])
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_select
                        source: "./asmcnc/skavaUI/img/file_select_select_disabled.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 

                
"""
)
job_cache_dir = "./jobCache/"
job_q_dir = "./jobQ/"
ftp_file_dir = "../../router_ftp/"


def date_order_sort(files, filesystem):
    return sorted(f for f in files if filesystem.is_dir(f)) + sorted(
        (f for f in files if not filesystem.is_dir(f)),
        key=lambda fi: os.stat(fi).st_mtime,
        reverse=False,
    )


def date_order_sort_reverse(files, filesystem):
    return sorted(f for f in files if filesystem.is_dir(f)) + sorted(
        (f for f in files if not filesystem.is_dir(f)),
        key=lambda fi: os.stat(fi).st_mtime,
        reverse=True,
    )


def name_order_sort(files, filesystem):
    return sorted(f for f in files if filesystem.is_dir(f)) + sorted(
        f for f in files if not filesystem.is_dir(f)
    )


def name_order_sort_reverse(files, filesystem):
    return sorted(f for f in files if filesystem.is_dir(f)) + sorted(
        (f for f in files if not filesystem.is_dir(f)), reverse=True
    )


decode_and_encode = lambda x: unicode(x, detect(x)["encoding"] or "utf-8").encode(
    "utf-8"
)


class LocalFileChooser(Screen):
    filename_selected_label_text = StringProperty()
    sort_by_date = ObjectProperty(date_order_sort)
    sort_by_date_reverse = ObjectProperty(date_order_sort_reverse)
    sort_by_name = ObjectProperty(name_order_sort)
    sort_by_name_reverse = ObjectProperty(name_order_sort_reverse)
    is_filechooser_scrolling = False

    def __init__(self, **kwargs):
        super(LocalFileChooser, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.jd = kwargs["job"]
        self.l = kwargs["localization"]
        self.model_manager = ModelManagerSingleton()
        self.usb_stick = usb_storage.USB_storage(self.sm, self.l)
        self.check_for_job_cache_dir()
        self.usb_status_label.text = self.l.get_str(
            "USB connected: Please do not remove USB until file is loaded."
        )
        self.list_layout_fc.ids.scrollview.bind(on_scroll_stop=self.scrolling_stop)
        self.list_layout_fc.ids.scrollview.bind(on_scroll_start=self.scrolling_start)
        self.icon_layout_fc.ids.scrollview.bind(on_scroll_stop=self.scrolling_stop)
        self.icon_layout_fc.ids.scrollview.bind(on_scroll_start=self.scrolling_start)
        self.list_layout_fc.ids.scrollview.effect_cls = kivy.effects.scroll.ScrollEffect
        self.icon_layout_fc.ids.scrollview.effect_cls = kivy.effects.scroll.ScrollEffect
        self.icon_layout_fc.ids.scrollview.funbind(
            "scroll_y", self.icon_layout_fc.ids.scrollview._update_effect_bounds
        )
        self.list_layout_fc.ids.scrollview.funbind(
            "scroll_y", self.list_layout_fc.ids.scrollview._update_effect_bounds
        )
        self.icon_layout_fc.ids.scrollview.fbind(
            "scroll_y", self.alternate_update_effect_bounds_icon
        )
        self.list_layout_fc.ids.scrollview.fbind(
            "scroll_y", self.alternate_update_effect_bounds_list
        )

    def alternate_update_effect_bounds_icon(self, *args):
        self.update_y_bounds_try_except(self.icon_layout_fc.ids.scrollview)

    def alternate_update_effect_bounds_list(self, *args):
        self.update_y_bounds_try_except(self.list_layout_fc.ids.scrollview)

    def update_y_bounds_try_except(sefl, scrollview_object):
        try:
            if not scrollview_object._viewport or not scrollview_object.effect_y:
                return
            scrollable_height = (
                scrollview_object.height - scrollview_object.viewport_size[1]
            )
            scrollview_object.effect_y.min = (
                0 if scrollable_height < 0 else scrollable_height
            )
            scrollview_object.effect_y.max = scrollable_height
            scrollview_object.effect_y.value = (
                scrollview_object.effect_y.max * scrollview_object.scroll_y
            )
        except:
            pass

    def scrolling_start(self, *args):
        self.is_filechooser_scrolling = True

    def scrolling_stop(self, *args):
        self.is_filechooser_scrolling = False

    def check_for_job_cache_dir(self):
        if not os.path.exists(job_cache_dir):
            os.mkdir(job_cache_dir)
            if not os.path.exists(job_cache_dir + ".gitignore"):
                file = open(job_cache_dir + ".gitignore", "w+")
                file.write("*.nc")
                file.close()

    def on_pre_enter(self):
        if self.model_manager.is_machine_drywall():
            self.button_usb.opacity = 0
            self.usb_status_label.opacity = 0
    def on_enter(self):
        self.filechooser.path = job_cache_dir
        if not self.model_manager.is_machine_drywall():
            self.usb_stick.enable()
        self.refresh_filechooser()
        if not self.model_manager.is_machine_drywall():
            self.check_USB_status(1)
            self.poll_USB = Clock.schedule_interval(self.check_USB_status, 0.25)
        self.switch_view()

    def on_pre_leave(self):
        self.sm.get_screen(
            "usb_filechooser"
        ).filechooser_usb.sort_func = self.filechooser.sort_func
        self.sm.get_screen("usb_filechooser").image_sort.source = self.image_sort.source
        if not self.model_manager.is_machine_drywall():
            Clock.unschedule(self.poll_USB)
            if self.sm.current != "usb_filechooser":
                self.usb_stick.disable()

    def on_leave(self):
        self.usb_status_label.size_hint_y = 0

    def check_USB_status(self, dt):
        if not self.is_filechooser_scrolling:
            if self.usb_stick.is_available():
                self.button_usb.disabled = False
                self.image_usb.source = "./asmcnc/skavaUI/img/file_select_usb.png"
                self.sm.get_screen("loading").usb_status_label.opacity = 1
                self.usb_status_label.size_hint_y = 0.7
                self.usb_status_label.canvas.before.clear()
                with self.usb_status_label.canvas.before:
                    Color(76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0)
                    Rectangle(
                        pos=self.usb_status_label.pos, size=self.usb_status_label.size
                    )
            else:
                self.button_usb.disabled = True
                self.image_usb.source = (
                    "./asmcnc/skavaUI/img/file_select_usb_disabled.png"
                )
                self.usb_status_label.size_hint_y = 0
                self.sm.get_screen("loading").usb_status = None
                self.sm.get_screen("loading").usb_status_label.opacity = 0

    def switch_view(self):
        if self.toggle_view_button.state == "normal":
            self.filechooser.view_mode = "icon"
            self.image_view.source = "./asmcnc/skavaUI/img/file_select_list_view.png"
        elif self.toggle_view_button.state == "down":
            self.filechooser.view_mode = "list"
            self.image_view.source = "./asmcnc/skavaUI/img/file_select_list_icon.png"

    def switch_sort(self):
        if self.filechooser.sort_func == self.sort_by_date_reverse:
            self.filechooser.sort_func = self.sort_by_date
            self.image_sort.source = "./asmcnc/skavaUI/img/file_select_sort_up_name.png"
        elif self.filechooser.sort_func == self.sort_by_date:
            self.filechooser.sort_func = self.sort_by_name
            self.image_sort.source = (
                "./asmcnc/skavaUI/img/file_select_sort_down_name.png"
            )
        elif self.filechooser.sort_func == self.sort_by_name:
            self.filechooser.sort_func = self.sort_by_name_reverse
            self.image_sort.source = "./asmcnc/skavaUI/img/file_select_sort_up_date.png"
        elif self.filechooser.sort_func == self.sort_by_name_reverse:
            self.filechooser.sort_func = self.sort_by_date_reverse
            self.image_sort.source = (
                "./asmcnc/skavaUI/img/file_select_sort_down_date.png"
            )
        self.filechooser._update_files()

    def open_USB(self):
        if not self.is_filechooser_scrolling:
            self.sm.get_screen("usb_filechooser").set_USB_path(
                self.usb_stick.get_path()
            )
            self.sm.get_screen("usb_filechooser").usb_stick = self.usb_stick
            self.sm.current = "usb_filechooser"

    def refresh_filechooser(self):
        self.filechooser._update_item_selection()
        try:
            if self.filechooser.selection[0] != "C":
                self.display_selected_file()
            else:
                self.load_button.disabled = True
                self.image_select.source = (
                    "./asmcnc/skavaUI/img/file_select_select_disabled.png"
                )
                self.delete_selected_button.disabled = True
                self.image_delete.source = (
                    "./asmcnc/skavaUI/img/file_select_delete_disabled.png"
                )
                self.file_selected_label.text = self.l.get_str(
                    "Press the icon to display the full filename here."
                )
                self.metadata_preview.text = self.l.get_str(
                    "Select a file to see metadata or gcode preview."
                )
        except:
            self.load_button.disabled = True
            self.image_select.source = (
                "./asmcnc/skavaUI/img/file_select_select_disabled.png"
            )
            self.file_selected_label.text = self.l.get_str(
                "Press the icon to display the full filename here."
            )
            self.metadata_preview.text = self.l.get_str(
                "Select a file to see metadata or gcode preview."
            )
            self.delete_selected_button.disabled = True
            self.image_delete.source = (
                "./asmcnc/skavaUI/img/file_select_delete_disabled.png"
            )
            self.file_selected_label.text = self.l.get_str(
                "Press the icon to display the full filename here."
            )
            self.metadata_preview.text = self.l.get_str(
                "Select a file to see metadata or gcode preview."
            )
        self.filechooser._update_files()

    def display_selected_file(self):
        if sys.platform == "win32":
            self.file_selected_label.text = self.filechooser.selection[0].split("\\")[
                -1
            ]
        else:
            self.file_selected_label.text = self.filechooser.selection[0].split("/")[-1]
        self.get_metadata()
        self.load_button.disabled = False
        self.image_select.source = "./asmcnc/skavaUI/img/file_select_select.png"
        self.delete_selected_button.disabled = False
        self.image_delete.source = "./asmcnc/skavaUI/img/file_select_delete.png"

    def get_metadata(self):
        def not_end_of_metadata(x):
            if "(End of YetiTool SmartBench MES-Data)" in x:
                return False
            else:
                return True

        def format_metadata(y):
            mini_list = y.split(": ")
            return str(self.l.get_bold(mini_list[0]) + "[b]: [/b]" + mini_list[1])

        try:
            with open(self.filechooser.selection[0]) as previewed_file:
                try:
                    if "(YetiTool SmartBench MES-Data)" in previewed_file.readline():
                        metadata_or_gcode_preview = map(
                            format_metadata,
                            [
                                decode_and_encode(i).strip("\n\r()")
                                for i in takewhile(not_end_of_metadata, previewed_file)
                                if decode_and_encode(i)
                                .split(":", 1)[1]
                                .strip("\n\r() ")
                            ],
                        )
                    else:
                        previewed_file.seek(0)
                        metadata_or_gcode_preview = [
                            self.l.get_bold("G-Code Preview (first 20 lines)"),
                            "",
                        ] + [
                            decode_and_encode(next(previewed_file, "")).strip("\n\r")
                            for x in xrange(20)
                        ]
                    self.metadata_preview.text = "\n".join(metadata_or_gcode_preview)
                except:
                    self.metadata_preview.text = self.l.get_bold(
                        "Could not preview file."
                    )
        except:
            self.metadata_preview.text = self.l.get_bold("Could not open file.")

    def get_FTP_files(self):
        if sys.platform != "win32":
            ftp_files = os.listdir(ftp_file_dir)
            if ftp_files:
                for file in ftp_files:
                    copy(ftp_file_dir + file, job_cache_dir)
                    os.remove(ftp_file_dir + file)

    def go_to_loading_screen(self):
        file_selection = self.filechooser.selection[0]
        if os.path.isfile(file_selection):
            self.jd.reset_values()
            self.jd.set_job_filename(file_selection)
            self.manager.current = "loading"
        else:
            error_message = self.l.get_str("File selected does not exist!")
            popup_info.PopupError(self.sm, self.l, error_message)

    def delete_popup(self, **kwargs):
        if kwargs["file_selection"] == "all":
            popup_info.PopupDeleteFile(
                screen_manager=self.sm,
                localization=self.l,
                function=self.delete_all,
                file_selection="all",
            )
        else:
            popup_info.PopupDeleteFile(
                screen_manager=self.sm,
                localization=self.l,
                function=self.delete_selected,
                file_selection=kwargs["file_selection"],
            )

    def delete_selected(self, filename):
        self.refresh_filechooser()
        if os.path.isfile(filename):
            try:
                os.remove(filename)
                self.filechooser.selection = []
            except:
                Logger.exception("attempt to delete folder, or undeletable file")
            self.refresh_filechooser()

    def delete_all(self):
        files_in_cache = os.listdir(job_cache_dir)
        self.refresh_filechooser()
        if files_in_cache:
            for file in files_in_cache:
                try:
                    os.remove(job_cache_dir + file)
                    if files_in_cache.index(file) + 2 >= len(files_in_cache):
                        self.refresh_filechooser()
                except:
                    Logger.exception("attempt to delete folder, or undeletable file")
        self.filechooser.selection = []
        self.refresh_filechooser()

    def quit_to_home(self):
        if not self.is_filechooser_scrolling:
            self.sm.current = "home"
