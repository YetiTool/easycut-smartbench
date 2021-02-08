# -*- coding: utf-8 -*-
'''
author: @Letty
module handles the system app popups
'''
import sys, textwrap
import kivy
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty  # @UnresolvedImport
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle



def format_popup_string(cmd):
    wrapped_cmd = textwrap.fill(cmd, width=70, break_long_words=False)
    return wrapped_cmd

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
        label = Label(size_hint_y=2, text_size=(320, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)
        
        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=back_string, markup = True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

       
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0,5,0,0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[30,20,30,0])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(360, 360),
                      auto_dismiss= False
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
        label = Label(size_hint_y=2, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)
        
        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=back_string, markup = True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

       
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0,5,0,0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[30,20,30,0])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(360, 360),
                      auto_dismiss= False
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
        label = Label(size_hint_y=2, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)
        
        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=back_string, markup = True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

       
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0,5,0,0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[30,20,30,0])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(360, 360),
                      auto_dismiss= False
                      )
        
        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=quit_console)
        back_button.bind(on_press=popup.dismiss)

        popup.open()


### Beta testing
class PopupBetaTesting(Widget):
    def __init__(self, screen_manager, localization):
        
        self.systemtools_sm = screen_manager
        self.l = localization

        # "Beta testing allows our engineers and beta testers to try out software updates " + \
        # "that might not be stable, or change how SmartBench behaves.\n\n" + \
        # "By updating to a beta version or developer branch you may risk causing damage to SmartBench.\n\n" + \
        # "Do you want to continue?"

        description = (
            format_popup_string(self.l.get_str(
                "Beta testing allows our engineers and beta testers to try out software updates " + \
                "that might not be stable, or change how SmartBench behaves."
                )) + "\n\n" + \
            format_popup_string(
                self.l.get_str("By updating to a beta version or developer branch you may risk causing damage to SmartBench.")
                ) + \
            "\n\n" + \
            self.l.get_str("Do you want to continue?")
        )

        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Yes')
        back_string = self.l.get_bold('No')

        def dev_app(*args):
            self.systemtools_sm.open_beta_testing_screen()
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)
        
        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=back_string, markup = True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

       
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0,5,0,0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[30,20,30,0])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 400),
                      auto_dismiss= False
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
    def __init__(self, screen_manager, localization):
        
        self.systemtools_sm = screen_manager
        self.l = localization
        
        # description = "Changing the GRBL settings will change how SmartBench behaves." + \
        # "By changing the settings you may risk causing damage to SmartBench.\n" + \
        # "Please enter the password if you want to continue."

        description = (
            format_popup_string(self.l.get_str("Changing the GRBL settings will change how SmartBench behaves.")) + \
            " " + \
            format_popup_string(self.l.get_str("By changing the settings you may risk causing damage to SmartBench.")) + \
            "\n" + \
            format_popup_string(self.l.get_str("Please enter the password if you want to continue."))
            )

        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Ok')

        def check_password(*args):
          if textinput.text == "grbl":
            self.systemtools_sm.open_grbl_settings_screen()
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(450, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)
        textinput = TextInput(size_hint_y=0.7, text = '')

        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]
       
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[20,0,20,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40,20,40,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(textinput)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 400),
                      auto_dismiss= False
                      )
        
        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=check_password)
        ok_button.bind(on_press=popup.dismiss)    

        popup.open()


### Factory settings and password
class PopupFactorySettingsPassword(Widget):   
    def __init__(self, screen_manager, localization):
        
        self.systemtools_sm = screen_manager
        self.l = localization
        
        description = self.l.get_str("Please enter the password to use the factory settings.")
        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Ok')

        def check_password(*args):
          if textinput.text == "fac":
            self.systemtools_sm.open_factory_settings_screen()
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=0.7, text_size=(450, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)
        textinput = TextInput(size_hint_y=1, text = '')

        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]
       
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[10,0,10,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=5, padding=[40,10,40,10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(textinput)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 260),
                      auto_dismiss= False,
                      pos_hint={'x': 150.0 / 800.0, 
                                'y':200.0 /  480.0},
                      )
        
        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=check_password)
        ok_button.bind(on_press=popup.dismiss)    

        popup.open()

### Update testing and password
class PopupUpdateTestingPassword(Widget):   
    def __init__(self, screen_manager, localization):
        
        self.systemtools_sm = screen_manager
        self.l = localization
        
        # description = "Update testing allows our engineers to try out full system updates " + \
        # "that might not be stable, or change how SmartBench behaves. " + \
        # "By carrying out any development updates you may risk causing damage to SmartBench.\n" + \
        # "Please enter the password if you want to continue."

        description = (
            format_popup_string(self.l.get_str("Update testing allows our engineers to try out full system updates " + \
                "that might not be stable, or change how SmartBench behaves.")) + \
            " " + \
            format_popup_string(self.l.get_str("By carrying out any development updates you may risk causing damage to SmartBench.")) + \
            "\n" + \
            format_popup_string(self.l.get_str("Please enter the password if you want to continue."))
            )

        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Ok')

        def check_password(*args):
          if textinput.text == "up":
            self.systemtools_sm.open_update_testing_screen()
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(450, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)
        textinput = TextInput(size_hint_y=0.7, text = '')

        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]
       
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[20,0,20,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40,20,40,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(textinput)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 400),
                      auto_dismiss= False
                      )
        
        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=check_password)
        ok_button.bind(on_press=popup.dismiss)    

        popup.open()


### Developer and password
class PopupDeveloperPassword(Widget):   
    def __init__(self, screen_manager, localization):
        
        self.systemtools_sm = screen_manager
        self.l = localization
        
        # description = "The developer app is to help our engineers access extra settings " + \
        # "and functions that might not be stable, or change how SmartBench behaves. " + \
        # "By using the developer app, you may risk causing damage to SmartBench.\n" + \
        # "Please enter the password if you want to continue."

        description = (
            format_popup_string(
            self.l.get_str("The developer app is to help our engineers access extra settings and functions " + \
                "that might not be stable, or change how SmartBench behaves.")) + \
            " " + \
            format_popup_string(self.l.get_str("By using the developer app, you may risk causing damage to SmartBench.")) + \
            "\n" + \
            format_popup_string(self.l.get_str("Please enter the password if you want to continue."))
            )

        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Ok')

        def check_password(*args):
          if textinput.text == "dev":
            self.systemtools_sm.open_developer_screen()
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(450, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)
        textinput = TextInput(size_hint_y=0.7, text = '')

        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]
       
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[20,0,20,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40,20,40,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(textinput)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 400),
                      auto_dismiss= False
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
        label = Label(size_hint_y=1.7, text_size=(260, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)
        
        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=cancel_string, markup = True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

       
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0,0,0,0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[30,20,30,0])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(300, 300),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'
        
        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=reboot_console)
        back_button.bind(on_press=popup.dismiss)

        popup.open()