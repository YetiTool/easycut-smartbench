# coding=utf-8
import os
from functools import partial

from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from asmcnc.comms.localization import Localization
from asmcnc.comms.model_manager import ModelManagerSingleton
from asmcnc.core_UI import path_utils
from asmcnc.core_UI.utils import color_provider

ASMCNC_PATH = path_utils.asmcnc_path
SKAVA_UI_IMG_PATH = os.path.join(ASMCNC_PATH, "skavaUI", "img")
FLAGS_PATH = os.path.join(SKAVA_UI_IMG_PATH, "flags")

WELCOME_STRINGS = [
    "Welcome to SmartBench",
    "Willkommen bei SmartBench",
    "Benvenuto in Smartbench",
    "Benvenuti in Smartbench",
    "Tervetuloa Smartbenchiin",
    "Witamy w SmartBench",
    "Velkommen til SmartBench",
    "SmartBench\xec\x97\x90 \xec\x98\xa4\xec\x8b\xa0 \xea\xb2\x83\xec\x9d\x84 \xed\x99\x98\xec\x98\x81\xed\x95\xa9\xeb\x8b\x88\xeb\x8b\xa4",
]


def get_language_flag_path(language):
    flag_name = language.split("(")[1][:-1].lower()
    return os.path.join(FLAGS_PATH, flag_name + ".png")


class LanguageSelectionScreen(Screen):

    __model_manager = ModelManagerSingleton()
    __localisation = Localization()

    __language_chosen = ""

    def __init__(self, screen_manager, start_seq, **kwargs):
        super(LanguageSelectionScreen, self).__init__(**kwargs)

        self.screen_manager = screen_manager
        self.start_seq = start_seq

        self.root_layout = BoxLayout(orientation='vertical')

        self.header = BoxLayout(size_hint=(1, 0.1))
        self.header.bind(size=self.__update_header, pos=self.__update_header)

        self.welcome_label = Label(text=self.__localisation.get_str(WELCOME_STRINGS[0]),
                                   font_size="30sp", color=color_provider.get_rgba("white"))
        self.header.add_widget(self.welcome_label)

        self.body = BoxLayout(size_hint=(1, 0.55))
        self.body.bind(size=self.__update_body, pos=self.__update_body)

        self.language_flags_container = GridLayout(cols=3, size_hint=(0.8, 0.8), pos_hint={"center_x": 0.5,
                                                                                           "center_y": 0.5})

        for language in self.__localisation.approved_languages:
            localisation_choice_option = self.__get_language_option_widget(language)

            if self.__model_manager.is_machine_drywall() and language != self.__localisation.gb:
                localisation_choice_option.opacity = 0

            self.language_flags_container.add_widget(localisation_choice_option)

        self.body.add_widget(self.language_flags_container)

        self.footer = BoxLayout(size_hint=(1, 0.35))
        self.footer.bind(size=self.__update_footer, pos=self.__update_footer)

        next_string = self.__localisation.get_str("Next") + "..."
        spacer = Label(text="", size_hint=(0.3, 0.8))
        self.next_button = Button(text=next_string, size_hint=(None, None), width=dp(291), height=dp(79),
                                  pos_hint={"center_x": 0.5, "center_y": 0.5},
                                  disabled=True, font_size="30sp", opacity=0,
                                  background_down=os.path.join(SKAVA_UI_IMG_PATH, "next.png"),
                                  background_normal=os.path.join(SKAVA_UI_IMG_PATH, "next.png"),
                                  on_press=self.__next_button_pressed)
        spacer2 = Label(text="", size_hint=(0.3, 0.8))

        self.footer.add_widget(spacer)
        self.footer.add_widget(self.next_button)
        self.footer.add_widget(spacer2)

        self.root_layout.add_widget(self.header)
        self.root_layout.add_widget(self.body)
        self.root_layout.add_widget(self.footer)
        self.add_widget(self.root_layout)

    def __next_button_pressed(self, *args):
        self.__localisation.load_in_new_language(self.__language_chosen)

        font_changed = self.welcome_label.font_name != self.__localisation.font_regular
        for screen_name in self.start_seq.screen_sequence + ["rebooting"]:
            screen = self.screen_manager.get_screen(screen_name)

            if hasattr(screen, "update_strings"):
                screen.update_strings()

            if font_changed:
                for widget in screen.walk():
                    if isinstance(widget, Label):
                        widget.font_name = self.__localisation.font_regular

        self.start_seq.next_in_sequence()

    def __get_language_option_widget(self, language):
        root_layout = GridLayout(cols=3, rows=1, spacing=dp(10), padding=[dp(20), 0, 0, 0])
        check_box = CheckBox(color=color_provider.get_rgba("dark_grey"), size_hint=(None, None), width=dp(30),
                             group="language_selection", on_press=partial(self.__on_language_selected, language))
        flag_path = get_language_flag_path(language)
        flag_image = Image(source=flag_path, allow_stretch=True, size_hint=(None, None),
                           width=dp(50))
        language_label = Label(text=language, color=color_provider.get_rgba("black"), valign="middle", halign="left")

        if flag_path.endswith("ko.png"):
            language_label.font_name = self.__localisation.korean_font

        language_label.bind(size=language_label.setter('text_size'))
        root_layout.add_widget(check_box)
        root_layout.add_widget(flag_image)
        root_layout.add_widget(language_label)
        return root_layout

    def __on_language_selected(self, language, instance):
        if instance.parent.opacity == 0 or not instance.active:
            self.__language_chosen = ""
            self.next_button.disabled = True
            self.next_button.opacity = 0
            return

        instance.color = color_provider.get_rgba("blue")
        self.__language_chosen = language
        self.next_button.disabled = False
        self.next_button.opacity = 1

    def __update_body(self, *args):
        self.body.canvas.before.clear()
        with self.body.canvas.before:
            Color(*color_provider.get_rgba("grey"))
            Rectangle(size=self.body.size, pos=self.body.pos)

    def __update_header(self, *args):
        self.header.canvas.before.clear()
        with self.header.canvas.before:
            Color(*color_provider.get_rgba("blue"))
            Rectangle(size=self.header.size, pos=self.header.pos)

    def __update_footer(self, *args):
        self.footer.canvas.before.clear()
        with self.footer.canvas.before:
            Color(*color_provider.get_rgba("grey"))
            Rectangle(size=self.footer.size, pos=self.footer.pos)
