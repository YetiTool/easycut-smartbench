'''
Created on 19 Aug 2017

@author: Ed
'''
# config

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.video import Video

import sys, os

Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex

<InitialScreen>:

    video:video


### VIDEO DOESN'T WORK WITH 3B+!!!!!
### https://stackoverflow.com/questions/51601976/kivy-video-player-is-not-working-on-raspberry-3b

### Initial Video code
#     FloatLayout:
#     
#         Video:
#             id: video
#             source: './asmcnc/skavaUI/vid/yeti_intro.mp4'
#             state: 'play'
# #             eos: 'loop'



#     home_button:home_button
#     message_label:message_label
#     status_label:status_label
    
#     canvas.before:
#         Rectangle:
#             pos: self.pos
#             size: self.size
#             source: 'asmcnc/skavaUI/img/scene_original.png'
    

#         Button:
#             id: home_button
#             pos_hint: {'center_x':0.5, 'center_y':0.7}
#             size_hint: None, None            
#             height: 130
#             width: 410    
#             background_color: hex('#F4433600')
#             on_release: 
#                 root.home_and_listen_for_idle()
#                 self.background_color = hex('#F4433600')
#             on_press: 
#                 self.background_color = hex('#F44336FF')
#             BoxLayout:
#                 padding: 0
#                 size: self.parent.size
#                 pos: self.parent.pos
#                 Image:
#                     source: "./asmcnc/skavaUI/img/yeti_home.png"
#                     center_x: self.parent.center_x
# #                     y: self.parent.y
# #                     size: 200, 200
# #                     allow_stretch: True    
# 
# 
#         BoxLayout:
#             padding: 10
#             spacing: 10
#             orientation: "vertical"
#             pos_hint: {'center_x':0.5, 'center_y':0.35}
#             size_hint: 0.7, 0.15            
#             canvas:
#                 Color:
#                     rgba: 1,1,1,0.9
#                 RoundedRectangle:
#                     pos: self.pos
#                     size: self.size
#              
#             Label:
#                 size_hint_y: 0.8
#                 markup: True 
#                 text: 'Checking serial connection...'
#                 font_size: 18
#                 color: 0,0,0,1
#                 id: message_label
#             Label:
#                 size_hint_y: 0.2
#                 markup: True 
#                 text: 'Status'
#                 font_size: 10
#                 color: 0,0,0,1
#                 id: status_label
# 
#         
#         BoxLayout:
#             padding: 10
#             spacing: 10
#             orientation: "horizontal"
#             pos_hint: {'center_x':0.5, 'center_y':0.15}
#             size_hint: 0.4, 0.15   
#             canvas.before:
#                 Color:
#                     rgba: 1,1,1,0.9
#                 RoundedRectangle:
#                     pos: self.pos
#                     size: self.size
#                      
#             Button:
#                 background_color: hex('#F4433600')
#                 on_release: 
#                     root.quit_to_console()
#                     self.background_color = hex('#F4433600')
#                 on_press: 
#                     self.background_color = hex('#F44336FF')
#                 BoxLayout:
#                     padding: 0
#                     size: self.parent.size
#                     pos: self.parent.pos
#                     Image:
#                         source: "./asmcnc/skavaUI/img/console.png"
#                         center_x: self.parent.center_x
#                         y: self.parent.y
#                         size: self.parent.width, self.parent.height
#                         allow_stretch: True                               
#             Button:
#                 background_color: hex('#F4433600')
#                 on_release: 
#                     root.reboot()
#                     self.background_color = hex('#F4433600')
#                 on_press: 
#                     self.background_color = hex('#F44336FF')
#                 BoxLayout:
#                     padding: 0
#                     size: self.parent.size
#                     pos: self.parent.pos
#                     Image:
#                         source: "./asmcnc/skavaUI/img/reboot.png"
#                         center_x: self.parent.center_x
#                         y: self.parent.y
#                         size: self.parent.width, self.parent.height
#                         allow_stretch: True                               
#             Button:
#                 background_color: hex('#F4433600')
#                 on_release: 
#                     root.skip_homing()
#                     self.background_color = hex('#F4433600')
#                 on_press: 
#                     self.background_color = hex('#F44336FF')
#                 BoxLayout:
#                     padding: 0
#                     size: self.parent.size
#                     pos: self.parent.pos
#                     Image:
#                         source: "./asmcnc/skavaUI/img/skip.png"
#                         center_x: self.parent.center_x
#                         y: self.parent.y
#                         size: self.parent.width, self.parent.height
#                         allow_stretch: True       
 

    

                

""")

GRBL_STATUS_INTERVAL = 0.2

class InitialScreen(Screen):

    
    def __init__(self, **kwargs):
        super(InitialScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.video.bind(eos=self.loop_video)

    def loop_video(self, *args, **kwargs):
        self.video.state = 'stop'
        self.go_to_lobby(0)
    
    def on_enter(self):
        if sys.platform == "win32": # TO SKIP VIDEO
            Clock.schedule_once(self.go_to_lobby, 1) # Delay for grbl to initialize 
#         Clock.schedule_once(self.refresh_serial_status, 2) # Delay for grbl to initialize 
#         Clock.schedule_interval(self.refresh_grbl_status, GRBL_STATUS_INTERVAL)      # Poll for status
    
    def refresh_serial_status(self, dt):
        if self.m.is_connected():
            self.home_button.disabled = False
            self.message_label.text = '[color=000000]Tap the logo to home[/color]'
        else:
            self.home_button.disabled = True
            self.message_label.text = '[color=f44336]No serial - check the cable.[/color]'


    def refresh_grbl_status(self, dt):
        if self.m.is_connected():
            self.status_label.text = 'Status: ' + self.m.state()


    def home_and_listen_for_idle(self):
        self.home_button.disabled = True
        self.message_label.text = "[color=4caf50ff]Homing...[/color]"
        self.m.home_all()
        self.detect_idle = Clock.schedule_interval(self.detect_homing_complete, 1)

         
    def detect_homing_complete(self, dt):
        if self.m.state() == 'Idle': 
            self.detect_idle.cancel()
            self.go_to_home_screen()

 
    # Dev functions TODO: remove, or make secure
    def quit_to_console(self):
        print 'Bye!'
        sys.exit()
    
    def reboot(self):
        if sys.platform != "win32": 
            sudoPassword = 'posys'
            command = 'sudo reboot'
            p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    
    def skip_homing(self):
        self.go_to_home_screen()
    
    def go_to_home_screen(self):
        self.video.state = 'stop'
        #self.sm.transition = SlideTransition()
        #self.sm.transition.direction = 'up'
        self.sm.current = 'home'         

    def go_to_lobby(self, dt):
        self.video.state = 'stop'
        #self.sm.transition = FadeTransition()
        self.sm.current = 'lobby'         

        
