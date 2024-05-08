# -*- coding: utf-8 -*-
'''
@author Letty
Info pop-up
'''

import kivy
import os

from asmcnc.comms.logging_system.logging_system import Logger
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty  
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.rst import RstDocument
from kivy.clock import Clock
from kivy.uix.checkbox import CheckBox
from datetime import datetime
from kivy.graphics import Color, Rectangle
from asmcnc.core_UI import console_utils
from asmcnc.core_UI.utils import color_provider


class PopupWelcome(Widget):

    def __init__(self, screen_manager, machine, localization, description):
        self.sm = screen_manager
        self.m = machine
        self.l = localization

        title_string = self.l.get_str('Welcome to SmartBench')
        ok_string = self.l.get_bold('Ok')
        remind_string = self.l.get_bold('Remind me later')

        def set_trigger_to_false(*args):
            self.m.write_set_up_options(False)
            self.sm.get_screen('lobby').carousel.load_next(mode='next')

        def set_trigger_to_true(*args):
            self.m.write_set_up_options(True)

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(420, None), markup=True, halign='center', valign='middle',
                      text=description, color=color_provider.get_rgba("black"), padding=[0, 0])

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        remind_me_button = Button(text=remind_string, markup=True)
        remind_me_button.background_normal = ''
        remind_me_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[20, 10, 20, 0])
        btn_layout.add_widget(remind_me_button)
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10, 10, 10, 10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      #                       title_color=[0.141, 0.596, 0.957, 1],
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 440),
                      auto_dismiss=False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=set_trigger_to_false)
        remind_me_button.bind(on_press=popup.dismiss)
        remind_me_button.bind(on_press=set_trigger_to_true)

        popup.open()


