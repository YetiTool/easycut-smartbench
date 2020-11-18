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
        padding: 10
        spacing: 10
        cols: 5
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
            text: 'Quit to Console'
            on_press: root.quit_to_console()

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
            text: 'Update testing'
            on_press: root.update_testing()

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
    	pass # need popup

    def reboot(self):
        self.sm.current = 'rebooting'

    def quit_to_console(self):
        print 'Bye!'
        sys.exit()

    def beta_testers(self):
    	self.systemtools_sm.open_beta_testers_screen()

    def grbl_settings(self):
    	self.systemtools_sm.open_grbl_settings_screen()

    def factory_settings(self):
    	self.systemtools_sm.open_factory_settings_screen()

    def update_testing(self):
        self.systemtools_sm.open_update_testing_screen()

    def developer(self):
    	self.systemtools_sm.open_developer_screen()









