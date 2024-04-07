import subprocess
import sys

from asmcnc.comms.logging_system.logging_system import Logger

WPA_SUPPLICANT_PATH = "/etc/wpa_supplicant/wpa_supplicant.conf"


def is_network_connected():
    """
    Check if the network is connected.
    :return: True if the network is connected, False otherwise
    """
    try:
        result = subprocess.Popen(['ip', 'addr', 'show', 'wlan0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = result.communicate()
        return "inet" in output.decode("utf-8")
    except subprocess.CalledProcessError:
        return False


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

    # Check if the network is connected successfully
    if not is_network_connected():
        Logger.error("Failed to get IP address for the interface")
        return False

    Logger.info("Connected to WiFi")

    return True
