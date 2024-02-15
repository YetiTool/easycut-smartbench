from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.skavaUI import popup_info

from asmcnc.apps.start_up_sequence.warranty_app.screens import \
    screen_warranty_registration_1, \
    screen_warranty_registration_2, \
    screen_warranty_registration_3, \
    screen_warranty_registration_4, \
    screen_warranty_registration_5


class ScreenManagerWarranty(object):

    def __init__(self, start_sequence, screen_manager, machine, localization, keyboard):

        self.start_seq = start_sequence
        self.sm = screen_manager
        self.m = machine
        self.l = localization
        self.kb = keyboard

        self.load_warranty_app()

    warranty_screens = {
        "warranty_1": screen_warranty_registration_1.WarrantyScreen1,
        "warranty_2": screen_warranty_registration_2.WarrantyScreen2,
        "warranty_3": screen_warranty_registration_3.WarrantyScreen3,
        "warranty_4": screen_warranty_registration_4.WarrantyScreen4,
        "warranty_5": screen_warranty_registration_5.WarrantyScreen5
    }

    def load_warranty_app(self):
        for name, cls in self.warranty_screens.items():
            if not self.sm.has_screen(name):
                screen = cls(name=name, start_sequence=self.start_seq, machine=self.m, localization=self.l,
                             keyboard=self.kb)
                self.sm.add_widget(screen)
            else:
                self.sm.get_screen(name).update_strings()

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
