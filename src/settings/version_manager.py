'''
Created 30 November 2020
@author: Letty
Version manager (replaces what was settings manager)
'''

import sys,os, subprocess
from __builtin__ import True, False
from datetime import datetime

from kivy.clock import Clock

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class VersionManager(object):
    
    sw_version = ''
    sw_hash = ''
    sw_branch = ''
    latest_sw_version = ''
    latest_sw_beta = ''
    pl_version = ''
    pl_hash = ''
    pl_branch = ''
    latest_pl_version = ''
    fw_version = ''
    latest_fw_version = ''
    grbl_mega_dir = '/home/pi/grbl-Mega/'
    repository = ''

    latest_pl_version_dir = "/home/pi/smartbench-version-manager/platform-version.txt"
    latest_sw_version_dir = "/home/pi/smartbench-version-manager/software-version.txt"

    def __init__(self, screen_manager):

    	self.sm = screen_manager

    	# first time this runs there won't be a version manager repo bc the pl won't be updated yet -_-
    	# maybs just put in a try-except, and then it won't even touch the excep most of the time. 

    	self.check_version_manager()

    def check_version_manager(self):

    	try: 
    		# go into version manager directory
    		os.system("cd /home/pi/smartbench-version-manager/ && git fetch " + repository + " --tags --quiet")

    		try:

    			# check out the latest tag
	            version_manager_version_list = (str(os.popen("git tag --sort=-refname |head -n 10").read()).split('\n'))
	            latest_version_manager_version = str([tag for tag in version_manager_version_list if "beta" not in tag][0])
				os.system('cd /home/pi/smartbench-version-manager/ && git checkout ' + latest_version_manager_version)

				if os.path.exists(latest_pl_version_dir):
					pl_version_file = open(latest_pl_version_dir, 'r')
					self.latest_pl_version = pl_version_file.read()
					pl_version_file.close()
				else: 
					print "problem"

				if os.path.exists(latest_sw_version_dir):
					sw_version_file = open(latest_sw_version_dir, 'r')
					self.latest_sw_version = sw_version_file.read()
					sw_version_file.close()

				else:
					print "problem"

	        except: 
	            print "Could not fetch version manager version tags"
    			
    	except: 
    		# clone the repo
    		try:
	    		os.system("cd /home/pi/ && git clone https://github.com/YetiTool/smartbench-version-manager.git")
	    		self.check_version_manager()
	    	except: 
	    		print "problem"


    def update_config(self):
        os.system('sudo sed -i "s/check_config=False/check_config=True/" /home/pi/easycut-smartbench/src/config.txt')
        sed_sw_version = (''.join(['sudo sed -i "s/version=', str(self.sw_version) + '/version=', 
                                str(self.latest_sw_version), '/" /home/pi/easycut-smartbench/src/config.txt'])).strip('\n')
        os.system(sed_sw_version)
        os.system('sudo sed -i "s/power_cycle_alert=False/power_cycle_alert=True/" /home/pi/easycut-smartbench/src/config.txt')

    def refresh_sw_version(self):
        self.sw_version = str(os.popen("git describe --tags").read()).strip('\n')
        self.sw_hash = str(os.popen("git rev-parse --short HEAD").read()).strip('\n')
        self.sw_branch = str(os.popen("git branch | grep \*").read()).strip('\n')

    def refresh_platform_version(self):
        self.pl_version = str(os.popen("cd /home/pi/console-raspi3b-plus-platform/ && git describe --tags").read()).strip('\n')
        self.pl_hash = str(os.popen("cd /home/pi/console-raspi3b-plus-platform/ && git rev-parse --short HEAD").read()).strip('\n')
        self.pl_branch = str(os.popen("cd /home/pi/console-raspi3b-plus-platform/ && git branch | grep \*").read()).strip('\n')

    def do_updates(self):

    	# get current versions and hold onto them    	
    	self.refresh_sw_version()
    	self.refresh_platform_version()
    	backup_pl_version = self.pl_version
    	backup_sw_version = self.sw_version
    	
    	# get tags
    	self.check_version_manager()

    	# fetch repositories
    	platform_tag_list, software_tag_list = self.fetch_tags_from_repositories()

    	# check tags are in list
    	if self.latest_pl_version in platform_tag_list and self.latest_sw_version in software_tag_list:
    		continue

    	else: 
    		# if tags not in list get latest tags
    		self.latest_sw_version = str([tag for tag in software_tag_list if "beta" not in tag][0])
    		self.latest_pl_version = str([tag for tag in platform_tag_list if "beta" not in tag][0])

    	# do compatibility check with tags
    	self.compatible, self.latest_pl_version, self.latest_sw_version = self.compatibility_check(self.latest_pl_version, self.latest_sw_version)

    	# checkout tags
    	self.checkout_tags(self.latest_pl_version, self.latest_sw_version)

    	# check success
    	self.check_update_success(backup_pl_version, backup_sw_version)

    	# run platform install & reboot:
    	self.platform_install()

    def fetch_tags_from_repositories(self):

    	if repository != '':
	    	platform_tag_list = os.system("cd /home/pi/console-raspi3b-plus-platform/ && git fetch " + repository + " --tags --quiet")
	    	software_tag_list = os.system("cd /home/pi/easycut-smartbench/ && git fetch " + repository + " --tags --quiet")

    	platform_tag_list = os.system("cd /home/pi/console-raspi3b-plus-platform/ && git fetch --tags --quiet")
    	software_tag_list = os.system("cd /home/pi/easycut-smartbench/ && git fetch --tags --quiet")

    	return platform_tag_list, software_tag_list

    def compatibility_check(self, platform_tag, software_tag):
    	data_by_platform, data_by_software = read_and_split_file()
    	platform_list = str(data_by_software[0]).('\n')
		software_list = str(data_by_platform[0]).('\t')

		platform_index = platform_list.index(platform_tag)
		software_index = software_list.index(software_tag)

		if str(str(data_by_platform[platform_index]).split('\t')[software_index]) == '1':
			return True, platform_tag, software_tag

		else: 
			for i in range(platform_index):
				if str(str(data_by_platform[platform_index-i]).split('\t')[software_index]) == '1':
					return True, platform_list[platform_index-i], software_tag

			return False, self.pl_version, self.sw_version

	def read_and_split_file(self):
	    text_data = list()
	    current_file = os.path.abspath(self.version_matrix_filepath)
	    if os.path.exists(current_file):
	        open_file = open(current_file, 'r')
	        text_data_by_platform = open_file.read().split('\n') # split by each new line (platform rows)
	        text_data_by_software = open_file.read().split('\t') # split by each new tab
	   		open_file.close()
	    return text_data_by_platform, text_data_by_software

    def checkout_tags(self, software_tag, platform_tag):
    	# do platform tag first
    	os.system('cd /home/pi/console-raspi3b-plus-platform/ && git checkout ' + platform_tag)
    	os.system('cd /home/pi/easycut-smartbench/ && git checkout ' + software_tag)

    def check_update_success(self, backup_pl_version, backup_sw_version):
    	
    	self.refresh_sw_version()
    	self.refresh_platform_version()

		# if not successful, revert to previous tags
    	if (self.pl_version == backup_pl_version) and (self.sw_version == backup_sw_version):
    		return True # success

    	else:
    		self.compatible, backup_pl_version, backup_sw_version = self.compatibility_check(backup_pl_version, backup_sw_version)
    		self.checkout_tags(backup_pl_version, backup_sw_version)
    		return False

    def platform_install(self):
    	os.system("/home/pi/console-raspi3b-plus-platform/ansible/templates/ansible-start.sh && sudo reboot")

    ## BETA AND DEVELOPER UPDATE FUNCTIONS


    ## FW UPDATE FUNCTIONS
	# if platform version enough: import pigpio