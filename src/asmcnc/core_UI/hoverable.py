from kivy.core.window.window_sdl2 import WindowSDL
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput

from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.core_UI.ScreenDesigner.add_widget_popup import AddWidgetPopup

INSPECTOR_WIDGET = True


class InspectorSingleton(EventDispatcher):
    """
    Uses the hoverable behavior to select widgets by hovering.
    This InspectorSingleton binds to keystrokes [l,p,i], so you can
    [l]ock on the selected widget (hovering will be disabled)
    un[l]ock from a selected widget to hover again
    p = go to parent widget
    c = goto child widget
    s = goto sibling
    arrow keys = move widget around
    [i]nspect the widget to print details on console
    
    

    can be deactivated by global INSPECTOR_WIDGET flag
    """
    _instance = None
    widgetType = None
    widget = None
    locked = False
    edit_mode = False

    def __new__(cls):
        if cls._instance is None:
            Logger.debug("Creating new instance of DataMinerSingleton")
            cls._instance = super(InspectorSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        super(EventDispatcher, self).__init__(**kwargs)
        self.child_index = -1
        self.child_max = -1
        if INSPECTOR_WIDGET:
            Window.bind(on_key_down=self._on_key_down)

    def _on_key_down(self, *args, **kwargs):
        """
        Callback being called when a key is pressed.
        Is used for debugging purposes to print debug info about the UI elements.
        """
        keycode = args[3]
        key = args[1]

        #Logger.debug('keycode: {}  | args {}').format(keycode,args)

        # [l]ock on widget:
        if keycode == 'l':
            if not self.locked:
                Logger.debug('LOCKED to: {}'.format(self.get_widget_name_class(self.widget)))
                self.locked = True
            else:
                Logger.debug('UNLOCKED')
                self.locked = False
        # go to [p]arent
        elif keycode == 'p':
            self.switch_to_parent()
        elif keycode == 'c':
            self.switch_to_child()
        elif keycode == 's':
            self.switch_to_sibling()
        elif keycode == 'a':
            self.switch_to_sibling_bw()
        # [i]nspect widget
        elif keycode == 'i':
            self.inspect_widget()
        elif keycode == 'd':
            pass
            #  not implemented yet in Screen
            # self.dump_screen()
        elif keycode == 'h':
            self.print_help()
        elif keycode == 'q':
            # pass
            self.show_popup()
        elif keycode == 'e':
            self.edit_mode = not self.edit_mode
            Logger.debug('edit_mode: {}'.format(self.edit_mode))

        # check for arrow keys to move the widget
        if 273 <= key <= 276:
            if self.edit_mode:
                self.move_widget(key)

        # Return True to accept the key. Otherwise, it will be used by the system.
        return True

    def show_popup(self):
        popup = AddWidgetPopup(widget=self.widget)
        popup.open()

    def move_widget(self, key):
        """
        Moves the selected widget 5 pixels into one direction.

        The direction is determined by the pressed arrow key.
        """
        try:
            if key == 273:  # up
                self.widget.pos[1] += 5
            elif key == 274:  # down
                self.widget.pos[1] -= 5
            elif key == 275:  # right
                self.widget.pos[0] += 5
            elif key == 276:  # left
                self.widget.pos[0] -= 5
            Logger.debug('pos: {}'.format(self.widget.pos))
        except Exception as ex:
            Logger.error("Failed to move widget!")

    def get_parent_screen(self):
        p = self.widget
        while not issubclass(type(p), Screen):
            p = p.parent
        return p
    def dump_screen(self):
        self.get_parent_screen().dump_screen()

    def dump_screen_tsv(self):
        j = self.get_parent_screen().dump_screen()

    def print_help(self):
        Logger.debug('Walking through the widget tree:')
        Logger.debug('--------------------------------')
        Logger.debug('l: (un)locks the selected widget.')
        Logger.debug('e: (e)dit_mode on/off (enables moving widgets)')
        Logger.debug('i: inspects the widget and shows its attributes.')
        Logger.debug('c: switches to the first child.')
        Logger.debug('s: cycles through siblings. You need to switch to a child first!')
        Logger.debug('a: cycles through siblings backwards. You need to switch to a child first!')
        Logger.debug('p: switches to the parent.\n')
        Logger.debug('q: Open popup to add new widgets to the currently selected one.\n')
        Logger.debug('When a widget is selected and edit_mode = True, you can use the arrow keys to move it.')
        Logger.debug("Or just drag'n drop it with the mouse\n")


    def get_widget_name_class(self, widget):
        """
        Tries to get the name of the given widget. If the widget has no name use 'NO_NAME' instead.
        returns name (class name)
        """
        # check if it has a name
        if hasattr(widget, 'name'):
            name = widget.name
        elif hasattr(widget, 'id') and widget.id:
            name = widget.id
        else:
            name = 'NO_NAME'
        return '{} ({})'.format(name, type(widget).__name__)

    def switch_to_sibling(self):
        """
        Switches to the next sibling. If there are no more siblings left it returns to the first one.
        This only works if switched to a child before to get the number of siblings.
        """
        if self.child_max > 1:
            if self.child_index < self.child_max - 1:
                self.child_index += 1
            else:
                self.child_index = 0
            self.widget = self.widget.parent.children[self.child_index]
            try:
                # check if it is a Layout and has no name
                name = self.widget.name
            except AttributeError:
                name = type(self.widget)
            Logger.debug('Switched to sibling {}/{}: {}'.format(self.child_index,
                                                                self.child_max,
                                                                self.get_widget_name_class(self.widget)))
            self.inspect_widget(short=True)
        elif self.child_max == 1:
            Logger.debug('No siblings. Only one child!')
        else:
            Logger.warning('Not switched to children first...')

    def switch_to_sibling_bw(self):
        """
        Switches to the next sibling. If there are no more siblings left it returns to the first one.
        This only works if switched to a child before to get the number of siblings.
        """
        if self.child_max > 1:
            if self.child_index > 0:
                self.child_index -= 1
            else:
                self.child_index = self.child_max - 1
            self.widget = self.widget.parent.children[self.child_index]
            try:
                # check if it is a Layout and has no name
                name = self.widget.name
            except AttributeError:
                name = type(self.widget)
            Logger.debug('Switched to sibling {}/{}: {}'.format(self.child_index,
                                                                self.child_max,
                                                                self.get_widget_name_class(self.widget)))
            self.inspect_widget(short=True)
        elif self.child_max == 1:
            Logger.debug('No siblings. Only one child!')
        else:
            Logger.warning('Not switched to children first...')

    def switch_to_child(self):
        """
        Switches to the first child if the currently selected widget has children.
        """
        children = self.widget.children
        if len(children) == 0:
            Logger.debug('{} has no children!'.format(self.get_widget_name_class(self.widget)))
        else:
            self.child_index = 0
            self.child_max = len(children)
            self.widget = children[self.child_index]
            Logger.debug('Switched to child: {}/{}: {}'.format(self.child_index,
                                                               self.child_max,
                                                               self.get_widget_name_class(self.widget)))
            self.inspect_widget(short=True)

    def switch_to_parent(self):
        """Switches to the parent of the currently selected widget."""

        self.child_index = -1
        self.child_max = -1
        parent = self.widget.parent
        if parent is None:
            Logger.debug('{} has no parent!'.format(self.get_widget_name_class(self.widget)))
        elif issubclass(type(parent), WindowSDL):
            Logger.warning('Orphaned!')
        else:
            self.widget = parent
            Logger.debug('Switched to parent: {}'.format(self.get_widget_name_class(self.widget)))
            self.inspect_widget(short=True)

    def inspect_widget(self, short=False):
        """Prints debug information about the currently selected widget."""
        Logger.debug('========================================')
        if not short:
            Logger.debug(self.get_widget_name_class(self.widget))
        Logger.debug('pos: {}\t\tsize:{}\t\tchildren: {}\t\topacity: {}'.format(self.widget.pos,
                                                                                self.widget.size,
                                                                                len(self.widget.children),
                                                                                self.widget.opacity))
        if issubclass(type(self.widget), (Label,TextInput)):
            Logger.debug('text: "{}"'.format(self.widget.text))
        if issubclass(type(self.widget), Image):
            Logger.debug('source: "{}"'.format(self.widget.source))
        Logger.debug('========================================')

    def set_widget(self, w):
        """Sets the given widget as selected, so it can be inspected."""
        self.widget = w
        self.widgetType = type(w)


class HoverBehavior(object):
    """
    Hover behavior.
    :Events:
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget
    """
    inspector = InspectorSingleton()
    hovered = BooleanProperty(False)
    drag = False

    def __init__(self, **kwargs):
        if INSPECTOR_WIDGET:
            self.register_event_type('on_enter')
            Window.bind(mouse_pos=self.on_mouse_pos)
            Window.bind(on_touch_down=self.on_mouse_press)
            Window.bind(on_touch_move=self.on_move)
            Window.bind(on_touch_up=self.on_mouse_release)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_press(self, *args):
        if self.inspector.edit_mode:
            if not self.drag:
                self.drag = True

    def on_mouse_release(self, *args):
        if self.inspector.edit_mode:
            if self.drag:
                self.drag = False

    def on_move(self, *args):
        if self.inspector.edit_mode:
            if self.drag:
                if self.inspector.widget:
                    self.inspector.widget.pos = args[1].pos
                    return True

    def on_mouse_pos(self, *args):
        """
        Called when the mouse position changes.

        WARNING!!!

        This is very cpu heavy as every widget will call this function every time the mouse moves.
        Use only for debugging purposes!!!

        (DE-)ACTIVATE with INSPECTOR_WIDGET at the beginning of hoverable.py
        """
        # only active if inspector is not locked to avoid unintended overwriting of the selected widget.

        if self.inspector.locked or self.drag:
            return
        if not self.get_root_window():
            return # do proceed if I'm not displayed <=> I have no parent
        pos = args[1]
        #Next line to_widget allow to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            # We have already done what was needed or there was nothing to do
            return
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')

    def on_enter(self):
        """A new widget has been entered. So safe yourself for later inspection."""
        self.inspector.set_widget(self)
        Logger.debug("Selected: {}".format(self.inspector.get_widget_name_class(self)))
