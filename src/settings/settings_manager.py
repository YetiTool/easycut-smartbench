'''
Created 5 March 2020
@author: Letty
Module to get and store settings info
'''

import sys,os, subprocess #, pigpio ## until production machines are running latest img
from __builtin__ import True, False
from datetime import datetime

from kivy.clock import Clock

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class Settings(object):
    
    sw_version = ''
    sw_hash = ''
    sw_branch = ''
    latest_sw_version = ''
    platform_version = ''
    pl_hash = ''
    pl_branch = ''
    latest_platform_version = ''
    fw_version = ''
    latest_fw_version = ''
    grbl_mega_dir = '/home/pi/grbl-Mega/' 

    def __init__(self, screen_manager):
        
        self.sm = screen_manager
    

## REFRESH EVERYTHING AT START UP    
    # def refresh_all(self):
        self.refresh_latest_platform_version()
        self.refresh_platform_version()
        self.refresh_latest_sw_version()
        self.refresh_sw_version()

## VERSION REFRESH
        
    def refresh_sw_version(self):
        self.sw_version = str(os.popen("git describe --tags").read()).strip('\n')
        self.sw_hash = str(os.popen("git rev-parse --short HEAD").read()).strip('\n')
        self.sw_branch = str(os.popen("git branch | grep \*").read()).strip('\n')

    def refresh_latest_sw_version(self):

        try: 
            os.system("cd /home/pi/easycut-smartbench/ && git fetch --tags --quiet")
            sw_version_list = (str(os.popen("git tag --sort=-refname |head -n 2").read()).split('\n'))

            if str(sw_version_list[1]) + '-beta' == str(sw_version_list[0]):
                self.latest_sw_version = str(sw_version_list[1])
            else: self.latest_sw_version = str(sw_version_list[0])
        except: 
            print "Could not fetch software version tags"


    def refresh_platform_version(self):
        self.platform_version = str(os.popen("cd /home/pi/console-raspi3b-plus-platform/ && git describe --tags").read()).strip('\n')
        self.pl_hash = str(os.popen("cd /home/pi/console-raspi3b-plus-platform/ && git rev-parse --short HEAD").read()).strip('\n')
        self.pl_branch = str(os.popen("cd /home/pi/console-raspi3b-plus-platform/ && git branch | grep \*").read()).strip('\n')

    def refresh_latest_platform_version(self):
        if self.sm.current == 'dev':
            os.system("cd /home/pi/console-raspi3b-plus-platform/ && git fetch --tags --quiet")
        self.latest_platform_version = str(os.popen("cd /home/pi/console-raspi3b-plus-platform/ && git describe --tags `git rev-list --tags --max-count=1`").read()).strip('\n')

            
## GET SOFTWARE UPDATES

    def get_sw_update_via_wifi(self):
        if sys.platform != 'win32' and sys.platform != 'darwin':       
            os.system("cd /home/pi/easycut-smartbench/ && git fetch origin")
        checkout_success = self.checkout_latest_version()
        return checkout_success
    
    def checkout_latest_version(self):    
        if sys.platform != 'win32' and sys.platform != 'darwin':
            if self.latest_sw_version != self.sw_version:
                os.system("cd /home/pi/easycut-smartbench/")

                cmd  = ["git", "checkout", self.latest_sw_version]
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                unformatted_git_output = p.communicate()[1]

                git_output = str(unformatted_git_output).split('\n')
                git_output = list(filter(lambda x: x!= '', git_output))
                     
                if str(git_output[-1]).startswith('HEAD is now at'):
                    self.update_config()
                    description = str(git_output[-1])
                    return description
                
                elif str(git_output[-1]).endswith('Could not resolve host: github.com'):
                    return "Could not resolve host: github.com"

                else:
                    return False

            else: return "Software already up to date!"

    def update_config(self):
        os.system('sudo sed -i "s/check_config=False/check_config=True/" /home/pi/easycut-smartbench/src/config.txt')
        sed_sw_version = (''.join(['sudo sed -i "s/version=', str(self.sw_version) + '/version=', 
                                str(self.latest_sw_version), '/" /home/pi/easycut-smartbench/src/config.txt'])).strip('\n')
        os.system(sed_sw_version)
        os.system('sudo sed -i "s/power_cycle_alert=False/power_cycle_alert=True/" /home/pi/easycut-smartbench/src/config.txt')

    def reclone_EC(self):
    
        def backup_EC():
            # check if backup directory exists, and delete it if it does
            os.system('[ -d "/home/pi/easycut-smartbench-backup/" ] && sudo rm /home/pi/easycut-smartbench-backup -r')
            # copy EC into a backup directory
            os.system('mkdir /home/pi/easycut-smartbench-backup && cp -RT /home/pi/easycut-smartbench /home/pi/easycut-smartbench-backup')
    
            # Update starteasycut shell script to look for backup/other folders if required
            # We really need to work on platform updates
            case = (os.popen('grep "\[ ! -d" /home/pi/starteasycut.sh').read()) #current/old directory command
            if not case.startswith('[ ! -d'):
                backup_command = '\[ ! -d \"/home/pi/easycut-smartbench/\" \] && mkdir \/home\/pi\/easycut-smartbench && cp -RT \/home\/pi\/easycut-smartbench-backup \/home\/pi\/easycut-smartbench'
                sed_cmd = ('sudo sed -i \'/echo \\"start easycut\\"/ a ' + backup_command + '\' /home/pi/starteasycut.sh') 
                os.system(sed_cmd)
            
            # compare backup and current directory just in case, and return true if all is well    
            directory_diff = (os.popen('diff -qr /home/pi/easycut-smartbench/ /home/pi/easycut-smartbench-backup/').read())
            if directory_diff == '': return True
            else: 
                os.system('[ -d "/home/pi/easycut-smartbench-backup/" ] && sudo rm /home/pi/easycut-smartbench-backup -r')                
                return False
              
        def clone_new_EC_and_restart():

            # Repair a git repo
            os.system('cd /home/pi/ && sudo rm /home/pi/easycut-smartbench -r && git clone https://github.com/YetiTool/easycut-smartbench.git' + 
            '&& cd /home/pi/easycut-smartbench/ && git checkout ' + self.latest_sw_version + ' && ../starteasycut.sh')
        
        if backup_EC() == True:
            clone_new_EC_and_restart()

        else: return False


