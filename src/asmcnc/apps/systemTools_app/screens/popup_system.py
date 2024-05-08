# -*- coding: utf-8 -*-
'''
author: @Letty
module handles the system app popups
'''
import sys
import kivy
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.properties import StringProperty  
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.rst import RstDocument

from asmcnc.core_UI.utils import color_provider

def on_touch(popup, touch):
    for child in popup.content.children:
        if isinstance(child, TextInput):
            child.focus = False


### DownloadLogs
class PopupDownloadLogs(Widget):
    def __init__(self, screen_manager, localization):
        self.systemtools_sm = screen_manager
        self.l = localization

        description = self.l.get_str("Would you like to download the system logs onto a USB stick?")
        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Yes')
        back_string = self.l.get_bold('No')

        def download_logs(*args):
            self.systemtools_sm.download_logs_to_usb()

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(320, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=back_string, markup=True)
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
                      size=(360, 360),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=download_logs)
        back_button.bind(on_press=popup.dismiss)

        popup.open()


### Reboot Console
class RebootConsole(Widget):
    def __init__(self, screen_manager, localization):
        self.systemtools_sm = screen_manager
        self.l = localization

        description = self.l.get_str("Would you like to reboot the console now?")
        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Yes')
        back_string = self.l.get_bold('No')

        def reboot_console(*args):
            self.systemtools_sm.sm.current = 'rebooting'

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(360, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=back_string, markup=True)
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
                      size=(360, 360),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=reboot_console)
        back_button.bind(on_press=popup.dismiss)

        popup.open()


### Quit To Console
class QuitToConsole(Widget):
    def __init__(self, screen_manager, localization):
        self.systemtools_sm = screen_manager
        self.l = localization

        description = self.l.get_str("Would you like to exit the software now?")
        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Yes')
        back_string = self.l.get_bold('No')

        def quit_console(*args):
            sys.exit()

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(360, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=back_string, markup=True)
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
                      size=(360, 360),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=quit_console)
        back_button.bind(on_press=popup.dismiss)

        popup.open()


### USB First Aid
class PopupUSBFirstAid(Widget):
    def __init__(self, screen_manager, localization):
        self.systemtools_sm = screen_manager
        self.l = localization

        description = (
                self.l.get_str("If your USB stick is plugged into the console, please remove it now.") + \
                "\n\n" + \
                self.l.get_str("When you have removed it, press 'Ok'.") + \
                "\n\n" + \
                self.l.get_bold("WARNING: Not following this step could cause files to be deleted from your USB stick.")
        )
        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Ok')
        cancel_string = self.l.get_bold('Cancel')

        def clear_mountpoint(*args):
            self.systemtools_sm.clear_usb_mountpoint()

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(320, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=cancel_string, markup=True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 10, 0, 0])
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
                      size=(360, 360),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=clear_mountpoint)
        back_button.bind(on_press=popup.dismiss)

        popup.open()


### Beta testing
class PopupBetaTesting(Widget):
    def __init__(self, screen_manager, localization):
        self.systemtools_sm = screen_manager
        self.l = localization

        description = (
                self.l.get_str(
                    "Beta testing allows our engineers and beta testers to try out software updates " + \
                    "that might not be stable, or change how SmartBench behaves."
                ) + \
                "\n\n" + \
                self.l.get_str(
                    "By updating to a beta version or developer branch you may risk causing damage to SmartBench.") + \
                "\n\n" + \
                self.l.get_str("Do you want to continue?")
        )

        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Yes')
        back_string = self.l.get_bold('No')

        def dev_app(*args):
            self.systemtools_sm.open_beta_testing_screen()

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(410, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=back_string, markup=True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 10, 0, 0])
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
                      size=(550, 400),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=dev_app)
        back_button.bind(on_press=popup.dismiss)

        popup.open()


