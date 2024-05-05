'''
Created 5 March 2020
@author: Letty
Module to get and store settings info
'''

import sys, os, subprocess, time, threading
from time import sleep
from asmcnc.core_UI import console_utils

from datetime import datetime

from asmcnc.comms.logging_system.logging_system import Logger
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty
from requests import get

try: 
    import pytz #, pigpio ## until production machines are running latest img
except:
    pytz = None

import socket
from kivy.clock import Clock


class Settings(EventDispatcher):
    
    wifi_check_thread = None

    ping_command = 'ping -c1 one.one.one.one'
    wifi_available = False
    ip_address = ''
    WIFI_REPORT_INTERVAL = 2
    full_hostname = socket.gethostname() 
    console_hostname = full_hostname.split('.')[0]
    public_ip_address = ''
    timezone = None

    sw_version = ''
    sw_hash = ''
    sw_branch = ''
    latest_sw_version = ''
    latest_sw_beta = ''
    platform_version = ''
    pl_hash = ''
    pl_branch = ''
    latest_platform_version = ''
    fw_version = ''
    latest_fw_version = ''
    grbl_mega_dir = '/home/pi/grbl-Mega/' 
    usb_or_wifi = ''
    interrupt_bars_active = BooleanProperty(True)

    def __init__(self, screen_manager):
        
        self.sm = screen_manager

        self.get_public_ip_address()
        self.get_timezone()

        self.wifi_check_thread = threading.Thread(target=self.check_wifi_and_refresh_ip_address)
        self.wifi_check_thread.daemon = True
        self.wifi_check_thread.start()

        self.read_interrupt_bars_setting()


## WIFI AND CONNECTIONS

    def check_wifi_and_refresh_ip_address(self):

        while True:

            if sys.platform == "win32":
                try:
                    # get IP address
                    IPAddr=socket.gethostbyname(self.full_hostname)
                    self.ip_address = str(IPAddr)
                    self.wifi_available = True

                except:
                    self.ip_address = ''
                    self.wifi_available = False

            elif sys.platform == 'darwin':
                try:
                    # get IP address
                    IPAddr=socket.gethostbyname(self.full_hostname)
                    self.ip_address = str(IPAddr)

                    # ping to check connection
                    # NB, if this comes out false but there's an IP it indicates connection in local network
                    self.wifi_available = self.do_ping_check()

                except:
                    self.ip_address = ''
                    self.wifi_available = False

            else: # i.e. is a linux platform
                try:

                    # get IP address
                    f = os.popen('hostname -I')
                    potential_IP_address = f.read().strip().split(' ')[0]
                    if len(potential_IP_address.split('.')) == 4:
                        self.ip_address = potential_IP_address

                        # ping to check connection
                        self.wifi_available = self.do_ping_check()

                    else:
                        self.ip_address = ''
                        self.wifi_available = False

                except:
                    self.ip_address = ''
                    self.wifi_available = False

            sleep(self.WIFI_REPORT_INTERVAL)


    def do_ping_check(self):

        ping_delay = 0.1
        ping_timeout = 1

        proc = subprocess.Popen(self.ping_command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)

        while proc.poll() is None and ping_timeout > 0:
            time.sleep(ping_delay)
            ping_timeout -= ping_delay

        if proc.poll() is not None:

            if proc.returncode == 0: return True
            else: return False

        else:
            return False


    def get_public_ip_address(self):

        try: 
            self.public_ip_address = get("https://api.ipify.org", timeout=2).content.decode("utf8")

        except:
            self.public_ip_address = ''

    def get_timezone(self):

        try:

            if pytz:
                self.timezone = pytz.timezone(get('http://ip-api.com/json/' + str(self.public_ip_address)).json()['timezone'])

            else:
                self.timezone = None

        except:
            self.timezone = None

        Logger.info('TIMEZONE: ' + str(self.timezone))


## REFRESH EVERYTHING AT START UP    
    def refresh_all(self):

        self.refresh_latest_platform_version()
        self.refresh_platform_version()
        self.refresh_latest_sw_version()
        self.refresh_sw_version()


