'''
Created 5 March 2020
@author: Letty
Module to get and store settings info
'''

import sys,os, subprocess
from asmcnc.skavaUI import popup_info

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
    
    def __init__(self, screen_manager):
        
        self.sm = screen_manager
        
        self.refresh_latest_platform_version()
        self.refresh_platform_version()
        self.refresh_latest_sw_version()
        self.refresh_sw_version()
        
    def refresh_sw_version(self):
        self.sw_version = str(os.popen("git describe --tags").read()).strip('\n')
        self.sw_hash = str(os.popen("git rev-parse --short HEAD").read()).strip('\n')
        self.sw_branch = str(os.popen("git branch | grep \*").read()).strip('\n')

    def refresh_latest_sw_version(self):
        self.latest_sw_version = str(os.popen("cd /home/pi/easycut-smartbench/ && git fetch --tags --quiet && git describe --tags `git rev-list --tags --max-count=1`").read()).strip('\n')

    def refresh_platform_version(self):
        self.platform_version = str(os.popen("cd /home/pi/console-raspi3b-plus-platform/ && git describe --tags").read()).strip('\n')
        self.pl_hash = str(os.popen("cd /home/pi/console-raspi3b-plus-platform/ && git rev-parse --short HEAD").read()).strip('\n')
        self.pl_branch = str(os.popen("cd /home/pi/console-raspi3b-plus-platform/ && git branch | grep \*").read()).strip('\n')

    def refresh_latest_platform_version(self):
        self.latest_platform_version = str(os.popen("cd /home/pi/console-raspi3b-plus-platform/ && git fetch --tags --quiet && git describe --tags `git rev-list --tags --max-count=1`").read()).strip('\n')

    def get_sw_update(self):
        
        if sys.platform != 'win32':
            if self.latest_sw_version != self.sw_version:
        ##      Update SW according to latest release:

                ## Normal update
                os.system("cd /home/pi/easycut-smartbench/")
                cmd  = ["git", "checkout", self.latest_sw_version]
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                unformatted_git_output = p.communicate()[1]
                 
                if unformatted_git_output.startswith('Note: checking out'):
                    self.update_config()
                    git_output = str(unformatted_git_output).split('\n')
                    git_output = list(filter(lambda x: x!= '', git_output))
                     
                    if str(git_output[-1]).startswith('HEAD is now at') and str(git_output[-1]).endswith('updated version number'):
                        description = str(git_output[0]) + '\n' + str(git_output[-1])
                        popup_info.PopupSoftwareUpdateSuccess(self.sm, description)
                    
                else: 
                    description = "There was a problem updating your software. \n\n" \
                    "We can try to fix the problem, but you MUST have a stable internet connection and" \
                    "power supply.\n\n" \
                    "Would you like to repair your software now?"
                    
                    popup_info.PopupSoftwareRepair(self.sm, self, description)
                    
                
            else: print "Software already up to date"

    def update_config(self):
        os.system('sudo sed -i "s/check_config=False/check_config=True/" /home/pi/easycut-smartbench/src/config.txt')
        sed_sw_version = (''.join(['sudo sed -i "s/version=', str(self.sw_version) + '/version=', 
                                str(self.latest_sw_version), '/" /home/pi/easycut-smartbench/src/config.txt'])).strip('\n')
        os.system(sed_sw_version)
        os.system('sudo sed -i "s/power_cycle_alert=False/power_cycle_alert=True/" /home/pi/easycut-smartbench/src/config.txt')

    
    def repair_EC(self):
    
        def backup_EC():
            # check if backup directory exists, and delete it if it does
            os.system('[ -d "/home/pi/easycut-smartbench-backup/" ] && sudo rm /home/pi/easycut-smartbench-backup -r')
            # copy EC into a backup directory
            os.system('mkdir /home/pi/easycut-smartbench-backup && cp -RT /home/pi/easycut-smartbench /home/pi/easycut-smartbench-backup')
    
            # Update starteasycut shell script to look for backup/other folders if required
            # We really need to work on platform updates
            case = (os.popen('grep -Fx "[ ! -d " /home/pi/starteasycut.sh').read()) #current/old directory command
            if not case.startswith('[ ! -d '):
                # if not, copy from backup
                backup_command = '\[ ! -d \"home/pi/easycut-smartbench/src/\" \] && mkdir \/home\/pi\/easycut-smartbench && cp -RT \/home\/pi\/easycut-smartbench-backup \/home\/pi\/easycut-smartbench'
                sed_cmd = ('sudo sed -i \'/echo \\"start easycut\\"/ a ' + backup_command + '\' /home/pi/starteasycut.sh') 
                os.system(sed_cmd)
                
            directory_diff = (os.popen('diff -qr /home/pi/easycut-smartbench/src/ /home/pi/easycut-smartbench-backup/src/'))
            print directory_diff
            
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

        else: 
            description = "It was not possible to backup EC safely, please try again later.\n\n" + \
            "If this issue persists, please contact Yeti Tool Ltd for support."
            popup_info.PopupError(self.sm, description)