class PopupDatum(Widget):

    def __init__(self, screen_manager, machine, localization, xy, warning_message):

        self.sm = screen_manager
        self.m = machine
        self.l = localization

        description = warning_message
        title_string = self.l.get_str('Warning!')
        yes_string = self.l.get_bold('Yes')
        no_string = self.l.get_bold('No')
        # chk_message = "         Use laser datum?"
        chk_message = self.l.get_str('Use laser crosshair?')

        def on_checkbox_active(checkbox, value):
            if value:
                self.sm.get_screen('home').default_datum_choice = 'laser'
            else:
                self.sm.get_screen('home').default_datum_choice = 'spindle'

        def set_datum(*args):

            if (self.sm.get_screen('home').default_datum_choice == 'laser' and self.m.is_laser_enabled == True):

                if xy == 'X':
                    self.m.set_x_datum_with_laser()  # testing!!
                elif xy == 'Y':
                    self.m.set_y_datum_with_laser()

                elif xy == 'XY':
                    self.m.set_workzone_to_pos_xy_with_laser()

            else:

                if xy == 'X':
                    self.m.set_x_datum()
                elif xy == 'Y':
                    self.m.set_y_datum()
                elif xy == 'XY':
                    self.m.set_workzone_to_pos_xy()

        def set_checkbox_default():
            if self.sm.get_screen('home').default_datum_choice == 'spindle':
                return False
            elif self.sm.get_screen('home').default_datum_choice == 'laser':
                return True

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[40, 20], markup=True)

        ok_button = Button(text=yes_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=no_string, markup=True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0, 0, 0, 0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)

        if self.m.is_laser_enabled == True:
            chk_label = Label(size_hint_y=1, size_hint_x=0.8, halign='center', valign='middle', text=chk_message,
                              text_size=[200, 100], color=color_provider.get_rgba("black"), padding=[0, 20], markup=True)
            checkbox = CheckBox(size_hint_x=0.2,
                                background_checkbox_normal="./asmcnc/skavaUI/img/checkbox_inactive.png",
                                active=set_checkbox_default())
            chk_layout = BoxLayout(orientation='horizontal', spacing=0, padding=[5, 0, 5, 0])
            chk_layout.add_widget(chk_label)
            chk_layout.add_widget(checkbox)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[20, 20, 20, 20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        if self.m.is_laser_enabled == True: layout_plan.add_widget(chk_layout)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(300, 350),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        if self.m.is_laser_enabled == True: checkbox.bind(active=on_checkbox_active)

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=set_datum)
        back_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupPark(Widget):

    def __init__(self, screen_manager, machine, localization, warning_message):
        self.sm = screen_manager
        self.m = machine
        self.l = localization

        description = warning_message
        title_string = self.l.get_str('Warning!')
        yes_string = self.l.get_bold('Yes')
        no_string = self.l.get_bold('No')

        def set_park(*args):
            self.m.set_standby_to_pos()
            self.m.get_grbl_status()

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[40, 20], markup=True)

        ok_button = Button(text=yes_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=no_string, markup=True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0, 0, 0, 0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40, 20, 40, 20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(300, 350),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=set_park)
        back_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupStop(Widget):

    def __init__(self, machine, screen_manager, localization):
        self.m = machine
        self.m.soft_stop()

        self.sm = screen_manager
        self.l = localization

        def machine_reset(*args):
            self.m.stop_from_soft_stop_cancel()

        def machine_resume(*args):
            self.m.resume_from_a_soft_door()

        stop_description = self.l.get_str("Is everything OK? You can resume the job, or cancel it completely.")
        resume_string = self.l.get_bold("Resume")
        cancel_string = self.l.get_bold("Cancel")
        title_string = self.l.get_str("Warning!")

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(360, None), halign='center', valign='middle', text=stop_description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        resume_button = Button(text=resume_string, markup=True)
        resume_button.background_normal = ''
        resume_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        cancel_button = Button(text=cancel_string, markup=True)
        cancel_button.background_normal = ''
        cancel_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 5, 0, 0], size_hint_y=2)
        btn_layout.add_widget(cancel_button)
        btn_layout.add_widget(resume_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=5, padding=[30, 20, 30, 0])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(400, 300),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        cancel_button.bind(on_press=machine_reset)
        cancel_button.bind(on_press=popup.dismiss)
        resume_button.bind(on_press=machine_resume)
        resume_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupUSBInfo(Widget):

    def __init__(self, screen_manager, localization, safe_to_remove):

        self.sm = screen_manager
        self.l = localization

        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Ok')

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''

        if safe_to_remove == 'mounted':

            description = (
                    self.l.get_str("USB stick found!") + "\n\n" + \
                    self.l.get_str("Please do not remove your USB stick until it is safe to do so.")
            )

            ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        elif safe_to_remove == False:

            description = (
                    self.l.get_str("Do not remove your USB stick yet.") + "\n\n" + \
                    self.l.get_str("Please wait") + "..."
            )

            ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        elif safe_to_remove == True:
            description = self.l.get_str('It is now safe to remove your USB stick.')
            ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(310, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[40, 20], markup=True)

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0, 0, 0, 0])
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40, 20, 40, 20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        self.popup = Popup(title=title_string,
                           title_color=color_provider.get_rgba("black"),
                           title_size='20sp',
                           content=layout_plan,
                           size_hint=(None, None),
                           size=(350, 350),
                           auto_dismiss=False
                           )

        self.popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        self.popup.separator_height = '4dp'
        self.popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=self.popup.dismiss)

        self.popup.open()


class PopupUSBError(Widget):

    def __init__(self, screen_manager, localization, usb):
        self.sm = screen_manager
        self.l = localization

        title_string = self.l.get_str('Error!')
        ok_string = self.l.get_bold('Ok')

        description = (
                self.l.get_str(
                    "Problem mounting USB stick. Please remove your USB stick, and check that it is working properly.") + \
                "\n\n" + \
                self.l.get_str("If this error persists, you may need to reformat your USB stick.")
        )

        def restart_polling(*args):
            usb.start_polling_for_usb()

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 10], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0, 0, 0, 0])
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40, 20, 40, 20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 400),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=restart_polling)

        popup.open()


