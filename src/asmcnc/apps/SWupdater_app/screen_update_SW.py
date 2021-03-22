'''
Created on 19 March 2020
Software updater screen

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import sys, os, socket

from asmcnc.comms import usb_storage
from asmcnc.skavaUI import popup_info
from asmcnc.apps.SWupdater_app import popup_update_SW

Builder.load_string("""

<SWUpdateScreen>:

    current_version_label : current_version_label
    sw_version_label : sw_version_label
    latest_software_version_label : latest_software_version_label

    update_using_wifi_label : update_using_wifi_label
    update_using_wifi_instructions_label : update_using_wifi_instructions_label
    wifi_update_button : wifi_update_button

    update_using_usb_label : update_using_usb_label
    update_using_usb_instructions_label : update_using_usb_instructions_label
    usb_update_button : usb_update_button

    wifi_image: wifi_image
    usb_image: usb_image

    BoxLayout:
        size_hint: (None, None)
        height: dp(480)
        width: dp(800)
        orientation: 'vertical'
        spacing: 0
        canvas:
            Color:
                rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
            Rectangle:
                pos: self.pos
                size: self.size
        
        # Header box    
        BoxLayout:
            size_hint: (None, None)
            height: dp(160)
            width: dp(800)
            padding: [30, 30, 30, 18]
            spacing: 30
            orientation: 'horizontal'

            # Version labels box
            BoxLayout: 
                size_hint: (None, None)
                height: dp(112)
                width: dp(598)
                padding: [0,0,0,12]
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(100)
                    width: dp(598)
                    orientation: "horizontal"
                    canvas:
                        Color:
                            rgba: [1,1,1,1]
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size

                    # Version labels:
                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(100)
                        width: dp(375)
                        orientation: "vertical"
                        padding: [0,0,30,0]

                        Label: 
                            id: current_version_label
                            color: 0,0,0,1
                            font_size: 18
                            markup: True
                            halign: "center"
                            valign: "bottom"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
            
                        Label:
                            id: sw_version_label
                            color: 0,0,0,1
                            font_size: 28
                            markup: True
                            halign: "center"
                            valign: "top"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(100)
                        width: dp(223)
                        orientation: "horizontal"
                        padding: [0,0,30,0]

                        BoxLayout: 
                            size_hint: (None, None) 
                            orientation: "vertical"
                            height: dp(100)
                            width: dp(49)
                            padding: [5,35,15,35]
                            Button:
                                size_hint: (None,None)
                                height: dp(30)
                                width: dp(29)
                                background_color: hex('#F4433600')
                                center: self.parent.center
                                pos: self.parent.pos
                                on_press: root.refresh_latest_software_version()
                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        source: "./asmcnc/apps/wifi_app/img/mini_refresh.png"
                                        center_x: self.parent.center_x
                                        y: self.parent.y
                                        size: self.parent.width, self.parent.height
                                        allow_stretch: True

                        Label: 
                            id: latest_software_version_label
                            color: 0,0,0,1
                            font_size: 18
                            markup: True
                            halign: "center"
                            valign: "center"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos

                                
            # Exit button
            BoxLayout: 
                size_hint: (None, None)
                height: dp(112)
                width: dp(112)
                Button:
                    size_hint: (None,None)
                    height: dp(112)
                    width: dp(112)
                    background_color: hex('#F4433600')
                    center: self.parent.center
                    pos: self.parent.pos
                    on_press: root.quit_to_lobby()
                    BoxLayout:
                        padding: 0
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/wifi_app/img/quit.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

        # Body box
        BoxLayout:
            size_hint: (None, None)
            height: dp(320)
            width: dp(800)
            padding: [30, 0, 30, 30]
            spacing: 30
            orientation: 'horizontal'
            
            BoxLayout: 
                size_hint: (None, None)
                height: dp(290)
                width: dp(355)    
                orientation: "vertical"  
                padding: [30, 30, 30, 30]
                spacing: 0
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(30)
                    width: dp(295)
                    padding: [0,5,0,0]
                    Label: 
                        id: update_using_wifi_label
                        color: 0,0,0,1
                        font_size: 18
                        markup: True
                        halign: "left"
                        valign: "top"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos            
                    
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(90)
                    width: dp(295)
                    padding: [0,5,0,0]
                    Label:
                        id: update_using_wifi_instructions_label
                        color: 0,0,0,1
                        font_size: 16
                        markup: True
                        halign: "left"
                        valign: "top"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos

                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(110)
                    width: dp(295)                    
                    BoxLayout:
                        size_hint: (None, None)
                        height: dp(110)
                        width: dp(145)
                        padding: [20,25,65,25]
                        Image:
                            id: wifi_image
                            source: root.wifi_on
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

                    BoxLayout:
                        size_hint: (None, None)
                        height: dp(110)
                        width: dp(150)
                        Button:
                            id: wifi_update_button
                            background_normal: "./asmcnc/apps/SWupdater_app/img/update_button.png"
                            background_down: "./asmcnc/apps/SWupdater_app/img/update_button.png"
                            border: [dp(14.5)]*4
                            size_hint: (None,None)
                            width: dp(150)
                            height: dp(110)
                            on_press: root.prep_for_sw_update_over_wifi()
                            text: 'Update'
                            font_size: '30sp'
                            color: hex('#f9f9f9ff')
                            markup: True
                            center: self.parent.center
                            pos: self.parent.pos           
                        
            BoxLayout: 
                size_hint: (None, None)
                height: dp(290)
                width: dp(355)
                orientation: "vertical"  
                padding: [30, 30, 30, 30]
                spacing: 0  
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size

                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(30)
                    width: dp(295)
                    Label:
                        id: update_using_usb_label
                        color: 0,0,0,1
                        font_size: 18
                        markup: True
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos              
                    
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(90)
                    width: dp(295)
                    Label:
                        id: update_using_usb_instructions_label
                        color: 0,0,0,1
                        font_size: 16
                        markup: True
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos

                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(110)
                    width: dp(295)
                    orientation: "horizontal"
                    BoxLayout:
                        size_hint: (None, None)
                        height: dp(110)
                        width: dp(145)
                        padding: [0,26.5,32,26.5]
                        Image:
                            id: usb_image
                            source: root.usb_off
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

                    BoxLayout:
                        size_hint: (None, None)
                        height: dp(110)
                        width: dp(150)
                        Button:
                            id: usb_update_button
                            background_normal: "./asmcnc/apps/SWupdater_app/img/update_button.png"
                            background_down: "./asmcnc/apps/SWupdater_app/img/update_button.png"
                            border: [dp(14.5)]*4
                            size_hint: (None,None)
                            width: dp(150)
                            height: dp(110)
                            on_press: root.prep_for_sw_update_over_usb()
                            text: 'Update'
                            font_size: '30sp'
                            color: hex('#f9f9f9ff')
                            markup: True
                            center: self.parent.center
                            pos: self.parent.pos

""")

class SWUpdateScreen(Screen):
    
    WIFI_CHECK_INTERVAL = 2
    
    wifi_on = "./asmcnc/apps/SWupdater_app/img/wifi_on.png"
    wifi_off = "./asmcnc/apps/SWupdater_app/img/wifi_off.png"
    usb_on = "./asmcnc/apps/SWupdater_app/img/USB_on.png"
    usb_off = "./asmcnc/apps/SWupdater_app/img/USB_off.png"
    
    def __init__(self, **kwargs):
        super(SWUpdateScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.set=kwargs['settings']
        self.l=kwargs['localization']
        
        self.update_strings()

        self.usb_stick = usb_storage.USB_storage(self.sm, self.l)
        
        self.sw_version_label.text = '[b]' + self.set.sw_version + '[/b]'
        self.update_screen_with_latest_version()


    def on_enter(self):

        self.update_strings()

        # Keep tabs on wifi connection
        self.check_wifi_connection(1)
        self.poll_wifi = Clock.schedule_interval(self.check_wifi_connection, self.WIFI_CHECK_INTERVAL)

        # Set up and keep tabs on usb connection
        self.usb_stick.enable()
        self.check_USB_status(1)
        self.poll_USB = Clock.schedule_interval(self.check_USB_status, 0.25)


    def on_leave(self):
        Clock.unschedule(self.poll_USB)
        Clock.unschedule(self.poll_wifi)
        self.usb_stick.disable()
        self.sm.remove_widget(self.sm.get_screen('update'))


    def quit_to_lobby(self):
        self.sm.current = 'lobby'


    def refresh_latest_software_version(self):

        self.latest_software_version_label.text = (
            self.l.get_bold('Refreshing') + \
            '...' + '\n\n' + \
            self.l.get_bold('Please wait')
        )

        def do_refresh():

            if self.usb_stick.is_available():
                dir_path_name = self.set.find_usb_directory()
        
                if dir_path_name != 2 and dir_path_name != 0:
                    if self.set.set_up_remote_repo(dir_path_name):
                        self.set.refresh_latest_sw_version()

                    else:
                        if self.wifi_image.source != self.wifi_on:
                            refresh_error_message = (
                                self.l.get_str('Could not refresh version!') + \
                                '\n\n' + \
                                self.l.get_str('Please check the file on your USB stick.')
                                )
                            popup_info.PopupError(self.sm, self.l, refresh_error_message)
                else:
                    if self.wifi_image.source != self.wifi_on:
                        refresh_error_message = (
                            self.l.get_str('Could not refresh version!')
                            +'\n\n' + \
                            self.l.get_str('Please check the file on your USB stick.')
                            )
                        popup_info.PopupError(self.sm, self.l, refresh_error_message)

                self.set.clear_remote_repo(dir_path_name)                 

            if self.wifi_image.source == self.wifi_on:
                self.set.refresh_latest_sw_version()

            if not self.usb_stick.is_available() and self.wifi_image.source != self.wifi_on:
                refresh_error_message = (
                    self.l.get_str('Could not refresh version!')
                    +'\n\n' + \
                    self.l.get_str('Please check your connection.')
                    )
                popup_info.PopupError(self.sm, self.l, refresh_error_message)

            self.update_screen_with_latest_version()

        Clock.schedule_once(lambda dt: do_refresh(),0.5)


    def update_screen_with_latest_version(self):
        if self.set.latest_sw_version != '':    
            self.latest_software_version_label.text = (
                self.l.get_bold('New version available') + \
                '[b]: ' + self.set.latest_sw_version + '[/b]'
                )
        elif self.wifi_image.source != self.wifi_on:
            self.latest_software_version_label.text = self.l.get_str('WiFi connection is needed to check if a new version is available.')
        else:
            self.latest_software_version_label.text = self.l.get_bold('You are up to date!')


    def prep_for_sw_update_over_wifi(self):

        wait_popup = popup_info.PopupWait(self.sm, self.l)

        def check_connection_and_version():
            if self.wifi_image.source != self.wifi_on:
                description = self.l.get_str("No WiFi connection!")
                popup_info.PopupError(self.sm, self.l, description)
                wait_popup.popup.dismiss()
                return

            if self.set.latest_sw_version.endswith('beta'):
                wait_popup.popup.dismiss()
                popup_update_SW.PopupBetaUpdate(self.sm, 'wifi')
                return

            Clock.schedule_once( lambda dt: wait_popup.popup.dismiss(), 0.2)
            self.get_sw_update_over_wifi()

        Clock.schedule_once(lambda dt: check_connection_and_version(), 3)

    def prep_for_sw_update_over_usb(self):

        wait_popup = popup_info.PopupWait(self.sm, self.l)

        def check_connection_and_version():
            if self.usb_image.source != self.usb_on:
                description = self.l.get_str("No USB drive found!")
                popup_info.PopupError(self.sm, self.l, description)
                wait_popup.popup.dismiss()
                return

            if self.set.latest_sw_version.endswith('beta'):
                wait_popup.popup.dismiss()
                popup_update_SW.PopupBetaUpdate(self.sm, 'usb')
                return

            Clock.schedule_once( lambda dt: wait_popup.popup.dismiss(), 0.2)
            self.get_sw_update_over_usb()

        Clock.schedule_once(lambda dt: check_connection_and_version(), 3)
        
        

    def get_sw_update_over_wifi(self):

        popup_info.PopupWait(self.sm,  self.l)

        def do_sw_update():

            outcome = self.set.get_sw_update_via_wifi()
            
            if outcome == False: 
                description = self.l.get_str("There was a problem updating your software.") + \
                " \n\n" + \
                self.l.get_str("We can try to fix the problem, but you MUST have a stable internet connection and power supply.") + \
                "\n\n" + \
                self.l.get_str("Would you like to repair your software now?")
                popup_info.PopupSoftwareRepair(self.sm, self, description)

            elif outcome == "Software already up to date!":
                description = self.l.get_str("Software already up to date!")
                popup_info.PopupError(self.sm, self.l, description)
                
            elif outcome == "Could not resolve host: github.com":
                description = self.l.get_str("Could not connect to github. Please check that your connection is stable, or try again later.")
                popup_info.PopupError(self.sm, self.l, description)

            else: 
                popup_info.PopupSoftwareUpdateSuccess(self.sm, self.l, outcome)

                message = (
                    self.l.get_str('Please wait') + \
                    '...\n\n' + \
                    self.l.get_str('Console will reboot to finish update.')
                    )

                Clock.schedule_once(lambda dt: popup_info.PopupMiniInfo(self.sm, self.l, message), 3)

        Clock.schedule_once(lambda dt: do_sw_update(), 2)

    def repair_sw_over_wifi(self):
            
        description = self.l.get_str("DO NOT restart your machine until you see instructions to do so on the screen.")
        popup_info.PopupWarning(self.sm, self.l, description)
               
        def delay_clone_to_update_screen():

            if self.wifi_image.source == self.wifi_on:

                outcome = self.set.reclone_EC()
                
                if outcome == False:

                    description = (
                        self.l.get_str("It was not possible to back up the software safely, please try again later.") + \
                        "\n\n" + \
                        self.l.get_str("If this issue persists, please contact Yeti Tool Ltd for support.")
                        )

                    popup_info.PopupError(self.sm, self.l, description)           
            else:

                description = (
                    self.l.get_str("No WiFi connection!") + \
                    "\n\n" + \
                    self.l.get_str("You MUST have a stable wifi connection to repair your software.") + \
                    "\n\n" + \
                    self.l.get_str("Please try again later.")
                )

                popup_info.PopupError(self.sm, self.l, description)

        Clock.schedule_once(lambda dt: delay_clone_to_update_screen(), 3)

    def get_sw_update_over_usb(self):

        popup_info.PopupWait(self.sm,  self.l)

        def do_sw_update():
            outcome = self.set.get_sw_update_via_usb()
            
            if outcome == 2:
                description = (
                    self.l.get_str("More than one folder called easycut-smartbench was found on the USB drive.").replace(
                        self.l.get_str('easycut-smartbench'), "[b]easycut-smartbench[/b]"
                        ) + \
                    "\n\n" + \
                    self.l.get_str("Please make sure that there is only one instance of easycut-smartbench on your USB drive, and try again.").replace(
                        self.l.get_str('easycut-smartbench'), "[b]easycut-smartbench[/b]"
                        )
                    )
                popup_info.PopupError(self.sm, self.l, description)

            elif outcome == 0:
                description = (
                    self.l.get_str("There was no folder or zipped folder called easycut-smartbench found on the USB drive.").replace(
                        self.l.get_str('easycut-smartbench'), "[b]easycut-smartbench[/b]"
                        ) + \
                    "\n\n" + \
                    self.l.get_str("Please make sure that the folder containing the software is called easycut-smartbench, and try again.").replace(
                        self.l.get_str('easycut-smartbench'), "[b]easycut-smartbench[/b]"
                        )
                    )
                popup_info.PopupError(self.sm, self.l, description)

            elif outcome == "update failed":
                
                description = (
                    self.l.get_str("It was not possible to update your software from the USB drive.") + \
                    "\n\n" + \
                    self.l.get_str("Please check your easycut-smartbench folder or try again later.").replace(
                        self.l.get_str('easycut-smartbench'), "[b]easycut-smartbench[/b]"
                        ) + \
                    " " + \
                    self.l.get_str("If this problem persists you may need to connect to the internet to update your software, and repair it if necessary.") + \
                    "\n\n"
                    )

                popup_info.PopupError(self.sm, self.l, description)              
            
            else:
                self.usb_stick.disable()
                update_success = outcome
                popup_info.PopupSoftwareUpdateSuccess(self.sm, self.l, update_success)

                message = (
                    self.l.get_str('Please wait') + \
                    '...\n\n' + \
                    self.l.get_str('Console will reboot to finish update.')
                    )

                Clock.schedule_once(lambda dt: popup_info.PopupMiniInfo(self.sm, self.l, message), 3)

        Clock.schedule_once(lambda dt: do_sw_update(), 2)
                
    def check_wifi_connection(self, dt):

        try:
            f = os.popen('hostname -I')
            first_info = f.read().strip().split(' ')[0]
            if len(first_info.split('.')) == 4:
                self.wifi_image.source = self.wifi_on
            else:
                self.wifi_image.source = self.wifi_off
        except:
            self.wifi_image.source = self.wifi_off

    def check_USB_status(self, dt): 
        if self.usb_stick.is_available():
            self.usb_image.source = self.usb_on
        else:
            self.usb_image.source = self.usb_off


    def update_strings(self):

        self.current_version_label.text = self.l.get_bold("Current Version")
        self.update_using_wifi_label.text = self.l.get_bold("Update using WiFi")
        self.update_using_wifi_instructions_label.text = self.l.get_str("Ensure connection is stable before attempting to update.")
        self.wifi_update_button.text = self.l.get_str("Update")
        self.update_using_usb_label.text = self.l.get_bold("Update using USB")
        self.update_using_usb_instructions_label.text = (
            self.l.get_str("Insert a USB stick containing the latest software.") + \
            "\n" + 
            self.l.get_str("Go to www.yetitool.com/support for help on how to do this.")
            )
        self.usb_update_button.text = self.l.get_str("Update")
