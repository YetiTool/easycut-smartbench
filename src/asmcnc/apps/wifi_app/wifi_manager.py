import subprocess
import sys

from asmcnc.comms.logging_system.logging_system import Logger

WPA_SUPPLICANT_PATH = "/etc/wpa_supplicant/wpa_supplicant.conf"


def connect_to_wifi(ssid, password, country_code):
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

    with open(WPA_SUPPLICANT_PATH, "w") as f:
        f.write("\n".join(config_lines))

    process = subprocess.Popen(["wpa_cli", "-i", "wlan0", "reconfigure"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = process.communicate()

    if process.returncode != 0:
        Logger.error("Failed to connect to WiFi: {}".format(err))
        return False

    Logger.info("Connected to WiFi")

    return True
