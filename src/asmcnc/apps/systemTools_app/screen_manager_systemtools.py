from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

from asmcnc.apps.systemTools_app.screens import screen_system_menu, screen_build_info

class ScreenManagerSystemTools(object):

    def __init__(self, app_manager, screen_manager, machine):

        self.am = app_manager
        self.sm = screen_manager
        self.m = machine

    def open_system_tools(self):
        if not self.sm.has_screen('system_menu'): 
            system_menu_screen = screen_system_menu.SystemMenuScreen(name = 'system_menu', machine = self.m, system_tools = self)
            self.sm.add_widget(system_menu_screen)
        self.sm.current = 'system_menu'

    def open_build_info_screen(self):
       if not self.sm.has_screen('build_info'):
           build_info_screen = screen_build_info.BuildInfoScreen(name = 'build_info', system_tools = self)
           self.sm.add_widget(build_info_screen)
           self.sm.current = 'build_info'

    def back_to_menu(self):
        self.sm.current = 'system_menu'

    def exit_app(self):
        self.sm.current = 'lobby'

    def destroy_screen(self, screen_name):
        if self.sm.has_screen(screen_name):
            self.sm.get_screen(screen_name).clear_widgets()
            self.sm.remove_widget(self.sm.get_screen(screen_name))
            print (screen_name + ' deleted')