class PopupInfo(Widget):

    def __init__(self, screen_manager, localization, popup_width, description):
        self.sm = screen_manager
        self.l = localization
        label_width = popup_width - 40

        title_string = self.l.get_str('Information')
        ok_string = self.l.get_bold('Ok')

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(label_width, None), markup=True, halign='left', valign='middle',
                      text=description, color=color_provider.get_rgba("black"), padding=[10, 10])

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[150, 20, 150, 0])
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10, 10, 10, 10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(popup_width, 440),
                      auto_dismiss=True
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupMiniInfo(Widget):

    def __init__(self, screen_manager, localization, description):
        self.sm = screen_manager
        self.l = localization

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[40, 20], markup=True)

        title_string = self.l.get_str('Information')
        ok_string = self.l.get_bold('Ok')

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0, 0, 0, 0])
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40, 20, 40, 20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(300, 300),
                      auto_dismiss=False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupSoftwareUpdateSuccess(Widget):
    def __init__(self, screen_manager, localization, message):
        self.sm = screen_manager
        self.l = localization

        description = self.l.get_str("Software update was successful.") + \
                      "\n\n" + \
                      self.l.get_str("Update message") + ": " + \
                      message + \
                      "\n" + \
                      self.l.get_str("Please do not restart your machine until you are prompted to do so.")

        title_string = self.l.get_str('Update Successful!')
        ok_string = self.l.get_bold('Ok')

        def reboot(*args):
            self.sm.current = 'rebooting'

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.2, text_size=(660, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[40, 10], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0, 0, 0, 0])
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40, 20, 40, 20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(700, 400),
                      auto_dismiss=False
                      )

        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)
        # ok_button.bind(on_press=reboot)

        popup.open()

        Clock.schedule_once(reboot, 6)

# Popup asking the user if they are sure they want to continue with the update with a given warning_message
class PopupSoftwareUpdateWarning(Widget):
    def __init__(self, screen_manager, localization, settings_manager, warning_message, update_method, prep_for_sw_update_over_wifi, prep_for_sw_update_over_usb):
        self.sm = screen_manager
        self.set = settings_manager
        self.l = localization

        title_string = self.l.get_str('Are you sure you want to update?')
        update_string = self.l.get_bold('Update')
        back_string = self.l.get_bold('Cancel')

        description = warning_message

        # Decide which update function should be run depending on which button was pressed
        def update(*args):
            if update_method == "WiFi":
                prep_for_sw_update_over_wifi()
            elif update_method == "USB":
                prep_for_sw_update_over_usb()
            else:  # Fail-safe message to make debugging easier in case usb_or_wifi strings are broken
                Logger.error("Error getting update method. Please check screen_update_SW.py" + \
                         "\nShould be: 'WiFi' or 'USB'" + \
                         "\nBut was: " + update_method)

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.4, text_size=(560, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[20, 20], markup=True)

        ok_button = Button(text=update_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=back_string, markup=True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0, 0, 0, 0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10, 20, 10, 20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(600, 420),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=update)
        back_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupSoftwareRepair(Widget):
    def __init__(self, screen_manager, localization, settings_manager, warning_message):
        self.sm = screen_manager
        self.set = settings_manager
        self.l = localization

        title_string = self.l.get_str('There was a problem updating the software') + '...'
        repair_string = self.l.get_bold('Repair')
        back_string = self.l.get_bold('Go Back')

        description = warning_message

        def repair(*args):
            self.sm.get_screen('update').repair_sw_over_wifi()

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.4, text_size=(560, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[20, 20], markup=True)

        ok_button = Button(text=repair_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=back_string, markup=True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0, 0, 0, 0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10, 20, 10, 20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(600, 420),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=repair)
        back_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupError(Widget):
    def __init__(self, screen_manager, localization, warning_message):
        self.sm = screen_manager
        self.l = localization

        description = warning_message

        title_string = self.l.get_str('Error!')
        ok_string = self.l.get_bold('Ok')

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(460, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 10], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0, 20, 0, 0])
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40, 20, 40, 20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 400),
                      auto_dismiss=True
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupWarning(Widget):
    def __init__(self, screen_manager, localization, warning_message):
        self.sm = screen_manager
        self.l = localization

        description = warning_message
        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Ok')

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[20, 10, 20, 0])
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40, 20, 40, 20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 400),
                      auto_dismiss=True
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupWait(Widget):
    def __init__(self, screen_manager, localization, description=False):
        self.sm = screen_manager
        self.l = localization

        if description == False:
            description = self.l.get_str("Please wait") + "..."

        title_string = self.l.get_str("Please Wait") + "..."
        # ok_string = self.l.get_bold("Ok")

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[40, 20], markup=True)

        # ok_button = Button(text=ok_string, markup = True)
        # ok_button.background_normal = ''
        # ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        # btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
        # btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40, 20, 40, 20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        # layout_plan.add_widget(btn_layout)

        self.popup = Popup(title=title_string,
                           title_color=color_provider.get_rgba("black"),
                           title_size='20sp',
                           content=layout_plan,
                           size_hint=(None, None),
                           size=(500, 200),
                           auto_dismiss=True
                           )

        self.popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        self.popup.separator_height = '4dp'
        self.popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        # ok_button.bind(on_press=self.popup.dismiss)

        self.popup.open()


