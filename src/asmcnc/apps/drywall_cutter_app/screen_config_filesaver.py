"""
Created on 19 Aug 2017

@author: Ed
edited by Archie 2023 for use in dwt app
"""
import os
import sys
import json
import kivy
from chardet import detect
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen
from asmcnc.comms import usb_storage
from asmcnc.skavaUI import popup_info
Builder.load_string(
    """

#:import hex kivy.utils.get_color_from_hex

<ConfigFileSaver>:

    on_enter: root.refresh_filechooser()

    filechooser : filechooser
    icon_layout_fc : icon_layout_fc
    list_layout_fc : list_layout_fc
    metadata_preview : metadata_preview
    toggle_view_button : toggle_view_button
    sort_button : sort_button
    save_button : save_button
    image_view : image_view
    image_sort: image_sort
    image_select : image_select
    file_selected_label : file_selected_label

    BoxLayout:
        padding: 0
        spacing:0.0208333333333*app.height
        size: root.size
        pos: root.pos
        orientation: "vertical"

        BoxLayout:
            orientation: 'vertical'
            size: self.parent.size
            pos: self.parent.pos
            spacing: 0

            TextInput:
                id: file_selected_label
                size_hint_y: 1
                text: root.filename_selected_label_text
                markup: True
                color: hex('#FFFFFFFF')
                font_size: str(0.0225*app.width) + 'sp'   
                valign: 'middle'
                halign: 'center'
                bold: True
                padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                multiline: False
                size_hint_x: 1

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
                        font_size: str(0.01875 * app.width) + 'sp'
                        id: metadata_preview
                        size_hint_y: None
                        height: self.texture_size[1]
                        text_size: self.width, None
                        padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                        markup: True


        BoxLayout:
            size_hint_y: None
            height: 100

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
                disabled: True
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                BoxLayout:
                    padding:[dp(0.03125)*app.width, dp(0.0520833333333)*app.height]
                    size: self.parent.size
                    pos: self.parent.pos
                    
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                disabled: True
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                BoxLayout:
                    padding:[dp(0.03125)*app.width, dp(0.0520833333333)*app.height]
                    size: self.parent.size
                    pos: self.parent.pos
                    
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                disabled: True
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                BoxLayout:
                    padding:[dp(0.03125)*app.width, dp(0.0520833333333)*app.height]
                    size: self.parent.size
                    pos: self.parent.pos
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                disabled: True
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                BoxLayout:
                    padding:[dp(0.03125)*app.width, dp(0.0520833333333)*app.height]
                    size: self.parent.size
                    pos: self.parent.pos
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                disabled: False
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    root.quit_to_home()
                    self.background_color = hex('#FFFFFF00')
                on_press:
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
                id: save_button
                disabled: False
                size_hint_x: 1
                on_release: 
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    root.save_config_and_return_to_dwt()
                    self.background_color = hex('#FFFFFFFF')
                BoxLayout:
                    padding:[dp(0.03125)*app.width, dp(0.0520833333333)*app.height]
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_select
                        source: "./asmcnc/skavaUI/img/file_select_select.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 


"""
    )
configs_dir = './asmcnc/apps/drywall_cutter_app/config/configurations/'


def date_order_sort(files, filesystem):
    return sorted(f for f in files if filesystem.is_dir(f)) + sorted((f for
        f in files if not filesystem.is_dir(f)), key=lambda fi: os.stat(fi)
        .st_mtime, reverse=False)


def date_order_sort_reverse(files, filesystem):
    return sorted(f for f in files if filesystem.is_dir(f)) + sorted((f for
        f in files if not filesystem.is_dir(f)), key=lambda fi: os.stat(fi)
        .st_mtime, reverse=True)


def name_order_sort(files, filesystem):
    return sorted(f for f in files if filesystem.is_dir(f)) + sorted(f for
        f in files if not filesystem.is_dir(f))


def name_order_sort_reverse(files, filesystem):
    return sorted(f for f in files if filesystem.is_dir(f)) + sorted((f for
        f in files if not filesystem.is_dir(f)), reverse=True)


decode_and_encode = lambda x: unicode(x, detect(x)['encoding'] or 'utf-8'
    ).encode('utf-8')