## USB SOFTWARE UPDATE            
    def get_sw_update_via_usb(self):
    
        def find_usb_directory():

            try:
                # look for new SB file name first
                zipped_file_name = (os.popen("find /media/usb/ -name 'SmartBench-SW-update*.zip'").read()).strip('\n')

                if zipped_file_name == '':
                    # if it doesn't exist, then look for easycut-smartbench.zip file as a backup
                    zipped_file_name = (os.popen("find /media/usb/ -name 'easycut-smartbench*.zip'").read()).strip('\n')

            except:
                zipped_file_name = ''

            if zipped_file_name != '':
                
                os.system('[ -d "/home/pi/temp_repo" ] && sudo rm /home/pi/temp_repo -r')
                
                unzip_dir_command = 'unzip ' + zipped_file_name + ' -d /home/pi/temp_repo'
                os.system(unzip_dir_command)

                dir_path_name = (os.popen('find /home/pi/temp_repo/ -name ' + str((zipped_file_name.strip('.zip')).split('/')[-1])).read()).strip('\n')

            else:

                try:
                    dir_path_name = (os.popen("find /media/usb/ -name 'SmartBench-SW-update*'").read()).strip('\n')

                    if dir_path_name == '':
                        dir_path_name = (os.popen("find /media/usb/ -name 'easycut-smartbench*'").read()).strip('\n')

                except:
                    dir_path_name = ''

            
            if ((dir_path_name.count('SmartBench-SW-update') > 1) or (dir_path_name.count('easycut-smartbench') > 1)):
                return 2
            elif ((dir_path_name.count('SmartBench-SW-update') == 0) and (dir_path_name.count('easycut-smartbench') == 0)):
                return 0
            else:
                return dir_path_name
        
        dir_path_name = find_usb_directory()
        
        if dir_path_name == 2 or dir_path_name == 0:
            return dir_path_name

        log('Updating software from: ' + dir_path_name)

        add_remote = 'cd /home/pi/easycut-smartbench && git remote add temp_repository ' + dir_path_name
        fetch_from_usb = 'cd /home/pi/easycut-smartbench && git fetch temp_repository'
        pull_master_from_usb = 'cd /home/pi/easycut-smartbench && git pull temp_repository master'

        try: 
            os.system(add_remote)
            os.system(fetch_from_usb)
            os.system(pull_master_from_usb)
        except:
            return "update failed"
        
        self.refresh_latest_sw_version()
        checkout_success = self.checkout_latest_version()
        rm_remote = 'git remote rm temp_repository'
        os.system(rm_remote)
        
        if dir_path_name.startswith('/home/pi/'):
            rm_temp_repo = 'sudo rm ' + dir_path_name + ' -r'
            os.system(rm_temp_repo)
           
        if checkout_success == False: 
            return "update failed"
        else:
            return checkout_success



## FIRMWARE UPDATE FUNCTIONS
    def get_fw_update(self):
        os.system("sudo pigpiod")
        print "pigpio daemon started"
        Clock.schedule_once(lambda dt: self.flash_fw(), 2)

    def get_hex_file(self):
        if not path.exists(self.grbl_mega_dir):
            pass 
            # clone git directory
        # then pull latest tags

    def edit_update_fw_shell_script():
        pass

    def flash_fw(self):

        pi = pigpio.pi()
        pi.set_mode(17, pigpio.ALT3)
        print(pi.get_mode(17))
        pi.stop()
        os.system("sudo service pigpiod stop")    
        os.system("./update_fw.sh")
        sys.exit()



            