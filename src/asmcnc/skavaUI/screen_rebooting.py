'''
Created Mayh 2019

@author: Letty

Basic screen 
'''
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os


# Kivy UI builder:
Builder.load_string("""

<RebootingScreen>:

    homing_label:homing_label

    canvas:
        Color: 
            rgba: hex('#000000')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding: 70
        spacing: 70
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 1
                
            Label:
                id: homing_label
                text_size: self.size
                size_hint_y: 0.5
                text: "Rebooting..."
                markup: True
                font_size: '40sp'   
                valign: 'middle'
                halign: 'center'            

""")

class RebootingScreen(Screen):
    
    def __init__(self, **kwargs):
        super(RebootingScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
    
    def on_enter(self): 
        self.reboot()
        
    def reboot(self):

        if sys.platform != "win32":
            sudoPassword = 'posys'
            command = 'sudo reboot'
            p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
        