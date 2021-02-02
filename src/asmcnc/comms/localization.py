import time
import os, csv
from datetime import datetime


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class Localization(object):

    dictionary = {}

    # use this for just getting user language, and if it's empty just assume english
    persistent_language_path = './sb_values/user_language.txt'
    complete_foreign_dictionary_path = './asmcnc/comms/foreign_dictionary.txt'
    fast_dictionary_path = './sb_values/fast_dictionary.csv'

    default_lang = 'English (GB)'
    lang = default_lang

    def __init__(self):

        if os.path.exists(self.persistent_language_path):
            self.read_in_language_name()

        if os.path.exists(self.fast_dictionary_path):
            # self.load_language() # only use this when not adding new keys!
            self.load_in_new_language(self.lang)

        else:
            self.load_in_new_language(self.lang)

    # Read in name of language, so it can be used as a key when accessing the complete language dictionary
    def read_in_language_name(self):
        try: 
            file = open(self.persistent_language_path, 'r')
            self.lang  = str(file.read())
            file.close()
            log("Read in language name")

        except: 
            log("Could not read in language name")

    # Save language name
    def save_language_name(self):
        try:
            file = open(self.persistent_language_path, 'w+')
            file.write(str(self.lang))
            file.close()
            log("Save language name to file")

        except:
            log("Could not save language name")


    def load_language(self):
        try: 
            # Read in from a file that only has English and corresponding chosen language (2 rows)
            csv_reader = csv.DictReader(open(self.fast_dictionary_path, "r"), delimiter=',')
            self.dictionary = (list(csv_reader))[0]
            log("Load from fast dictionary")
        except:
            log("Could not load from fast dictionary")

    def load_in_new_language(self, language):
        # When choosing a language, read in from full dictionary
        self.lang = language

        try:
            with open(self.complete_foreign_dictionary_path, "r") as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter='\t')
                for lines in csv_reader:
                    self.dictionary[str(lines[self.default_lang])] = str(lines[self.lang])
            log("Loaded language in from full dictionary")

        except:
            log("Could not load in from full dictionary")

        self.save_language_name()
        self.save_fast_dictionary()

        # still need to make language chosen persistent and save it

    def save_fast_dictionary(self):
        # Saves language choice into it's own file with the English langauge keys, for faster loading
        try: 
            with open(self.fast_dictionary_path,  'w') as csv_file:
                dict_writer = csv.DictWriter(csv_file, fieldnames=list(self.dictionary.keys()))
                dict_writer.writeheader()
                dict_writer.writerow(self.dictionary)
                log("Save fast dictionary")

        except:
            log("Could not save fast dictionary")

    # List of language headers
    supported_languages = ["English (GB)", "Deutsche (DE)", "Francais (FR)", "Italiano (IT)"]