"""
OS-level Bluetooth controller (gamepad) management via BlueZ.

Self-contained and app-agnostic: any app can pair/connect a Bluetooth game
controller by importing this module - see popup_pairing.py for the ready-made
UI. The trace app is the first consumer.

Everything talks to bluetoothctl with commands piped over stdin, which works
on every BlueZ version in the field (the non-interactive CLI argument form
only appeared after the version shipped with Raspbian Stretch). Once a
controller is paired AND trusted, BlueZ reconnects it automatically whenever
it is switched on, so nothing needs persisting app-side.

On Windows (development) a mock implementation is returned so the whole UI
flow can be exercised without hardware or OS support.

@author: Benji
"""
import os
import re
import subprocess
import sys
import threading
import time

from kivy.clock import Clock

from asmcnc.comms.logging_system.logging_system import Logger


# Matches both "Device XX:XX:XX:XX:XX:XX Name" (from `devices`/`paired-devices`)
# and discovery lines like "[NEW] Device XX:XX:XX:XX:XX:XX Name".
DEVICE_LINE_RE = re.compile(r"Device ([0-9A-Fa-f:]{17}) (.+)")

# bluetoothctl colours its interactive output; strip ANSI sequences before parsing.
ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]|\x01|\x02")

CONTROLLER_NAME_HINTS = ("xbox", "controller", "gamepad", "joystick", "wireless pad")


def _looks_like_controller(name):
    lowered = name.lower()
    return any(hint in lowered for hint in CONTROLLER_NAME_HINTS)


def _run_on_main_thread(callback, *args):
    Clock.schedule_once(lambda dt: callback(*args), 0)


