"""
Created on 3 Feb 2018

WARNINGS:
- For Linux, make sure that /media/usb/ dir has already been created
- Windows for debug, assumes a single default path which may or may not change - check default variable
- Insecure for Linux
- Don't forget to disable() when not in use, since there's a clock running on it

@author: Ed
"""

from asmcnc.comms.logging_system.logging_system import Logger
from kivy.clock import Clock
import sys, os, subprocess
from asmcnc.core_UI.popups import ErrorPopup
from asmcnc.skavaUI import popup_info


class USB_storage(object):
    windows_usb_path = "E:\\"
    linux_usb_path = "/media/usb/"
    IS_USB_VERBOSE = False
    poll_usb_event = None
    mount_event = None
    stick_enabled = False
    alphabet_string = "abcdefghijklmnopqrstuvwxyz"
    usb_notifications = True

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
        if self.poll_usb_event != None:
            Clock.unschedule(self.poll_usb_event)
        if self.mount_event != None:
            Clock.unschedule(self.mount_event)

    is_usb_mounted_flag = False
    is_usb_mounting = False

    def get_USB(self, dt):
        if sys.platform != "win32":
            try:
                files_in_usb_dir = os.listdir(self.linux_usb_path)
                if files_in_usb_dir:
                    self.is_usb_mounted_flag = True
                    if self.IS_USB_VERBOSE:
                        Logger.info("USB: OK")
                else:
                    if self.IS_USB_VERBOSE:
                        Logger.info("USB: NONE")
                    if self.is_usb_mounted_flag:
                        self.unmount_linux_usb()
                    else:
                        devices = os.listdir("/dev/")
                        for char in self.alphabet_string:
                            if "sd" + char in devices:
                                self.stop_polling_for_usb()
                                if self.IS_USB_VERBOSE:
                                    Logger.debug("Stopped polling")
                                self.mount_event = Clock.schedule_once(
                                    lambda dt: self.mount_linux_usb("sd" + char), 1
                                )
                                break
            except OSError:
                pass

    def unmount_linux_usb(self):
        dismiss_event = None
        unmount_command = "echo posys | sudo umount " + self.linux_usb_path
        self.show_user_usb_status("ejecting")
        try:
            os.system(unmount_command)
        except:
            if self.IS_USB_VERBOSE:
                Logger.error("FAILED: Could not UNmount USB")

        def check_linux_usb_unmounted():
            if sys.platform != "win32":
                files_in_usb_dir = os.listdir(self.linux_usb_path)
                if files_in_usb_dir:
                    self.is_usb_mounted_flag = True
                    if self.IS_USB_VERBOSE:
                        Logger.info("USB: STILL MOUNTED")
                else:
                    if self.IS_USB_VERBOSE:
                        Logger.info("USB: UNMOUNTED")
                    self.is_usb_mounted_flag = False
                    Clock.unschedule(poll_for_dismount)

                    def tell_user_safe_to_remove_usb():
                        self.sm.pm.close_error_popup()
                        self.show_user_usb_status("ejected")

                    Clock.schedule_once(lambda dt: tell_user_safe_to_remove_usb(), 0.75)

        poll_for_dismount = Clock.schedule_interval(
            lambda dt: check_linux_usb_unmounted(), 0.5
        )

    def mount_linux_usb(self, device):
        if self.mount_event != None:
            Clock.unschedule(self.mount_event)
        if self.IS_USB_VERBOSE:
            Logger.debug("Attempting to mount")
        mount_command = (
            "echo posys | sudo mount /dev/" + device + "1 " + self.linux_usb_path
        )
        try:
            proc = subprocess.Popen(
                mount_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
            )
            stdout, stderr = proc.communicate()
            exit_code = int(proc.returncode)
            if exit_code == 0:
                self.is_usb_mounted_flag = True
                self.start_polling_for_usb()
                if self.IS_USB_VERBOSE:
                    Logger.info("USB: MOUNTED")
                self.show_user_usb_status("connected")
            else:
                description = (
                    self.l.get_str(
                        "Problem mounting USB stick. Please remove your USB stick, and check that it is working properly."
                    )
                    + "\n\n"
                    + self.l.get_str(
                        "If this error persists, you may need to reformat your USB stick."
                    )
                )
                self.sm.pm.show_error_popup(
                    description, button_one_callback=self.start_polling_for_usb
                )
        except:
            if self.IS_USB_VERBOSE:
                Logger.error("FAILED: Could not mount USB")
            self.is_usb_mounted_flag = False
            self.start_polling_for_usb()

    def show_user_usb_status(self, mode):
        if self.usb_notifications:
            if (
                self.sm.current == "local_filechooser"
                or self.sm.current == "usb_filechooser"
                or self.sm.current == "loading"
            ):
                self.sm.get_screen("loading").usb_status = mode
                self.sm.get_screen("loading").update_usb_status()
                self.sm.get_screen("usb_filechooser").update_usb_status()
            else:
                if mode == "connected":
                    popup_mode = "mounted"
                elif mode == "ejected":
                    popup_mode = True
                elif mode == "ejecting":
                    popup_mode = False
                description = None
                ok_button_background_color = None
                if popup_mode == "mounted":
                    description = (
                        self.l.get_str("USB stick found!")
                        + "\n\n"
                        + self.l.get_str(
                            "Please do not remove your USB stick until it is safe to do so."
                        )
                    )
                    ok_button_background_color = [
                        230 / 255.0,
                        74 / 255.0,
                        25 / 255.0,
                        1.0,
                    ]
                elif not popup_mode:
                    description = (
                        self.l.get_str("Do not remove your USB stick yet.")
                        + "\n\n"
                        + self.l.get_str("Please wait")
                        + "..."
                    )
                    ok_button_background_color = [
                        230 / 255.0,
                        74 / 255.0,
                        25 / 255.0,
                        1.0,
                    ]
                elif popup_mode:
                    description = self.l.get_str(
                        "It is now safe to remove your USB stick."
                    )
                    ok_button_background_color = [
                        76 / 255.0,
                        175 / 255.0,
                        80 / 255.0,
                        1.0,
                    ]
                self.sm.pm.show_error_popup(
                    main_string=description,
                    width=350,
                    height=350,
                    main_label_padding=(40, 20),
                    button_layout_padding=(0, 0, 0, 0),
                    button_one_background_color=ok_button_background_color,
                )
                event = Clock.schedule_once(
                    lambda dt: self.sm.pm.close_error_popup(), 1.8
                )
