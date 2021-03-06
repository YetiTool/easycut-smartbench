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

    sw_version_label: sw_version_label
    latest_software_version_label: latest_software_version_label
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
                            color: 0,0,0,1
                            font_size: 18
                            markup: True
                            halign: "center"
                            valign: "bottom"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                            text: "[b]Current Version[/b]"                  
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
                            text: "[b]-[/b]"                         
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
                            text: "[b]-[/b]"

                                
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
                        color: 0,0,0,1
                        font_size: 18
                        markup: True
                        halign: "left"
                        valign: "top"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                        text: "[b]Update using WiFi[/b]"                    
                    
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(90)
                    width: dp(295)
                    padding: [0,5,0,0]
                    Label: 
                        color: 0,0,0,1
                        font_size: 16
                        markup: True
                        halign: "left"
                        valign: "top"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                        text: root.wifi_instructions

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
                            size_hint: (None,None)
                            height: dp(110)
                            width: dp(150)
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.prep_for_sw_update_over_wifi()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/SWupdater_app/img/update_button_with_text.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True                
                        
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
                        color: 0,0,0,1
                        font_size: 18
                        markup: True
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                        text: "[b]Update using USB[/b]"                  
                    
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(90)
                    width: dp(295)
                    Label: 
                        color: 0,0,0,1
                        font_size: 16
                        markup: True
                        halign: "left"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                        text: root.usb_instructions

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
                            size_hint: (None,None)
                            height: dp(110)
                            width: dp(150)
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.prep_for_sw_update_over_usb()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/SWupdater_app/img/update_button_with_text.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
""")

class SWUpdateScreen(Screen):

    wifi_instructions = 'Ensure connection is stable before attempting to update.'
    usb_instructions = 'Insert a USB stick containing the latest software.\n' + \
    'Go to www.yetitool.com/support for help on how to do this.'
    
    WIFI_CHECK_INTERVAL = 2
    
    wifi_on = "./asmcnc/apps/SWupdater_app/img/wifi_on.png"
    wifi_off = "./asmcnc/apps/SWupdater_app/img/wifi_off.png"
    usb_on = "./asmcnc/apps/SWupdater_app/img/USB_on.png"
    usb_off = "./asmcnc/apps/SWupdater_app/img/USB_off.png"
    
    def __init__(self, **kwargs):
        super(SWUpdateScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.set=kwargs['settings']
        
        self.usb_stick = usb_storage.USB_storage(self.sm)
        
        self.sw_version_label.text = '[b]' + self.set.sw_version + '[/b]'
        self.update_screen_with_latest_version()

        
    def refresh_latest_software_version(self):

        self.latest_software_version_label.text = '[b]Refreshing...\n\nPlease wait.[/b]'

        def do_refresh():

            try:
                if self.usb_stick.is_available():
                    dir_path_name = self.set.find_usb_directory()
            
                    if dir_path_name != 2 and dir_path_name != 0 and dir_path_name != '':
                        if self.set.set_up_remote_repo(dir_path_name):
                            self.set.refresh_latest_sw_version()

                        else:
                            if self.wifi_image.source != self.wifi_on:
                                refresh_error_message = 'Could not refresh version!\n\nPlease check the file on your USB stick.'
                                popup_info.PopupError(self.sm, refresh_error_message)
                    else:
                        if self.wifi_image.source != self.wifi_on:
                            refresh_error_message = 'Could not refresh version!\n\nPlease check the file on your USB stick.'
                            popup_info.PopupError(self.sm, refresh_error_message)

                    try: self.set.clear_remote_repo(dir_path_name)
                    except: pass

                if self.wifi_image.source == self.wifi_on:
                    self.set.refresh_latest_sw_version()

                if not self.usb_stick.is_available() and self.wifi_image.source != self.wifi_on:
                    refresh_error_message = 'Could not refresh version!\n\nPlease check your connection.'
                    popup_info.PopupError(self.sm, refresh_error_message)
            except:
                refresh_error_message = 'Could not refresh version!\n\nPlease check your connection.'
                popup_info.PopupError(self.sm, refresh_error_message)

            self.update_screen_with_latest_version()

        Clock.schedule_once(lambda dt: do_refresh(),0.5)
    
    def update_screen_with_latest_version(self):
        if self.set.latest_sw_version != '':
            if self.set.latest_sw_version != self.set.sw_version:
                self.latest_software_version_label.text = '[b]New version available: ' + self.set.latest_sw_version + '[/b]'
            else: 
                self.latest_software_version_label.text = '[b]You are up to date![/b]'
        else:
            self.latest_software_version_label.text = '[b]Could not fetch version! Connection issue.[/b]'
 
    def on_enter(self):

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

    def prep_for_sw_update_over_wifi(self):

        wait_popup = popup_info.PopupWait(self.sm)

        def check_connection_and_version():
            if self.wifi_image.source != self.wifi_on:
                description = "No WiFi connection!"
                popup_info.PopupError(self.sm, description)
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

        wait_popup = popup_info.PopupWait(self.sm)

        def check_connection_and_version():
            if self.usb_image.source != self.usb_on:
                description = "No USB drive found!"
                popup_info.PopupError(self.sm, description)
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

        popup_info.PopupWait(self.sm)

        def do_sw_update():

            outcome = self.set.get_sw_update_via_wifi()
            
            if outcome == False: 
                description = "There was a problem updating your software. \n\n" \
                "We can try to fix the problem, but you MUST have a stable internet connection and" \
                " power supply.\n\n" \
                "Would you like to repair your software now?"
                popup_info.PopupSoftwareRepair(self.sm, self, description)

            elif outcome == "Software already up to date!": 
                popup_info.PopupError(self.sm, outcome)
                
            elif "Could not resolve host: github.com" in outcome:
                description = "Could not connect to github. Please check that your connection is stable, or try again later"
                popup_info.PopupError(self.sm, description)

            else: 
                popup_info.PopupSoftwareUpdateSuccess(self.sm, outcome)

                message = 'Please wait...\n\nConsole will reboot to finish update.'
                Clock.schedule_once(lambda dt: popup_info.PopupMiniInfo(self.sm, message), 3)

        Clock.schedule_once(lambda dt: do_sw_update(), 2)

    def repair_sw_over_wifi(self):
            
        description = "DO NOT restart your machine until you see instructions to do so on the screen."
        popup_info.PopupWarning(self.sm, description)
               
        def delay_clone_to_update_screen():
            if self.wifi_image.source == self.wifi_on:
                outcome = self.set.reclone_EC()
                
                if outcome == False:
                    description = "It was not possible to backup the software safely, please check your connection and try again later.\n\n" + \
                    "If this issue persists, please contact Yeti Tool Ltd for support."
                    popup_info.PopupError(self.sm, description)           
            else: 
                description = "No WiFi connection!\n\nYou MUST have a stable wifi connection to repair your software.\n\n" + \
                "Please try again later."
                popup_info.PopupError(self.sm, description)

        Clock.schedule_once(lambda dt: delay_clone_to_update_screen(), 3)

    def get_sw_update_over_usb(self):

        popup_info.PopupWait(self.sm)

        def do_sw_update():
            outcome = self.set.get_sw_update_via_usb()
            
            if outcome == 2:
                description = "More than one folder called [b]easycut-smartbench[/b] was found on the USB drive.\n\n" + \
                "Please make sure that there is only one instance of [b]easycut-smartbench[/b] on your USB drive, and try again."
                popup_info.PopupError(self.sm, description)

            elif outcome == 0:
                description = "There was no folder or zipped folder called [b]easycut-smartbench[/b] found on the USB drive.\n\n" + \
                "Please make sure that the folder containing the software is called [b]easycut-smartbench[/b], and try again."
                popup_info.PopupError(self.sm, description)

            elif outcome == "update failed":
                
                # this may need its own special bigger pop-up
                
                description = "It was not possible to update your software from the USB drive.\n\n" + \
                "Please check your [b]easycut-smartbench[/b] folder or try again later. If this problem persists you may need to connect to the " + \
                "internet to update your software, and repair it if necessary.\n\n"
                popup_info.PopupError(self.sm, description)              
            
            else:
                self.usb_stick.disable()
                update_success = outcome
                popup_info.PopupSoftwareUpdateSuccess(self.sm, update_success)

                message = 'Please wait...\n\nConsole will reboot to finish update.'
                Clock.schedule_once(lambda dt: popup_info.PopupMiniInfo(self.sm, message), 3)

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