## GRBL settings and password
class PopupGRBLSettingsPassword(Widget):
    def __init__(self, screen_manager, localization, keyboard):
        self.systemtools_sm = screen_manager
        self.l = localization
        self.kb = keyboard

        description = (
                self.l.get_str("Changing the GRBL settings will change how SmartBench behaves.") + \
                " " + \
                self.l.get_str("By changing the settings you may risk causing damage to SmartBench.") + \
                "\n" + \
                self.l.get_str("Please enter the password if you want to continue.")
        )

        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Ok')

        def check_password(*args):
            if textinput.text == "grbl":
                self.systemtools_sm.open_grbl_settings_screen()

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(450, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)
        textinput = TextInput(size_hint_y=0.7, text='')

        self.kb.setup_text_inputs([textinput])

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[20, 0, 20, 0])
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40, 20, 40, 20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(textinput)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 400),
                      auto_dismiss=False,
                      on_touch_down=on_touch
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=check_password)
        ok_button.bind(on_press=popup.dismiss)

        popup.open()


### Factory settings and password
class PopupFactorySettingsPassword(Widget):
    def __init__(self, screen_manager, localization, keyboard):
        self.systemtools_sm = screen_manager
        self.l = localization
        self.kb = keyboard

        description = self.l.get_str("Please enter the password to use the factory settings.")
        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Ok')

        def check_password(*args):
            if textinput.text == "fac":
                self.systemtools_sm.open_factory_settings_screen()

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=0.7, text_size=(450, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)
        textinput = TextInput(size_hint_y=1, text='', multiline=False)

        self.kb.setup_text_inputs([textinput])

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[10, 0, 10, 0])
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=5, padding=[40, 10, 40, 10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(textinput)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 260),
                      auto_dismiss=False,
                      pos_hint={'x': 150.0 / 800.0,
                                'y': 200.0 / 480.0},
                      on_touch_down=on_touch
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=check_password)
        ok_button.bind(on_press=popup.dismiss)

        popup.open()


### Update testing and password
class PopupUpdateTestingPassword(Widget):
    def __init__(self, screen_manager, localization, keyboard):
        self.systemtools_sm = screen_manager
        self.l = localization
        self.kb = keyboard

        description = (
                self.l.get_str("Update testing allows our engineers to try out full system updates " + \
                               "that might not be stable, or change how SmartBench behaves.") + \
                " " + \
                self.l.get_str("By carrying out development updates you may risk causing damage to SmartBench.") + \
                "\n" + \
                self.l.get_str("Please enter the password if you want to continue.")
        )

        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Ok')

        def check_password(*args):
            if textinput.text == "up":
                self.systemtools_sm.open_update_testing_screen()

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(550, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)
        textinput = TextInput(size_hint_y=0.7, text='')

        self.kb.setup_text_inputs([textinput])

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[20, 0, 20, 0])
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40, 20, 40, 20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(textinput)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(600, 400),
                      auto_dismiss=False,
                      on_touch_down=on_touch
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=check_password)
        ok_button.bind(on_press=popup.dismiss)

        popup.open()


### Developer and password
class PopupDeveloperPassword(Widget):
    def __init__(self, screen_manager, localization, keyboard):
        self.systemtools_sm = screen_manager
        self.l = localization
        self.kb = keyboard

        description = (
                self.l.get_str("The developer app is to help our engineers access extra settings and " + \
                               "functions that might not be stable, or change how SmartBench behaves.") + \
                " " + \
                self.l.get_str("By using the developer app, you may risk causing damage to SmartBench.") + \
                "\n" + \
                self.l.get_str("Please enter the password if you want to continue.")
        )

        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Ok')

        def check_password(*args):
            if textinput.text == "dev":
                self.systemtools_sm.open_developer_screen()

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(550, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)
        textinput = TextInput(size_hint_y=0.7, text='')

        self.kb.setup_text_inputs([textinput])

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[20, 0, 20, 0])
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40, 10, 40, 10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(textinput)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(600, 400),
                      auto_dismiss=False,
                      on_touch_down=on_touch
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=check_password)
        ok_button.bind(on_press=popup.dismiss)

        popup.open()


