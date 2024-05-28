import csv
import os
import re
import threading
from datetime import datetime
from asmcnc.comms.logging_system.logging_system import Logger
from kivy.core.text import LabelBase
from kivy.lang import Builder
from asmcnc.comms.model_manager import ModelManagerSingleton

asmcnc_path = os.path.dirname(os.path.dirname(__file__))
fonts_path = os.path.join(asmcnc_path, "keyboard", "fonts")
kr_font_path = os.path.join(fonts_path, "KRFont.ttf")
kr_font_bold_path = os.path.join(fonts_path, "KRFont-Bold.ttf")
LabelBase.register(name="KRFont", fn_regular=kr_font_path, fn_bold=kr_font_bold_path)
LabelBase.register(name="KRFont-Bold", fn_regular=kr_font_bold_path)
builder_font_string = """
<Widget>:
    font_name: "%s"
    title_font: "%s\"
"""


class Localization(object):
    """Class for handling localization of the software. This class is a singleton.

    You can access the instance of this class by calling Localization()."""

    _lock = threading.Lock()
    _initialized = False
    _instance = None
    dictionary = {}
    gb = "English (GB)"
    it = "Italiano (IT)"
    fi = "Suomalainen (FI)"
    de = "Deutsch (DE)"
    fr = "Français (FR)"
    pl = "Polski (PL)"
    dk = "Dansk (DK)"
    ko = "Korean (KO)"
    nl = "Nederlands (NL)"
    approved_languages = [gb, it, fi, de, fr, pl, dk, ko]
    supported_languages = approved_languages + [nl]
    persistent_language_path = "./sb_values/user_language.txt"
    complete_foreign_dictionary_path = os.path.join(
        asmcnc_path, "comms", "foreign_dictionary.txt"
    )
    default_lang = "English (GB)"
    lang = default_lang
    standard_font = "Roboto"
    standard_font_bold = "Roboto-Bold"
    korean_font = "KRFont"
    korean_font_bold = "KRFont-Bold"
    kivy_markup_regex = re.compile("\\[.*?\\]")
    ORIGINAL_PRODUCT_NAME = "SmartBench"
    PRODUCT_NAME = "SmartBench"

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                Logger.info("Creating new instance of Localization")
                cls._instance = super(Localization, cls).__new__(cls)
            return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            if os.path.exists(self.persistent_language_path):
                self.read_in_language_name()
            self.load_from_dictionary()
            self.model_manager = ModelManagerSingleton()
            if self.model_manager.is_machine_drywall():
                self.PRODUCT_NAME = "SmartCNC"

    def get_str(self, string):
        return self.__get(string)

    def get_bold(self, string):
        return "[b]{0}[/b]".format(self.__get(string))

    def get_italic(self, string):
        return "[i]{0}[/i]".format(self.__get(string))

    def __get(self, string):
        string = self.dictionary.get(str(string), str(string))
        if (
            self.ORIGINAL_PRODUCT_NAME in string
            and self.ORIGINAL_PRODUCT_NAME != self.PRODUCT_NAME
        ):
            string = string.replace(self.ORIGINAL_PRODUCT_NAME, self.PRODUCT_NAME)
        if (
            "PrecisionPro +" in string
            and self.ORIGINAL_PRODUCT_NAME != self.PRODUCT_NAME
        ):
            string = string.replace("PrecisionPro +", self.PRODUCT_NAME)
        return string

    def get_localized_days(self, string):
        if "days" in string:
            return string.replace("days", self.get_str("days"))
        elif "day" in string:
            return string.replace("day", self.get_str("day"))
        return string

    def get_text_length(self, string):
        if self.lang == self.ko:
            string = string.decode("utf-8")
        return len(re.sub(self.kivy_markup_regex, "", string))

    def read_in_language_name(self):
        try:
            file = open(self.persistent_language_path, "r")
            self.lang = str(file.read())
            file.close()
            Logger.info("Read in language name: using " + self.lang)
        except:
            self.lang = self.default_lang
            Logger.warning(
                "Could not read in language name, using English (GB) as default"
            )
        if self.lang in self.supported_languages:
            Logger.info("Loading software in " + self.lang)
        else:
            Logger.warning(
                "Could not find "
                + self.lang
                + " in list of supported_languages, using English (GB) as default"
            )
            self.lang = self.default_lang

    def save_language_name(self):
        try:
            file = open(self.persistent_language_path, "w+")
            file.write(str(self.lang))
            file.close()
            Logger.info("Save language name to file")
        except:
            Logger.error("Could not save language name, using English (GB) as default")

    def load_from_dictionary(self):
        try:
            with open(self.complete_foreign_dictionary_path, "r") as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter="\t")
                for lines in csv_reader:
                    self.dictionary[str(lines[self.default_lang])] = str(
                        lines[self.lang]
                    )
            Logger.info("Loaded language in from full dictionary")
            if self.lang == self.ko:
                self.font_regular = self.korean_font
                self.font_bold = self.korean_font_bold
                Builder.load_string(
                    builder_font_string % (self.font_regular, self.font_bold)
                )
            else:
                self.font_regular = self.standard_font
                self.font_bold = self.standard_font_bold
        except:
            Logger.warning("Could not load in from full dictionary")

    def load_in_new_language(self, language):
        self.lang = language
        self.load_from_dictionary()
        self.save_language_name()
