import subprocess
import sys
import time

from asmcnc.comms.logging_system.logging_system import Logger

WPA_SUPPLICANT_PATH = "/etc/wpa_supplicant/wpa_supplicant.conf"


def is_connected_to_internet():
    """
    Check if the device is connected to the internet.
    Note, this won't work for networks that aren't connected to the internet.
    :return:
    """
    response = subprocess.Popen("ping -c 1 8.8.8.8 > /dev/null 2>&1", shell=True).wait()
    Logger.info("Internet connection status: {}".format(response == 0))
    return response == 0


def connect_to_wifi(ssid, password, country_code):
    """
    Connect to a Wi-Fi network.
    :param ssid: The SSID of the network
    :param password: The password of the network
    :param country_code: The country code of the network
    :return: True if the connection was successful, False otherwise
    """
    if not sys.platform.startswith("linux"):
        Logger.warning("This function is only available on Linux")
        return False

    Logger.info("Connecting to {} ({})".format(ssid, country_code))

    config_lines = [
        "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev",
        "update_config=1",
        "country={}".format(country_code),
        "\n",
        "network={",
        "\tssid=\"{}\"".format(ssid),
        "\tpsk=\"{}\"".format(password),
        "}"
    ]

    subprocess.Popen("sudo chmod 666 {}".format(WPA_SUPPLICANT_PATH), shell=True).wait()

    with open(WPA_SUPPLICANT_PATH, "w") as f:
        f.write("\n".join(config_lines))

    process = subprocess.Popen(["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = process.communicate()

    if process.returncode != 0:
        Logger.error("Failed to connect to WiFi: {}".format(err))
        return False

    Logger.info("Connected to WiFi")

    subprocess.Popen("sudo systemctl restart dhcpcd", shell=True).wait()

    time.sleep(2)

    return is_connected_to_internet()