### Reboot Console
class RebootAfterLanguageChange(Widget):
    def __init__(self, screen_manager, localization):
        self.systemtools_sm = screen_manager
        self.l = localization

        description = self.l.get_str('Console needs to reboot to update language settings.')
        title_string = self.l.get_str('Information')
        ok_string = self.l.get_bold('Ok')
        cancel_string = self.l.get_bold('Cancel')

        def reboot_console(*args):
            self.systemtools_sm.sm.current = 'rebooting'

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.7, text_size=(260, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=cancel_string, markup=True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 0, 0, 0])
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
                      size=(300, 300),
                      auto_dismiss=False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=reboot_console)
        back_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupSSHToggleFailed(Widget):
    def __init__(self, localization):
        self.l = localization

        description = self.l.get_str("Reboot console and try again")
        title_string = self.l.get_str("Failed to toggle SSH Service")
        ok_string = self.l.get_str("Ok")

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.7, text_size=(260, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 0, 0, 0])
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
                      size=(300, 300),
                      auto_dismiss=False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupFailedToSendSSHKey(Widget):
    def __init__(self):
        description = "The public SSH key file failed to send, please contact Archie or Lettie"
        title_string = "Couldn't send SSH Key"
        ok_string = 'Ok'

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.7, text_size=(260, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 0, 0, 0])
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
                      size=(300, 300),
                      auto_dismiss=False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupNoSSHFile(Widget):
    def __init__(self):
        description = "The public SSH key file hasn't been generated, please contact Archie/Lettie"
        title_string = "Couldn't find SSH Key"
        ok_string = 'Ok'

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.7, text_size=(260, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 0, 0, 0])
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
                      size=(300, 300),
                      auto_dismiss=False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupCSVOnUSB(Widget):
    def __init__(self):
        description = 'The final test data has been transferred to the USB stick, please hand it to Archie or Lettie ' \
                      'when possible. '
        title_string = 'Transfer Failed'
        ok_string = 'Ok'

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.7, text_size=(260, None), halign='center', valign='middle', text=description,
                      color=color_provider.get_rgba("black"), padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 0, 0, 0])
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
                      size=(300, 300),
                      auto_dismiss=False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupStopOvernightTest(Widget):

    def __init__(self, machine, screen_manager, localization, overnight_test_class):
        self.m = machine
        self.m.soft_stop()

        self.sm = screen_manager
        self.l = localization

        self.ot = overnight_test_class

        def machine_reset(*args):
            self.ot.overnight_running = False
            self.m.stop_from_soft_stop_cancel()
            self.ot.cancel_active_polls()
            self.ot.buttons_disabled(False)
            self.ot.stage = ''

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


