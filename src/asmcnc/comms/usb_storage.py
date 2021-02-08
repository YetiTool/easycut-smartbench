'''
Created on 3 Feb 2018

WARNINGS:
- For Linux, make sure that /media/usb/ dir has already been created
- Windows for debug, assumes a single default path which may or may not change - check default variable
- Insecure for Linux
- Don't forget to disable() when not in use, since there's a clock running on it

@author: Ed
'''

from kivy.clock import Clock
import sys, os
from asmcnc.skavaUI import popup_info

class USB_storage(object):
    
    # Default paths
    windows_usb_path = "E:\\" 
    linux_usb_path = "/media/usb/"

    # For debug
    IS_USB_VERBOSE = False
    
    poll_usb_event = None
    mount_event = None
    stick_enabled = False
 
    alphabet_string = 'abcdefghijklmnopqrstuvwxyz'
 
    def __init__(self, screen_manager, localization):
        
        self.sm = screen_manager
        self.l = localization

        if sys.platform == "win32":
            self.usb_path = self.windows_usb_path
        else:
            self.usb_path = self.linux_usb_path

    def enable(self):
        if self.stick_enabled != True:
            self.start_polling_for_usb()
            self.stick_enabled = True

    def disable(self):
        self.stick_enabled = False
        self.stop_polling_for_usb()
        if self.is_usb_mounted_flag == True:
            if sys.platform != "win32":
                self.unmount_linux_usb()
    
    def is_available(self):
        
        files_in_usb_dir = []
        try:
            files_in_usb_dir = os.listdir(self.usb_path)
        except:
            pass
        if files_in_usb_dir:
            return True
        else:
            return False
    
    def get_path(self):
        return self.usb_path
    
    def start_polling_for_usb(self):
        self.poll_usb_event = Clock.schedule_interval(self.get_USB, 0.25)
    
    def stop_polling_for_usb(self):
        if self.poll_usb_event != None: Clock.unschedule(self.poll_usb_event)
        if self.mount_event != None: Clock.unschedule(self.mount_event)

    is_usb_mounted_flag = False
    is_usb_mounting = False

    def get_USB(self, dt):
        
        # Polled by Clock to enable button if USB storage device is present, if so, mount or unmount as necessary
        # Linux
        if sys.platform != "win32":
            try:
                files_in_usb_dir = os.listdir(self.linux_usb_path)
                
                # If files are in directory
                if files_in_usb_dir:
                    self.is_usb_mounted_flag = True
                    if self.IS_USB_VERBOSE: print 'USB: OK'

                # If directory is empty
                else:
                    if self.IS_USB_VERBOSE: print 'USB: NONE'

                    # UNmount the usb if: it is mounted but not present (since the directory is empty)
                    if self.is_usb_mounted_flag:
                        self.unmount_linux_usb()
                    
                    # IF not mounted and location empty, scan for device
                    else:
                        # read devices dir
                        devices = os.listdir('/dev/')
#                         for device in devices:
                        for char in self.alphabet_string:
                            if ('sd' + char) in devices: # sda is a file to a USB storage device. Subsequent usb's = sdb, sdc, sdd etc
                                self.stop_polling_for_usb() # temporarily stop polling for USB while mounting, and attempt to mount
                                if self.IS_USB_VERBOSE: print 'Stopped polling'
                                self.mount_event = Clock.schedule_once(lambda dt: self.mount_linux_usb('sd' + char), 1) # allow time for linux to establish filesystem after os detection of device
                                break
            except (OSError):
                pass

    def unmount_linux_usb(self):
        dismiss_event = None
        popup_USB = None
        unmount_command = 'echo posys | sudo umount -fl '+ self.linux_usb_path

        if (self.sm.current == 'local_filechooser' or 
            self.sm.current == 'usb_filechooser' or
            self.sm.current == 'loading'):

            self.sm.get_screen('loading').usb_status = 'ejecting'
            self.sm.get_screen('loading').update_usb_status()
            self.sm.get_screen('usb_filechooser').update_usb_status()

        else:
            popup_USB = popup_info.PopupUSBInfo(self.sm, self.l, False)
            dismiss_event = Clock.schedule_once(lambda dt: popup_USB.popup.dismiss(), 1.8)


     
        try:
            os.system(unmount_command)
                       
        except:
            if self.IS_USB_VERBOSE: print 'FAILED: Could not UNmount USB'

        def check_linux_usb_unmounted(popup_USB):
            if sys.platform != "win32":

                files_in_usb_dir = os.listdir(self.linux_usb_path)
                
                # If files are in directory
                if files_in_usb_dir:
                    self.is_usb_mounted_flag = True
                    if self.IS_USB_VERBOSE: print 'USB: STILL MOUNTED'

                # If directory is empty
                else:      
                    if self.IS_USB_VERBOSE: print 'USB: UNMOUNTED'
                    self.is_usb_mounted_flag = False
                    Clock.unschedule(poll_for_dismount)

                    def tell_user_safe_to_remove_usb():
                        if dismiss_event != None: popup_USB.popup.dismiss()

                        if (self.sm.current == 'local_filechooser' or 
                            self.sm.current == 'usb_filechooser' or
                            self.sm.current == 'loading'):

                            self.sm.get_screen('loading').usb_status = 'ejected'
                            self.sm.get_screen('loading').update_usb_status()
                            self.sm.get_screen('usb_filechooser').update_usb_status()

                        else:
                            new_popup_USB = popup_info.PopupUSBInfo(self.sm, self.l, True)
                            Clock.schedule_once(lambda dt: new_popup_USB.popup.dismiss(), 1.8)


                    Clock.schedule_once(lambda dt: tell_user_safe_to_remove_usb(), 0.75)
  
        
        poll_for_dismount = Clock.schedule_interval(lambda dt: check_linux_usb_unmounted(popup_USB), 0.5)
    
    def mount_linux_usb(self, device):

        if self.mount_event != None: Clock.unschedule(self.mount_event)
        if self.IS_USB_VERBOSE: print 'Attempting to mount'

        mount_command = "echo posys | sudo mount /dev/" + device + "1 " + self.linux_usb_path # TODO: NOT SECURE
        try:
            os.system(mount_command)
            
            self.is_usb_mounted_flag = True
            self.start_polling_for_usb() # restart checking for USB
            if self.IS_USB_VERBOSE: print 'USB: MOUNTED'

            if (self.sm.current == 'local_filechooser' or 
                self.sm.current == 'usb_filechooser' or
                self.sm.current == 'loading'):

                self.sm.get_screen('loading').usb_status = 'connected'
                self.sm.get_screen('loading').update_usb_status()
                self.sm.get_screen('usb_filechooser').update_usb_status()

            else:
                popup_USB = popup_info.PopupUSBInfo(self.sm, self.l, 'mounted')
                Clock.schedule_once(lambda dt: popup_USB.popup.dismiss(), 1.8)

        except:
            if self.IS_USB_VERBOSE: print 'FAILED: Could not mount USB'        
            self.is_usb_mounted_flag = False
            self.start_polling_for_usb()  # restart checking for USB