# -*- coding: utf-8 -*-
import time
import os, csv
from datetime import datetime


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class Localization(object):

    dictionary = {}
    supported_languages = ["English (GB)", "Deutsche (DE)",  "Français (FR)", "Italiano (IT)", "Suomalainen (FI)", "Nederlands (NL)", "Polskie (PL)", "Dansk (DK)"]

    # use this for just getting user language, and if it's empty just assume english
    persistent_language_path = './sb_values/user_language.txt'
    complete_foreign_dictionary_path = './asmcnc/comms/foreign_dictionary.txt'

    default_lang = 'English (GB)'
    lang = default_lang

    def __init__(self):

        if os.path.exists(self.persistent_language_path):
            self.read_in_language_name()

        self.load_from_dictionary()

    # Getters/formatters
    def get_str(self, string):
        return str(self.dictionary.get(str(string), str(string)))

    def get_bold(self, string):
        return ('[b]' + str(self.dictionary.get(str(string), str(string))) + '[/b]')

    def get_italic(self, string):
        return ('[i]' + str(self.dictionary.get(str(string), str(string))) + '[/i]')


    ## DEBUGGING (forces KeyErrors)
    # def get_str(self, string):
    #     return str(self.dictionary[str(string)])

    # def get_bold(self, string):
    #     return ('[b]' + str(self.dictionary[str(string)]) + '[/b]')

    # def get_italic(self, string):
    #     return ('[i]' + str(self.dictionary[str(string)]) + '[/i]')

    # LANGUAGE NAME
    # Read in name of language, so it can be used as a key when accessing the complete language dictionary
    def read_in_language_name(self):
        try: 
            file = open(self.persistent_language_path, 'r')
            self.lang  = str(file.read())
            file.close()
            log("Read in language name: using " + self.lang)

        except: 
            self.lang = self.default_lang
            log("Could not read in language name, using English (GB) as default")

        if self.lang in self.supported_languages:
            log("Loading software in " + self.lang)

        else:
            log("Could not find " + self.lang + " in list of supported_languages, using English (GB) as default")
            self.lang = self.default_lang
            

    # Save language name
    def save_language_name(self):
        try:
            file = open(self.persistent_language_path, 'w+')
            file.write(str(self.lang))
            file.close()
            log("Save language name to file")

        except:
            log("Could not save language name, using English (GB) as default")


    ## DICTIONARY
    def load_from_dictionary(self):
        try:
            with open(self.complete_foreign_dictionary_path, "r") as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter='\t')
                for lines in csv_reader:
                    self.dictionary[str(lines[self.default_lang])] = str(lines[self.lang])
            log("Loaded language in from full dictionary")

        except:
            log("Could not load in from full dictionary")


    ## LOAD IN NEW LANGUAGE
    def load_in_new_language(self, language):
        # When choosing a language, read in from full dictionary
        self.lang = language
        self.load_from_dictionary()
        self.save_language_name()

    
    ## LOAD SUPPORTED LANGUAGES
    # def load_supported_languages(self):
    #     try: 
    #         with open(self.complete_foreign_dictionary_path, "r") as csv_file:
    #             self.supported_languages = (csv_file.readline()).strip().split('\t')
    #         log("supported_languages: ")
    #         print(self.supported_languages)

    #     except:
    #         log("Could not load list of supported_languages from dictionary")


    ## FAST DICTIONARY

        # fast_dictionary_path = './sb_values/fast_dictionary.csv'

        # if os.path.exists(self.fast_dictionary_path):
        #     # self.load_language() # only use this when not adding new keys!
        #     self.load_in_new_language(self.lang)

        # else:
        #     self.load_in_new_language(self.lang)

    # def load_language(self):
    #     try: 
    #         # Read in from a file that only has English and corresponding chosen language (2 rows)
    #         csv_reader = csv.DictReader(open(self.fast_dictionary_path, "r"), delimiter=',')
    #         self.dictionary = (list(csv_reader))[0]
    #         log("Load from fast dictionary")
    #     except:
    #         log("Could not load from fast dictionary")

    #     self.save_fast_dictionary()

    #     # still need to make language chosen persistent and save it

    # def save_fast_dictionary(self):
    #     # Saves language choice into it's own file with the English langauge keys, for faster loading
    #     try: 
    #         with open(self.fast_dictionary_path,  'w') as csv_file:
    #             dict_writer = csv.DictWriter(csv_file, fieldnames=list(self.dictionary.keys()))
    #             dict_writer.writeheader()
    #             dict_writer.writerow(self.dictionary)
    #             log("Save fast dictionary")

    #     except:
    #         log("Could not save fast dictionary")

    # List of language headers
