from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.popups import ErrorPopup, InfoPopup, MiniInfoPopup, StopPopup, ParkPopup, SoftwareUpdateSuccessPopup, WarningPopup, WaitPopup


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

        self.stop_popup = StopPopup(
            sm=self.sm, m=self.m, l=self.l
        )

        self.park_popup = ParkPopup(
            sm=self.sm, m=self.m, l=self.l, main_string=""
        )

        self.software_update_successful_popup = SoftwareUpdateSuccessPopup(
            sm=self.sm, m=self.m, l=self.l, main_string=""
        )

        self.wait_popup = WaitPopup(
            sm=self.sm, m=self.m, l=self.l, main_string=self.l.get_str("Please wait") + "...",
            title=self.l.get_str("Please Wait") + "..."
        )

    def show_error_popup(self, main_string, button_one_callback=None):
        self.error_popup.main_string = main_string
        self.error_popup.button_one_callback = button_one_callback
        self.error_popup.build()
        self.error_popup.open()

    def show_info_popup(self, main_string, width):
        self.info_popup.main_string = main_string
        self.info_popup.width = scaling_utils.get_scaled_width(width)
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

    def show_wait_popup(self, main_string=None):
        if main_string:
            self.wait_popup.main_label.text = main_string
        else:
            self.wait_popup.main_label.text = self.l.get_str("Please wait") + "..."
        self.wait_popup.open()

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

    def close_wait_popup(self):
        self.wait_popup.dismiss()
