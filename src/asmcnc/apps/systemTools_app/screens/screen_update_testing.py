'''
Created on 18 November 2020
Menu screen for system tools app

@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""

<UpdateTestingScreen>
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

class UpdateTestingScreen(Screen):

    def __init__(self, **kwargs):
        super(UpdateTestingScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
		self.m = kwargs['machine']

    def go_back(self):
    	self.systemtools_sm.exit_app()

    def go_to_build_info(self):
    	self.systemtools_sm.open_build_info_screen()