class PopupDeleteFile(Widget):
    def __init__(self, **kwargs):

        self.sm = kwargs['screen_manager']
        self.l = kwargs['localization']
        self.function = kwargs['function']
        self.file_selection = kwargs['file_selection']

        if self.file_selection == 'all':
            description = self.l.get_str("Are you sure you want to delete these files?")
        else:
            description = self.l.get_str("Are you sure you want to delete this file?")

        title_string = self.l.get_str('Warning!')
        yes_string = self.l.get_bold('Yes')
        no_string = self.l.get_bold('No')

        def delete(*args):
            if self.file_selection == 'all':
                self.function()
            else:
                self.function(self.file_selection)

        def back(*args):
            return False

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(260, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        ok_button = Button(text=yes_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=no_string, markup=True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 5, 0, 0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[30, 20, 30, 0])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(300, 350),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=delete)
        back_button.bind(on_press=popup.dismiss)
        back_button.bind(on_press=back)

        popup.open()


class PopupReminder(Widget):

    def __init__(self, screen_manager, app_manager, machine, localization, message, go_to):

        self.sm = screen_manager
        self.am = app_manager
        self.m = machine
        self.l = localization

        if go_to == 'calibration':
            description = message
        else:
            description = (
                    message + "\n\n" + \
                    self.l.get_bold("WARNING") + ": " + \
                    self.l.get_bold(
                        "Delaying key maintenance tasks or dismissing reminders could cause wear and breakage of important parts!")
            )

        def open_app(*args):

            if go_to == 'calibration':
                self.am.start_calibration_app('go')

            elif go_to == 'brushes':
                self.am.start_maintenance_app('brush_tab')

            elif go_to == 'lubrication':
                self.m.write_z_head_maintenance_settings(0)

        def calibration_delay(*args):
            new_time = float(float(320 * 3600) + self.m.time_to_remind_user_to_calibrate_seconds)
            self.m.write_calibration_settings(self.m.time_since_calibration_seconds, new_time)

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(680, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[10, 0], markup=True)

        title_string = self.l.get_str('Maintenance reminder!')

        if go_to == 'calibration':
            ok_text = self.l.get_bold('Calibrate now!')
            back_text = self.l.get_bold('Remind me in 320 hours')

        if go_to == 'lubrication':
            ok_text = self.l.get_bold('Ok! Z-head lubricated!')
            back_text = self.l.get_bold('Remind me later')

        if go_to == 'brushes':
            ok_text = self.l.get_bold('Change brushes now!')
            back_text = self.l.get_bold('Remind me later')

        ok_button = Button(text=ok_text, markup=True)
        back_button = Button(text=back_text, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0, 0, 0, 0], size_hint_y=0.6)
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=0, padding=[10, 10, 10, 5])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='22sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(700, 460),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=open_app)
        back_button.bind(on_press=popup.dismiss)

        if go_to == 'calibration':
            back_button.bind(on_press=calibration_delay)

        popup.open()


