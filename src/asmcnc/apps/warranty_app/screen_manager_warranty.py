from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.skavaUI import popup_info

from asmcnc.apps.warranty_app.screens import \
screen_language_select, \
screen_warranty_registration_1, \
screen_warranty_registration_2, \
screen_warranty_registration_3, \
screen_warranty_registration_4, \
screen_warranty_registration_5

class ScreenManagerWarranty(object):

    def __init__(self, app_manager, screen_manager, machine, localization):

        self.am = app_manager
        self.sm = screen_manager
        self.m = machine
        self.l = localization

    def open_language_select_screen(self):
        if not self.sm.has_screen('language_select'):
            language_select_screen = screen_language_select.LanguageSelectScreen(name = 'language_select', warranty_manager = self, machine = self.m, localization = self.l)
            self.sm.add_widget(language_select_screen)

        self.sm.current = 'language_select'

        self.destroy_screen('warranty_1')
        self.destroy_screen('warranty_2')
        self.destroy_screen('warranty_3')
        self.destroy_screen('warranty_4')
        self.destroy_screen('warranty_5')

    def open_warranty_app(self):

        if not self.sm.has_screen('warranty_1'):
            warranty_registration_1_screen = screen_warranty_registration_1.WarrantyScreen1(name = 'warranty_1', warranty_manager = self, machine = self.m, localization = self.l)
            self.sm.add_widget(warranty_registration_1_screen)
        if not self.sm.has_screen('warranty_2'):
            warranty_registration_2_screen = screen_warranty_registration_2.WarrantyScreen2(name = 'warranty_2', warranty_manager = self, machine = self.m, localization = self.l)
            self.sm.add_widget(warranty_registration_2_screen)
        if not self.sm.has_screen('warranty_3'):
            warranty_registration_3_screen = screen_warranty_registration_3.WarrantyScreen3(name = 'warranty_3', warranty_manager = self, machine = self.m, localization = self.l)
            self.sm.add_widget(warranty_registration_3_screen)
        if not self.sm.has_screen('warranty_4'):
            warranty_registration_4_screen = screen_warranty_registration_4.WarrantyScreen4(name = 'warranty_4', warranty_manager = self, machine = self.m, localization = self.l)
            self.sm.add_widget(warranty_registration_4_screen)
        if not self.sm.has_screen('warranty_5'):
            warranty_registration_5_screen = screen_warranty_registration_5.WarrantyScreen5(name = 'warranty_5', warranty_manager = self, machine = self.m, localization = self.l)
            self.sm.add_widget(warranty_registration_5_screen)

        def first_screen():
            self.sm.current = 'warranty_1'

        Clock.schedule_once(lambda dt: first_screen(), 0.8)

    def exit_app(self):
        self.sm.current = 'safety'
        self.destroy_screen('language_select')
        self.destroy_screen('warranty_1')
        self.destroy_screen('warranty_2')
        self.destroy_screen('warranty_3')
        self.destroy_screen('warranty_4')
        self.destroy_screen('warranty_5')

    def destroy_screen(self, screen_name):
        if self.sm.has_screen(screen_name):
            self.sm.remove_widget(self.sm.get_screen(screen_name))
            print (screen_name + ' deleted')