## VERSION REFRESH
        
    def refresh_sw_version(self):
        self.sw_version = str(os.popen("git describe --tags").read()).strip('\n')
        self.sw_hash = str(os.popen("git rev-parse --short HEAD").read()).strip('\n')
        self.sw_branch = str(os.popen("git branch | grep \*").read()).strip('\n')

        if self.sw_version == "" or self.sw_version == None:
            self.sw_version = "Unknown"        

    def refresh_latest_sw_version(self):

        delay = 1.0
        timeout = 10.0
        fetch_command = "cd /home/pi/easycut-smartbench/ && git fetch --tags --quiet"

        proc = subprocess.Popen(fetch_command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)

        while proc.poll() is None and timeout > 0:
            time.sleep(delay)
            timeout -= delay

        if proc.poll() is not None:

            try:
                sw_version_list = (str(os.popen("git tag --sort=-refname |head -n 10").read()).split('\n'))
                self.latest_sw_version = str([tag for tag in sw_version_list if "beta" not in tag][0])

                beta_list = [tag for tag in sw_version_list if "beta" in tag]
                if beta_list:
                    self.latest_sw_beta = str(beta_list[0])
                else:
                    self.latest_sw_beta = ""

            except: 
                Logger.info("Could not sort software version tags")
                self.latest_sw_version = ""

        else:
            Logger.info("Could not fetch software version tags")
            self.latest_sw_version = ""

    def fetch_platform_tags(self):
        os.system("cd /home/pi/console-raspi3b-plus-platform/ && git fetch --tags --quiet")

    def refresh_platform_version(self):
        self.platform_version = str(os.popen("cd /home/pi/console-raspi3b-plus-platform/ && git describe --tags").read()).strip('\n')
        self.pl_hash = str(os.popen("cd /home/pi/console-raspi3b-plus-platform/ && git rev-parse --short HEAD").read()).strip('\n')
        self.pl_branch = str(os.popen("cd /home/pi/console-raspi3b-plus-platform/ && git branch | grep \*").read()).strip('\n')

    def refresh_latest_platform_version(self):
        self.latest_platform_version = str(os.popen("cd /home/pi/console-raspi3b-plus-platform/ && git describe --tags `git rev-list --tags --max-count=1`").read()).strip('\n')
    
