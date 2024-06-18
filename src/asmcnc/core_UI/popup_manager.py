import sys

from kivy.uix.rst import RstDocument
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.popups import (
    ErrorPopup,
    InfoPopup,
    MiniInfoPopup,
    StopPopup,
    ParkPopup,
    SoftwareUpdateSuccessPopup,
    WaitPopup,
    WarningPopup,
    UploadSettingsFromUsbPopup,
    DownloadSettingsToUsbPopup, 
    SpindleSafetyPopup, 
    JobValidationPopup,
    SimulatingJobPopup,
    OverwriteSerialNumberPopup
)


class PopupManager:
    sm = None
    l = None
    m = None

    error_popup = None
    info_popup = None
    warning_popup = None
    mini_info_popup = None
    stop_popup = None
    park_popup = None
    software_update_successful_popup = None
    wait_popup = None
    upload_settings_from_usb = None
    download_settings_to_usb = None
    spindle_safety_popup = None
    job_validation_popup = None

    def __init__(self, sm, m, l):
        self.sm = sm
        self.m = m
        self.l = l

        self.setup_popups()

    def setup_popups(self):
        self.error_popup = ErrorPopup(sm=self.sm, m=self.m, l=self.l, main_string="")

        self.info_popup = InfoPopup(
            sm=self.sm,
            m=self.m,
            l=self.l,
            main_string="",
            popup_width=500,
            popup_height=440,
        )

        self.warning_popup = WarningPopup(
            sm=self.sm, m=self.m, l=self.l, main_string=""
        )

        self.mini_info_popup = MiniInfoPopup(
            sm=self.sm, m=self.m, l=self.l, main_string=""
        )

        self.stop_popup = StopPopup(sm=self.sm, m=self.m, l=self.l)

        self.park_popup = ParkPopup(sm=self.sm, m=self.m, l=self.l, main_string="")

        self.software_update_successful_popup = SoftwareUpdateSuccessPopup(
            sm=self.sm, m=self.m, l=self.l, main_string=""
        )

        self.wait_popup = WaitPopup(sm=self.sm, m=self.m, l=self.l)

        self.upload_settings_from_usb = UploadSettingsFromUsbPopup(sm=self.sm, m=self.m, l=self.l, main_string="")

        self.download_settings_to_usb = DownloadSettingsToUsbPopup(sm=self.sm, m=self.m, l=self.l, main_string="")

        self.spindle_safety_popup = SpindleSafetyPopup(sm=self.sm, m=self.m, l=self.l)

        self.job_validation_popup = JobValidationPopup(sm=self.sm, m=self.m, l=self.l, main_string="")

        self.simulating_job_popup = SimulatingJobPopup(sm=self.sm, m=self.m, l=self.l, main_string="")

        self.overwrite_serial_number_popup = OverwriteSerialNumberPopup(sm=self.sm, m=self.m, l=self.l, main_string="")

    def show_spindle_safety_popup(self, button_one_callback, button_two_callback):
        self.spindle_safety_popup.button_one_callback = button_one_callback
        self.spindle_safety_popup.button_two_callback = button_two_callback
        self.spindle_safety_popup.open()

    def hide_spindle_safety_popup(self):
        self.spindle_safety_popup.dismiss()

    def show_error_popup(
        self,
        main_string,
        button_one_callback=None,
        button_two_callback=None,
        button_one_text="Ok",
        button_two_text=None,
        width=500,
        height=400,
        main_label_size_delta=40,
        main_label_h_align="center",
        title="Error!",
        main_label_padding=(0, 10),
        main_layout_padding=(40, 20, 40, 20),
        main_layout_spacing=10,
        button_layout_padding=(0, 20, 0, 0),
        button_layout_spacing=10,
        button_one_background_color=(230 / 255.0, 74 / 255.0, 25 / 255.0, 1.0),
        button_two_background_color=None,
    ):

        self.error_popup.main_string = main_string
        self.error_popup.button_one_text = button_one_text
        self.error_popup.button_two_text = button_two_text
        self.error_popup.button_one_callback = button_one_callback
        self.error_popup.button_two_callback = button_two_callback
        self.error_popup.width = scaling_utils.get_scaled_width(width)
        self.error_popup.height = scaling_utils.get_scaled_height(height)
        self.error_popup.main_label_size_delta = main_label_size_delta
        self.error_popup.main_label_h_align = main_label_h_align
        self.error_popup.title = self.l.get_str(title)
        self.error_popup.main_label_padding = main_label_padding
        self.error_popup.main_layout_padding = main_layout_padding
        self.error_popup.main_layout_spacing = main_layout_spacing
        self.error_popup.button_layout_padding = button_layout_padding
        self.error_popup.button_layout_spacing = button_layout_spacing
        self.error_popup.button_one_background_color = button_one_background_color
        self.error_popup.button_two_background_color = button_two_background_color
        self.error_popup.build()
        self.error_popup.open()

    def show_info_popup(
        self,
        main_string,
        width,
        button_one_callback=None,
        button_two_callback=None,
        button_one_text="Ok",
        button_two_text=None,
        button_one_background_color=(76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0),
        button_two_background_color=None,
        height=440,
        main_label_size_delta=40,
        title="Information",
        main_label_h_align="left",
        main_label_padding=(10, 10),
        main_layout_padding=(10, 10, 10, 10),
        main_layout_spacing=10,
        button_layout_padding=(150, 20, 150, 0),
        button_layout_spacing=15,
    ):
        self.info_popup.main_string = main_string
        self.info_popup.button_one_text = button_one_text
        self.info_popup.button_two_text = button_two_text
        self.info_popup.button_one_callback = button_one_callback
        self.info_popup.button_two_callback = button_two_callback
        self.info_popup.button_one_background_color = button_one_background_color
        self.info_popup.button_two_background_color = button_two_background_color
        self.info_popup.height = scaling_utils.get_scaled_height(height)
        self.info_popup.main_label_size_delta = main_label_size_delta
        self.info_popup.width = scaling_utils.get_scaled_width(width)
        self.info_popup.title = title
        self.info_popup.main_label_h_align = main_label_h_align
        self.info_popup.main_label_padding = main_label_padding
        self.info_popup.main_layout_padding = main_layout_padding
        self.info_popup.main_layout_spacing = main_layout_spacing
        self.info_popup.button_layout_padding = button_layout_padding
        self.info_popup.button_layout_spacing = button_layout_spacing
        self.info_popup.build()
        self.info_popup.open()

    def show_warning_popup(self, main_string):
        self.warning_popup.main_label.text = main_string
        self.warning_popup.open()

    def show_mini_info_popup(self, main_string):
        self.mini_info_popup.main_label.text = main_string
        self.mini_info_popup.open()

    def show_stop_popup(self):
        self.stop_popup.open()

    def show_park_popup(self, main_string):
        self.park_popup.main_label.text = main_string
        self.park_popup.open()

    def show_software_update_successful_popup(self, main_string):
        description = (
            self.l.get_str("Software update was successful.")
            + "\n\n"
            + self.l.get_str("Update message")
            + ": "
            + main_string
            + "\n"
            + self.l.get_str(
                "Please do not restart your machine until you are prompted to do so."
            )
        )
        self.software_update_successful_popup.main_label.text = description
        self.software_update_successful_popup.open()

        def reboot(*args):
            self.sm.current = 'rebooting'
        Clock.schedule_once(reboot, 6)

    def show_wait_popup(self, main_string=None):
        if main_string:
            self.wait_popup.main_label.text = main_string
        else:
            self.wait_popup.main_label.text = self.l.get_str("Please wait") + "..."
        self.wait_popup.open()

    def show_upload_settings_popup(self, sm):
        description = self.l.get_str(
            'This will restore all necessary files from USB for migrating to a new console:') + '\n' + \
            '\n-' + self.l.get_str('Machine settings') + \
            '\n-' + self.l.get_str('Job files') + \
            '\n-' + self.l.get_str('Log files') + \
            '\n\n' + self.l.get_str('Make sure a USB-stick is connected properly!') + \
            '\n\n' + self.l.get_str('This might take a few minutes, depending of the size of your files.')
        self.upload_settings_from_usb.main_label.text = description
        self.upload_settings_from_usb.sm = sm
        self.upload_settings_from_usb.open()

    def show_download_settings_popup(self, sm):
        description = self.l.get_str('This will copy all necessary files for migrating to a new console:') + '\n' + \
            '\n-' + self.l.get_str('Machine settings') + \
            '\n-' + self.l.get_str('Job files') + \
            '\n-' + self.l.get_str('Log files') + \
            '\n\n' + self.l.get_str('Make sure a USB-stick is connected properly!') + \
            '\n\n' + self.l.get_str('This might take a few minutes, depending of the size of your files.')
        self.download_settings_to_usb.main_label.text = description
        self.download_settings_to_usb.sm = sm
        self.download_settings_to_usb.open()

    def show_overwrite_serial_number_popup(self, sm, button_one_callback=None, button_two_callback=None):
        description = self.l.get_str('This will overwrite the serial number of the console.') + \
            '\n\n' + self.l.get_str('Make sure you have the correct serial number before proceeding!') + \
            '\n\n' + self.l.get_str('This action cannot be undone.')
        self.overwrite_serial_number_popup.main_label.text = description
        self.overwrite_serial_number_popup.main_label.halign = 'center'
        self.overwrite_serial_number_popup.sm = sm
        self.overwrite_serial_number_popup.button_one_callback = button_one_callback
        self.overwrite_serial_number_popup.button_two_callback = button_two_callback
        self.overwrite_serial_number_popup.open()
    def close_upload_settings_popup(self):
        self.upload_settings_from_usb.dismiss()

    def close_download_settings_popup(self):
        self.download_settings_to_usb.dismiss()

    def close_mini_info_popup(self):
        self.mini_info_popup.dismiss()

    def close_info_popup(self):
        self.info_popup.dismiss()

    def close_warning_popup(self):
        self.warning_popup.dismiss()

    def close_error_popup(self):
        self.error_popup.dismiss()

    def close_stop_popup(self):
        self.stop_popup.dismiss()

    def close_software_update_successful_popup(self):
        self.software_update_successful_popup.dismiss()

    def close_wait_popup(self):
        self.wait_popup.dismiss()

    # INDIVIDUAL POPUPS
    def show_quit_to_console_popup(self):
        def button_two_callback(*args):
            sys.exit()

        self.show_error_popup(
            main_string="Would you like to exit the software now?",
            title="Warning!",
            button_one_text="No",
            button_two_text="Yes",
            button_two_callback=button_two_callback,
            width=360,
            height=360,
            main_label_size_delta=0,
            main_label_padding=(0, 0),
            main_layout_padding=(30, 20, 30, 0),
            main_layout_spacing=10,
            button_layout_padding=(0, 5, 0, 0),
            button_layout_spacing=15,
            button_two_background_color=(76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0),
            button_one_background_color=(230 / 255.0, 74 / 255.0, 25 / 255.0, 1.0),
        )

    def show_usb_first_aid_popup(self, systemtools_sm):
        def button_two_callback(*args):
            systemtools_sm.clear_usb_mountpoint()

        main_string = (
            self.l.get_str(
                "If your USB stick is plugged into the console, please remove it now."
            )
            + "\n\n"
            + self.l.get_str("When you have removed it, press 'Ok'.")
            + "\n\n"
            + self.l.get_bold(
                "WARNING: Not following this step could cause files to be deleted from your USB stick."
            )
        )

        self.show_error_popup(
            main_string=main_string,
            title="Warning!",
            button_one_text="Cancel",
            button_two_text="Ok",
            button_two_callback=button_two_callback,
            button_one_background_color=(230 / 255.0, 74 / 255.0, 25 / 255.0, 1.0),
            button_two_background_color=(76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0),
            width=360,
            height=360,
            main_label_size_delta=40,
            main_label_padding=(0, 0),
            main_layout_padding=(30, 20, 30, 0),
            main_layout_spacing=10,
            button_layout_padding=(0, 10, 0, 0),
            button_layout_spacing=15,
        )

    def show_beta_testing_popup(self, systemtools_sm):
        def button_two_callback(*args):
            systemtools_sm.open_beta_testing_screen()

        main_string = (
            self.l.get_str(
                "Beta testing allows our engineers and beta testers to try out software updates "
                + "that might not be stable, or change how SmartBench behaves."
            )
            + "\n\n"
            + self.l.get_str(
                "By updating to a beta version or developer branch you may risk causing damage to SmartBench."
            )
            + "\n\n"
            + self.l.get_str("Do you want to continue?")
        )

        self.show_error_popup(
            main_string=main_string,
            title="Warning!",
            button_one_text="No",
            button_two_text="Ok",
            button_two_callback=button_two_callback,
            button_one_background_color=(230 / 255.0, 74 / 255.0, 25 / 255.0, 1.0),
            button_two_background_color=(76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0),
            width=550,
            height=400,
            main_label_size_delta=140,
            main_label_padding=(0, 0),
            main_layout_padding=(30, 20, 30, 0),
            main_layout_spacing=10,
            button_layout_padding=(0, 10, 0, 0),
            button_layout_spacing=15,
        )

    def show_reboot_after_language_change_popup(self):
        def button_two_callback(*args):
            self.sm.current = "rebooting"

        main_string = "Console needs to reboot to update language settings."

        self.show_info_popup(
            main_string=main_string,
            title="Information",
            button_one_text="Cancel",
            button_two_text="Ok",
            button_two_callback=button_two_callback,
            button_one_background_color=(230 / 255.0, 74 / 255.0, 25 / 255.0, 1.0),
            button_two_background_color=(76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0),
            width=300,
            height=300,
            main_label_size_delta=40,
            main_label_padding=(0, 0),
            main_layout_padding=(30, 20, 30, 0),
            main_layout_spacing=10,
            button_layout_padding=(0, 0, 0, 0),
            button_layout_spacing=15,
            main_label_h_align="center",
            main_label_size_hint_y=1.7,
        )

    """
    fsck_type: "good", "error", "info"
    """

    def show_git_fsck_popup(self, main_string, more_info, fsck_type):
        def button_two_callback(*args):
            if fsck_type == "good" or fsck_type == "error":
                self.show_git_fsck_popup(main_string, more_info, "info")

        if not more_info or fsck_type == "info":
            button_two_callback = None

        title = (
            "Information" if fsck_type == "info" or fsck_type == "good" else "Error!"
        )
        width = 500 if fsck_type == "good" or fsck_type == "error" else 600

        parameters = {
            "main_string": main_string,
            "title": title,
            "button_one_text": "Ok",
            "button_two_text": "More Info" if button_two_callback else None,
            "button_two_callback": button_two_callback,
            "button_one_background_color": (
                33 / 255.0,
                150 / 255.0,
                243 / 255.0,
                98 / 100.0,
            ),
            "button_two_background_color": (76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0),
            "width": width,
            "height": 440,
            "main_label_size_delta": 40,
            "main_label_padding": (10, 10),
            "main_layout_padding": (10, 10, 10, 10),
            "main_layout_spacing": 10,
            "button_layout_padding": (10, 20, 10, 0),
            "main_label_h_align": "center",
            "button_layout_spacing": 15,
        }

        if fsck_type == "good" or fsck_type == "info":
            self.show_info_popup(**parameters)
            if fsck_type == "info":
                scroll_view = ScrollView(do_scroll_x=True, do_scroll_y=True, scroll_type=['content'],
                                         always_overscroll=True, size_hint_y=1.2)
                rst_doc = RstDocument(
                    text=more_info,
                    background_color=(1, 1, 1, 1),
                    base_font_size=scaling_utils.get_scaled_width(26),
                    underline_color="000000",
                )
                scroll_view.add_widget(rst_doc)

                self.info_popup.main_layout.remove_widget(self.info_popup.main_label)
                self.info_popup.main_layout.remove_widget(self.info_popup.button_layout)
                self.info_popup.main_layout.add_widget(scroll_view)
                self.info_popup.main_layout.add_widget(self.info_popup.button_layout)
        else:
            self.show_error_popup(**parameters)

    def show_job_validation_popup(self, main_string):
        self.job_validation_popup.main_label.text = main_string
        self.job_validation_popup.open()

    def close_job_validation_popup(self):
        self.job_validation_popup.dismiss()

    def show_simulating_job_popup(self):
        self.simulating_job_popup.main_label.text = self.l.get_str("Simulating job") + "..."
        self.simulating_job_popup.open()

    def close_simulating_job_popup(self):
        self.simulating_job_popup.dismiss()
