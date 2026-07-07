"""
Reusable popup for connecting a game controller, with distinct Bluetooth and
USB modes.

App-agnostic: construct with just the screen manager and localization object
that every screen already holds, e.g.

    from asmcnc.bluetooth_controller import popup_pairing
    popup_pairing.PopupControllerPairing(self.sm, self.l)

Bluetooth mode scans/pairs/forgets via BlueZ (manager.py); USB mode needs no
pairing and simply shows the controllers SDL can currently see. Passing the
optional input_map (a ControllerInputMap) adds a "Configure controls" button
that opens the button/axis assignment popup.

Scanning/pairing/forgetting run in the manager's background threads; every UI
update here happens on the main thread. On a successful connect the SDL
hot-plug shim is invoked so the controller starts delivering Kivy joystick
events immediately, without an app restart.

@author: Benji
"""
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView

from asmcnc.bluetooth_controller import manager as bt_manager
from asmcnc.bluetooth_controller import input_map as input_map_module
from asmcnc.bluetooth_controller import popup_input_mapping
from asmcnc.bluetooth_controller import sdl_joystick_hotplug

GREEN = [76 / 255., 175 / 255., 80 / 255., 1.]
RED = [230 / 255., 74 / 255., 25 / 255., 1.]
BLUE = [25 / 255., 118 / 255., 210 / 255., 1.]
GREY = [120 / 255., 120 / 255., 120 / 255., 1.]
DARK_GREY = [0.25, 0.25, 0.25, 1.]

MODE_BLUETOOTH = 'bluetooth'
MODE_USB = 'usb'


