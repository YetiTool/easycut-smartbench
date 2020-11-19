'''
Created on 18 November 2020
Menu screen for system tools app

@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""

<FactorySettingsScreen>
    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas.before:
            Color: 
                rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
            Rectangle: 
                size: self.size
                pos: self.pos

""")

class FactorySettingsScreen(Screen):

    def __init__(self, **kwargs):
        super(FactorySettingsScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.m = kwargs['machine']

    ## EXIT BUTTONS
    def go_back(self):
        self.systemtools_sm.back_to_menu()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    # def on_enter(self):
    #     self.z_touch_plate_entry.text = str(self.m.z_touch_plate_thickness)