class PopupFSCKGood(Widget):

    def __init__(self, screen_manager, localization, description, more_info):

        self.sm = screen_manager
        self.l = localization
        popup_width = 500
        label_width = popup_width - 40

        def open_more_info(*args):
            PopupFSCKInfo(self.sm, self.l, more_info)

        title_string = self.l.get_str('Information')
        ok_string = self.l.get_bold('Ok')
        more_info_string = self.l.get_bold('More info')

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(label_width, None), markup=True, halign='center', valign='middle',
                      text=description, color=color_provider.get_rgba("black"), padding=[10, 10])

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        more_info_button = Button(text=more_info_string, markup=True)
        more_info_button.background_normal = ''
        more_info_button.background_color = [33 / 255., 150 / 255., 243 / 255., 98 / 100.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[10, 20, 10, 0])
        if more_info: btn_layout.add_widget(more_info_button)
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
        if more_info:
            more_info_button.bind(on_press=open_more_info)
            more_info_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupFSCKErrors(Widget):

    def __init__(self, screen_manager, localization, description, more_info):
        self.sm = screen_manager
        self.l = localization
        popup_width = 500
        label_width = popup_width - 40

        def open_more_info(*args):
            PopupFSCKInfo(self.sm, self.l, more_info)

        title_string = self.l.get_str('Error!')
        ok_string = self.l.get_bold('Ok')
        more_info_string = self.l.get_bold('More info')

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(label_width, None), markup=True, halign='center', valign='middle',
                      text=description, color=color_provider.get_rgba("black"), padding=[10, 10])

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        more_info_button = Button(text=more_info_string, markup=True)
        more_info_button.background_normal = ''
        more_info_button.background_color = [33 / 255., 150 / 255., 243 / 255., 98 / 100.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[10, 20, 10, 0])
        btn_layout.add_widget(more_info_button)
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
        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)
        more_info_button.bind(on_press=open_more_info)
        more_info_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupFSCKInfo(Widget):

    def __init__(self, screen_manager, localization, description):
        self.sm = screen_manager
        self.l = localization
        popup_width = 600

        title_string = self.l.get_str('Information')
        ok_string = self.l.get_bold('Ok')

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        info_label = RstDocument(text=description, background_color=[1, 1, 1, 1], base_font_size=26,
                                 underline_color='000000')

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[10, 20, 10, 0], size_hint_y=0.6)
        btn_layout.add_widget(ok_button)

        scroll_layout = ScrollView(do_scroll_x=True, do_scroll_y=True, scroll_type=['content'], always_overscroll=True,
                                   size_hint_y=1.2)
        scroll_layout.add_widget(info_label)

        layout_plan = BoxLayout(orientation='vertical', spacing=0, padding=[10, 10, 10, 10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(scroll_layout)
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


class PopupStopStallJig(Widget):

    def __init__(self, machine, screen_manager, localization, stall_jig_class):
        self.m = machine
        self.m.soft_stop()
        self.test_stopped = True

        self.sm = screen_manager
        self.l = localization

        self.sj = stall_jig_class

        def machine_reset(*args):
            self.m.stop_from_soft_stop_cancel()
            self.sj.unschedule_all_events()
            self.sj.set_default_thresholds()
            self.sj.test_stopped = False
            self.sj.restore_grbl_settings()
            self.sj.enable_all_buttons_except_run()
            self.sj.test_status_label.text = "STOPPED"

        def machine_resume(*args):
            self.m.resume_from_a_soft_door()
            self.m.continue_measuring_running_data()
            self.sj.test_stopped = False

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


class PopupConfirmStoreCurrentValues(Widget):

    def __init__(self, machine, screen_manager, localization, current_adjustment_screen):
        self.m = machine
        self.sm = screen_manager
        self.l = localization

        self.cs = current_adjustment_screen

        def store_tmc_values(*args):
            self.cs.store_values_and_wait_for_handshake()

        stop_description = self.l.get_str(
            "THIS WILL STORE ALL MODIFIED TMC PARAMS IN EEPROM. Only continue if you know what you're doing.")
        resume_string = self.l.get_bold("DANGER: Store")
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
                      size=(400, 500),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        cancel_button.bind(on_press=popup.dismiss)
        resume_button.bind(on_press=store_tmc_values)
        resume_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupConfirmSpindleTest(Widget):
    popup = None
    confirm_func = None

    def __init__(self, confirm_func, **kwargs):
        super(PopupConfirmSpindleTest, self).__init__(**kwargs)
        self.confirm_func = confirm_func
        self.build()

    def build(self):
        stop_description = "Pressing the confirm button will start the spindle test. Ensure it is safe to do so."
        resume_string = "Confirm"
        cancel_string = "Cancel"
        title_string = "Warning!"

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

        self.popup = Popup(title=title_string,
                           title_color=color_provider.get_rgba("black"),
                           title_size='20sp',
                           content=layout_plan,
                           size_hint=(None, None),
                           size=(400, 300),
                           auto_dismiss=False)

        self.popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        self.popup.separator_height = '4dp'
        self.popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        cancel_button.bind(on_press=self.popup.dismiss)
        resume_button.bind(on_press=lambda x: self.confirm_func())
        resume_button.bind(on_press=self.popup.dismiss)

    def open(self):
        self.popup.open()
