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
    IS_USB_VERBOSE = True
 
 
    def __init__(self, screen_manager):
        
        self.sm = screen_manager

        if sys.platform == "win32":
            self.usb_path = self.windows_usb_path
        else:
            self.usb_path = self.linux_usb_path

 
    def enable(self):
        
        self.start_polling_for_usb()


    def disable(self):
        
        self.stop_polling_for_usb()
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
        self.poll_usb_event = Clock.schedule_interval(self.get_USB, .25)
    
    def stop_polling_for_usb(self):
        Clock.unschedule(self.poll_usb_event)

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
                        for device in devices:
                            if device == 'sda': # sda is a file to a USB storage device. Subsequent usb's = sdb, sdc, sdd etc
                                self.stop_polling_for_usb() # temporarily stop polling for USB while mounting, and attempt to mount
                                if self.IS_USB_VERBOSE: print 'Stopped polling'
                                Clock.schedule_once(self.mount_linux_usb, 1) # allow time for linux to establish filesystem after os detection of device
            except (OSError):
                pass

    def unmount_linux_usb(self):
        unmount_command = 'echo posys | sudo umount -fl '+ self.linux_usb_path
        
        try:
#             USB_message = 'Don\'t remove your USB stick yet.\n\nPlease wait...'
#             popup_USB = popup_info.PopupUSBInfo(self.sm, USB_message)
            os.system(unmount_command)
            
            def check_linux_usb_unmounted():
                if sys.platform != "win32":
                    try:
                        files_in_usb_dir = os.listdir(self.linux_usb_path)
                        
                        # If files are in directory
                        if files_in_usb_dir:
                            self.is_usb_mounted_flag = True
                            if self.IS_USB_VERBOSE: print 'USB: STILL MOUNTED'
        
                        # If directory is empty
                        else:
                            USB_message = 'It is now safe to remove your USB stick.'         
                            if self.IS_USB_VERBOSE: print 'USB: UNMOUNTED'
                            self.is_usb_mounted_flag = False
                            Clock.unschedule(poll_for_dismount)   
#                             popup_USB.popup.dismiss()
#                             popup_USB = popup_info.PopupUSBInfo(self.sm, USB_message)
#                             Clock.schedule_once(lambda dt: popup_USB.popup.dismiss(), 1)
                            
                    except: pass    
            
            poll_for_dismount = Clock.schedule_interval(lambda dt: check_linux_usb_unmounted(), 0.5)
            
        except:
            if self.IS_USB_VERBOSE: print 'FAILED: Could not UNmount USB'


    
    def mount_linux_usb(self, dt):

        if self.IS_USB_VERBOSE: print 'Attempting to mount'

        mount_command = "echo posys | sudo mount /dev/sda1 " + self.linux_usb_path # TODO: NOT SECURE
        try:
            os.system(mount_command)
            
            self.is_usb_mounted_flag = True
            self.start_polling_for_usb() # restart checking for USB
            if self.IS_USB_VERBOSE: print 'USB: MOUNTED'
        except:
            if self.IS_USB_VERBOSE: print 'FAILED: Could not mount USB'        
            self.is_usb_mounted_flag = False
            self.start_polling_for_usb()  # restart checking for USB