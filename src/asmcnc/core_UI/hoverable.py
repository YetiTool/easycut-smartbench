from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
import json



INSPECTOR_WIDGET = True


class InspectorSingleton(EventDispatcher):
    """
    Uses the hoverable behavior to select widgets by hovering.
    This InspectorSingleton binds to keystrokes [l,p,i], so you can
    [l]ock on the selected widget (hovering will be disabled)
    un[l]ock from a selected widget to hover again
    go to [p]arent widget
    [i]nspect the widget to print details on console

    can be deactivated by global INSPECTOR_WIDGET flag
    """
    _instance = None
    widgetType = None
    widget = None
    locked = False

    def __new__(cls):
        if cls._instance is None:
            print("Creating new instance of DataMinerSingleton")
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

        #print('keycode: {}  | args {}').format(keycode,args)

        # [l]ock on widget:
        if keycode == 'l':
            if not self.locked:
                print('LOCKED to: {}').format(self.get_widget_name_class(self.widget))
                self.locked = True
            else:
                print('UNLOCKED')
                self.locked = False
        # go to [p]arent
        elif keycode == 'p':
            self.switch_to_parent()
        elif keycode == 'c':
            self.switch_to_child()
        elif keycode == 's':
            self.switch_to_sibling()
        # [i]nspect widget
        elif keycode == 'i':
            self.inspect_widget()
        elif keycode == 'd':
            self.dump_screen()

        # check for arrow keys to move the widget
        if 273 <= key <= 276:
            #Clock.schedule_once(lambda dt: self.move_widget(key), 0.1)
            self.move_widget(key)

        # Return True to accept the key. Otherwise, it will be used by the system.
        return True

    def move_widget(self, key):
        try:
            if key == 273:
                self.widget.pos[1] += 5
            elif key == 274:
                self.widget.pos[1] -= 5
            elif key == 275:
                self.widget.pos[0] += 5
            elif key == 276:
                self.widget.pos[0] -= 5
            print('pos: {}'.format(self.widget.pos))
        except Exception as ex:
            print("oh oh!")

    def get_parent_screen(self):
        p = self.widget
        while not issubclass(type(p), Screen):
            p = p.parent
        return p
    def dump_screen(self):
        self.get_parent_screen().dump_screen()

    def dump_screen_tsv(self):
        j = self.get_parent_screen().dump_screen()

    def get_widget_name_class(self, widget):
        """
        Tries to get the name of the given widget. If the widget has no name use 'NO_NAME' instead.
        returns name (class name)
        """
        try:
            # check if it is a Layout and has no name
            name = widget.name
        except AttributeError:
            name = 'NO_NAME'
        return '{} ({})'.format(name,type(widget))

    def switch_to_sibling(self):
        """
        Switches to the next sibling. If there are no more siblings left it returns to the first one.
        This onyl works if switched to a child before to get the number of siblings.
        """
        if self.child_max > 0:
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
            print('Switched to sibling: {}').format(self.get_widget_name_class(self.widget))
        else:
            print('Not switched to children first...')

    def switch_to_child(self):
        """
        Switches to the first child if the currently selected widget has children.
        """
        children = self.widget.children
        if len(children) == 0:
            print('{} has no children!').format(self.get_widget_name_class(self.widget))
        else:
            self.child_index = 0
            self.child_max = len(children)
            self.widget = children[self.child_index]
            print('Switched to child: {}').format(self.get_widget_name_class(self.widget))

    def switch_to_parent(self):
        """Switches to the parent of the currently selected widget."""
        self.child_index = -1
        self.child_max = -1
        parent = self.widget.parent
        if parent is None:
            print('{} has no parent!').format(self.get_widget_name_class(self.widget))
        else:
            self.widget = parent
            print('Switched to parent: {}').format(self.get_widget_name_class(self.widget))

    def inspect_widget(self):
        """Prints debug information about the currently selected widget."""
        s = '========================================\n{}:\n'.format(self.get_widget_name_class(self.widget))
        s += 'pos: {}\tsize:{}'.format(self.widget.pos, self.widget.size)
        print(s)

    def set_widget(self, w):
        """Sets the given widget as selected so it can be inspected."""
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
        if not self.drag:
            self.drag = True

    def on_mouse_release(self, *args):
        if self.drag:
            self.drag = False

    def on_move(self, *args, **kwargs):
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
        try:
            name = self.name
        except AttributeError:
            name = type(self)
        print("Selected: {}").format(name)
        self.inspector.set_widget(self)
