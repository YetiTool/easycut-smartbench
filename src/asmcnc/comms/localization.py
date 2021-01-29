import time
import csv

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class Localization(object):

	dictionary = {}

	# use this for just getting user language, and if it's empty just assume english
	persistent_language_path = '/home/pi/easycut-smartbench/src/sb_values/user_language.txt'
	complete_foreign_dictionary_path = '/home/pi/easycut-smartbench/src/asmcnc/comms/foreign_dictionary.csv'

	default_lang = 'English (GB)'
	lang = default_lang

	# want to test:
	# how fast is loading in from multi-language file vs two-language file (for start-up purposes)

	def __init__(self):
		pass

	def load_language(self):
		pass

	def load_in_new_language(self, language):
		self.lang = language

		with open(self.complete_foreign_dictionary_path, "r") as csv_file:
		    csv_reader = csv.DictReader(csv_file, delimiter=',')
		    for lines in csv_reader:
		    	self.dictionary[str(lines[self.default_lang])] = str(lines[self.lang])

	def save_active_dictionary(self):
		with open(self.complete_foreign_dictionary_path,  'w', newline='') as csv_file:
		    csv_reader = csv.DictReader(csv_file, delimiter=',')

		    lang_writer = csv.writer(csvfile, delimiter=',')
		    

	supported_languages = ['English (GB)', 'Korean (KOR)', 'German (DE)', 'French (FR)', 'Italian (IT)']