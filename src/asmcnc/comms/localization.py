import time
import os, csv
from datetime import datetime


def log(message):
    timestamp = datetime.now()
    print(timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message))


class Localization(object):
    dictionary = {}
    approved_languages = ['English (GB)', 'Italiano (IT)',
        'Suomalainen (FI)', 'Deutsch (DE)', 'Fran\xc3\xa7ais (FR)',
        'Polski (PL)', 'Dansk (DK)']
    supported_languages = ['English (GB)', 'Deutsch (DE)',
        'Fran\xc3\xa7ais (FR)', 'Italiano (IT)', 'Suomalainen (FI)',
        'Nederlands (NL)', 'Polski (PL)', 'Dansk (DK)']
    persistent_language_path = './sb_values/user_language.txt'
    complete_foreign_dictionary_path = './asmcnc/comms/foreign_dictionary.txt'
    default_lang = 'English (GB)'
    lang = default_lang

    def __init__(self):
        if os.path.exists(self.persistent_language_path):
            self.read_in_language_name()
        self.load_from_dictionary()

    def get_str(self, string):
        return str(self.dictionary.get(str(string), str(string)))

    def get_bold(self, string):
        return '[b]' + str(self.dictionary.get(str(string), str(string))
            ) + '[/b]'

    def get_italic(self, string):
        return '[i]' + str(self.dictionary.get(str(string), str(string))
            ) + '[/i]'

    def get_localized_days(self, string):
        if 'days' in string:
            return string.replace('days', self.get_str('days'))
        elif 'day' in string:
            return string.replace('day', self.get_str('day'))
        else:
            return string

    def read_in_language_name(self):
        try:
            file = open(self.persistent_language_path, 'r')
            self.lang = str(file.read())
            file.close()
            log('Read in language name: using ' + self.lang)
        except:
            self.lang = self.default_lang
            log('Could not read in language name, using English (GB) as default'
                )
        if self.lang in self.supported_languages:
            log('Loading software in ' + self.lang)
        else:
            log('Could not find ' + self.lang +
                ' in list of supported_languages, using English (GB) as default'
                )
            self.lang = self.default_lang

    def save_language_name(self):
        try:
            file = open(self.persistent_language_path, 'w+')
            file.write(str(self.lang))
            file.close()
            log('Save language name to file')
        except:
            log('Could not save language name, using English (GB) as default')

    def load_from_dictionary(self):
        try:
            with open(self.complete_foreign_dictionary_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter='\t')
                for lines in csv_reader:
                    self.dictionary[str(lines[self.default_lang])] = str(lines
                        [self.lang])
            log('Loaded language in from full dictionary')
        except:
            log('Could not load in from full dictionary')

    def load_in_new_language(self, language):
        self.lang = language
        self.load_from_dictionary()
        self.save_language_name()
