from kivy.core.window.window_sdl2 import WindowSDL
from kivy.event import EventDispatcher
from kivy.graphics import InstructionGroup, Color, Line
from kivy.properties import BooleanProperty
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from asmcnc.comms.logging_system.logging_system import Logger


class InspectorSingleton(EventDispatcher):
    """
    Uses the hoverable behavior to select widgets by hovering.
    This InspectorSingleton binds to keystrokes, so you can
    [l]ock on the selected widget (hovering will be disabled)
    un[l]ock from a selected widget to hover again
    p = go to parent widget
    c = goto child widget
    s = goto sibling
    a = goto sibling backwards
    w = opens "Add widget" popup (if instantiated)
    h = prints help
    e = en-/disable edit_mode to move widgets around
    +/- = change step width for arrow keys
    t = tetris mode. snaps widgets to the closest one in the given direction (with padding)
    [del] = deletes the selected widget
    arrow keys = move widget around
    [i]nspect the widget to print details on console
    """
    _instance = None
    widget = []  # the widget(s) that will be inspected
    locked = False  # locked to a widget. MouseMove doesn't select new one
    edit_mode = False  # widgets are movable when edit_mode = True
    enabled = False  # Only reacting/listening to key events when enabled
    step_width = 5  # stepwidth for moving widgets
    key_input_enabled = True # disable key input e.g. when keyboard is shown
    multiselect = False  # select more than one widget at once
    snap_mode = False  # using arrow keys lets widgets snap to the next one
    default_padding = 5  # default padding used for snapping widgets
    selection_rectangle = None  # reference to the red selection rectange

    def __new__(cls):
        if cls._instance is None:
            Logger.debug("Creating new instance of DataMinerSingleton")
            cls._instance = super(InspectorSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        super(EventDispatcher, self).__init__(**kwargs)
        self.child_index = -1
        self.child_max = -1
        self.register_event_type('on_show_component_popup')
        # self.enable()

    def disable(self):
        """Disables all inspector functionality."""
        self.enabled = False
        Logger.info('Inspector disabled')

    def enable(self):
        """Enables all inspector functionality. """
        self.enabled = True
        Window.bind(on_key_down=self._on_key_down)
        Logger.info('Inspector enabled')

    def disable_key_input(self):
        """disables the key inputs. Useful when a keyboard is open."""
        self.key_input_enabled = False
        Logger.info('Key input disabled')

    def enable_key_input(self):
        """enable the key inputs. Key are used to control the inspector."""
        self.key_input_enabled = True
        Logger.info('Key input enabled')

    def on_show_component_popup(self, *args):
        """Default callback. Needed for event creation."""
        pass

    def _on_key_down(self, *args, **kwargs):
        """
        Callback being called when a key is pressed.
        Is used for debugging purposes to print debug info about the UI elements.
        """
        if not self.enabled or not self.key_input_enabled:
            return True

        keycode = args[3]
        key = args[1]

        # Uncomment for info about keys. E.g. 'what's the key for "backspace"?'
        # Logger.debug('args: {}'.format(args))

        if self.multiselect and keycode and keycode in 'lpcsai':
            Logger.warning('"{}" not allowed during multi_select!'.format(keycode))
        if keycode == 'l':
            self.switch_lock_state()
        elif keycode == 'p':
            self.switch_to_parent()
        elif keycode == 'c':
            self.switch_to_child()
        elif keycode == 's':
            self.switch_to_sibling()
        elif keycode == 'a':
            self.switch_to_sibling_bw()
        elif keycode == 'i':
            self.inspect_widget()
        if keycode == 'h':
            self.print_help()
        elif keycode == 'w':
            self.open_close_component_popup()
        elif keycode == 'e':
            self.switch_edit_mode()
        elif keycode == 'm':
            pass
            # self.switch_multi_select_state()
        elif keycode == 't':
            self.switch_snap_mode()
        elif 273 <= key <= 276:  # check for arrow keys to move the widget
            if self.snap_mode:
                self.snap_widget(key)
            else:
                self.move_widget(key)
        elif key in [43, 270]:  # '+' keys
            self.adjust_step_width(1)
        elif key in [45, 269]:  # '-' keys
            self.adjust_step_width(-1)
        elif key == 127:  # del key
            self.delete_widget()
        elif key in [303, 304]:  # shift
            # self.add_remove_widget_to_selection()
            pass

        # Return True to accept the key. Otherwise, it will be used by the system.
        return True

    def switch_snap_mode(self):
        """
        En-/Disables snap_mode.

        When enabled, widgets can be snapped to the nearest widget using the arrow keys.
        """
        self.snap_mode = not self.snap_mode
        Logger.debug('snap_mode: {}'.format(self.snap_mode))

    def switch_lock_state(self):
        """
        En-/Disables locking to widgets.

        When enabled, a mouse hover event will not select new widgets.
        """
        if not self.locked:
            Logger.debug('LOCKED to: {}'.format(self.get_widget_name_class(self.widget)))
            self.locked = True
        else:
            Logger.debug('UNLOCKED')
            self.locked = False

    def open_close_component_popup(self):
        """
        Fires the event 'on_show_component_popup' to the widget to open and close it.
        """
        self.dispatch('on_show_component_popup')

    def adjust_step_width(self, value):
        """Adjusts the step width for moving widgets with the arrow keys by the given amount."""
        self.step_width += value
        if self.step_width < 1:  # min value of 1
            self.step_width = 1
        Logger.debug('Step width: {}'.format(self.step_width))

    def switch_multi_select_state(self):
        """Switches multiselect mode between True and False."""
        self.multiselect = not self.multiselect
        Logger.debug('multiselect: {}'.format(self.multiselect))

    def switch_edit_mode(self):
        """Switches edit_mode between True and False."""
        self.edit_mode = not self.edit_mode
        Logger.debug('edit_mode: {}'.format(self.edit_mode))

    def delete_widget(self):
        """Deletes the selected widget from the screen."""
        if self.widget:
            self.widget.parent.remove_widget(self.widget)
            self.remove_selection_rectangle()
            self.widget = None
            Logger.warning('Deleted selected widget!')

    def snap_widget(self, key):
        """
        Snaps the selected widget to the closest other widget within the same container.
        If no widget is in the way, the selected widget will snap to the border.

        Uses default padding.
        """
        if not self.widget:
            return
        self.remove_selection_rectangle()
        # get all siblings within the same container:
        widgets_to_check = self.widget.parent.children
        target_widget = None
        min_distance = 9999  # used to determine the closes widget
        w = self.widget   # just for readability
        if key == 274:  # down
            for t in widgets_to_check:
                if t is self.widget:
                    continue
                # check if widget would collide:
                if w.x <= t.x <= w.right or w.x <= t.right <= w.right or t.x <= w.x <= t.right:
                    # check if to the bottom:
                    distance = w.y - t.top
                    if 0 < distance < min_distance:  # widget is to the left and closer
                        min_distance = distance  # keep track in case another widget is even closer
                        target_widget = t
            # check if widget was found:
            if target_widget:
                w.y -= min_distance - self.default_padding
            else:
                w.y = self.default_padding  # move to bottom border
        elif key == 273:  # up
            for t in widgets_to_check:
                if t is self.widget:
                    continue
                # check if widget would collide:
                if w.x <= t.x <= w.right or w.x <= t.right <= w.right or t.x <= w.x <= t.right:
                    # check if to the top:
                    distance = t.y - w.top
                    if 0 < distance < min_distance:  # widget is to the left and closer
                        min_distance = distance  # keep track in case another widget is even closer
                        target_widget = t
            # check if widget was found:
            if target_widget:
                w.y += min_distance - self.default_padding
            else:
                w.top = w.parent.top - self.default_padding  # move to top border
        elif key == 275:  # right
            for t in widgets_to_check:
                if t is self.widget:
                    continue
                # check if widget would collide:
                if w.y <= t.y <= w.top or w.y <= t.top <= w.top or t.y <= w.y <= t.top:
                    # check if to the right:
                    distance = t.x - w.right
                    if 0 < distance < min_distance:  # widget is to the left and closer
                        min_distance = distance  # keep track in case another widget is even closer
                        target_widget = t
            # check if widget was found:
            if target_widget:
                w.x += min_distance - self.default_padding
            else:
                w.right = w.parent.right - self.default_padding  # move to right border
        elif key == 276:  # left
            for t in widgets_to_check:
                if t is self.widget:
                    continue
                # check if widget would collide:
                if w.y <= t.y <= w.top or w.y <= t.top <= w.top or t.y <= w.y <= t.top:
                    # check if to the left:
                    distance = w.x - t.right
                    if 0 < distance < min_distance:  # widget is to the left and closer
                        min_distance = distance  # keep track in case another widget is even closer
                        target_widget = t
            # check if widget was found:
            if target_widget:
                w.x -= min_distance - self.default_padding
            else:
                w.x = self.default_padding  # move to left border
        self.paint_selection_rectangle()

    def move_widget(self, key):
        """
        Moves the selected widget 5 pixels into one direction.

        The direction is determined by the pressed arrow key.
        """
        if not self.edit_mode or self.widget is None:
            return
        try:
            self.remove_selection_rectangle()
            if key == 273:  # up
                self.widget.pos[1] += self.step_width
            elif key == 274:  # down
                self.widget.pos[1] -= self.step_width
            elif key == 275:  # right
                self.widget.pos[0] += self.step_width
            elif key == 276:  # left
                self.widget.pos[0] -= self.step_width
            Logger.debug('pos: {}'.format(self.widget.pos))
        except Exception as ex:
            Logger.error("Failed to move widget!")
        finally:
            self.paint_selection_rectangle()

    def get_parent_screen(self):
        """Returns the screen object for the selected widget."""
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
        Logger.debug('p: switches to the parent.')
        Logger.debug('[del]: deletes the selected widget.')
        Logger.debug('+/-: in-/decreases the step width for moving widgets with arrow keys')
        Logger.debug('w: Open/Close popup to add new widgets to the currently selected one.')
        Logger.debug('t: Tetris mode. snaps widgets to the closest one in the given direction (with padding).')
        Logger.debug('When a widget is selected and edit_mode = True, you can use the arrow keys to move it.')
        Logger.debug("Or just drag'n drop it with the mouse")

    def get_widget_name_class(self, widget):
        """
        Tries to get the name of the given widget.
        If the widget has no attribute 'name' or 'id' it uses 'NO_NAME' instead.

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
            self.set_widget(self.widget.parent.children[self.child_index])
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
            self.set_widget(self.widget.parent.children[self.child_index])
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
        if self.widget:
            children = self.widget.children
            if len(children) == 0:
                Logger.debug('{} has no children!'.format(self.get_widget_name_class(self.widget)))
            else:
                self.child_index = 0
                self.child_max = len(children)
                self.set_widget(children[self.child_index])
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
            self.set_widget(parent)
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

    def paint_selection_rectangle(self):
        """
        Paints the red selection rectangle on the selected widget.

        Removes old one if left over."""
        if self.widget and self.selection_rectangle:
            self.widget.canvas.remove(self.selection_rectangle)
        self.selection_rectangle = InstructionGroup()
        self.selection_rectangle.add(Color(1, 0, 0))
        self.selection_rectangle.add(Line(rectangle=(self.widget.x, self.widget.y, self.widget.width, self.widget.height)))
        self.widget.canvas.add(self.selection_rectangle)

    def remove_selection_rectangle(self):
        """Removes the last painted red selection rectangle."""
        if self.widget and self.selection_rectangle:
            self.widget.canvas.remove(self.selection_rectangle)

    def set_widget(self, w):
        """Sets the given widget as selected, so it can be inspected."""
        self.remove_selection_rectangle()
        self.widget = w
        self.widgetType = type(w)
        self.paint_selection_rectangle()
        Logger.debug("Selected: {}".format(self.get_widget_name_class(w)))


class HoverBehavior(object):
    """
    Handles mouse move events. Enables drag'n drop for widgets with left mouse button.

    """
    inspector = InspectorSingleton()
    hovered = BooleanProperty(False)
    drag = False
    offset_x = 0
    offset_y = 0

    def __init__(self, **kwargs):
        super(HoverBehavior, self).__init__(**kwargs)
        if self.inspector.enabled:
            self.register_event_type('on_enter')
            Window.bind(mouse_pos=self.on_mouse_pos)
            Window.bind(on_touch_down=self.on_mouse_press)
            Window.bind(on_touch_move=self.on_move)
            Window.bind(on_touch_up=self.on_mouse_release)

    def on_mouse_press(self, *args):
        """
        Start drag with selected widget if Inspector is in edit_mode.
        Saves offset between mouse position and widget bottom left corner.
        """
        if self.inspector.edit_mode:
            if not self.drag:
                self.drag = True
                self.inspector.remove_selection_rectangle()
                self.offset_x = args[1].px - self.inspector.widget.x
                self.offset_y = args[1].py - self.inspector.widget.y

    def on_mouse_release(self, *args):
        """
        Drops the dragged widget.
        """
        if self.inspector.edit_mode:
            if self.drag:
                self.inspector.paint_selection_rectangle()
                self.drag = False

    def on_move(self, *args):
        """
        Drags the item with the mouse. Offset from mouse click pos to lower left corner
        of the widget is compensated for smoother user experience.

        The new position is restricted to the parents frame.
        """
        if self.inspector.edit_mode:
            if self.drag:
                if self.inspector.widget:
                    self.inspector.widget.x = self.constrain_x(args[1].px - self.offset_x)
                    self.inspector.widget.y = self.constrain_y(args[1].py - self.offset_y)
                    return True

    def constrain_x(self, x):
        """Checks if the widget would leave the parents frame in x direction."""
        if x < 0:  # left
            return 0
        elif x + self.inspector.widget.width > self.inspector.widget.parent.width:  # right
            return self.inspector.widget.parent.width - self.inspector.widget.width
        else:
            return x


    def constrain_y(self, y):
        """Checks if the widget would leave the parents frame in y direction."""
        if y < 0:  # bottom
            return 0
        elif y + self.inspector.widget.height > self.inspector.widget.parent.height:  # top
            return self.inspector.widget.parent.height - self.inspector.widget.height
        else:
            return y

    def on_mouse_pos(self, *args):
        """
        Called when the mouse position changes.

        WARNING!!!

        This is very cpu heavy as every widget will call this function every time the mouse moves.
        Use only for debugging purposes!!!

        (DE-)ACTIVATE with InspectorSingleton().en/disable()
        """
        # only active if inspector is not locked to avoid unintended overwriting of the selected widget.

        # check if inspector may change selected widget:
        if self.inspector.locked or self.drag or not self.inspector.enabled:
            return
        # should not work on designer items:
        if self.id and 'DESIGNER' in self.id:
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
        """A new widget has been entered. So safe it for later inspection."""
        self.inspector.set_widget(self)
