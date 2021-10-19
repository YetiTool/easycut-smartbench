from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.skavaUI import popup_info

from asmcnc.apps.start_up_sequence.warranty_app.screens import \
screen_warranty_registration_1, \
screen_warranty_registration_2, \
screen_warranty_registration_3, \
screen_warranty_registration_4, \
screen_warranty_registration_5, \
screen_CNC_academy


class ScreenManagerWarranty(object):



    def __init__(self, start_sequence, screen_manager, machine, localization):

        self.start_seq = start_sequence
        self.sm = screen_manager
        self.m = machine
        self.l = localization

        self.load_warranty_app()

    def load_warranty_app(self):

        if not self.sm.has_screen('warranty_1'):
            warranty_registration_1_screen = screen_warranty_registration_1.WarrantyScreen1(name = 'warranty_1', start_sequence = self.start_seq, machine = self.m, localization = self.l)
            self.sm.add_widget(warranty_registration_1_screen)
        else:
            self.sm.get_screen('warranty_1').update_strings()

        if not self.sm.has_screen('warranty_2'):
            warranty_registration_2_screen = screen_warranty_registration_2.WarrantyScreen2(name = 'warranty_2', start_sequence = self.start_seq, machine = self.m, localization = self.l)
            self.sm.add_widget(warranty_registration_2_screen)
        else:
            self.sm.get_screen('warranty_2').update_strings()

        if not self.sm.has_screen('warranty_3'):
            warranty_registration_3_screen = screen_warranty_registration_3.WarrantyScreen3(name = 'warranty_3', start_sequence = self.start_seq, machine = self.m, localization = self.l)
            self.sm.add_widget(warranty_registration_3_screen)
        else:
            self.sm.get_screen('warranty_3').update_strings()

        if not self.sm.has_screen('warranty_4'):
            warranty_registration_4_screen = screen_warranty_registration_4.WarrantyScreen4(name = 'warranty_4', start_sequence = self.start_seq, machine = self.m, localization = self.l)
            self.sm.add_widget(warranty_registration_4_screen)
        else:
            self.sm.get_screen('warranty_4').update_strings()

        if not self.sm.has_screen('warranty_5'):
            warranty_registration_5_screen = screen_warranty_registration_5.WarrantyScreen5(name = 'warranty_5', start_sequence = self.start_seq, machine = self.m, localization = self.l)
            self.sm.add_widget(warranty_registration_5_screen)
        else:
            self.sm.get_screen('warranty_5').update_strings()

        self.start_seq.add_screen_to_sequence('warranty_1')
        self.start_seq.add_screen_to_sequence('warranty_2')
        self.start_seq.add_screen_to_sequence('warranty_3')
        self.start_seq.add_screen_to_sequence('warranty_4')
        self.start_seq.add_screen_to_sequence('warranty_5')

        if not self.start_seq.screen_sequence.index('warranty_1'):
            self.sm.get_screen('warranty_1').prev_screen_button.opacity = 0


    def open_warranty_app(self):
        self.load_warranty_app()
        self.sm.current = 'warranty_1' 

    def destroy_screen(self, screen_name):

        if self.sm.has_screen(screen_name):
            self.sm.remove_widget(self.sm.get_screen(screen_name))
            print (screen_name + ' deleted')