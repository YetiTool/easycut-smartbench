"""
Workaround for Kivy 1.10.1's missing joystick hot-plug support.

Kivy's SDL2 window provider only opens the joysticks present when the window
is created (see _window_sdl2.pyx), so a controller that connects later - the
normal case for Bluetooth, where the app boots long before the pad is
switched on - never delivers on_joy_* events. SDL itself does notice the new
device (its udev/WM backends keep SDL_NumJoysticks() current as long as the
event pump runs, which Kivy's loop does); the device just never gets opened.

This shim reaches into the SDL2 library already loaded in the process via
ctypes and opens any joystick Kivy missed. Events then flow through Kivy's
normal on_joy_axis/on_joy_button_* dispatch with no other changes.

SDL's joystick API is not thread-safe alongside the event pump: only call
open_new_joysticks() from the main (Kivy) thread, e.g. a Clock callback.

@author: Benji
"""
import ctypes
import os
import sys

from asmcnc.comms.logging_system.logging_system import Logger

_sdl = None
_sdl_load_failed = False


class _SDLJoystickGUID(ctypes.Structure):
    # SDL_JoystickGUID: 16 raw bytes identifying the controller model
    # (bus/vendor/product/version) - stable across reconnects and reboots.
    _fields_ = [("data", ctypes.c_uint8 * 16)]

# Instance ids of joysticks this shim has seen. Re-opening a device that is
# already open (whether by Kivy at boot or by an earlier call here) just bumps
# SDL's refcount; once an id is in this set the duplicate handle is closed
# again immediately, so repeated polling doesn't leak references.
_opened_instance_ids = set()


def _load_sdl():
    global _sdl, _sdl_load_failed
    if _sdl is not None or _sdl_load_failed:
        return _sdl

    candidates = []
    if sys.platform.startswith("linux"):
        candidates = ["libSDL2-2.0.so.0", "libSDL2.so"]
    elif sys.platform == "win32":
        candidates = ["SDL2.dll"]
        # Kivy's Windows SDL2 lives in a dependency package's bin dir which
        # may not be on the DLL search path under this name - but since Kivy
        # has already loaded it into the process, loading by bare name
        # resolves to the same module. The dep bin paths are appended as a
        # fallback for unusual setups.
        try:
            from kivy.deps import sdl2 as sdl2_dep
            candidates.extend(os.path.join(p, "SDL2.dll") for p in sdl2_dep.dep_bins)
        except ImportError:
            try:
                from kivy_deps import sdl2 as sdl2_dep
                candidates.extend(os.path.join(p, "SDL2.dll") for p in sdl2_dep.dep_bins)
            except ImportError:
                pass

    for name in candidates:
        try:
            sdl = ctypes.CDLL(name)
        except OSError:
            continue
        sdl.SDL_NumJoysticks.restype = ctypes.c_int
        sdl.SDL_JoystickOpen.restype = ctypes.c_void_p
        sdl.SDL_JoystickOpen.argtypes = [ctypes.c_int]
        sdl.SDL_JoystickInstanceID.restype = ctypes.c_int
        sdl.SDL_JoystickInstanceID.argtypes = [ctypes.c_void_p]
        sdl.SDL_JoystickClose.restype = None
        sdl.SDL_JoystickClose.argtypes = [ctypes.c_void_p]
        sdl.SDL_JoystickNameForIndex.restype = ctypes.c_char_p
        sdl.SDL_JoystickNameForIndex.argtypes = [ctypes.c_int]
        sdl.SDL_JoystickGetDeviceGUID.restype = _SDLJoystickGUID
        sdl.SDL_JoystickGetDeviceGUID.argtypes = [ctypes.c_int]
        _sdl = sdl
        return _sdl

    _sdl_load_failed = True
    Logger.warning("Joystick hotplug: could not load SDL2 (tried {}) - "
                   "controllers connected after app start won't be seen".format(candidates))
    return None


def open_new_joysticks():
    """
    Open any joystick SDL knows about that isn't already open. Returns the
    number of newly opened devices. Safe to call repeatedly (e.g. on screen
    entry or a slow poll); errors are logged, never raised.
    """
    try:
        sdl = _load_sdl()
        if sdl is None:
            return 0

        newly_opened = 0
        for device_index in range(sdl.SDL_NumJoysticks()):
            joystick = sdl.SDL_JoystickOpen(device_index)
            if not joystick:
                continue
            instance_id = sdl.SDL_JoystickInstanceID(joystick)
            if instance_id in _opened_instance_ids:
                # Already opened by a previous call - release the extra
                # refcount this open just added.
                sdl.SDL_JoystickClose(joystick)
                continue
            _opened_instance_ids.add(instance_id)
            newly_opened += 1
            Logger.info("Joystick hotplug: opened joystick {} (instance id {})".format(
                device_index, instance_id))
        return newly_opened
    except Exception:
        Logger.exception("Joystick hotplug: open_new_joysticks failed")
        return 0


def list_joysticks():
    """
    Names of the joysticks SDL currently sees, as [(device_index, name)].
    Covers USB and Bluetooth alike. Main thread only; errors are logged,
    never raised.
    """
    try:
        sdl = _load_sdl()
        if sdl is None:
            return []

        joysticks = []
        for device_index in range(sdl.SDL_NumJoysticks()):
            raw_name = sdl.SDL_JoystickNameForIndex(device_index)
            if raw_name is None:
                name = 'Unknown controller'
            elif isinstance(raw_name, bytes):
                name = raw_name.decode('utf-8', 'replace')
            else:
                name = raw_name
            joysticks.append((device_index, name))
        return joysticks
    except Exception:
        Logger.exception("Joystick hotplug: list_joysticks failed")
        return []


def get_device_guid_string(device_index):
    """
    SDL GUID of the joystick at device_index as a 32-char hex string, or None.
    The GUID identifies the controller *model*, so a mapping stored against it
    applies to that pad on every reconnect - and doesn't leak onto a different
    model with a different layout.
    """
    try:
        sdl = _load_sdl()
        if sdl is None or device_index >= sdl.SDL_NumJoysticks():
            return None
        guid = sdl.SDL_JoystickGetDeviceGUID(device_index)
        guid_string = ''.join('{:02x}'.format(b) for b in guid.data)
        if guid_string == '0' * 32:  # SDL's "invalid/zero" GUID
            return None
        return guid_string
    except Exception:
        Logger.exception("Joystick hotplug: get_device_guid_string failed")
        return None


def get_primary_device_key():
    """GUID string of the first joystick SDL sees, or None if none connected."""
    return get_device_guid_string(0)


def get_primary_device_name():
    """Name of the first joystick SDL sees, or None if none connected."""
    joysticks = list_joysticks()
    return joysticks[0][1] if joysticks else None
