from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '440')
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty 
from kivy.uix.widget import Widget
from kivy.clock import Clock
import sys, os
from kivy.base import runTouchApp


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex


<HelpScreen>

    video_player:video_player
    
    on_enter: video_player.source = './asmcnc/skavaUI/help/welcome.mp4'

    BoxLayout:
        
        BoxLayout:
            size_hint_x: 1.5
            orientation: 'vertical'

            FileChooserIconView:
                size_hint_y: 6
                id: filechooser
                rootpath: './asmcnc/skavaUI/help/'
                filter_dirs: True
                filters: ['*.mp4']
                on_selection: 
                    root.load_video(filechooser.selection[0])
            Button:
                disabled: False
                size_hint_y: 1
                background_color: color_provider.get_rgba("invisible")
                on_release: 
                    self.background_color = hex('#FFFFFF00')
                on_press:
                    root.quit_to_home()
                    self.background_color = hex('#FFFFFFFF')
                BoxLayout:
                    padding: 15
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: image_cancel
                        source: "./asmcnc/skavaUI/img/file_select_cancel.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True 

        BoxLayout:
            size_hint_x: 8
            padding: 10
            VideoPlayer:
                id: video_player
#                 state: "stop"
#                 volume: 0

                
""")



class HelpScreen(Screen):

    def __init__(self, **kwargs):

        super(HelpScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']

    
    def load_video(self, selection):
    
#         self.video_player.state = "stop"
        self.video_player.source = selection
            

    def quit_to_home(self):
        
        self.video_player.state = 'stop'
        self.sm.current = 'home'
        #self.sm.transition.direction = 'up' 
        
