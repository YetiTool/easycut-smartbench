"""
Reusable, persistent mapping of controller buttons/axes to app functions.

An app declares named actions (fired on button press) and named axes (polled
for analogue values), each with a default binding, and gets back an object
that dispatches Kivy's SDL joystick events accordingly - transport-agnostic,
so USB and Bluetooth controllers behave identically. E.g.:

    input_map = ControllerInputMap(
        app_id='trace',
        actions=[('capture_point', 'Capture point', 0, self.add_segment)],
        axes=[('jog_x', 'Jog left/right', {'axis': 4, 'sign': 1})],
    )
    ...
    value = input_map.get_axis('jog_x')   # raw SDL int16 * sign

Bindings the user reassigns (see popup_input_mapping.py) are saved to
sb_values/controller_mappings.json, keyed by app, platform and controller:
 - platform, because SDL's axis/button numbering differs between Windows and
   Linux, so a mapping made on one must not leak onto the other;
 - controller (SDL device GUID, which identifies the pad model), so each
   controller only ever needs configuring once - reconnects and reboots reuse
   its saved mapping, and a different pad model gets safe defaults rather
   than another pad's layout. When a controller connects mid-session the map
   notices (new stick id in the event stream) and reloads its bindings.

@author: Benji
"""
import json
import os
import sys

from kivy.core.window import Window

from asmcnc import paths
from asmcnc.bluetooth_controller import sdl_joystick_hotplug
from asmcnc.comms.logging_system.logging_system import Logger

MAPPINGS_FILE_PATH = os.path.join(paths.SB_VALUES_PATH, "controller_mappings.json")

BUTTON = 'button'
AXIS = 'axis'

# See start_capture(): an axis must be seen this close to rest before a
# push past the capture threshold will bind it.
AXIS_ARM_THRESHOLD = 10000
AXIS_CAPTURE_THRESHOLD = 20000


def _platform_key():
    if sys.platform.startswith("linux"):
        return "linux"
    return sys.platform


def _device_key():
    # Keyed to the first connected controller's GUID; "default" when nothing
    # is connected yet (a controller connecting later triggers a reload).
    return sdl_joystick_hotplug.get_primary_device_key() or "default"


def _load_mappings_file():
    if not os.path.exists(MAPPINGS_FILE_PATH):
        return {}
    try:
        with open(MAPPINGS_FILE_PATH, 'r') as f:
            return json.load(f)
    except (IOError, ValueError) as e:
        Logger.warning("Controller input map: could not read {}: {}".format(MAPPINGS_FILE_PATH, e))
        return {}


def _save_mappings_file(data):
    try:
        if not os.path.isdir(paths.SB_VALUES_PATH):
            os.makedirs(paths.SB_VALUES_PATH)
        with open(MAPPINGS_FILE_PATH, 'w') as f:
            json.dump(data, f, indent=2, sort_keys=True)
    except (IOError, OSError) as e:
        Logger.exception("Controller input map: could not write {}: {}".format(MAPPINGS_FILE_PATH, e))


def get_shared_value(key, default=None):
    """Read a top-level value from the shared mappings file (e.g. last UI mode)."""
    return _load_mappings_file().get(key, default)


def set_shared_value(key, value):
    data = _load_mappings_file()
    data[key] = value
    _save_mappings_file(data)