class ConfigFileSaver(Screen):
    filename_selected_label_text = StringProperty()
    sort_by_date = ObjectProperty(date_order_sort)
    sort_by_date_reverse = ObjectProperty(date_order_sort_reverse)
    sort_by_name = ObjectProperty(name_order_sort)
    sort_by_name_reverse = ObjectProperty(name_order_sort_reverse)
    is_filechooser_scrolling = False
    json_config_order = {u'shape_type': 0, u'units': 1,
        u'canvas_shape_dims': 2, u'cutter_type': 3, u'toolpath_offset': 4,
        u'cutting_depths': 5, u'datum_position': 6}

    def __init__(self, **kwargs):
        super(ConfigFileSaver, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.l = kwargs['localization']
        self.callback = kwargs['callback']
        self.usb_stick = usb_storage.USB_storage(self.sm, self.l)
        self.check_for_job_cache_dir()
        self.list_layout_fc.ids.scrollview.bind(on_scroll_stop=self.
            scrolling_stop)
        self.list_layout_fc.ids.scrollview.bind(on_scroll_start=self.
            scrolling_start)
        self.icon_layout_fc.ids.scrollview.bind(on_scroll_stop=self.
            scrolling_stop)
        self.icon_layout_fc.ids.scrollview.bind(on_scroll_start=self.
            scrolling_start)
        self.list_layout_fc.ids.scrollview.effect_cls = (kivy.effects.
            scroll.ScrollEffect)
        self.icon_layout_fc.ids.scrollview.effect_cls = (kivy.effects.
            scroll.ScrollEffect)
        self.icon_layout_fc.ids.scrollview.funbind('scroll_y', self.
            icon_layout_fc.ids.scrollview._update_effect_bounds)
        self.list_layout_fc.ids.scrollview.funbind('scroll_y', self.
            list_layout_fc.ids.scrollview._update_effect_bounds)
        self.icon_layout_fc.ids.scrollview.fbind('scroll_y', self.
            alternate_update_effect_bounds_icon)
        self.list_layout_fc.ids.scrollview.fbind('scroll_y', self.
            alternate_update_effect_bounds_list)

    def alternate_update_effect_bounds_icon(self, *args):
        self.update_y_bounds_try_except(self.icon_layout_fc.ids.scrollview)

    def alternate_update_effect_bounds_list(self, *args):
        self.update_y_bounds_try_except(self.list_layout_fc.ids.scrollview)

    def update_y_bounds_try_except(sefl, scrollview_object):
        try:
            if (not scrollview_object._viewport or not scrollview_object.
                effect_y):
                return
            scrollable_height = (scrollview_object.height -
                scrollview_object.viewport_size[1])
            scrollview_object.effect_y.min = (0 if scrollable_height < 0 else
                scrollable_height)
            scrollview_object.effect_y.max = scrollable_height
            scrollview_object.effect_y.value = (scrollview_object.effect_y.
                max * scrollview_object.scroll_y)
        except:
            pass

    def scrolling_start(self, *args):
        self.is_filechooser_scrolling = True

    def scrolling_stop(self, *args):
        self.is_filechooser_scrolling = False

    def check_for_job_cache_dir(self):
        if not os.path.exists(configs_dir):
            os.mkdir(configs_dir)
            if not os.path.exists(configs_dir + '.gitignore'):
                file = open(configs_dir + '.gitignore', 'w+')
                file.write('*.json')
                file.close()

    def on_enter(self):
        self.filechooser.path = configs_dir
        self.refresh_filechooser()
        self.switch_view()

    def switch_view(self):
        if self.toggle_view_button.state == 'normal':
            self.filechooser.view_mode = 'icon'
            self.image_view.source = (
                './asmcnc/skavaUI/img/file_select_list_view.png')
        elif self.toggle_view_button.state == 'down':
            self.filechooser.view_mode = 'list'
            self.image_view.source = (
                './asmcnc/skavaUI/img/file_select_list_icon.png')

    def switch_sort(self):
        if self.filechooser.sort_func == self.sort_by_date_reverse:
            self.filechooser.sort_func = self.sort_by_date
            self.image_sort.source = (
                './asmcnc/skavaUI/img/file_select_sort_up_name.png')
        elif self.filechooser.sort_func == self.sort_by_date:
            self.filechooser.sort_func = self.sort_by_name
            self.image_sort.source = (
                './asmcnc/skavaUI/img/file_select_sort_down_name.png')
        elif self.filechooser.sort_func == self.sort_by_name:
            self.filechooser.sort_func = self.sort_by_name_reverse
            self.image_sort.source = (
                './asmcnc/skavaUI/img/file_select_sort_up_date.png')
        elif self.filechooser.sort_func == self.sort_by_name_reverse:
            self.filechooser.sort_func = self.sort_by_date_reverse
            self.image_sort.source = (
                './asmcnc/skavaUI/img/file_select_sort_down_date.png')
        self.filechooser._update_files()

    def refresh_filechooser(self):
        self.filechooser._update_item_selection()
        try:
            if self.filechooser.selection[0] != 'C':
                self.display_selected_file()
            else:
                self.save_button.disabled = False
                self.metadata_preview.text = self.l.get_str(
                    'Select a file to see configuration preview.')
        except:
            self.metadata_preview.text = self.l.get_str(
                'Select a file to see configuration preview.')
        self.filechooser._update_files()

    def display_selected_file(self):
        if sys.platform == 'win32':
            self.file_selected_label.text = self.filechooser.selection[0
                ].split('\\')[-1]
        else:
            self.file_selected_label.text = self.filechooser.selection[0
                ].split('/')[-1]
        with open(self.filechooser.selection[0], 'r') as f:
            json_obj = json.load(f)
        sorted_json = self.sort_json(json_obj)
        self.metadata_preview.text = self.to_human_readable(sorted_json)
        self.image_select.source = (
            './asmcnc/skavaUI/img/file_select_select.png')

    def sort_json(self, json_obj):
        items = json_obj.items()
        items.sort(key=lambda x: self.json_config_order[x[0]])
        return dict(items)

    def to_human_readable(self, json_obj, indent=0):

        def format_key(json_key):
            return json_key.replace('_', ' ').title()
        result = ''
        for key, value in json_obj.items():
            if isinstance(value, dict):
                result += ' ' * indent + format_key(key
                    ) + ':\n' + self.to_human_readable(value, indent + 4)
            else:
                result += ' ' * indent + format_key(key) + ': ' + str(value
                    ) + '\n'
        return result

    def save_config_and_return_to_dwt(self):
        self.callback(self.file_selected_label.text)
        self.sm.current = 'drywall_cutter'

    def quit_to_home(self):
        if not self.is_filechooser_scrolling:
            self.sm.current = 'drywall_cutter'