class BluetoothControllerManager(object):
    """Scan for, pair, connect and forget Bluetooth controllers via BlueZ."""

    SCAN_DURATION_SECONDS = 8

    # Generous upper bound on any single bluetoothctl session; enforced with
    # coreutils `timeout` because Python 2's subprocess has no timeout support.
    SESSION_TIMEOUT_SECONDS = 40

    def __init__(self):
        self._bluetooth_ready = False

    # --- OS setup ---------------------------------------------------------

    def ensure_bluetooth_ready(self):
        """
        Idempotent runtime setup so pairing works on machines in the field
        without re-provisioning. Safe to call repeatedly; only the first call
        does any work.
        """
        if self._bluetooth_ready:
            return
        os.system("sudo rfkill unblock bluetooth")
        os.system("sudo systemctl start bluetooth")

        # Xbox One controllers drop the connection unless Enhanced
        # Re-Transmission Mode is off. Set it now and persist it for future
        # boots (the ansible provisioning also writes the modprobe file, but
        # units in the field never re-run provisioning).
        os.system("echo 1 | sudo tee /sys/module/bluetooth/parameters/disable_ertm > /dev/null")
        os.system(
            "grep -q disable_ertm /etc/modprobe.d/bluetooth.conf 2>/dev/null || "
            "echo 'options bluetooth disable_ertm=Y' | sudo tee -a /etc/modprobe.d/bluetooth.conf > /dev/null"
        )

        self._run_bluetoothctl_session([("power on", 1)])
        self._bluetooth_ready = True

    # --- bluetoothctl plumbing --------------------------------------------

    def _run_bluetoothctl_session(self, commands_with_delays):
        """
        Run one interactive bluetoothctl session, writing each command then
        sleeping the paired delay (so slow operations like pairing get time to
        finish before the session moves on). Returns the session's combined
        output with ANSI colour codes stripped. Blocking - call from a worker
        thread.
        """
        try:
            process = subprocess.Popen(
                ["timeout", str(self.SESSION_TIMEOUT_SECONDS), "bluetoothctl"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )
        except OSError as e:
            Logger.exception("Bluetooth controller: could not start bluetoothctl: {}".format(e))
            return ""

        try:
            for command, delay in commands_with_delays:
                process.stdin.write(command + "\n")
                process.stdin.flush()
                time.sleep(delay)
            output = process.communicate("quit\n")[0]
        except (IOError, OSError, ValueError) as e:
            Logger.exception("Bluetooth controller: bluetoothctl session failed: {}".format(e))
            try:
                process.kill()
            except OSError:
                pass
            return ""

        return ANSI_ESCAPE_RE.sub("", output or "")

    @staticmethod
    def _parse_device_lines(output):
        """Return an ordered {mac: name} dict-alike (list of pairs) from session output."""
        devices = []
        seen_macs = set()
        for line in output.splitlines():
            match = DEVICE_LINE_RE.search(line)
            if not match:
                continue
            mac, name = match.group(1).upper(), match.group(2).strip()
            if mac in seen_macs:
                continue
            seen_macs.add(mac)
            devices.append((mac, name))
        return devices

    @staticmethod
    def _is_unnamed(mac, name):
        # Devices that haven't shared a name show their MAC (dash-separated)
        # as the name - useless in a picker, so they get filtered out.
        return name.replace("-", ":").upper() == mac

    # --- Public async API ---------------------------------------------------

    def scan_async(self, on_done):
        """
        Scan for nearby devices in a background thread. Calls
        on_done(devices) on the main thread, where devices is a list of dicts
        {'mac', 'name', 'paired', 'connected'}, likely controllers first.
        """

        def worker():
            self.ensure_bluetooth_ready()

            paired = self._get_paired_devices_blocking()
            paired_macs = dict((d["mac"], d) for d in paired)

            output = self._run_bluetoothctl_session([
                ("scan on", self.SCAN_DURATION_SECONDS),
                ("scan off", 1),
                ("devices", 1),
            ])

            devices = []
            for mac, name in self._parse_device_lines(output):
                if self._is_unnamed(mac, name):
                    continue
                paired_entry = paired_macs.pop(mac, None)
                devices.append({
                    "mac": mac,
                    "name": name,
                    "paired": paired_entry is not None,
                    "connected": bool(paired_entry and paired_entry["connected"]),
                })
            # Paired devices that didn't show up in the scan (e.g. switched
            # off) still belong in the list so they can be forgotten.
            devices.extend(paired_macs.values())

            devices.sort(key=lambda d: (not d["connected"], not d["paired"],
                                        not _looks_like_controller(d["name"]), d["name"]))
            Logger.info("Bluetooth controller: scan found {} device(s)".format(len(devices)))
            _run_on_main_thread(on_done, devices)

        self._start_worker(worker, "scan")

    def pair_async(self, mac, on_done):
        """
        Pair, trust and connect the given device in a background thread.
        Calls on_done(success, message) on the main thread. Trusting is what
        makes BlueZ auto-reconnect the controller on future power-ups.
        """

        def worker():
            self.ensure_bluetooth_ready()
            output = self._run_bluetoothctl_session([
                ("pair " + mac, 8),
                ("trust " + mac, 2),
                ("connect " + mac, 6),
                ("info " + mac, 1),
            ])
            success = "Connected: yes" in output
            if success:
                message = "Controller connected"
                Logger.info("Bluetooth controller: {} paired and connected".format(mac))
            else:
                message = "Could not connect. Make sure the controller is in pairing mode and try again."
                Logger.warning(
                    "Bluetooth controller: pairing {} failed. Session output:\n{}".format(mac, output))
            _run_on_main_thread(on_done, success, message)

        self._start_worker(worker, "pair")

    def forget_async(self, mac, on_done):
        """Un-pair the device (stops auto-reconnect). Calls on_done() on the main thread."""

        def worker():
            self.ensure_bluetooth_ready()
            self._run_bluetoothctl_session([("remove " + mac, 2)])
            Logger.info("Bluetooth controller: removed {}".format(mac))
            _run_on_main_thread(on_done)

        self._start_worker(worker, "forget")

    # --- Queries ------------------------------------------------------------

    def _get_paired_devices_blocking(self):
        output = self._run_bluetoothctl_session([("paired-devices", 1)])
        paired = []
        for mac, name in self._parse_device_lines(output):
            info = self._run_bluetoothctl_session([("info " + mac, 1)])
            paired.append({
                "mac": mac,
                "name": name,
                "paired": True,
                "connected": "Connected: yes" in info,
            })
        return paired

    def get_connected_controller_async(self, on_done):
        """
        Calls on_done(device_or_None) on the main thread with the first
        connected paired device, if any.
        """

        def worker():
            connected = None
            for device in self._get_paired_devices_blocking():
                if device["connected"]:
                    connected = device
                    break
            _run_on_main_thread(on_done, connected)

        self._start_worker(worker, "query")

    @staticmethod
    def _start_worker(target, label):
        thread = threading.Thread(target=target, name="bt_controller_" + label)
        thread.daemon = True
        thread.start()


class MockBluetoothControllerManager(BluetoothControllerManager):
    """
    Windows/dev stand-in: fakes a scan result and pairing flow so the pairing
    UI can be developed and demonstrated without a Pi or a controller.
    """

    MOCK_SCAN_SECONDS = 2
    MOCK_PAIR_SECONDS = 2

    def __init__(self):
        super(MockBluetoothControllerManager, self).__init__()
        self._mock_paired = {}

    def ensure_bluetooth_ready(self):
        self._bluetooth_ready = True

    def scan_async(self, on_done):
        def deliver(dt):
            devices = [
                {"mac": "AA:BB:CC:DD:EE:01", "name": "Xbox Wireless Controller",
                 "paired": "AA:BB:CC:DD:EE:01" in self._mock_paired,
                 "connected": "AA:BB:CC:DD:EE:01" in self._mock_paired},
                {"mac": "AA:BB:CC:DD:EE:02", "name": "Some Bluetooth Speaker",
                 "paired": False, "connected": False},
            ]
            on_done(devices)

        Clock.schedule_once(deliver, self.MOCK_SCAN_SECONDS)

    def pair_async(self, mac, on_done):
        def deliver(dt):
            self._mock_paired[mac] = True
            on_done(True, "Controller connected")

        Clock.schedule_once(deliver, self.MOCK_PAIR_SECONDS)

    def forget_async(self, mac, on_done):
        self._mock_paired.pop(mac, None)
        Clock.schedule_once(lambda dt: on_done(), 0.5)

    def get_connected_controller_async(self, on_done):
        connected = None
        for mac in self._mock_paired:
            connected = {"mac": mac, "name": "Xbox Wireless Controller",
                         "paired": True, "connected": True}
        Clock.schedule_once(lambda dt: on_done(connected), 0.2)


_manager = None


def get_manager():
    """Shared manager instance (mocked off-Linux) for use by any app."""
    global _manager
    if _manager is None:
        if sys.platform.startswith("linux"):
            _manager = BluetoothControllerManager()
        else:
            _manager = MockBluetoothControllerManager()
    return _manager
