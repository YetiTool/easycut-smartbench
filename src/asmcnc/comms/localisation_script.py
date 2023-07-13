import csv, sys, os
from datetime import datetime

if sys.version_info < (3, 1):
    print("This script requires Python version 3.1 or higher")
    exit(0)

"""
This script requires Python 3.1 or higher. Edit the variables below to change the settings on the script. 
Download the .tsv file from the Localisation Master spreadsheet and update the path variables below.
Once all the variables are updated correctly, simply run the script. It will generate a log file (in a logs folder) to 
help keep track of any new phrases added.
"""

# List of languages to add to the new dictionary file
supported_languages = ["English (GB)", "Deutsch (DE)", "Français (FR)", "Italiano (IT)", "Suomalainen (FI)",
                       "Nederlands (NL)", "Polski (PL)", "Dansk (DK)", "Korean (KO)"]

# Specify which phrases you wish to add to the new dictionary. These phrases should be in the localisation master,
# but not in the foreign_dictionary.txt file. If list is empty and `new_strings` is True, it will add all phrases from
# the localisation master file.
phrases_to_add = []

# When True it will keep the same order of the foreign_dictionary.txt and add any extra phrases from the localisation
# master at the end.
# When False it will keep the same order as the foreign_dictionary.txt and not add any new phrases
new_strings = True

# File paths of the current foreign dictionary and the localisation master
foreign_dictionary = "foreign_dictionary.txt"
localisation_master = "Localisation Master - Human edits.tsv"

# File path of the new dictionary file to write
new_file = "new.txt"

default_lang = 'English (GB)'

with open(foreign_dictionary, "r", encoding="utf8") as foreign_dict:
    foreign_dict_reader = csv.DictReader(foreign_dict, delimiter='\t')

    # If you iterate through foreign_dict_reader directly, it deletes instances that have been iterated through.
    # Converting to a list prevents this.
    foreign_lst = list(foreign_dict_reader)

    with open(localisation_master, "r", encoding="utf8") as localisation_master:
        localisation_master_reader = csv.DictReader(localisation_master, delimiter='\t')

        localisation_lst = list(localisation_master_reader)

        with open(new_file, "w", encoding="utf8", newline='') as f:
            writer = csv.writer(f, delimiter='\t')

            writer.writerow(supported_languages)
            count = 0
            failed_phrases = []
            for foreign_line in foreign_lst:
                row = []
                for localisation_line in localisation_lst:
                    if foreign_line[default_lang].strip() == localisation_line[default_lang].strip():
                        for language in supported_languages:
                            row.append(localisation_line[language].strip())
                        # writer.writerow doesn't deal well with quotes so writing directly to the file is easiest
                        # writer.writerow(row)
                        f.write('\t'.join(row) + '\n')
                        localisation_lst.remove(localisation_line)
                        break
                else:
                    failed_phrases.append(foreign_line[default_lang])

            # Log generation

            # Get only the english phrases in the dictionary
            english_lst = [x[default_lang] for x in foreign_lst]

            try:
                os.mkdir("logs")
            except:
                pass

            with open("logs\\log " + datetime.now().strftime("%d-%m-%Y %H-%M-%S") + ".txt", "w",
                      encoding="utf8") as log:
                log.write("Languages: \n")
                log.write("\t- " + " ".join(supported_languages) + "\n")

                if new_strings:
                    log.write("\nNewly added phrases: \n")
                    for localisation_line in localisation_lst:
                        row = []

                        condition = localisation_line[default_lang] in phrases_to_add or len(phrases_to_add) == 0

                        if localisation_line[default_lang] not in english_lst and condition:
                            for language in supported_languages:
                                row.append(localisation_line[language].strip())
                            writer.writerow(row)
                            log.write("\t- " + localisation_line[default_lang] + "\n")
                else:
                    log.write("\nNo newly added phrases.\n")

                if len(failed_phrases) > 0:
                    log.write("\nFailed to add following phrases (phrases in foreign dictionary but not in "
                              "localisation master - possible duplicate) \n")
                    for phrase in failed_phrases:
                        log.write("\t- " + phrase + "\n")
                else:
                    log.write("\nNo failed phrases")