from asmcnc.core_UI.popups import ErrorPopup, InfoPopup, MiniInfoPopup


class PopupManager:
    sm = None
    l = None
    m = None

    def __init__(self, sm, m, l):
        self.sm = sm
        self.m = m
        self.l = l

    error_popup = ErrorPopup(sm=sm, m=m, l=l,
                             main_string="")

    def show_error_popup(self, main_string):
        self.error_popup.main_label.text = main_string
        self.error_popup.open()

    info_popup = InfoPopup(sm=sm, m=m, l=l,
                           main_string="",
                           popup_width=400,
                           popup_height=440)

    def show_info_popup(self, main_string, width):
        self.info_popup.main_label.text = main_string
        self.info_popup.width = width
        self.info_popup.open()

    mini_info_popup = MiniInfoPopup(sm=sm, m=m, l=l,
                                    main_string="")

    def show_mini_info_popup(self, main_string):
        self.mini_info_popup.main_label.text = main_string
        self.mini_info_popup.open()
