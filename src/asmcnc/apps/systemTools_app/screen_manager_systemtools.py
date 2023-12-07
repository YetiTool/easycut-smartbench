# -*- coding: utf-8 -*-
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.comms import usb_storage
from asmcnc.skavaUI import popup_info, screen_diagnostics
from asmcnc.apps.systemTools_app.screens import (
    popup_system,
    screen_system_menu,
    screen_build_info,
    screen_beta_testing,
    screen_grbl_settings,
    screen_factory_settings,
    screen_update_testing,
    screen_developer_temp,
    screen_final_test,
    screen_support_menu,
)


class ScreenManagerSystemTools(object):
    def __init__(
        self, app_manager, screen_manager, machine, settings, localization, keyboard
    ):
        self.am = app_manager
        self.sm = screen_manager
        self.m = machine
        self.set = settings
        self.l = localization
        self.kb = keyboard
        self.usb_stick = usb_storage.USB_storage(self.sm, self.l)

    def open_system_tools(self):
        if not self.sm.has_screen("system_menu"):
            system_menu_screen = screen_system_menu.SystemMenuScreen(
                name="system_menu",
                machine=self.m,
                system_tools=self,
                localization=self.l,
                keyboard=self.kb,
            )
            self.sm.add_widget(system_menu_screen)
        self.sm.current = "system_menu"

    def open_build_info_screen(self):
        if not self.sm.has_screen("build_info"):
            build_info_screen = screen_build_info.BuildInfoScreen(
                name="build_info",
                machine=self.m,
                system_tools=self,
                settings=self.set,
                localization=self.l,
                keyboard=self.kb,
            )
            self.sm.add_widget(build_info_screen)
        self.sm.current = "build_info"

    def open_support_menu_screen(self):
        if not self.sm.has_screen("support_menu"):
            support_menu_screen = screen_support_menu.SupportMenuScreen(
                name="support_menu",
                machine=self.m,
                system_tools=self,
                settings=self.set,
                localization=self.l,
            )
            self.sm.add_widget(support_menu_screen)
        self.sm.current = "support_menu"

    def download_logs_to_usb(self):
        self.usb_stick.enable()
        message = self.l.get_str("Downloading logs, please wait") + "..."
        wait_popup = popup_info.PopupWait(self.sm, self.l, description=message)
        count = 0

        def get_logs(count):
            if self.usb_stick.is_usb_mounted_flag == True:
                os.system(
                    "journalctl > smartbench_logs.txt && sudo cp --no-preserve=mode,ownership smartbench_logs.txt /media/usb/ && rm smartbench_logs.txt"
                )
                wait_popup.popup.dismiss()
                self.usb_stick.disable()

                message = self.l.get_str("Logs downloaded")
                popup_info.PopupMiniInfo(self.sm, self.l, description=message)

            elif count > 30:
                message = self.l.get_str("No USB found!")
                popup_info.PopupMiniInfo(self.sm, self.l, description=message)
                wait_popup.popup.dismiss()
                if self.usb_stick.is_available():
                    self.usb_stick.disable()

            else:
                count += 1
                Clock.schedule_once(lambda dt: get_logs(count), 0.2)
                print(count)

        Clock.schedule_once(lambda dt: get_logs(count), 0.2)

    def reinstall_pika(self):
        message = self.l.get_str("Please wait") + "..."
        wait_popup = popup_info.PopupWait(self.sm, self.l, description=message)

        def do_reinstall():
            try:
                os.system("python -m pip uninstall pika -y")
                os.system("python -m pip install pika==1.2.0")
                os.system("sudo reboot")
                wait_popup.popup.dismiss()

            except:
                message = self.l.get_str("Issue trying to reinstall pika!")
                popup_info.PopupMiniInfo(self.sm, self.l, description=message)
                wait_popup.popup.dismiss()

        Clock.schedule_once(lambda dt: do_reinstall(), 0.2)

    def open_beta_testing_screen(self):
        if not self.sm.has_screen("beta_testing"):
            beta_testing_screen = screen_beta_testing.BetaTestingScreen(
                name="beta_testing",
                system_tools=self,
                settings=self.set,
                localization=self.l,
                keyboard=self.kb,
            )
            self.sm.add_widget(beta_testing_screen)
        self.sm.current = "beta_testing"

    # GRBL Settings and popups
    def open_grbl_settings_screen(self):
        if not self.sm.has_screen("grbl_settings"):
            grbl_settings_screen = screen_grbl_settings.GRBLSettingsScreen(
                name="grbl_settings",
                machine=self.m,
                system_tools=self,
                localization=self.l,
            )
            self.sm.add_widget(grbl_settings_screen)
        self.sm.current = "grbl_settings"

    def download_grbl_settings_to_usb(self):  # system tools manager
        self.m.save_grbl_settings()

        self.usb_stick.enable()
        message = self.l.get_str("Downloading grbl settings, please wait") + "..."
        wait_popup = popup_info.PopupWait(self.sm, self.l, description=message)

        def get_grbl_settings_onto_usb():
            if self.usb_stick.is_usb_mounted_flag == True:
                os.system(
                    "sudo cp --no-preserve=mode,ownership /home/pi/easycut-smartbench/src/sb_values/saved_grbl_settings_params.txt /media/usb/"
                )
                os.system(
                    "rm /home/pi/easycut-smartbench/src/sb_values/saved_grbl_settings_params.txt"
                )

                wait_popup.popup.dismiss()
                self.usb_stick.disable()

                message = self.l.get_str("GRBL settings downloaded")
                popup_info.PopupMiniInfo(self.sm, self.l, description=message)

            else:
                Clock.schedule_once(lambda dt: get_grbl_settings_onto_usb(), 0.2)

        Clock.schedule_once(lambda dt: get_grbl_settings_onto_usb(), 0.2)

    def restore_grbl_settings_from_usb(self):
        self.usb_stick.enable()
        message = self.l.get_str("Restoring grbl settings, please wait") + "..."
        wait_popup = popup_info.PopupWait(self.sm, self.l, description=message)

        def get_grbl_settings_from_usb():
            if self.usb_stick.is_usb_mounted_flag == True:
                filename = "/media/usb/saved_grbl_settings_params.txt"
                success_flag = self.m.restore_grbl_settings_from_file(filename)
                wait_popup.popup.dismiss()
                self.usb_stick.disable()
                if success_flag:
                    message = self.l.get_str("GRBL settings restored!")
                    popup_info.PopupMiniInfo(self.sm, self.l, description=message)
                else:
                    message = self.l.get_str(
                        "Could not restore settings, please check file!"
                    )
                    popup_info.PopupMiniInfo(self.sm, self.l, description=message)

            else:
                Clock.schedule_once(lambda dt: get_grbl_settings_from_usb(), 0.2)

        Clock.schedule_once(lambda dt: get_grbl_settings_from_usb(), 0.2)

    def restore_grbl_settings_from_file(
        self,
    ):  # first half to system tools, second half to machine module
        filename = (
            "/home/pi/easycut-smartbench/src/sb_values/saved_grbl_settings_params.txt"
        )
        success_flag = self.m.restore_grbl_settings_from_file(filename)
        if success_flag:
            message = self.l.get_str("GRBL settings restored!")
            popup_info.PopupMiniInfo(self.sm, self.l, description=message)
        else:
            message = self.l.get_str("Could not restore settings, please check file!")
            popup_info.PopupMiniInfo(self.sm, self.l, description=message)

    def open_factory_settings_screen(self):
        if not self.sm.has_screen("factory_settings"):
            factory_settings_screen = screen_factory_settings.FactorySettingsScreen(
                name="factory_settings",
                machine=self.m,
                system_tools=self,
                settings=self.set,
                localization=self.l,
                keyboard=self.kb,
                usb_stick=self.usb_stick,
            )
            self.sm.add_widget(factory_settings_screen)
        self.sm.current = "factory_settings"

    def open_diagnostics_screen(self):
        if not self.sm.has_screen("diagnostics"):
            diagnostics_screen = screen_diagnostics.DiagnosticsScreen(
                name="diagnostics", screen_manager=self.sm, machine=self.m
            )
            self.sm.add_widget(diagnostics_screen)
        self.sm.current = "diagnostics"

    def open_final_test_screen(self, board):
        if not self.sm.has_screen("final_test"):
            final_test_screen = screen_final_test.FinalTestScreen(
                name="final_test",
                machine=self.m,
                system_tools=self,
                localization=self.l,
                keyboard=self.kb,
            )
            self.sm.add_widget(final_test_screen)

        # SET VALUES FOR BOARD
        self.sm.get_screen("final_test").set_board_up(board)
        self.sm.current = "final_test"

    def open_update_testing_screen(self):
        if not self.sm.has_screen("update_testing"):
            update_testing_screen = screen_update_testing.UpdateTestingScreen(
                name="update_testing", machine=self.m, system_tools=self
            )
            self.sm.add_widget(update_testing_screen)
        self.sm.current = "update_testing"

    def open_developer_screen(self):
        if not self.sm.has_screen("developer_temp"):
            developer_temp_screen = screen_developer_temp.DeveloperTempScreen(
                name="developer_temp", machine=self.m, system_tools=self
            )
            self.sm.add_widget(developer_temp_screen)
        self.sm.current = "developer_temp"

    def back_to_menu(self):
        self.sm.current = "system_menu"

    def exit_app(self):
        self.sm.current = "lobby"
        self.destroy_screen("build_info")
        self.destroy_screen("support_menu")
        self.destroy_screen("system_menu")
        self.destroy_screen("beta_testing")
        self.destroy_screen("grbl_settings")
        self.destroy_screen("factory_settings")
        self.destroy_screen("update_testing")
        self.destroy_screen("developer_temp")
        self.destroy_screen("diagnostics")
        self.destroy_screen("retrieve_lb_cal_data")
        self.destroy_screen("calibration_testing")
        self.destroy_screen("overnight_testing")
        self.destroy_screen("current_adjustment")
        self.destroy_screen("stall_jig")
        self.destroy_screen("set_thresholds")

    def destroy_screen(self, screen_name):
        if self.sm.has_screen(screen_name):
            self.sm.remove_widget(self.sm.get_screen(screen_name))
            print(screen_name + " deleted")

    def do_usb_first_aid(self):
        message = self.l.get_str("Ensuring USB is unmounted, please wait...")
        wait_popup = popup_info.PopupWait(self.sm, self.l, description=message)
        umount_out = str(
            os.popen("sudo umount /media/usb/").read()
        )  # using popen for the block
        popup_system.PopupUSBFirstAid(self, self.l)
        wait_popup.popup.dismiss()

    def clear_usb_mountpoint(self):
        clear_mountpoint_out = str(
            os.popen("sudo rm /media/usb/*").read()
        )  # using popen for the block
        message = (
            self.l.get_str("First aid complete.")
            + "\n\n"
            + self.l.get_str("You can now use your USB stick.")
        )
        popup_info.PopupMiniInfo(self.sm, self.l, description=message)

    def check_git_repository(self):
        message = self.l.get_str("Please wait")
        wait_popup = popup_info.PopupWait(self.sm, self.l, description=message)

        def nested_check_git_repository(dt):
            if self.set.do_git_fsck():
                message = self.l.get_str("No errors found. You're good to go!")
                popup_system.PopupFSCKGood(
                    self.sm, self.l, message, self.set.details_of_fsck
                )

            else:
                message = (
                    self.l.get_str("Errors found!")
                    + "\n"
                    + self.l.get_str("Contact us at https://www.yetitool.com/support")
                )

                popup_system.PopupFSCKErrors(
                    self.sm, self.l, message, self.set.details_of_fsck
                )

            wait_popup.popup.dismiss()

        Clock.schedule_once(nested_check_git_repository, 0.1)
