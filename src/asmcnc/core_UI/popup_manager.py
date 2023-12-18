from asmcnc.core_UI.popups import ErrorPopup, InfoPopup, MiniInfoPopup


class PopupManager:
    sm = None
    l = None
    m = None

    error_popup = None
    info_popup = None
    mini_info_popup = None

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
            popup_width=400,
            popup_height=440,
        )

        self.mini_info_popup = MiniInfoPopup(
            sm=self.sm, m=self.m, l=self.l, main_string=""
        )

    def show_error_popup(self, main_string):
        self.error_popup.main_label.text = main_string
        self.error_popup.open()

    def show_info_popup(self, main_string, width):
        self.info_popup.main_label.text = main_string
        self.info_popup.width = width
        self.info_popup.open()

    def show_mini_info_popup(self, main_string):
        self.mini_info_popup.main_label.text = main_string
        self.mini_info_popup.open()