## GET SOFTWARE UPDATES


    def do_fetch_from_github_check(self):

        # do a fetch to check that we have access to git
        fetch_command = "cd /home/pi/easycut-smartbench && git fetch origin"
        proc = subprocess.Popen(fetch_command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
        stdout, stderr = proc.communicate()

        # if it fails, return an error message for the user
        if ("Could not resolve" in str(stdout)) or ("unable to resolve" in str(stdout)):
            return False

        else: 
            return True

    def get_sw_update_via_wifi(self, beta = False):
        if sys.platform != 'win32' and sys.platform != 'darwin':

            if not self.do_fetch_from_github_check():
                return "Could not resolve host: github.com"

            self.refresh_latest_sw_version()
        self.refresh_sw_version()
        checkout_success = self.checkout_latest_version(beta)
        return checkout_success
    
    def checkout_latest_version(self, beta = False):

        if not beta:
            version_to_checkout = self.latest_sw_version
        else:
            version_to_checkout = self.latest_sw_beta

        if sys.platform != 'win32' and sys.platform != 'darwin':
            if version_to_checkout != self.sw_version:
                os.system("cd /home/pi/easycut-smartbench/")

                cmd  = ["git", "checkout", "-f", version_to_checkout]
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                unformatted_git_output = p.communicate()[1]

                git_output = str(unformatted_git_output).split('\n')
                git_output = list(filter(lambda x: x!= '', git_output))
                     
                if str(git_output[-1]).startswith('HEAD is now at'):
                    self.update_config()
                    description = str(git_output[-1])
                    return description
                
                # elif str(git_output[-1]).endswith('Could not resolve host: github.com'):
                elif "Could not resolve host: github.com" in str(git_output[-1]):
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

        if not self.do_fetch_from_github_check():
            return False
    
        def backup_EC():
            # check if backup directory exists, and delete it if it does
            os.system('[ -d "/home/pi/easycut-smartbench-backup/" ] && sudo rm /home/pi/easycut-smartbench-backup -r')
            # copy EC into a backup directory
            os.system('mkdir /home/pi/easycut-smartbench-backup && cp -RT /home/pi/easycut-smartbench /home/pi/easycut-smartbench-backup')
                
            # compare backup and current directory just in case, and return true if all is well    
            directory_diff = (os.popen('diff -qr /home/pi/easycut-smartbench/ /home/pi/easycut-smartbench-backup/').read())
            if directory_diff == '': return True
            else: 
                os.system('[ -d "/home/pi/easycut-smartbench-backup/" ] && sudo rm /home/pi/easycut-smartbench-backup -r')                
                return False
              
        def clone_new_EC_and_restart():

            if not self.do_fetch_from_github_check():
                return False

            else: 
                # Repair git repo by re-cloning from origin
                os.system('cd /home/pi/ && sudo rm /home/pi/easycut-smartbench -r && git clone https://github.com/YetiTool/easycut-smartbench.git' + 
                '&& cd /home/pi/easycut-smartbench/ && git checkout ' + self.latest_sw_version)
                console_utils.reboot()
        
        if backup_EC() == True:
            clone_new_EC_and_restart()

        else: return False


## USB SOFTWARE UPDATE

    def find_usb_directory(self):
        try:
            # look for new SB file name first
            zipped_file_name = (os.popen("find /media/usb/ -maxdepth 2 -name 'SmartBench-SW-update*.zip'").read()).strip('\n')

            if zipped_file_name == '':
                # if it doesn't exist, then look for easycut-smartbench.zip file as a backup
                zipped_file_name = (os.popen("find /media/usb/ -maxdepth 2 -name 'easycut-smartbench*.zip'").read()).strip('\n')

        except:
            zipped_file_name = ''

        if zipped_file_name != '':
            
            os.system('[ -d "/home/pi/temp_repo" ] && sudo rm /home/pi/temp_repo -r')
            
            unzip_dir_command = 'unzip -q ' + zipped_file_name + ' -d /home/pi/temp_repo/'
            os.system(unzip_dir_command)

            dir_path_name = (os.popen("find /home/pi/temp_repo/ -name 'easycut-smartbench*'").read()).strip('\n')

        else:

            try:
                dir_path_name = (os.popen("find /media/usb/ -maxdepth 2 -name 'SmartBench-SW-update*'").read()).strip('\n')

                if dir_path_name == '':
                    dir_path_name = (os.popen("find /media/usb/ -maxdepth 2 -name 'easycut-smartbench*'").read()).strip('\n')

            except:
                dir_path_name = 0

        
        Logger.info('directory name: ' + dir_path_name)

        if ((dir_path_name.count('SmartBench-SW-update') > 1) or (dir_path_name.count('easycut-smartbench') > 1)):
            return 2
        elif ((dir_path_name.count('SmartBench-SW-update') == 0) and (dir_path_name.count('easycut-smartbench') == 0)):
            return 0
        else:
            return dir_path_name

    def set_up_remote_repo(self, dir_path_name):
        add_remote = 'cd /home/pi/easycut-smartbench && git remote add temp_repository ' + dir_path_name
        fetch_from_usb = 'cd /home/pi/easycut-smartbench && git fetch temp_repository'
        fetch_tags = 'cd /home/pi/easycut-smartbench/ && git fetch temp_repository --tags --quiet'

        try:
            os.system(add_remote)
            os.system(fetch_from_usb)
            os.system(fetch_tags)
            return True

        except:
            return "update failed"

    def clear_remote_repo(self, dir_path_name):
        rm_remote = 'git remote rm temp_repository'
        try: 
            os.system(rm_remote)
        except: 
            pass

        if dir_path_name.startswith('/home/pi/temp_repo/'):
            rm_temp_repo = 'sudo rm /home/pi/temp_repo/ -r'
            os.system(rm_temp_repo)

    def get_sw_update_via_usb(self, beta = False):
        dir_path_name = self.find_usb_directory()
        
        if dir_path_name == 2 or dir_path_name == 0:
            return dir_path_name

        if self.set_up_remote_repo(dir_path_name):
            Logger.info('Updating software from: ' + dir_path_name)
            self.refresh_sw_version()
            self.refresh_latest_sw_version()
            checkout_success = self.checkout_latest_version(beta)   

        self.clear_remote_repo(dir_path_name)

        if checkout_success == False: 
            return "update failed"
        else:
            return checkout_success


## FIRMWARE UPDATE FUNCTIONS
    def get_fw_update(self):
        os.system("sudo pigpiod")
        Logger.info("pigpio daemon started")
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
        Logger.info(pi.get_mode(17))
        pi.stop()
        os.system("sudo service pigpiod stop")    
        os.system("./update_fw.sh")
        sys.exit()

## PLATFORM UPDATES

    def update_platform(self):
        self.refresh_latest_platform_version()
        self.refresh_platform_version()

        if self.latest_platform_version != self.platform_version:
            os.system("cd /home/pi/console-raspi3b-plus-platform/ && git checkout " + self.latest_platform_version)
            os.system("/home/pi/console-raspi3b-plus-platform/ansible/templates/ansible-start.sh")
            os.system("/home/pi/easycut-smartbench/ansible/templates/ansible-start.sh && sudo systemctl restart ansible.service")
            console_utils.reboot()

        else:
            os.system("/home/pi/easycut-smartbench/ansible/templates/ansible-start.sh && sudo systemctl restart ansible.service")
            console_utils.reboot()


    def ansible_service_run(self):
        os.system("/home/pi/easycut-smartbench/ansible/templates/ansible-start.sh")
        console_utils.reboot()

    def ansible_service_run_without_reboot(self):
        os.system("/home/pi/easycut-smartbench/ansible/templates/ansible-start.sh")


## REPOSITORY HEALTHCARE

    details_of_fsck = ""

    def do_git_fsck(self):

        bad_repo_signs = ["error", "loose", "fatal", "broken", "missing"]
        process = subprocess.Popen("git fsck", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        self.details_of_fsck = str(process.communicate()[0])

        if self.details_of_fsck:
            Logger.info("GIT FSCK ERRORS FOUND: ")
            Logger.info(self.details_of_fsck)
            Logger.info("END OF GIT FSCK DETAILS")

        if any(sign in self.details_of_fsck for sign in bad_repo_signs): 
            return False

        return True

    # disable ssh (will not start on boot)
    def disable_ssh(self):
        self.stop_ssh()
        os.system('sudo systemctl disable ssh')

    # enable ssh (will start on boot, only for dev use)
    def enable_ssh(self):
        self.start_ssh()
        os.system('sudo systemctl enable ssh')

    # toggle ssh service running or not
    def toggle_ssh(self):
        ssh_running = self.is_service_running('ssh')

        if ssh_running:
            return self.stop_ssh()

        return self.start_ssh()

    # stop ssh (doesn't change status on boot)
    def stop_ssh(self):
        os.system('sudo systemctl stop ssh')

        return not self.is_service_running('ssh')

    # start ssh (doesn't change status on boot)
    def start_ssh(self):
        os.system('sudo systemctl start ssh')

        return self.is_service_running('ssh')

    def is_service_running(self, service):
        try:
            with open(os.devnull, 'wb') as hide_output:
                exit_code = subprocess.Popen(['systemctl', 'is-active', service],
                                             stdout=hide_output, stderr=hide_output).wait()
                return exit_code == 0
        except:
            # this will happen on non linux systems
            Logger.info("Couldn't check status of service: " + service)

    def read_interrupt_bars_setting(self):
        interrupt_bars_setting = os.popen(
            'grep "interrupt_bars_active" /home/pi/easycut-smartbench/src/config.txt'
        ).read()
        if not interrupt_bars_setting:
            os.system(
                "sudo sed -i -e '$ainterrupt_bars_active=True' /home/pi/easycut-smartbench/src/config.txt"
            )
            self.interrupt_bars_active = True
        else:
            self.interrupt_bars_active = interrupt_bars_setting.split("=")[1].strip() == "True"
        Logger.info("Interrupt bars active: " + str(self.interrupt_bars_active))

    def enable_interrupt_bars(self):
        self.interrupt_bars_active = True
        os.system(
            'sudo sed -i "s/interrupt_bars_active=False/interrupt_bars_active=True/" config.txt'
        )
        Logger.info("Interrupt bars enabled")

    def disable_interrupt_bars(self):
        self.interrupt_bars_active = False
        os.system(
            'sudo sed -i "s/interrupt_bars_active=True/interrupt_bars_active=False/" config.txt'
        )
        Logger.info("Interrupt bars disabled")
            