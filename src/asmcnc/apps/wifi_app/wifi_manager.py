import os
import subprocess
import sys

from asmcnc.comms.logging_system.logging_system import Logger

WPA_SUPPLICANT_PATH = "/etc/wpa_supplicant/wpa_supplicant.conf"
WPA_SUPPLICANT_WLAN0_PATH = "/etc/wpa_supplicant/wpa_supplicant-wlan0.conf"


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

    os.popen("sudo chmod a+w {}".format(WPA_SUPPLICANT_PATH))
    os.popen("sudo chmod a+w {}".format(WPA_SUPPLICANT_PATH))

    with open(WPA_SUPPLICANT_PATH, "w") as f:
        f.write("\n".join(config_lines))

    Logger.info("Configuration written, reconfiguring...")

    # Flush all the IP addresses from cache
    os.system("sudo ip addr flush dev wlan0")

    # Reconfigure the wifi interface
    process = subprocess.Popen(
        ["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"],
    )  # sudo wpa_cli -i wlan0 reconfigure

    output, error = process.communicate()

    if error or "fail" in output.lower():
        Logger.error("Error while connecting to wifi: {}".format(error))
        return False

    # Restart the DHCP service to allocate a new IP address on the new network
    os.system("sudo systemctl restart dhcpcd")

    Logger.info("Connected to wifi successfully!")
    return True




