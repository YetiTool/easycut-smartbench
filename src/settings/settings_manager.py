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
#                 os.system('sudo sed -i "s/check_config=False/check_config=True/" /home/pi/easycut-smartbench/src/config.txt')
#                 
#                 sed_sw_version = (''.join(['sudo sed -i "s/version=', str(self.sw_version) + '/version=', 
#                                         str(self.latest_sw_version), '/" /home/pi/easycut-smartbench/src/config.txt'])).strip('\n')
#                 os.system(sed_sw_version)
# 
#                 os.system('sudo sed -i "s/power_cycle_alert=False/power_cycle_alert=True/" /home/pi/easycut-smartbench/src/config.txt')

                os.system('cd /home/pi/ && sudo rm easycut-smartbench -r && git clone https://github.com/YetiTool/easycut-smartbench.git',
                ' && cd /home/pi/easycut-smartbench/ && git checkout ' + self.latest_sw_version + '../starteasycut.sh')

#                 os.system("cd /home/pi/easycut-smartbench/")
#                 cmd  = ["git", "checkout", self.latest_sw_version]
#                 #output = str(os.popen("git checkout " + self.latest_sw_version).read()).strip('\n')
#                 p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#                 
#                 unformatted_git_output = p.communicate()[1]
#                 
#                 if unformatted_git_output.startswith('Note: checking out'):
#                     git_output = str(unformatted_git_output).split('\n')
#                     git_output = list(filter(lambda x: x!= '', git_output))
#                     
#                     print git_output
#                     
#                     print str(git_output[0])
#                     print str(git_output[-1])
#                     
#                     if str(git_output[-1]).startswith('HEAD is now at') and str(git_output[-1]).endswith('updated version number'):
#                         description = str(git_output[0]) + '\n' + str(git_output[-1])
#                         popup_info.PopupWelcome(self.sm, description)
#                 
#                 else: 
#                     print "error message!"
                #self.sm.current = 'rebooting'
            else: print "Software already up to date"