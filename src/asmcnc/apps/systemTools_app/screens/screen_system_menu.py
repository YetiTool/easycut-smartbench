'''
Created on 18 November 2020
Menu screen for system tools app

@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen

from asmcnc.skavaUI import popup_info

Builder.load_string("""

<SystemMenuScreen>

    canvas.before:
        Color: 
            rgba: hex('#0d47a1FF')
        Rectangle: 
            size: self.size
            pos: self.pos

    GridLayout:
        size: self.parent.size
        pos: self.parent.pos
        padding: 0
        spacing: 0
        cols: 4
        rows: 2

		Button:
			text: 'Go Back'
			on_press: root.go_back()

		Button:
			text: 'Build Info'
			on_press: root.go_to_build_info()

		Button:
			text: 'Download Logs'
			on_press: root.download_logs()

		Button:
			text: 'Reboot'
			on_press: root.reboot()

		Button:
			text: 'Beta Testers'
			on_press: root.beta_testers()

		Button:
			text: 'GRBL Settings'
			on_press: root.grbl_settings()

		Button:
			text: 'Factory Settings'
			on_press: root.factory_settings()

		Button:
			text: 'Developer'
			on_press: root.developer()

""")

class SystemMenuScreen(Screen):

    def __init__(self, **kwargs):
        super(SystemMenuScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']

    def go_back(self):
    	self.systemtools_sm.exit_app()

    def go_to_build_info(self):
    	self.systemtools_sm.open_build_info_screen()

    def download_logs(self):
    	pass

    def reboot(self):
    	pass

    def beta_testers(self):
    	pass

    def grbl_settings(self):
    	pass

    def factory_settings(self):
    	pass

    def developer(self):
    	pass