class PopupControllerPairing(Widget):

    def __init__(self, screen_manager, localization, input_map=None):
        self.sm = screen_manager
        self.l = localization
        self.input_map = input_map
        self.manager = bt_manager.get_manager()
        self.busy = False

        # Mode toggle - two linked ToggleButtons acting as tabs
        self.bluetooth_toggle = ToggleButton(text=self.l.get_bold('Bluetooth'), markup=True,
                                             group='controller_connection_mode', allow_no_selection=False,
                                             background_normal='', background_color=GREY)
        self.usb_toggle = ToggleButton(text=self.l.get_bold('USB'), markup=True,
                                       group='controller_connection_mode', allow_no_selection=False,
                                       background_normal='', background_color=GREY)
        self.bluetooth_toggle.bind(on_press=lambda *args: self.set_mode(MODE_BLUETOOTH))
        self.usb_toggle.bind(on_press=lambda *args: self.set_mode(MODE_USB))
        toggle_row = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=42)
        toggle_row.add_widget(self.bluetooth_toggle)
        toggle_row.add_widget(self.usb_toggle)

        self.instruction_label = Label(size_hint_y=None, height=30, markup=True,
                                       color=[0.3, 0.3, 0.3, 1], font_size=15)
        self.status_label = Label(size_hint_y=None, height=30, markup=True,
                                  color=[0, 0, 0, 1], font_size=18)

        # Scrollable list of devices
        self.device_list = GridLayout(cols=1, spacing=6, size_hint_y=None, padding=[0, 0])
        self.device_list.bind(minimum_height=self.device_list.setter('height'))
        scroll = ScrollView(do_scroll_x=False, scroll_type=['content', 'bars'])
        scroll.add_widget(self.device_list)

        self.scan_button = Button(markup=True, background_normal='', background_color=BLUE)
        self.scan_button.bind(on_press=lambda *args: self.refresh())
        close_button = Button(text=self.l.get_bold('Close'), markup=True,
                              background_normal='', background_color=RED)

        button_row = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=None, height=50)
        button_row.add_widget(close_button)
        if self.input_map is not None:
            configure_button = Button(text=self.l.get_bold('Configure controls'), markup=True,
                                      background_normal='', background_color=GREY)
            configure_button.bind(on_press=self.open_input_mapping)
            button_row.add_widget(configure_button)
        button_row.add_widget(self.scan_button)

        layout = BoxLayout(orientation='vertical', spacing=8, padding=[20, 10, 20, 15])
        layout.add_widget(toggle_row)
        layout.add_widget(self.instruction_label)
        layout.add_widget(self.status_label)
        layout.add_widget(scroll)
        layout.add_widget(button_row)

        self.popup = Popup(title=self.l.get_str('Connect a controller'),
                           title_color=[0, 0, 0, 1],
                           title_size='20sp',
                           content=layout,
                           size_hint=(None, None),
                           size=(560, 440),
                           auto_dismiss=False)
        self.popup.separator_color = BLUE
        self.popup.separator_height = '4dp'
        self.popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        close_button.bind(on_press=self.popup.dismiss)

        self.popup.open()
        self.set_mode(input_map_module.get_shared_value('ui_mode', MODE_BLUETOOTH))

    # --- Mode handling --------------------------------------------------------

    def set_mode(self, mode):
        self.mode = MODE_USB if mode == MODE_USB else MODE_BLUETOOTH
        input_map_module.set_shared_value('ui_mode', self.mode)

        is_bluetooth = self.mode == MODE_BLUETOOTH
        self.bluetooth_toggle.state = 'down' if is_bluetooth else 'normal'
        self.usb_toggle.state = 'normal' if is_bluetooth else 'down'
        self.bluetooth_toggle.background_color = BLUE if is_bluetooth else GREY
        self.usb_toggle.background_color = GREY if is_bluetooth else BLUE

        if is_bluetooth:
            self.instruction_label.text = self.l.get_str(
                'Hold the pair button on the controller until its light flashes rapidly.')
            self.scan_button.text = self.l.get_bold('Scan again')
        else:
            self.instruction_label.text = self.l.get_str(
                "Plug the controller into the console's USB port.")
            self.scan_button.text = self.l.get_bold('Refresh')

        self.refresh()

    def refresh(self):
        if self.mode == MODE_BLUETOOTH:
            self.start_scan()
        else:
            self.refresh_usb()

    def open_input_mapping(self, *args):
        popup_input_mapping.PopupInputMapping(self.sm, self.l, self.input_map)

    # --- USB mode ---------------------------------------------------------------

    def refresh_usb(self):
        # Open anything newly plugged in first, then show what SDL sees.
        # Instant, so no busy state or worker thread needed.
        sdl_joystick_hotplug.open_new_joysticks()
        joysticks = sdl_joystick_hotplug.list_joysticks()

        self.device_list.clear_widgets()
        if not joysticks:
            self.set_status(self.l.get_str('No controller detected.'), RED)
            return

        self.set_status(self.l.get_str('Controller detected - ready to use.'), GREEN)
        for _index, name in joysticks:
            row = Button(text='{}\n[size=13]{}[/size]'.format(name, self.l.get_str('Detected')),
                         markup=True, halign='center', size_hint_y=None, height=52,
                         background_normal='', background_color=GREEN,
                         color=[1, 1, 1, 1])
            self.device_list.add_widget(row)

    # --- Bluetooth mode: scanning -------------------------------------------------

    def start_scan(self):
        if self.busy:
            return
        self.busy = True
        self.scan_button.disabled = True
        self.set_status(self.l.get_str('Scanning...'), GREY)
        self.device_list.clear_widgets()
        self.manager.scan_async(self.on_scan_done)

    def on_scan_done(self, devices):
        self.busy = False
        self.scan_button.disabled = False
        if self.mode != MODE_BLUETOOTH:
            # Mode was switched while the scan was in flight - the USB view
            # is showing its own content now.
            return
        self.device_list.clear_widgets()

        if not devices:
            self.set_status(self.l.get_str('No devices found. Is the controller in pairing mode?'), RED)
            return

        connected = [d for d in devices if d['connected']]
        if connected:
            self.set_status(self.l.get_str('Controller connected') + ': ' + connected[0]['name'], GREEN)
        else:
            self.set_status(self.l.get_str('Tap a device to connect it.'), GREY)

        for device in devices:
            self.device_list.add_widget(self.build_device_row(device))

    # --- Bluetooth mode: device rows ------------------------------------------------

    def build_device_row(self, device):
        if device['connected']:
            detail = self.l.get_str('Connected')
        elif device['paired']:
            detail = self.l.get_str('Paired')
        else:
            detail = device['mac']

        row = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=52)

        device_button = Button(
            text='{}\n[size=13]{}[/size]'.format(device['name'], detail),
            markup=True, halign='center',
            background_normal='',
            background_color=GREEN if device['connected'] else [1, 1, 1, 1],
            color=[1, 1, 1, 1] if device['connected'] else [0, 0, 0, 1])
        if not device['connected']:
            device_button.bind(on_press=self.get_pair_func(device))
        row.add_widget(device_button)

        if device['paired']:
            forget_button = Button(text=self.l.get_str('Forget'), size_hint_x=0.3,
                                   background_normal='', background_color=RED)
            forget_button.bind(on_press=self.get_forget_func(device))
            row.add_widget(forget_button)

        return row

    # --- Bluetooth mode: pairing / forgetting ------------------------------------------

    def get_pair_func(self, device):
        def pair(*args):
            if self.busy:
                return
            self.busy = True
            self.scan_button.disabled = True
            self.set_status(self.l.get_str('Connecting to') + ' ' + device['name'] + '...', GREY)
            self.manager.pair_async(device['mac'], self.on_pair_done)
        return pair

    def on_pair_done(self, success, message):
        self.busy = False
        self.scan_button.disabled = False
        if success:
            self.set_status(self.l.get_str('Controller connected'), GREEN)
            # Make the freshly connected pad visible to Kivy right away
            # (works around Kivy 1.10.1's missing joystick hot-plug).
            sdl_joystick_hotplug.open_new_joysticks()
            if self.mode == MODE_BLUETOOTH:
                self.start_scan()
        else:
            self.set_status(self.l.get_str(message), RED)

    def get_forget_func(self, device):
        def forget(*args):
            if self.busy:
                return
            self.busy = True
            self.scan_button.disabled = True
            self.set_status(self.l.get_str('Forgetting') + ' ' + device['name'] + '...', GREY)
            self.manager.forget_async(device['mac'], self.on_forget_done)
        return forget

    def on_forget_done(self):
        self.busy = False
        self.scan_button.disabled = False
        if self.mode == MODE_BLUETOOTH:
            self.start_scan()

    # --- Helpers ----------------------------------------------------------------

    def set_status(self, text, color):
        self.status_label.color = color
        self.status_label.text = text
