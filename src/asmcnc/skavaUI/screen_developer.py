'''
Created on 13 July 2019

@author: Letty

Screen that contains developer options; old developer tab now contains 
settings that are user-level (inc. Get Updates, version info etc.)
'''

import kivy
import time
#import pigpio
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.clock import Clock

import sys, os

PLATFORM_REPOSITORY = "https://github.com/YetiTool/console-raspi3b-plus-platform.git"
PLATFORM_DIRECTORY = "/home/pi/console-raspi3b-plus-platform"
PLATFORM_HOME= "/home/pi/"


Builder.load_string("""

<DeveloperScreen>:

    sw_version_label:sw_version_label
    sw_hash_label:sw_hash_label
    sw_branch_label:sw_branch_label
    platform_version_label:platform_version_label
    pl_hash_label:pl_hash_label
    pl_branch_label:pl_branch_label
    fw_version_label:fw_version_label
#     latest_platform_version_label:latest_platform_version_label

    GridLayout:
        size: self.parent.size
        pos: self.parent.pos
        cols: 2

        Label:
            text: 'Support & Debugging'
            color: 1,1,1,1
            size_hint_y: 0.25

        Label:
            text: 'Install Updates'
            color: 1,1,1,1
            size_hint_y: 0.25

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2
            size_hint_y: 0.4

            Button:
                text: 'Allow Remote Access'
#                 on_release: root.allow_access()
                disabled: 'true'
                
            Button:
                text: 'Send logs'
                on_release: root.send_logs()
                
            Button:
                text: 'E-mail state'
                on_release: root.email_state()
                
            Button:
                text: 'Diagnostics'
                on_release: root.diagnostics()
                
        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2
            size_hint_y: 0.4
                        
            Button:
                text: 'Pull Software'
                on_release: root.get_sw_update()

            Button:
                text: 'Pull Firmware'
                on_release: root.flash_fw()
                disabled: 'true'

            Button:
                text: 'Pull Platform'
                on_release: root.set_tag_pl_update()
                
            Button:
                text: 'Re-run Platform Install'
                on_release: root.ansible_service_run()

        Label:
            text: 'Roll Back Updates'
            color: 1,1,1,1
            size_hint_y: 0.25
            
        Label:
            text: 'GRBL Settings'
            color: 1,1,1,1
            size_hint_y: 0.25
            
        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2
            size_hint_y: 0.4
                        
            Button:
                text: 'Roll Back Software'
                disabled: 'true'
#                 on_release: root.get_sw_update()

            Button:
                text: 'Roll Back Firmware'
#                 on_release: root.flash_fw()
                disabled: 'true'

            Button:
                text: 'Roll Back Platform'
#                 on_release: root.set_tag_pl_update()
                disabled: 'true'
                
            Button:
                text: 'Roll Back All'
#                 on_release: root.ansible_service_run()
                disabled: 'true'
    
        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2
            size_hint_y: 0.4     

            Button:
                text: ''
                background_normal: ''
                background_color: [0,0,0,0]
                        
            Button:
                text: ''
                background_normal: ''
                background_color: [0,0,0,0]
                           
            Button:
                text: ''
                background_normal: ''
                background_color: [0,0,0,0]
                
            Button:
                text: 'Bake GRBL settings'
                on_release: root.bake_grbl_settings()

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2
            size_hint_y: 0.25
            
            Label:
                text: 'Misc'
                color: 1,1,1,1
#                 size_hint_y: 0.25
#                 size_hint_x: 0.25

            Label:
                text: ''
                color: 1,1,1,1
        
        
        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2
            size_hint_y: 0.25

            Label:
                text: 'Build Information'
                color: 1,1,1,1
#                 size_hint_y: 0.25
#                 size_hint_x: 0.75

            Label:
                text: ''
                color: 1,1,1,1


                
        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2
            size_hint_y: 1
 
            Button:
                text: 'Go back'
                on_release: root.go_back()               

            Label:
                text: 'EasyCut'
                color: 1,1,1,1
            
            Button:
                text: 'Quit to Console'
                on_release: root.quit_to_console()

            Label:
                text: 'EC branch'
                color: 1,1,1,1
                id: sw_branch_label 

            
            Button:
                text: 'Reboot'
                on_release: root.reboot() 
                
            Label:
                text: 'EC hash'
                color: 1,1,1,1
                id: sw_hash_label 
                
            Label: 
                text: ''
                
            Label: 
                text: 'EC version'
                color: 1,1,1,1
                id: sw_version_label 

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2
            size_hint_y: 1
            size_hint_x: 0.75
       
            Label:
                text: 'Platform'
                color: 1,1,1,1
                
            Label:
                text: 'Firmware'
                color: 1,1,1,1
                
            Label:
                text: 'PL branch'
                color: 1,1,1,1
                id: pl_branch_label               

            Label:
                text: 'FW branch'
                color: 1,1,1,1
                
            Label:
                text: 'PL hash'
                color: 1,1,1,1
                id: pl_hash_label

            Label:
                text: 'FW hash'
                color: 1,1,1,1

            Label:
                text: 'PL version'
                color: 1,1,1,1
                id: platform_version_label 

            Label:
                text: 'FW version'
                color: 1,1,1,1
                id: fw_version_label 
""")