class PopupConfirmJobCancel(Widget):

    def __init__(self, screen_manager, localization):
        self.sm = screen_manager
        self.l = localization

        def confirm_cancel(*args):
            self.sm.get_screen('stop_or_resume_job_decision').confirm_job_cancel()

        stop_description = self.l.get_str("Are you sure you want to cancel the job?")
        title_string = self.l.get_str("Warning!")
        yes_string = self.l.get_bold("Yes")
        no_string = self.l.get_bold("No")

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(360, None), halign='center', valign='middle', text=stop_description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        resume_button = Button(text=no_string, markup=True)
        resume_button.background_normal = ''
        resume_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        cancel_button = Button(text=yes_string, markup=True)
        cancel_button.background_normal = ''
        cancel_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 5, 0, 0], size_hint_y=2)
        btn_layout.add_widget(cancel_button)
        btn_layout.add_widget(resume_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=5, padding=[30, 20, 30, 0])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(400, 300),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        cancel_button.bind(on_press=confirm_cancel)
        cancel_button.bind(on_press=popup.dismiss)
        resume_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupHomingWarning(Widget):

    def __init__(self, screen_manager, machine, localization, return_to_screen, cancel_to_screen):
        self.sm = screen_manager
        self.m = machine
        self.l = localization

        def home_now(*args):
            self.m.request_homing_procedure(return_to_screen, cancel_to_screen)

        stop_description = self.l.get_str("You need to home SmartBench first!")
        title_string = self.l.get_str("Warning!")
        home_string = self.l.get_bold("Home")
        cancel_string = self.l.get_bold("Cancel")

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(360, None), halign='center', valign='middle', text=stop_description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        home_button = Button(text=home_string, markup=True)
        home_button.background_normal = ''
        home_button.background_color = [33 / 255., 150 / 255., 243 / 255., 98 / 100.]

        cancel_button = Button(text=cancel_string, markup=True)
        cancel_button.background_normal = ''
        cancel_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 5, 0, 0], size_hint_y=2)
        btn_layout.add_widget(cancel_button)
        btn_layout.add_widget(home_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=5, padding=[30, 20, 30, 0])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(400, 300),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        home_button.bind(on_press=home_now)
        home_button.bind(on_press=popup.dismiss)
        cancel_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupShutdown(Widget):

    def __init__(self, screen_manager, localization):
        self.sm = screen_manager
        self.l = localization

        description = (
                self.l.get_str(
                    'The console will close any critical processes and shut down safely after 60 seconds, ready for power off.') + \
                "\n\n" + \
                self.l.get_str('This extends the lifetime of the console.') + '\n\n' + \
                self.l.get_str(
                    'You will still need to power down your machine separately after the console has finished shutting down.')
        )
        title_string = self.l.get_str('Shutting down') + '...'
        shutdown_string = self.l.get_bold('Shutdown now')
        cancel_string = self.l.get_bold('Cancel')

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.5, text_size=(480, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        ok_button = Button(text=shutdown_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        cancel_button = Button(text=cancel_string, markup=True)
        cancel_button.background_normal = ''
        cancel_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0, 10, 0, 0])
        btn_layout.add_widget(cancel_button)
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[20, 10, 20, 10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      # size=(300, 300),
                      size=(540, 400),
                      auto_dismiss=False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=console_utils.shutdown_now)
        cancel_button.bind(on_press=console_utils.cancel_shutdown)
        cancel_button.bind(on_press=popup.dismiss)

        popup.open()

class PopupScrollableInfo(Widget):

    def __init__(self, screen_manager, localization, popup_width, description):
        
        self.sm = screen_manager
        self.l = localization
        label_width = popup_width - 20
        
        title_string = self.l.get_str('Information')
        ok_string = self.l.get_bold('Ok')

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        scrollview = ScrollView(size_hint_y=4, padding=[10,10])
        label = RstDocument(text_size=(label_width, None), markup=True, halign='left', valign='middle', text=description, color=color_provider.get_rgba("black"), background_color=[0.95,0.95,0.95,1])
        scrollview.add_widget(label)
        
        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[150,10,150,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical')
        layout_plan.add_widget(img)
        layout_plan.add_widget(scrollview)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(popup_width, 440),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()

class PopupQRInfo(Widget):

    def __init__(self, screen_manager, localization, popup_width, description, qr_source):
        self.sm = screen_manager
        self.l = localization
        label_width = popup_width - 40

        title_string = self.l.get_str('Information')
        ok_string = self.l.get_bold('Ok')

        img = Image(source=qr_source, allow_stretch=False, size_hint_y=1.5)
        label = Label(size_hint_y=2, text_size=(label_width, None), markup=True, halign='left', valign='middle',
                      text=description, color=color_provider.get_rgba("black"), padding=[10, 10])

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[150, 20, 150, 0])
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10, 10, 10, 10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(popup_width, 440),
                      auto_dismiss=False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()
