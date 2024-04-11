from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

INDENT = '    '

DONT_DO_CHILDREN = ['ProbeButton']
CODE_ONLY_ITEMS = {'ProbeButton': ['{} = ProbeButton(None, None, None)  # TODO: fill args!',
                                   '{}.size_hint = [None, None]',
                                   '{}.size = [70, 70]',
                                   '{}.disabled = True',
                                   'self.children[0].add_widget({})'],
                   'SpindleButton': ['{} = SpindleButton(MagicMock(), MagicMock(), MagicMock())  # TODO: fill args!',
                                     '{}.size_hint = [None, None]',
                                     '{}.size = [71, 72]',
                                     '{}.disabled = True',
                                     'self.children[0].add_widget({})'],
                   'VacuumButton': ['{} = VacuumButton(MagicMock(), MagicMock())  # TODO: fill args!',
                                    '{}.size_hint = [None, None]',
                                    '{}.size = [71, 72]',
                                    '{}.disabled = True',
                                    'self.children[0].add_widget({})'],
                   'XYMove': ['{} = XYMove(machine=MagicMock(), screen_manager=MagicMock(), localization=MagicMock())',
                              '{}.size_hint = [None, None]',
                              '{}.size = [270.5, 391.6]',
                              'self.children[0].add_widget({})']}


def get_screen_name(widget):
    # type: (Widget) -> str
    """
    Returns the name of the widgets parent screen as string.
    """
    screen = widget.parent
    while not issubclass(type(screen), Screen):
        screen = screen.parent
    return screen.name


def get_python_code_from_screen(widget):
    # type: (Widget) -> str
    """
    widget = entrypoint into the screen's widget tree.
    Walks through the whole widget tree of the screen and generates either kivy builder string or python code
    for each widget.
    Imports are gathered and generated.
    Basic class code is generated.
    """
    screen = widget.parent

    while not issubclass(type(screen), Screen):
        screen = screen.parent
    #  assuming every screen has exactly one child as the main layout!!!
    main_layout = screen.children[0]
    # now make an import string:
    s = '# IMPORTS:\n\n'
    s += 'from kivy.lang import Builder\n'
    s += 'from kivy.uix.screenmanager import Screen\n'
    s += 'from mock.mock import MagicMock\n'
    d = get_import_dict_from_widget(main_layout)
    for k, v in d.items():
        imp_list = ','.join(v)
        s += 'from ' + k + ' import ' + imp_list + '\n'

    s += '\n# BUILDER_STRING:\n\n'
    s += 'Builder.load_string(\n"""'
    s += '<' + screen.name + '>\n'
    s += builder_string_from_widget(main_layout)
    s += '"""\n)'

    s += '\n# CLASS_CODE:\n\n'
    s += get_class_code(screen)
    s += get_code_for_widgets(screen)

    s += '\n'  # final new line

    return s

def get_code_for_widgets(widget):
    # type: (Widget) -> str
    """
    Returns python code for the CODE_ONLY_ITEMS.
    """
    s= ''
    if type(widget).__name__ in CODE_ONLY_ITEMS:
        s += INDENT + INDENT + '# Code for {}:\n'.format(str(widget.id))
        # add specific code block:
        for line in CODE_ONLY_ITEMS[type(widget).__name__]:
            s += INDENT + INDENT + line.format(widget.id) + '\n'
        # add position:
        s += INDENT + INDENT + str(widget.id) + '.pos = ' + str(widget.pos) + '\n'
        s += INDENT + INDENT + str(widget.id) + '.id = "' + str(widget.id) + '"\n'
    else:
        # no do the children
        for child in widget.children:
            s += get_code_for_widgets(child)
    s += '\n'
    return s



def builder_string_from_widget(widget, indent_level=1, do_children=True):
    # type: (Widget, int, bool) -> str
    """
    Returns a generated builder string that represents the given widget.
    """
    # list of attributes with specific formatting options. E.g.: wrapping the actual text in ""
    # attributes = {'allow_stretch': '{}',
    #               'always_release': '{}',
    #               'center_x': '{}',
    #               'center_y': '{}',
    #               'cols': '{}',
    #               'background_color': '{}',
    #               'background_normal': '"{}"',
    #               'background_down': '"{}"',
    #               'border': '{}',
    #               'color': '{}',
    #               'font_size': 'dp({})',
    #               'halign': '"{}"',
    #               'height': '{}',
    #               'id': '{}',
    #               'markup': '{}',
    #               'orientation': '"{}"',
    #               'padding': 'dp({})',
    #               'padding_x': 'dp({})',
    #               'padding_y': 'dp({})',
    #               'pos': '{}',
    #               'rows': '{}',
    #               'size': '{}',
    #               # 'size_hint': '{}',
    #               'size_hint_x': '{}',
    #               'size_hint_y': '{}',
    #               'source': '"{}"',
    #               'spacing': 'dp({})',
    #               'text': '"{}"',
    #               'text_size': '{}',
    #               'width': '{}',
    #               'valign':  '"{}"'
    #               }
    attributes = {'allow_stretch': '{}',
                  'cols': '{}',
                  'background_color': '{}',
                  'background_normal': '"{}"',
                  'background_down': '"{}"',
                  'border': '{}',
                  'color': '{}',
                  'font_size': 'dp({})',
                  'halign': '"{}"',
                  # 'height': '{}',
                  'id': '{}',
                  'pos': '{}',
                  'size': '{}',
                  'size_hint': '{}',
                  'size_hint_x': '{}',
                  'size_hint_y': '{}',
                  'source': '"{}"',
                  'text': '"{}"',
                  'text_size': '{}',
                  # 'width': '{}',
                  'valign':  '"{}"'
                  }
    # CODE_ONLY_ITEMS will not appear in the BuilderString
    if type(widget).__name__ in CODE_ONLY_ITEMS:
        return ''
    # setup indentation level:
    base_indent = ''
    for i in range(0, indent_level * len(INDENT)):
        base_indent += ' '

    s = base_indent + type(widget).__name__ + ':\n'

    # list of attributes that need to be part of the builder string:
    for attribute in attributes.keys():
        value = getattr(widget, attribute, 'no_attr')
        if value and value != 'no_attr':
            s += base_indent + INDENT + attribute + ': ' + attributes[attribute].format(str(value)) + '\n'
    s += '\n'
    # now handle children
    if do_children:
        for child in widget.children:
            kivy_class = type(child).__name__ not in DONT_DO_CHILDREN
            s += builder_string_from_widget(child, indent_level+1, kivy_class)
    return s


def get_import_dict_from_widget(widget):
    # type: (Widget) -> dict
    """
    Returns a dictionary with the widgets module name as the key and the class names as the value.
    """
    ret = {}
    klass = widget.__class__
    module = klass.__module__
    if module != 'builtins':
        ret = {module: {klass.__name__}}

    # now handle children:
    for child in widget.children:
        c = get_import_dict_from_widget(child)
        for k, v in c.items():
            #check if the same module is needed -> update set:
            if k in ret:
                ret[k].union(v)
            else:
                ret[k] = v

    return ret


def get_class_code(screen):
    # type: (Screen) -> str
    """
    Returns basic class code (ctor and super call) as string.
    sets the name attribute of the screen!
    """
    s = 'class ' + screen.name + '(Screen):\n'
    s += INDENT + 'def __init__(self, **kwargs):\n'
    s += INDENT + INDENT + 'super(' + screen.name + ', self).__init__(name="' + screen.name + '", **kwargs)\n'
    return s