class DeveloperScreen(Screen):

    buffer_log_mode = StringProperty('normal') # toggles between 'normal' or 'down'(/looks like it's been pressed)
    virtual_hw_mode = StringProperty('normal') # toggles between 'normal' or 'down'(/looks like it's been pressed)
    scraped_grbl_settings = []


    def __init__(self, **kwargs):

        super(DeveloperScreen, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.set = kwargs['settings']

        self.sw_version_label.text = self.set.sw_version
        self.platform_version_label.text = self.set.platform_version
        self.latest_sw_version = self.set.latest_sw_version
        self.latest_platform_version = self.set.latest_platform_version
        self.sw_hash_label.text = self.set.sw_hash
        self.sw_branch_label.text = self.set.sw_branch
        self.pl_hash_label.text = self.set.pl_hash
        self.pl_branch_label.text = self.set.pl_branch
    
    def on_enter(self, *args):
        self.scrape_fw_version()
        
    def go_back(self):
        self.sm.current = 'home'

    def reboot(self):
        self.sm.current = 'rebooting'

    def quit_to_console(self):
        print 'Bye!'
        sys.exit()

    def square_axes(self):
        self.sm.get_screen('homing').is_squaring_XY_needed_after_homing = True
        self.m.home_all()

    def return_to_lobby(self):
        #self.sm.transition = SlideTransition()
        #self.sm.transition.direction = 'up'
        self.sm.current = 'lobby'

    def scrape_fw_version(self):
        self.fw_version_label.text =str(self.m.s.fw_version)

    def get_sw_update(self): 
        os.system("cd /home/pi/easycut-smartbench/ && git checkout " + self.latest_sw_version)
        os.system('sudo sed -i "s/check_config=False/check_config=True/" /home/pi/easycut-smartbench/src/config.txt')
        os.system('sudo sed -i "s/power_cycle_alert=False/power_cycle_alert=True/" /home/pi/easycut-smartbench/src/config.txt') 
        self.sm.current = 'rebooting'

## Diagnostics

    def send_logs(self):
        os.system("/home/pi/console-raspi3b-plus-platform/ansible/templates/scp-logs.sh")

    def email_state(self):
        os.system("/home/pi/console-raspi3b-plus-platform/ansible/templates/e-mail-state.sh")

    def diagnostics(self):
        self.sm.current = 'diagnostics'

    ## Platform updates

    def set_tag_pl_update(self):
        os.system("cd /home/pi/console-raspi3b-plus-platform/ && git checkout " + self.latest_platform_version)
        os.system("/home/pi/console-raspi3b-plus-platform/ansible/templates/ansible-start.sh && sudo reboot")

    def ansible_service_run(self):
        os.system("/home/pi/console-raspi3b-plus-platform/ansible/templates/ansible-start.sh && sudo reboot")



## GRBL Settings

    def bake_grbl_settings(self):
        grbl_settings = [
                    '$0=10',          #Step pulse, microseconds
                    '$1=255',         #Step idle delay, milliseconds
                    '$2=4',           #Step port invert, mask
                    '$3=1',           #Direction port invert, mask
                    '$4=0',           #Step enable invert, boolean
                    '$5=1',           #Limit pins invert, boolean
                    '$6=0',           #Probe pin invert, boolean
                    '$10=3',          #Status report, mask <----------------------
                    '$11=0.010',      #Junction deviation, mm
                    '$12=0.002',      #Arc tolerance, mm
                    '$13=0',          #Report inches, boolean
                    '$20=1',          #Soft limits, boolean <-------------------
                    '$21=1',          #Hard limits, boolean <------------------
                    '$22=1',          #Homing cycle, boolean <------------------------
                    '$23=3',          #Homing dir invert, mask
                    '$24=600.0',      #Homing feed, mm/min
                    '$25=3000.0',     #Homing seek, mm/min
                    '$26=250',        #Homing debounce, milliseconds
                    '$27=15.000',     #Homing pull-off, mm
                    '$30=25000.0',    #Max spindle speed, RPM
                    '$31=0.0',        #Min spindle speed, RPM
                    '$32=0',          #Laser mode, boolean
#                     '$100=56.649',    #X steps/mm
#                     '$101=56.665',    #Y steps/mm
#                     '$102=1066.667',  #Z steps/mm
                    '$110=8000.0',    #X Max rate, mm/min
                    '$111=6000.0',    #Y Max rate, mm/min
                    '$112=750.0',     #Z Max rate, mm/min
                    '$120=130.0',     #X Acceleration, mm/sec^2
                    '$121=130.0',     #Y Acceleration, mm/sec^2
                    '$122=200.0',     #Z Acceleration, mm/sec^2
                    '$130=1300.0',    #X Max travel, mm TODO: Link to a settings object
                    '$131=2502.0',    #Y Max travel, mm
                    '$132=150.0',     #Z Max travel, mm
                    '$$',             # Echo grbl settings, which will be read by sw, and internal parameters sync'd
                    '$#'              # Echo grbl parameter info, which will be read by sw, and internal parameters sync'd
            ]

        self.m.s.start_sequential_stream(grbl_settings, reset_grbl_after_stream=True)   # Send any grbl specific parameters

    def save_grbl_settings(self):

        self.m.send_any_gcode_command("$$")
        self.m.send_any_gcode_command("$#")

        grbl_settings_and_params = [
                    '$0=' + str(self.m.s.setting_0),    #Step pulse, microseconds
                    '$1=' + str(self.m.s.setting_1),    #Step idle delay, milliseconds
                    '$2=' + str(self.m.s.setting_2),           #Step port invert, mask
                    '$3=' + str(self.m.s.setting_3),           #Direction port invert, mask
                    '$4=' + str(self.m.s.setting_4),           #Step enable invert, boolean
                    '$5=' + str(self.m.s.setting_5),           #Limit pins invert, boolean
                    '$6=' + str(self.m.s.setting_6),           #Probe pin invert, boolean
                    '$10=' + str(self.m.s.setting_10),          #Status report, mask <----------------------
                    '$11=' + str(self.m.s.setting_11),      #Junction deviation, mm
                    '$12=' + str(self.m.s.setting_12),      #Arc tolerance, mm
                    '$13=' + str(self.m.s.setting_13),          #Report inches, boolean
                    '$20=' + str(self.m.s.setting_20),          #Soft limits, boolean <-------------------
                    '$21=' + str(self.m.s.setting_21),          #Hard limits, boolean <------------------
                    '$22=' + str(self.m.s.setting_22),          #Homing cycle, boolean <------------------------
                    '$23=' + str(self.m.s.setting_23),          #Homing dir invert, mask
                    '$24=' + str(self.m.s.setting_24),     #Homing feed, mm/min
                    '$25=' + str(self.m.s.setting_25),    #Homing seek, mm/min
                    '$26=' + str(self.m.s.setting_26),        #Homing debounce, milliseconds
                    '$27=' + str(self.m.s.setting_27),      #Homing pull-off, mm
                    '$30=' + str(self.m.s.setting_30),      #Max spindle speed, RPM
                    '$31=' + str(self.m.s.setting_31),         #Min spindle speed, RPM
                    '$32=' + str(self.m.s.setting_32),           #Laser mode, boolean
                    '$100=' + str(self.m.s.setting_100),   #X steps/mm
                    '$101=' + str(self.m.s.setting_101),   #Y steps/mm
                    '$102=' + str(self.m.s.setting_102),   #Z steps/mm
                    '$110=' + str(self.m.s.setting_110),   #X Max rate, mm/min
                    '$111=' + str(self.m.s.setting_111),   #Y Max rate, mm/min
                    '$112=' + str(self.m.s.setting_112),   #Z Max rate, mm/min
                    '$120=' + str(self.m.s.setting_120),    #X Acceleration, mm/sec^2
                    '$121=' + str(self.m.s.setting_121),    #Y Acceleration, mm/sec^2
                    '$122=' + str(self.m.s.setting_122),    #Z Acceleration, mm/sec^2
                    '$130=' + str(self.m.s.setting_130),   #X Max travel, mm TODO: Link to a settings object
                    '$131=' + str(self.m.s.setting_131),   #Y Max travel, mm
                    '$132=' + str(self.m.s.setting_132),   #Z Max travel, mm
                    'G10 L2 P1 X' + str(self.m.s.g54_x) + ' Y' + str(self.m.s.g54_y) + ' Z' + str(self.m.s.g54_z) # tell GRBL what position it's in                        
            ]

        f = open('saved_grbl_settings_params.txt', 'w')
        f.write("auto_restore = True,")
        f.write(str(grbl_settings_and_params))
        f.close()
        
        print(grbl_settings_and_params)

    def restore_grbl_settings(self):
        
        g = open('saved_grbl_settings_params.txt', 'r')
        settings_to_restore = g.read()
#         self.m.s.start_sequential_stream(settings_to_restore)   # Send any grbl specific parameters

    def flash_fw(self):
        pass
#         os.system("sudo service pigpiod start")
#         pi = pigpio.pi()
#         pi.set_mode(17, pigpio.ALT3)
#         print(pi.get_mode(17))
#         pi.stop()
#         os.system("sudo service pigpiod stop")        
#         os.system("./update_fw.sh")
#         # sys.exit()
#     


