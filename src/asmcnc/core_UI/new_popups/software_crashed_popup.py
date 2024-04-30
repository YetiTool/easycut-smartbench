import json
import os
import socket
import threading

from kivy.base import runTouchApp
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from asmcnc import paths
from asmcnc.comms.localization import Localization
from asmcnc.comms.logging_system import logging_system
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.new_popups.popup_bases import PopupBase, PopupErrorTitle, PopupScrollableBody
from asmcnc.core_UI.utils import color_provider

CRASH_LOG = os.path.join(paths.COMMS_PATH, "logging_system", "logs", "crash.log")


def check_for_crash():
    return os.path.exists(CRASH_LOG)


class SoftwareCrashedPopup(PopupBase):
    """This popup is displayed on startup if the software crashed during the last session."""

    localisation = Localization()
    auto_dismiss = False
    serial_number = None

    def __init__(self, serial_number, **kwargs):
        super(SoftwareCrashedPopup, self).__init__(**kwargs)
        self.serial_number = serial_number

        title = PopupErrorTitle(size_hint_y=0.15, localisation=self.localisation)
        self.root_layout.add_widget(title)

        main_string = (
            "SmartBench has detected that it crashed during the last session.\n\n"
            "Would you like to send a crash report to YetiTool to help diagnose the issue?"
        )
        body = PopupScrollableBody(size_hint_y=0.6, text=main_string)
        self.root_layout.add_widget(body)

        button_layout = BoxLayout(size_hint_y=0.15, spacing=dp(30))
        button_layout.add_widget(
            Button(
                text=self.localisation.get_bold("Don't send crash report"),
                on_press=self.dont_send_crash_report,
                background_color=color_provider.get_rgba("red"),
                background_normal="",
                font_size=scaling_utils.get_scaled_sp("15sp"),
                markup=True,
            )
        )
        button_layout.add_widget(
            Button(
                text=self.localisation.get_bold("Send crash report"),
                on_press=self.send_crash_report,
                background_color=color_provider.get_rgba("green"),
                background_normal="",
                font_size=scaling_utils.get_scaled_sp("15sp"),
                markup=True,
            )
        )

        self.root_layout.add_widget(button_layout)

    def send_crash_report(self, instance):
        self.dismiss()

        try:
            import pika
        except ImportError:
            Logger.exception("Pika not installed. Cannot send crash report.")
            return

        t = threading.Thread(target=self.__send_crash_report)
        t.start()

    def __send_crash_report(self):
        sent = logging_system.send_logs_to_server(CRASH_LOG, self.serial_number)

        if sent:
            Logger.info("Deleting CRASH_LOG file after sending")
            os.remove(CRASH_LOG)

    def dont_send_crash_report(self, instance):
        self.dismiss()
        os.remove(CRASH_LOG)


if __name__ == "__main__":
    popup = SoftwareCrashedPopup(size_hint=(0.8, 0.8), serial_number="123456")
    popup.open()
    runTouchApp()
