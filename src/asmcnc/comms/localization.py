import time

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class Localization(object):

	dictionary = {}

	# use this for just getting user language, and if it's empty just assume english
	persistent_language_path = '/home/pi/easycut-smartbench/src/sb_values/user_language.txt'

	lang = 'English'

	# want to test:
	# how fast is loading in from multi-language file vs two-language file (for start-up purposes)

	def __init__(self, screen_manager):
		pass

	def load_language(self):
		pass

	def load_in_new_language(self, lanugage):
		self.lang = language
		pass

	supported_languages = ['English', 'Korean', 'German', 'French', 'Italian']