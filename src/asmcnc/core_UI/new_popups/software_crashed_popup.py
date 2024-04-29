import base64
import os
import socket
import threading

from kivy.base import runTouchApp
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from asmcnc import paths
from asmcnc.comms.localization import Localization
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.new_popups.popup_bases import PopupBase, PopupErrorTitle, PopupScrollableBody
from asmcnc.core_UI.utils import color_provider

CRASH_LOG = os.path.join(paths.COMMS_PATH, "logging_system", "logs", "crash.log")


def check_for_crash():
    return os.path.exists(CRASH_LOG)


def serialize_log_file():
    with open(CRASH_LOG, "rb") as log_file:
        log_file_contents = log_file.read()

    encoded_data = base64.b64encode(log_file_contents)
    return encoded_data


class SoftwareCrashedPopup(PopupBase):
    """This popup is displayed on startup if the software crashed during the last session."""

    localisation = Localization()

    def __init__(self, **kwargs):
        super(SoftwareCrashedPopup, self).__init__(**kwargs)

        title = PopupErrorTitle(size_hint_y=0.15, localisation=self.localisation)
        self.root_layout.add_widget(title)

        main_string = (
            "SmartBench has detected that it crashed during the last session.\n\n"
            "Would you like to send an anonymous crash report to help us diagnose the issue?"
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
        import pika

        encoded_data = serialize_log_file()

        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters('sm-receiver.yetitool.com', 5672, '/',
                                          pika.PlainCredentials(
                                              'console',
                                              '2RsZWRceL3BPSE6xZ6ay9xRFdKq3WvQb')
                                          )
            )
            channel = connection.channel()

            channel.queue_declare(queue="crash_reports", durable=True)

            message = {
                "hostname": socket.gethostname(),
                "log_data": encoded_data,
            }

            channel.basic_publish(exchange="", routing_key="crash_reports", body=str(message))

            Logger.info("Sent crash report, hostname: {}.".format(socket.gethostname()))
        except Exception:
            Logger.exception("Failed to send crash report.")

    def dont_send_crash_report(self, instance):
        self.dismiss()


if __name__ == "__main__":
    popup = SoftwareCrashedPopup(size_hint=(0.8, 0.8))
    popup.open()
    runTouchApp()
