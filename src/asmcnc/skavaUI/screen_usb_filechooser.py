# -*- coding: utf-8 -*-
"""
Created on 19 Aug 2017

@author: Ed
"""
import os
import sys
from itertools import takewhile
from os import path
from shutil import copy

import kivy
from chardet import detect
from asmcnc.comms.logging_system.logging_system import Logger
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.properties import (
    ObjectProperty,
    StringProperty,
)
from kivy.uix.screenmanager import Screen

Builder.load_string(
    """

<USBFileChooser>:

    on_enter: root.refresh_filechooser()

    file_selected_label : file_selected_label
    filechooser_usb : filechooser_usb
    metadata_preview : metadata_preview
    icon_layout_fc : icon_layout_fc
    list_layout_fc : list_layout_fc
    toggle_view_button : toggle_view_button
    sort_button: sort_button
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
            font_size: str(0.01875 * app.width) + 'sp'
            canvas.before:
                Color:
                    rgba: hex('#333333FF')
                Rectangle:
                    size: self.size
                    pos: self.pos
            id: usb_status_label
            size_hint_y: 0.7
            markup: True
            font_size: str(0.0225*app.width) + 'sp'   
            valign: 'middle'
            halign: 'left'
            text_size: self.size
            padding:[dp(0.0125)*app.width, 0]

        Label:
            font_size: str(0.01875 * app.width) + 'sp'
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
            font_size: str(0.025*app.width) + 'sp'   
            valign: 'middle'
            halign: 'center' 
            bold: True               

        BoxLayout: 
            orientation: 'horizontal'
            size_hint_y: 5

            FileChooser:
                padding:[0, dp(0.0208333333333)*app.height]
                id: filechooser_usb
                show_hidden: False
                filters: ['*.nc','*.NC','*.gcode','*.GCODE','*.GCode','*.Gcode','*.gCode']
                on_selection: root.refresh_filechooser()
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
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: metadata_preview
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None
                    padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                    markup: True
               
        BoxLayout:
            size_hint_y: None
            height: dp(100.0/480.0)*app.height

            ToggleButton:
                font_size: str(0.01875 * app.width) + 'sp'
                id: toggle_view_button
                size_hint_x: 1
                on_press: root.switch_view()
                background_color: hex('#FFFFFF00')
                BoxLayout:
                    padding:[dp(0.03125)*app.width, dp(0.0520833333333)*app.height]
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
                font_size: str(0.01875 * app.width) + 'sp'
                id: sort_button
                size_hint_x: 1
                on_press: root.switch_sort()
                background_color: hex('#FFFFFF00')
                BoxLayout:
                    padding:[dp(0.03125)*app.width, dp(0.0520833333333)*app.height]
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
                font_size: str(0.01875 * app.width) + 'sp'
                disabled: False
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    root.refresh_filechooser() 
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    self.background_color = hex('#FFFFFFFF')
                BoxLayout:
                    padding:[dp(0.03125)*app.width, dp(0.0520833333333)*app.height]
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
                font_size: str(0.01875 * app.width) + 'sp'
                disabled: False
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    root.quit_to_local()
                    self.background_color = hex('#FFFFFFFF')
                BoxLayout:
                    padding:[dp(0.03125)*app.width, dp(0.0520833333333)*app.height]
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
                font_size: str(0.01875 * app.width) + 'sp'
                id: load_button
                disabled: True
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    root.import_usb_file()
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    self.background_color = hex('#FFFFFFFF')
                BoxLayout:
                    padding:[dp(0.03125)*app.width, dp(0.0520833333333)*app.height]
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
verbose = True


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


class USBFileChooser(Screen):
    filename_selected_label_text = StringProperty()
    usb_stick = ObjectProperty()
    sort_by_date = ObjectProperty(date_order_sort)
    sort_by_date_reverse = ObjectProperty(date_order_sort_reverse)
    is_filechooser_scrolling = False

    def __init__(self, **kwargs):
        super(USBFileChooser, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.jd = kwargs["job"]
        self.l = kwargs["localization"]
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

    def set_USB_path(self, usb_path):
        self.usb_path = usb_path
        self.filechooser_usb.rootpath = usb_path
        if verbose:
            Logger.debug("Filechooser_usb path: " + self.filechooser_usb.path)

    def on_enter(self):
        self.filechooser_usb.path = self.usb_path
        self.refresh_filechooser()
        self.filename_selected_label_text = self.l.get_str(
            "Press the icon to display the full filename here."
        )
        self.update_usb_status()
        self.switch_view()

    def on_pre_leave(self):
        self.sm.get_screen(
            "local_filechooser"
        ).filechooser.sort_func = self.filechooser_usb.sort_func
        self.sm.get_screen(
            "local_filechooser"
        ).image_sort.source = self.image_sort.source
        if self.sm.current != "local_filechooser":
            self.usb_stick.disable()

    def check_for_job_cache_dir(self):
        if not path.exists(job_cache_dir):
            os.mkdir(job_cache_dir)
            if not path.exists(job_cache_dir + ".gitignore"):
                file = open(job_cache_dir + ".gitignore", "w+")
                file.write("*.nc")
                file.close()

    def update_usb_status(self):
        try:
            if self.usb_stick.is_available():
                self.usb_status_label.size_hint_y = 0.7
                self.usb_status_label.text = self.l.get_str(
                    "USB connected: Please do not remove USB until file is loaded."
                )
                self.usb_status_label.canvas.before.clear()
                with self.usb_status_label.canvas.before:
                    Color(76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0)
                    Rectangle(
                        pos=self.usb_status_label.pos, size=self.usb_status_label.size
                    )
            else:
                self.usb_status_label.text = self.l.get_str(
                    "USB removed! Files will not load properly."
                )
                self.usb_status_label.size_hint_y = 0.7
                self.usb_status_label.canvas.before.clear()
                with self.usb_status_label.canvas.before:
                    Color(230 / 255.0, 74 / 255.0, 25 / 255.0, 1.0)
                    Rectangle(
                        pos=self.usb_status_label.pos, size=self.usb_status_label.size
                    )
        except:
            pass

    def switch_view(self):
        if self.toggle_view_button.state == "normal":
            self.filechooser_usb.view_mode = "icon"
            self.image_view.source = "./asmcnc/skavaUI/img/file_select_list_view.png"
        elif self.toggle_view_button.state == "down":
            self.filechooser_usb.view_mode = "list"
            self.image_view.source = "./asmcnc/skavaUI/img/file_select_list_icon.png"

    def switch_sort(self):
        if (
            self.filechooser_usb.sort_func
            == self.sm.get_screen("local_filechooser").sort_by_date_reverse
        ):
            self.filechooser_usb.sort_func = self.sm.get_screen(
                "local_filechooser"
            ).sort_by_date
            self.image_sort.source = "./asmcnc/skavaUI/img/file_select_sort_up_name.png"
        elif (
            self.filechooser_usb.sort_func
            == self.sm.get_screen("local_filechooser").sort_by_date
        ):
            self.filechooser_usb.sort_func = self.sm.get_screen(
                "local_filechooser"
            ).sort_by_name
            self.image_sort.source = (
                "./asmcnc/skavaUI/img/file_select_sort_down_name.png"
            )
        elif (
            self.filechooser_usb.sort_func
            == self.sm.get_screen("local_filechooser").sort_by_name
        ):
            self.filechooser_usb.sort_func = self.sm.get_screen(
                "local_filechooser"
            ).sort_by_name_reverse
            self.image_sort.source = "./asmcnc/skavaUI/img/file_select_sort_up_date.png"
        elif (
            self.filechooser_usb.sort_func
            == self.sm.get_screen("local_filechooser").sort_by_name_reverse
        ):
            self.filechooser_usb.sort_func = self.sm.get_screen(
                "local_filechooser"
            ).sort_by_date_reverse
            self.image_sort.source = (
                "./asmcnc/skavaUI/img/file_select_sort_down_date.png"
            )
        self.filechooser_usb._update_files()

    def refresh_filechooser(self):
        if verbose:
            Logger.debug("Refreshing filechooser")
        try:
            if self.filechooser_usb.selection[0] != "C":
                self.display_selected_file()
            else:
                self.loadButton.disabled = True
                self.image_select.source = (
                    "./asmcnc/skavaUI/img/file_select_select_disabled.png"
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
        self.filechooser_usb._update_files()

    def display_selected_file(self):
        if sys.platform == "win32":
            self.file_selected_label.text = self.filechooser_usb.selection[0].split(
                "\\"
            )[-1]
        else:
            self.file_selected_label.text = self.filechooser_usb.selection[0].split(
                "/"
            )[-1]
        self.get_metadata()
        self.load_button.disabled = False
        self.image_select.source = "./asmcnc/skavaUI/img/file_select_select.png"

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
            with open(self.filechooser_usb.selection[0]) as previewed_file:
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

    def import_usb_file(self):
        file_selection = self.filechooser_usb.selection[0]
        self.check_for_job_cache_dir()
        if os.path.isfile(file_selection):
            copy(file_selection, job_cache_dir)
            file_name = os.path.basename(file_selection)
            new_file_path = job_cache_dir + file_name
            Logger.info(new_file_path)
            self.go_to_loading_screen(new_file_path)

    def quit_to_local(self):
        if not self.is_filechooser_scrolling:
            self.sm.current = "local_filechooser"

    def go_to_loading_screen(self, file_selection):
        if not self.is_filechooser_scrolling:
            self.jd.reset_values()
            self.jd.set_job_filename(file_selection)
            self.manager.current = "loading"
