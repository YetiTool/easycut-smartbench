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
                        width: dp(385)
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
                        width: dp(213)
                        orientation: "vertical"
                        padding: [0,0,30,0]
#                         Label: 
#                             color: 0,0,0,1
#                             font_size: 18
#                             markup: True
#                             halign: "center"
#                             valign: "bottom"
#                             text_size: self.size
#                             size: self.parent.size
#                             pos: self.parent.pos
#                             text: "[b]Available Version[/b]"
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
                            on_press: root.get_sw_update_over_wifi()
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
                            on_press: root.get_sw_update_over_usb()
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
        
        if self.set.latest_sw_version != '':    
            self.latest_software_version_label.text = '[b]New version available: ' + self.set.latest_sw_version + '[/b]'
        elif self.wifi_image.source != self.wifi_on:
            self.latest_software_version_label.text = 'WiFi connection is needed to check if a new version is available.'
        else:
            self.latest_software_version_label.text = '[b]You are up to date![/b]'
 
    def on_enter(self):
        self.check_wifi_connection(1)
        self.poll_wifi = Clock.schedule_interval(self.check_wifi_connection, self.WIFI_CHECK_INTERVAL)

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

    def get_sw_update_over_wifi(self):
               
        if self.wifi_image.source == self.wifi_on:
            
            popup_info.PopupWait(self.sm)
            
            def do_update():
            
                outcome = self.set.get_sw_update_via_wifi()
                
                if outcome == False: 
                    description = "There was a problem updating your software. \n\n" \
                    "We can try to fix the problem, but you MUST have a stable internet connection and" \
                    " power supply.\n\n" \
                    "Would you like to repair your software now?"
                    popup_info.PopupSoftwareRepair(self.sm, self, description)               
                elif outcome == "Software already up to date!": 
                    popup_info.PopupError(self.sm, outcome)
                    
                elif outcome == "Could not resolve host: github.com":
                    description = "Could not connect to github. Please check that your connection is stable, or try again later"
                    popup_info.PopupError(self.sm, outcome)
                else: 
                    popup_info.PopupSoftwareUpdateSuccess(self.sm, outcome)
            
            Clock.schedule_once(lambda dt: do_update(), 2)
            
        else: 
            description = "No WiFi connection!"
            popup_info.PopupError(self.sm, description)

    def repair_sw_over_wifi(self):
            
        description = "DO NOT restart your machine until you see instructions to do so on the screen."
        popup_info.PopupWarning(self.sm, description)
               
        def delay_clone_to_update_screen():
            if self.wifi_image.source == self.wifi_on:
                outcome = self.set.reclone_EC()
                
                if outcome == False:
                    description = "It was not possible to backup EasyCut safely, please try again later.\n\n" + \
                    "If this issue persists, please contact Yeti Tool Ltd for support."
                    popup_info.PopupError(self.sm, description)           
            else: 
                description = "No WiFi connection!\n\nYou MUST have a stable wifi connection to repair your software.\n\n" + \
                "Please try again later."
                popup_info.PopupError(self.sm, description)


        Clock.schedule_once(lambda dt: delay_clone_to_update_screen(), 3)

    def get_sw_update_over_usb(self):
        if self.usb_image.source == self.usb_on:
            
            popup_info.PopupWait(self.sm)
            
            def do_update():
                outcome = self.set.get_sw_update_via_usb()
                
                if outcome == 2:
                    description = "More than one folder called [b]easycut-smartbench[/b] was found on the USB drive.\n\n" + \
                    "Please make sure that there is only one instance of EasyCut on your USB drive, and try again."
                    popup_info.PopupError(self.sm, description)
                elif outcome == 0:
                    description = "There was no folder or zipped folder called [b]easycut-smartbench[/b] found on the USB drive.\n\n" + \
                    "Please make sure that the folder containing EasyCut is called [b]easycut-smartbench[/b], and try again."
                    popup_info.PopupError(self.sm, description)
                elif outcome == "update failed":
                    
                    # this may need its own special bigger pop-up
                    
                    description = "It was not possible to update your software from the USB drive.\n\n" + \
                    "Please check your EasyCut folder or try again later. If this problem persists you may need to connect to the " + \
                    "internet to update your software, and repair it if necessary.\n\n"
                    popup_info.PopupError(self.sm, description)              
                
                else:
                    self.usb_stick.disable()
                    update_success = outcome
                    popup_info.PopupSoftwareUpdateSuccess(self.sm, update_success)
                
            
            Clock.schedule_once(lambda dt: do_update(), 2)
            
        else: 
            description = "No USB drive found!"
            popup_info.PopupError(self.sm, description)

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