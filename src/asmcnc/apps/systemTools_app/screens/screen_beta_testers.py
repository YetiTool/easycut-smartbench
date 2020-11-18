'''
Created on 18 November 2020
Beta testers screen for system tools app

@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""

<BetaTestersScreen>
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

class BetaTestersScreen(Screen):

    def __init__(self, **kwargs):
        super(BetaTestersScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']

    def go_back(self):
    	self.systemtools_sm.exit_app()

    def go_to_build_info(self):
    	self.systemtools_sm.open_build_info_screen()