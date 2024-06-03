import json
import platform
import threading
import time
from functools import partial

import pika
from kivy.app import App
from pika.exceptions import UnroutableError, NackError, ConnectionWrongStateError

from asmcnc.comms.grbl_settings_manager import GRBLSettingsManagerSingleton
from asmcnc.comms.localization import Localization
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.comms.model_manager import ModelManagerSingleton

LOCAL_HOST = False  # Set to True to use a local RabbitMQ server

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

EXCHANGE = "flurry"
CONSOLE_QUEUE = "console"
GRBL_SETTINGS_QUEUE = "grbl_settings"
SPINDLE_QUEUE = "spindle"


class Flurry(object):
    """Class to handle the connection and communication with the Flurry server. This class will replace the current
    implementation of the Flurry connection in the future."""

    def __init__(self):
        Logger.info("Initialising Flurry connection")

        self.app = App.get_running_app()
        self.settings = self.app.settings_manager
        self.machine = self.app.machine
        self.localisation = Localization()
        self.model_manager = ModelManagerSingleton()
        self.grbl_settings_manager = GRBLSettingsManagerSingleton()
        self.parameters_to_update = {}

        # Required parameters for Console payload (won't change during runtime)
        self.hostname = self.settings.console_hostname
        self.screen_version = 1 if self.app.width == 800 else 2
        self.pi_version = 3 if platform.machine() == "armv7l" else 4 if platform.machine() == "aarch64" else 0
        self.model_version = self.model_manager.get_product_code().value

        self.connection_thread = None
        self.connection = None
        self.channel = None

        self.connection_thread = threading.Thread(target=self.__setup)
        self.connection_thread.daemon = True  # Daemonize the thread, so it closes when the main thread closes
        self.connection_thread.start()

    def __setup(self):
        """Set up the connection to the Flurry server. Create the connection, channel and start the sending loop."""
        self.__create_connection()
        self.__create_channel()
        self.__on_start_up()
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
        try:
            self.channel = self.connection.channel()
            Logger.info("Channel created")
        except ConnectionWrongStateError:
            Logger.exception("Connection not established, cannot create channel")

    def __on_start_up(self):
        """Send the initial payloads to the Flurry server on start up to sync."""

        Logger.info("Waiting for Smartbench to be ready...")
        self.app.smartbench_ready.wait()
        self.bind_listeners()  # Bind listeners after the Smartbench is ready
        Logger.info("Sending initial payloads to Flurry server")

        self.__publish(self.__get_full_console_payload(), EXCHANGE, CONSOLE_QUEUE)
        self.__publish(self.__get_grbl_settings_payload(), EXCHANGE, GRBL_SETTINGS_QUEUE)

        # Spindle payload isn't sent on start up, as the spindle serial number is not available yet. It will be sent
        # when the spindle serial number is set.

    def __send_loop(self):
        """Main sending loop for the Flurry connection. Publishes the parameter update payloads to the queue every
        MESSAGE_INTERVAL seconds. If the connection is closed, wait RECONNECT_INTERVAL seconds before attempting to
        reconnect."""
        while self.connection.is_open:
            if self.parameters_to_update:
                for queue, payload in self.parameters_to_update.items():
                    payload['timestamp'] = time.time()  # Insert timestamp just before sending
                    self.__publish(payload, EXCHANGE, queue)
                self.parameters_to_update = {}

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
                "firmware_version": self.machine.s.fw_version,
                "hardware_version": self.machine.s.hw_version,
                "screen_version": self.screen_version,
                "pi_version": self.pi_version,
                "model_version": self.model_version,
                "total_uptime": self.machine.s.total_uptime_seconds
            }
        }

    def __get_grbl_settings_payload(self):
        """Get the GRBL settings payload to send to the Flurry server."""
        return {
            "hostname": self.hostname,
            "data": {
                "3": self.machine.s.setting_3,
                "100": self.machine.s.setting_100,
                "101": self.machine.s.setting_101,
                "102": self.machine.s.setting_102,
            }
        }

    def __get_spindle_payload(self):
        """Get the spindle payload to send to the Flurry server."""
        return {
            "serial_number": self.machine.s.spindle_serial_number,
            "hostname": self.hostname,
            "data": {
                "total_uptime": self.machine.s.spindle_total_run_time_seconds
            }
        }

    def bind_listeners(self):
        """Bind the listeners for the Flurry connection."""

        # Binds for GRBL settings
        self.machine.s.bind(setting_3=partial(self.__add_pending_update, GRBL_SETTINGS_QUEUE, "3"))
        self.machine.s.bind(setting_100=partial(self.__add_pending_update, GRBL_SETTINGS_QUEUE, "100"))
        self.machine.s.bind(setting_101=partial(self.__add_pending_update, GRBL_SETTINGS_QUEUE, "101"))
        self.machine.s.bind(setting_102=partial(self.__add_pending_update, GRBL_SETTINGS_QUEUE, "102"))

        # Binds for Console
        self.machine.bind(device_label=partial(self.__add_pending_update, CONSOLE_QUEUE, "display_name"))
        self.machine.bind(device_location=partial(self.__add_pending_update, CONSOLE_QUEUE, "location"))
        self.settings.bind(ip_address=partial(self.__add_pending_update, CONSOLE_QUEUE, "local_ip_addr"))
        self.settings.bind(public_ip_address=partial(self.__add_pending_update, CONSOLE_QUEUE, "remote_ip_addr"))
        self.localisation.bind(lang=partial(self.__add_pending_update, CONSOLE_QUEUE, "language"))

        # Binds for Spindle
        self.machine.s.bind(spindle_serial_number=partial(self.__add_pending_full_payload, SPINDLE_QUEUE,
                                                          self.__get_spindle_payload))
        self.machine.s.bind(spindle_total_run_time_seconds=partial(self.__add_pending_update, SPINDLE_QUEUE,
                                                                   "total_uptime"))

    def __add_pending_full_payload(self, queue, payload_func, instance, value):
        """Add a full payload to the pending messages to be sent to the Flurry server."""
        payload = payload_func()
        Logger.info("{}, {}, {}, {}".format(queue, payload_func, instance, value))
        if queue not in self.parameters_to_update:
            self.parameters_to_update[queue] = payload
        else:
            for key, value in payload.items():
                self.parameters_to_update[queue][key] = value

    def __add_pending_update(self, queue, key, instance, value):
        """Add an update to the pending messages to be sent to the Flurry server."""
        Logger.info("{}, {}, {}, {}".format(queue, key, instance, value))
        if queue not in self.parameters_to_update:
            self.parameters_to_update[queue] = {
                "hostname": self.hostname,
                "data": {
                    key: value
                }
            }
        else:
            self.parameters_to_update[queue]["data"][key] = value
