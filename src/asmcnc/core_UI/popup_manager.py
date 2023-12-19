import sys

from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.popups import ErrorPopup, InfoPopup, MiniInfoPopup, StopPopup, ParkPopup, SoftwareUpdateSuccessPopup


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
        self.error_popup.title = title
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
            height=400,
            main_label_size_delta=40,
            title="Information",
            main_label_h_align="left",
    ):
        self.info_popup.main_string = main_string
        self.info_popup.button_one_text = button_one_text
        self.info_popup.button_two_text = button_two_text
        self.info_popup.button_one_callback = button_one_callback
        self.info_popup.button_two_callback = button_two_callback
        self.info_popup.height = scaling_utils.get_scaled_height(height)
        self.info_popup.main_label_size_delta = main_label_size_delta
        self.info_popup.width = scaling_utils.get_scaled_width(width)
        self.info_popup.title = title
        self.info_popup.main_label_h_align = main_label_h_align
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
        description = self.l.get_str("Software update was successful.") + \
                      "\n\n" + \
                      self.l.get_str("Update message") + ": " + \
                      main_string + \
                      "\n" + \
                      self.l.get_str("Please do not restart your machine until you are prompted to do so.")
        self.software_update_successful_popup.main_label.text = description
        self.software_update_successful_popup.open()

    def close_mini_info_popup(self):
        self.mini_info_popup.dismiss()

    def close_info_popup(self):
        self.info_popup.dismiss()

    def close_warning_popup(self,):
        self.warning_popup.dismiss()

    def close_error_popup(self):
        self.error_popup.dismiss()

    def close_stop_popup(self):
        self.stop_popup.dismiss()

    def close_software_update_successful_popup(self):
        self.software_update_successful_popup.dismiss()

    # SPECIALIZED POPUPS
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
            button_two_background_color=(76 / 255., 175 / 255., 80 / 255., 1.),
            button_one_background_color=(230 / 255., 74 / 255., 25 / 255., 1.),
        )
