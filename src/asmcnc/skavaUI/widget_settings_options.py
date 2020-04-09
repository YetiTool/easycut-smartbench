'''
Created on 1 Feb 2018
@author: Ed
'''

import sys, os
#import pigpio

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.clock import Clock


PLATFORM_REPOSITORY = "https://github.com/YetiTool/console-raspi3b-plus-platform.git"
PLATFORM_DIRECTORY = "/home/pi/console-raspi3b-plus-platform"
PLATFORM_HOME= "/home/pi/"

Builder.load_string("""

<SettingsOptions>:

    sw_version_label:sw_version_label
    platform_version_label:platform_version_label
    latest_platform_version_label:latest_platform_version_label
    fw_version_label:fw_version_label
    latest_software_version_label:latest_software_version_label

    GridLayout:
        size: self.parent.size
        pos: self.parent.pos
        cols: 3

        Button:
            text: 'Square axes'
            on_press: root.square_axes()
        Button:
            text: 'Get software update'
            on_press: root.get_sw_update()
        Button:
            text: 'Developer'
            on_press: root.go_to_dev()                     


        Label:
            text: ''
            color: 0,0,0,1
        Label:
            text: ''
            color: 0,0,0,1
        Label:
            text: ''
            color: 0,0,0,1


        Label:
            text: 'Code base'
            color: 0,0,0,1
        Label:
            text: 'Current'
            color: 0,0,0,1
        Label:
            text: 'Available'
            color: 0,0,0,1
        Label:
            text: 'EasyCut'
            color: 0,0,0,1
        Label:
            text: 'not found'
            color: 0,0,0,1
            id: sw_version_label
        Label:
            text: '-'
            color: 0,0,0,1
            id: latest_software_version_label
        Label:
            text: 'Platform'
            color: 0,0,0,1
        Label:
            text: 'not found'
            color: 0,0,0,1
            id: platform_version_label
        Label:
            text: '-'
            color: 0,0,0,1
            id: latest_platform_version_label
        Label:
            text: 'Firmware'
            color: 0,0,0,1
        Label:
            text: 'not found'
            color: 0,0,0,1
            id: fw_version_label
        Label:
            text: '-'
            color: 0,0,0,1
#            id: latest_firmware_version_label    
        
""")


class SettingsOptions(Widget):

    buffer_log_mode = StringProperty('normal') # toggles between 'normal' or 'down'(/looks like it's been pressed)
    virtual_hw_mode = StringProperty('normal') # toggles between 'normal' or 'down'(/looks like it's been pressed)
    scraped_grbl_settings = []


    def __init__(self, **kwargs):

        super(SettingsOptions, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.set=kwargs['settings']

        Clock.schedule_once(lambda dt: self.scrape_fw_version(),9)

        self.sw_version_label.text = self.set.sw_version
        self.platform_version_label.text = self.set.platform_version
        self.latest_software_version_label.text = self.set.latest_sw_version
        self.latest_platform_version_label.text = self.set.latest_platform_version

    def scrape_fw_version(self):
        self.fw_version_label.text = str(self.m.s.fw_version)
        
    def reboot(self):
        self.sm.current = 'rebooting'

    def quit_to_console(self):
        print 'Bye!'
        sys.exit()

    def square_axes(self):
        self.m.is_squaring_XY_needed_after_homing = True
        self.m.home_all()

    def return_to_lobby(self):
        self.sm.current = 'lobby'

    def get_sw_update(self):
        self.set.get_sw_update()
        self.sm.current = 'rebooting'
        
        ## FW flash functions: 
        
        # save grbl settings
        # flash fw
        # restore grbl settings - will need to do this auto after FW flash. 
        ### - do by looking for saved settings on start up.
        
        ## PL update: 
        # set tag
        # ansible run
        
        
# Stuff for later------------------------------------------

    def set_tag_pl_update(self):
        os.system("cd /home/pi/console-raspi3b-plus-platform/ && git checkout " + self.latest_platform_version_label.text)
        os.system("/home/pi/console-raspi3b-plus-platform/ansible/templates/ansible-start.sh && sudo reboot")

    def ansible_service_run(self):
        os.system("/home/pi/console-raspi3b-plus-platform/ansible/templates/ansible-start.sh && sudo reboot")
   
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

    def restore_grbl_settings(self):
        g = open('saved_grbl_settings_params.txt', 'r')
        settings_to_restore = g.read()
        print(settings_to_restore)
#         self.m.s.start_sequential_stream(settings_to_restore)   # Send any grbl specific parameters

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
        f.write("auto_restore = True")
        f.write(str(grbl_settings_and_params))
        f.close()
        
        print(grbl_settings_and_params)
#

    def go_to_dev(self): ## Dev screen
        self.sm.current = 'dev'
