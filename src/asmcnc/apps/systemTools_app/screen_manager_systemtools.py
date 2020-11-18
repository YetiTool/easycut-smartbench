from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.comms import usb_storage
from asmcnc.skavaUI import popup_info
from asmcnc.apps.systemTools_app.screens import screen_system_menu, screen_build_info, screen_beta_testers, screen_grbl_settings, screen_factory_settings, screen_update_testing

class ScreenManagerSystemTools(object):

    def __init__(self, app_manager, screen_manager, machine):

        self.am = app_manager
        self.sm = screen_manager
        self.m = machine
        self.usb_stick = usb_storage.USB_storage(self.sm)

    def open_system_tools(self):
        if not self.sm.has_screen('system_menu'): 
            system_menu_screen = screen_system_menu.SystemMenuScreen(name = 'system_menu', machine = self.m, system_tools = self)
            self.sm.add_widget(system_menu_screen)
        self.sm.current = 'system_menu'

    def open_build_info_screen(self):
       if not self.sm.has_screen('build_info'):
           build_info_screen = screen_build_info.BuildInfoScreen(name = 'build_info', machine = self.m, system_tools = self)
           self.sm.add_widget(build_info_screen)
       self.sm.current = 'build_info'

    def download_logs_to_usb(self):
        self.usb_stick.enable()

        def get_logs():

                message = 'Downloading logs, please wait...'
                wait_popup = popup_info.PopupWait(self.sm, description = message)
            if self.usb_stick.is_usb_mounted_flag == True:
                os.system("journalctl > smartbench_logs.txt && sudo cp --no-preserve=mode,ownership smartbench_logs.txt /media/usb/ && rm smartbench_logs.txt")
                self.usb_stick.disable()
                message = 'Logs downloaded'
                updated_wait_popup = popup_info.PopupWait(self.sm, description = message)
                wait_popup.popup.dismiss()
                Clock.schedule_once(lambda dt: updated_wait_popup.popup.dismiss(), 0.5)
            else:
                Clock.schedule_once(lambda dt: get_logs(), 0.2)

        Clock.schedule_once(lambda dt: get_logs(), 0.2)

    def open_beta_testers_screen(self):
       if not self.sm.has_screen('beta_testers'):
           beta_testers_screen = screen_beta_testers.BetaTestersScreen(name = 'beta_testers', system_tools = self)
           self.sm.add_widget(beta_testers_screen)
       self.sm.current = 'beta_testers'

    def open_grbl_settings_screen(self):
       if not self.sm.has_screen('grbl_settings'):
           grbl_settings_screen = screen_grbl_settings.GRBLSettingsScreen(name = 'grbl_settings', machine = self.m, system_tools = self)
           self.sm.add_widget(grbl_settings_screen)
       self.sm.current = 'grbl_settings'

    def open_factory_settings_screen(self):
       if not self.sm.has_screen('factory_settings'):
           factory_settings_screen = screen_factory_settings.FactorySettingsScreen(name = 'factory_settings', machine = self.m, system_tools = self)
           self.sm.add_widget(factory_settings_screen)
       self.sm.current = 'factory_settings'

    def open_update_testing_screen(self):
       if not self.sm.has_screen('update_testing'):
           update_testing_screen = screen_update_testing.UpdateTestingScreen(name = 'update_testing', machine = self.m, system_tools = self)
           self.sm.add_widget(update_testing_screen)
       self.sm.current = 'update_testing'

    def open_developer_screen(self):
       if not self.sm.has_screen('developer_temp'):
           developer_temp_screen = screen_developer_temp.DeveloperTempScreen(name = 'developer_temp', machine = self.m, system_tools = self)
           self.sm.add_widget(developer_temp_screen)
       self.sm.current = 'developer_temp'

    def back_to_menu(self):
        self.sm.current = 'system_menu'

    def exit_app(self):
        self.destroy_screen('build_info')

        self.sm.current = 'lobby'
        # self.destroy_screen('system_menu')

    def destroy_screen(self, screen_name):
        if self.sm.has_screen(screen_name):
            self.sm.get_screen(screen_name).clear_widgets()
            self.sm.remove_widget(self.sm.get_screen(screen_name))
            print (screen_name + ' deleted')