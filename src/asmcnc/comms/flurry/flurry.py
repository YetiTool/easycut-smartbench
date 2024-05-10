import json
import time
import threading
import pika

from kivy.app import App
from pika.exceptions import UnroutableError, NackError

from asmcnc.comms.localization import Localization
from asmcnc.comms.logging_system.logging_system import Logger

LOCAL_HOST = True

HOST = "localhost" if LOCAL_HOST else "sm-receiver.yetitool.com"
PORT = 5672
VIRTUAL_HOST = "/"

USERNAME = "console"
PASSWORD = "2RsZWRceL3BPSE6xZ6ay9xRFdKq3WvQb"

CREDENTIALS = pika.PlainCredentials(
    username=USERNAME,
    password=PASSWORD
)

CONNECTION_PARAMETERS = pika.ConnectionParameters(
    host=HOST,
    port=PORT,
    virtual_host=VIRTUAL_HOST,
)

if not LOCAL_HOST:
    CONNECTION_PARAMETERS.credentials = CREDENTIALS

MESSAGE_INTERVAL = 15
RECONNECT_INTERVAL = 10


class Flurry(object):
    """Class to handle the connection and communication with the Flurry server."""

    def __init__(self):
        self.app = App.get_running_app()
        self.settings = self.app.settings_manager
        self.machine = self.app.machine
        self.localisation = Localization()

        self.hostname = self.settings.console_hostname
        self.screen_resolution = "{}x{}".format(str(self.app.width), str(self.app.height))

        self.connection_thread = None
        self.connection = None
        self.channel = None

        self.connection_thread = threading.Thread(target=self.__setup)
        self.connection_thread.start()

    def __setup(self):
        """Setup the connection to the Flurry server. Create the connection, channel and start the sending loop."""
        self.__create_connection()
        self.__create_channel()
        self.__send_loop()

    def __create_connection(self):
        """Create a connection to the Flurry server. If the connection can't be established, log an error."""
        try:
            self.connection = pika.BlockingConnection(CONNECTION_PARAMETERS)
            Logger.info("Connection to {} established".format(HOST))
        except RuntimeError:
            Logger.exception("Failed to create connection to {}".format(HOST))

    def __create_channel(self):
        """Create a channel for the connection. If the connection is not established, log an error."""
        if not self.connection:
            Logger.error("Connection not established, cannot create channel")
            return

        self.channel = self.connection.channel()
        Logger.info("Channel created")

    def __send_loop(self):
        """Main sending loop for the Flurry connection. Publishes the console payload to the queue every MESSAGE_INTERVAL
        seconds. If the connection is closed, wait RECONNECT_INTERVAL seconds before attempting to reconnect."""
        while self.connection.is_open:
            self.__publish(self.__get_full_console_payload(), "", "console")
            time.sleep(MESSAGE_INTERVAL)

        Logger.info("Connection to {} closed".format(HOST))
        time.sleep(RECONNECT_INTERVAL)
        self.__setup()

    def __publish(self, payload, exchange, routing_key):
        """Publish a message to the queue. If the message can't be routed, log the error.

        :param payload: The message to send.
        :param exchange: The exchange to send the message to.
        :param routing_key: The routing key to use."""
        try:
            Logger.info("Publishing message to queue: {}".format(routing_key))
            Logger.debug("Payload: {}".format(payload))
            self.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=json.dumps(payload)
            )
        except UnroutableError:
            Logger.exception("Failed to publish message to queue: {}".format(routing_key))
        except NackError:
            Logger.exception("Message to {} was rejected by the consumer".format(routing_key))

    def __get_full_console_payload(self):
        """Get the full console payload to send to the Flurry server."""
        return {
            "hostname": self.hostname,
            "timestamp": time.time(),
            "data": {
                "display_name": self.machine.device_label,
                "location": self.machine.device_location,
                "local_ip_addr": self.settings.ip_address,
                "remote_ip_addr": self.settings.public_ip_address,
                "language": self.localisation.lang,
                "software_version": self.settings.sw_version,
                "firmware_version": self.settings.fw_version,
                "screen_resolution": self.screen_resolution,
            }
        }
