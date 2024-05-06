"""
Created on 19 Aug 2017
@author: Ed
Screen allows user to select their job for loading into easycut, either from JobCache or from a memory stick.
"""
# config
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock
import sys, os
from os.path import expanduser
from shutil import copy
from asmcnc.comms import usb_storage
from asmcnc.skavaUI import popup_info

Builder.load_string(
    """
<SCFileChooser>:
    on_enter: root.refresh_filechooser()
    filechooser_sc_params:filechooser_sc_params
    toggle_view_button : toggle_view_button
    load_button:load_button
    delete_selected_button:delete_selected_button
    delete_all_button:delete_all_button
    image_delete:image_delete
    image_delete_all:image_delete_all
    image_select:image_select
    image_view : image_view

    BoxLayout:
        padding: 0
        spacing: app.get_scaled_width(9.99999999998)
        size: root.size
        pos: root.pos
        orientation: "vertical"
        BoxLayout:
            orientation: 'horizontal'
            size: self.parent.size
            pos: self.parent.pos
            spacing: app.get_scaled_width(10.0)
            FileChooser:
                size_hint_x: 5
                id: filechooser_sc_params
                rootpath: './asmcnc/apps/shapeCutter_app/parameter_cache/'
                filter_dirs: True
                filters: ['*.csv', '*.CSV']
                on_selection: root.refresh_filechooser()
                FileChooserIconLayout
                FileChooserListLayout
       
                
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
                disabled: False
                size_hint_x: 1
                background_color: hex('#FFFFFF00')
                on_release: 
                    self.background_color = hex('#FFFFFF00')
                on_press:
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
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    root.delete_popup(file_selection = filechooser_sc_params.selection[0])
                    # root.delete_selected(filechooser_sc_params.selection[0])
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
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    root.quit_to_home()
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
                    root.return_to_SC17(filechooser_sc_params.selection[0])
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
parameter_file_dir = (
    "/home/pi/easycut-smartbench/src/asmcnc/apps/shapeCutter_app/parameter_cache/"
)


class SCFileChooser(Screen):
    def __init__(self, **kwargs):
        super(SCFileChooser, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs["shapecutter"]
        self.l = kwargs["localization"]
        self.j = kwargs["job_parameters"]
#         self.usb_stick = usb_storage.USB_storage() # object to manage presence of USB stick (fun in Linux)
#         self.usb_stick.enable() # start the object scanning for USB stick

    def on_enter(self):
        self.refresh_filechooser()
        self.switch_view()

    def switch_view(self):
        if self.toggle_view_button.state == "normal":
            self.filechooser_sc_params.view_mode = "icon"
            self.image_view.source = "./asmcnc/skavaUI/img/file_select_list_view.png"
        elif self.toggle_view_button.state == "down":
            self.filechooser_sc_params.view_mode = "list"
            self.image_view.source = "./asmcnc/skavaUI/img/file_select_list_icon.png"

    def refresh_filechooser(self):
        self.filechooser_sc_params._update_item_selection()
        try:
            if self.filechooser_sc_params.selection[0] != "C":
                self.load_button.disabled = False
                self.image_select.source = "./asmcnc/skavaUI/img/file_select_select.png"
                self.delete_selected_button.disabled = False
                self.image_delete.source = "./asmcnc/skavaUI/img/file_select_delete.png"
            else:
                self.load_button.disabled = True
                self.image_select.source = (
                    "./asmcnc/skavaUI/img/file_select_select_disabled.png"
                )
                self.delete_selected_button.disabled = True
                self.image_delete.source = (
                    "./asmcnc/skavaUI/img/file_select_delete_disabled.png"
                )
        except:
            self.load_button.disabled = True
            self.image_select.source = (
                "./asmcnc/skavaUI/img/file_select_select_disabled.png"
            )
            self.delete_selected_button.disabled = True
            self.image_delete.source = (
                "./asmcnc/skavaUI/img/file_select_delete_disabled.png"
            )
        self.filechooser_sc_params._update_files()

    def return_to_SC17(self, file_selection):
        if os.path.isfile(file_selection):
            self.j.load_parameters(file_selection)
            self.shapecutter_sm.next_screen()
        else:
            error_message = "File selected does not exist!"
            popup_info.PopupError(self.shapecutter_sm, self.l, error_message)

    def delete_popup(self, **kwargs):
        if kwargs["file_selection"] == "all":
            popup_info.PopupDeleteFile(
                screen_manager=self.shapecutter_sm,
                localization=self.l,
                function=self.delete_all,
                file_selection="all",
            )
        else:
            popup_info.PopupDeleteFile(
                screen_manager=self.shapecutter_sm,
                localization=self.l,
                function=self.delete_selected,
                file_selection=kwargs["file_selection"],
            )

    def delete_selected(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)
            self.filechooser_sc_params.selection = []
            Clock.schedule_once(lambda dt: self.refresh_filechooser(), 0.25)

    def delete_all(self):
        files_in_cache = os.listdir(parameter_file_dir) # clean cache
        if files_in_cache:
            for file in files_in_cache:
                os.remove(parameter_file_dir + file)
                self.filechooser_sc_params.selection = []
        self.refresh_filechooser()

    def quit_to_home(self):
        self.shapecutter_sm.previous_screen()