class ControllerInputMap(object):
    """
    Routes joystick events to named app actions/axes, with user-reassignable,
    persisted bindings. Construct once per app; call activate()/deactivate()
    from the owning screen's on_enter/on_leave so actions can't fire while the
    app isn't showing.
    """

    def __init__(self, app_id, actions=None, axes=None):
        self.app_id = app_id

        # Declaration order is preserved for the mapping UI.
        # actions: (action_id, display_name, default_button_id, callback)
        # axes:    (axis_name, display_name, {'axis': int, 'sign': 1 or -1})
        self.actions = list(actions or [])
        self.axes = list(axes or [])

        self._callbacks = dict((a[0], a[3]) for a in self.actions)
        self._default_buttons = dict((a[0], a[2]) for a in self.actions)
        self._default_axes = dict((a[0], dict(a[2])) for a in self.axes)

        # Live bindings: action_id -> button_id, axis_name -> {'axis', 'sign'}
        self.button_bindings = {}
        self.axis_bindings = {}

        # Latest raw SDL value per hardware axis id, filled from on_joy_axis.
        self._axis_values = {}

        self._active = False
        self._capture = None  # dict while capturing, see start_capture()
        self._capture_armed_axes = set()

        # Which controller (GUID) the current bindings belong to, and which
        # SDL stick instance ids have been seen - a new id means a controller
        # (re)connected, so the right device's bindings get loaded.
        self._bindings_device_key = None
        self._seen_stick_ids = set()

        self._load()

        Window.bind(on_joy_button_down=self._on_joy_button_down)
        Window.bind(on_joy_axis=self._on_joy_axis)

    # --- App-facing API ------------------------------------------------------

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False
        self.cancel_capture()

    def get_axis(self, axis_name):
        """Latest raw SDL value (+/-32768 range) for the named axis, sign applied."""
        binding = self.axis_bindings.get(axis_name)
        if not binding:
            return 0
        return self._axis_values.get(binding['axis'], 0) * binding['sign']

    # --- Event dispatch --------------------------------------------------------

    def _check_device(self, stick_id):
        if stick_id in self._seen_stick_ids:
            return
        self._seen_stick_ids.add(stick_id)
        if _device_key() != self._bindings_device_key:
            self._load()

    def _on_joy_button_down(self, window, stick_id, button_id):
        self._check_device(stick_id)
        if self._capture:
            if self._capture['kind'] == BUTTON:
                self._complete_capture(button_id)
            return
        if not self._active:
            return
        for action_id, bound_button in self.button_bindings.items():
            if bound_button == button_id:
                callback = self._callbacks.get(action_id)
                if callback:
                    callback()

    def _on_joy_axis(self, window, stick_id, axis_id, value):
        self._check_device(stick_id)
        if self._capture and self._capture['kind'] == AXIS:
            # An axis only becomes eligible ("armed") once seen near rest, so
            # a stick already held over - or noise the instant the capture
            # starts - can't bind itself before the user actually pushes.
            if abs(value) < AXIS_ARM_THRESHOLD:
                self._capture_armed_axes.add(axis_id)
            elif axis_id in self._capture_armed_axes and abs(value) >= AXIS_CAPTURE_THRESHOLD:
                self._complete_capture({'axis': axis_id, 'sign': 1 if value > 0 else -1})
            return
        self._axis_values[axis_id] = value

    # --- Capture (assignment UI) -------------------------------------------------

    def start_capture(self, kind, target_id, on_captured):
        """
        Suspend normal dispatch and bind target_id (an action_id for kind
        BUTTON, an axis_name for kind AXIS) to the next button press / firm
        axis push. on_captured(binding) runs after the mapping is saved. For
        axes, the push direction is stored as the binding's sign - so pushing
        the "wrong" way simply inverts the axis to match the user.
        """
        self._capture = {'kind': kind, 'target': target_id, 'on_captured': on_captured}
        self._capture_armed_axes = set()

    def cancel_capture(self):
        self._capture = None
        self._capture_armed_axes = set()

    def _complete_capture(self, binding):
        capture, self._capture = self._capture, None
        if capture['kind'] == BUTTON:
            self.button_bindings[capture['target']] = binding
        else:
            self.axis_bindings[capture['target']] = binding
        self.save()
        Logger.info("Controller input map: '{}' {} '{}' bound to {}".format(
            self.app_id, capture['kind'], capture['target'], binding))
        if capture['on_captured']:
            capture['on_captured'](binding)

    # --- Binding descriptions (for UI labels) ---------------------------------------

    def describe_action_binding(self, action_id):
        button_id = self.button_bindings.get(action_id)
        if button_id is None:
            return 'Unassigned'
        return 'Button {}'.format(button_id)

    def describe_axis_binding(self, axis_name):
        binding = self.axis_bindings.get(axis_name)
        if not binding:
            return 'Unassigned'
        description = 'Axis {}'.format(binding['axis'])
        if binding['sign'] < 0:
            description += ' (inverted)'
        return description

    # --- Persistence ------------------------------------------------------------------

    def reset_to_defaults(self):
        self.button_bindings = dict(self._default_buttons)
        self.axis_bindings = dict((name, dict(b)) for name, b in self._default_axes.items())
        self.save()

    def save(self):
        # Written under the device key the bindings were loaded for, so a
        # capture always lands against the controller that produced it.
        data = _load_mappings_file()
        data.setdefault(self.app_id, {}).setdefault(_platform_key(), {})[
            self._bindings_device_key or _device_key()] = {
            'buttons': self.button_bindings,
            'axes': self.axis_bindings,
        }
        _save_mappings_file(data)

    def _load(self):
        self._bindings_device_key = _device_key()
        stored = (_load_mappings_file()
                  .get(self.app_id, {})
                  .get(_platform_key(), {})
                  .get(self._bindings_device_key, {}))
        if stored:
            Logger.info("Controller input map: '{}' loaded stored bindings for device {}".format(
                self.app_id, self._bindings_device_key))

        self.button_bindings = dict(self._default_buttons)
        for action_id, button_id in stored.get('buttons', {}).items():
            if action_id in self._callbacks:
                self.button_bindings[action_id] = button_id

        self.axis_bindings = dict((name, dict(b)) for name, b in self._default_axes.items())
        for axis_name, binding in stored.get('axes', {}).items():
            if axis_name in self.axis_bindings and 'axis' in binding:
                self.axis_bindings[axis_name] = {'axis': binding['axis'],
                                                 'sign': binding.get('sign', 1)}
